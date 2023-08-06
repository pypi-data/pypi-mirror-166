"""
https://github.com/xhrg-product/apollo-client-python/blob/master/apollo/apollo_client.py
"""
import json
import threading
import time
import requests
import hmac
import base64
import logging
import os
from urllib import parse
import hashlib
import socket

Logger = logging.getLogger(__file__)

# 定义常量
CONFIGURATIONS = "configurations"
NOTIFICATION_ID = "notificationId"
NAMESPACE_NAME = "namespaceName"


# 对时间戳，uri，秘钥进行加签
def signature(timestamp, uri, secret):
    string_to_sign = '' + timestamp + '\n' + uri
    hmac_code = hmac.new(secret.encode(), string_to_sign.encode(), hashlib.sha1).digest()
    return base64.b64encode(hmac_code).decode()


def url_encode_wrapper(params):
    return url_encode(params)


def no_key_cache_key(namespace, key):
    return "{}{}{}".format(namespace, len(namespace), key)


# 返回是否获取到的值，不存在则返回None
def get_value_from_dict(namespace_cache, key):
    if namespace_cache:
        kv_data = namespace_cache.get(CONFIGURATIONS)
        if kv_data is None:
            return None
        if key in kv_data:
            return kv_data[key]
    return None


def init_ip():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 53))
        ip = s.getsockname()[0]
        return ip
    except Exception as e:
        return ""
    finally:
        if s:
            s.close()


def http_request(url, timeout, headers):
    res = requests.get(url, headers=headers, timeout=timeout)
    print(res.status_code, url, res.text)
    return res.status_code, res.text


def url_encode(params):
    return parse.urlencode(params)


def makedirs_wrapper(path):
    os.makedirs(path, exist_ok=True)


class ApolloClient(object):

    def __init__(
            self,
            config_url,
            app_id,
            cluster='default',
            secret='',
            start_hot_update=True,
            change_listener=None,
            cycle_time=2
    ):

        # 核心路由参数
        self.config_url = config_url
        self.cluster = cluster
        self.app_id = app_id

        # 非核心参数
        self.ip = init_ip()
        self.secret = secret

        # 检查参数变量

        # 私有控制变量
        self._cycle_time = cycle_time
        self._stopping = False
        self._cache = {}
        self._no_key = {}
        self._hash = {}
        self._pull_timeout = 75
        self._cache_file_path = os.path.expanduser('~') + '/cache/'
        self._long_poll_thread = None
        self._change_listener = change_listener  # "add" "delete" "update"
        self._notification_map = {'application': -1}
        self.last_release_key = None
        # 私有启动方法
        self._path_checker()
        if start_hot_update:
            self._start_hot_update()

        # 启动心跳线程
        heartbeat = threading.Thread(target=self._heartBeat)
        heartbeat.setDaemon(True)
        heartbeat.start()

    def get_json_from_net(self, namespace='application'):
        url = '{}/configs/{}/{}/{}?releaseKey={}&ip={}'.format(self.config_url, self.app_id, self.cluster, namespace,
                                                               "", self.ip)
        try:
            code, body = http_request(url, timeout=3, headers=self._signHeaders(url))
            if code == 200:
                data = json.loads(body)
                data = data["configurations"]
                return_data = {CONFIGURATIONS: data}
                return return_data
            else:
                return None
        except Exception as e:
            Logger.error(str(e))
            return None

    def get_value(self, key, default_val=None, namespace='application'):
        try:
            # 读取内存配置
            namespace_cache = self._cache.get(namespace)
            val = get_value_from_dict(namespace_cache, key)
            if val is not None:
                return val

            no_key = no_key_cache_key(namespace, key)
            if no_key in self._no_key:
                return default_val

            # 读取网络配置
            namespace_data = self.get_json_from_net(namespace)
            val = get_value_from_dict(namespace_data, key)
            if val is not None:
                self._update_cache_and_file(namespace_data, namespace)
                return val

            # 读取文件配置
            namespace_cache = self._get_local_cache(namespace)
            val = get_value_from_dict(namespace_cache, key)
            if val is not None:
                self._update_cache_and_file(namespace_cache, namespace)
                return val

            # 如果全部没有获取，则把默认值返回，设置本地缓存为None
            self._set_local_cache_none(namespace, key)
            return default_val
        except Exception as e:
            Logger.error("get_value has error, [key is %s], [namespace is %s], [error is %s], ",
                         key, namespace, e)
            return default_val

    # 设置某个namespace的key为none，这里不设置default_val，是为了保证函数调用实时的正确性。
    # 假设用户2次default_val不一样，然而这里却用default_val填充，则可能会有问题。
    def _set_local_cache_none(self, namespace, key):
        no_key = no_key_cache_key(namespace, key)
        self._no_key[no_key] = key

    def _start_hot_update(self):
        self._long_poll_thread = threading.Thread(target=self._listener)
        # 启动异步线程为守护线程，主线程推出的时候，守护线程会自动退出。
        self._long_poll_thread.setDaemon(True)
        self._long_poll_thread.start()

    def stop(self):
        self._stopping = True
        Logger.info("Stopping listener...")

    # 调用设置的回调函数，如果异常，直接try掉
    def _call_listener(self, namespace, old_kv, new_kv):
        if self._change_listener is None:
            return
        if old_kv is None:
            old_kv = {}
        if new_kv is None:
            new_kv = {}
        try:
            for key in old_kv:
                new_value = new_kv.get(key)
                old_value = old_kv.get(key)
                if new_value is None:
                    # 如果newValue 是空，则表示key，value被删除了。
                    self._change_listener("delete", namespace, key, old_value)
                    continue
                if new_value != old_value:
                    self._change_listener("update", namespace, key, new_value)
                    continue
            for key in new_kv:
                new_value = new_kv.get(key)
                old_value = old_kv.get(key)
                if old_value is None:
                    self._change_listener("add", namespace, key, new_value)
        except BaseException as e:
            Logger.warning(str(e))

    def _path_checker(self):
        if not os.path.isdir(self._cache_file_path):
            makedirs_wrapper(self._cache_file_path)

    # 更新本地缓存和文件缓存
    def _update_cache_and_file(self, namespace_data, namespace='application'):
        # 更新本地缓存
        self._cache[namespace] = namespace_data
        # 更新文件缓存
        new_string = json.dumps(namespace_data)
        new_hash = hashlib.md5(new_string.encode('utf-8')).hexdigest()
        if self._hash.get(namespace) == new_hash:
            pass
        else:
            with open(os.path.join(self._cache_file_path, '%s_configuration_%s.txt' % (self.app_id, namespace)),
                      'w') as f:
                f.write(new_string)
            self._hash[namespace] = new_hash

    # 从本地文件获取配置
    def _get_local_cache(self, namespace='application'):
        cache_file_path = os.path.join(self._cache_file_path, '%s_configuration_%s.txt' % (self.app_id, namespace))
        if os.path.isfile(cache_file_path):
            with open(cache_file_path, 'r') as f:
                result = json.loads(f.readline())
            return result
        return {}

    def _long_poll(self):
        notifications = []
        for key in self._cache:
            namespace_data = self._cache[key]
            notification_id = -1
            if NOTIFICATION_ID in namespace_data:
                notification_id = self._cache[key][NOTIFICATION_ID]
            notifications.append({
                NAMESPACE_NAME: key,
                NOTIFICATION_ID: notification_id
            })
        try:
            # 如果长度为0直接返回
            if len(notifications) == 0:
                return
            url = '{}/notifications/v2'.format(self.config_url)
            params = {
                'appId': self.app_id,
                'cluster': self.cluster,
                'notifications': json.dumps(notifications, ensure_ascii=False)
            }
            param_str = url_encode_wrapper(params)
            url = url + '?' + param_str
            code, body = http_request(url, self._pull_timeout, headers=self._signHeaders(url))
            http_code = code
            if http_code == 304:
                Logger.debug('No change, loop...')
                return
            if http_code == 200:
                data = json.loads(body)
                for entry in data:
                    namespace = entry[NAMESPACE_NAME]
                    n_id = entry[NOTIFICATION_ID]
                    Logger.info("%s has changes: notificationId=%d", namespace, n_id)
                    self._get_net_and_set_local(namespace, n_id, call_change=True)
                    return
            else:
                Logger.warning('Sleep...')
        except Exception as e:
            Logger.warning(str(e))

    def _get_net_and_set_local(self, namespace, n_id, call_change=False):
        namespace_data = self.get_json_from_net(namespace)
        namespace_data[NOTIFICATION_ID] = n_id
        old_namespace = self._cache.get(namespace)
        self._update_cache_and_file(namespace_data, namespace)
        if self._change_listener is not None and call_change:
            old_kv = old_namespace.get(CONFIGURATIONS)
            new_kv = namespace_data.get(CONFIGURATIONS)
            self._call_listener(namespace, old_kv, new_kv)

    def _listener(self):
        Logger.info('start long_poll')
        while not self._stopping:
            self._long_poll()
            time.sleep(self._cycle_time)
        Logger.info("stopped, long_poll")

    # 给header增加加签需求
    def _signHeaders(self, url):
        headers = {}
        if self.secret == '':
            return headers
        uri = url[len(self.config_url):len(url)]
        time_unix_now = str(int(round(time.time() * 1000)))
        headers['Authorization'] = 'Apollo ' + self.app_id + ':' + signature(time_unix_now, uri, self.secret)
        headers['Timestamp'] = time_unix_now
        return headers

    def _heartBeat(self):
        while not self._stopping:
            for namespace in self._notification_map:
                self._do_heartBeat(namespace)
            time.sleep(60 * 10)  # 10分钟

    def _do_heartBeat(self, namespace):
        url = '{}/configs/{}/{}/{}?ip={}'.format(self.config_url, self.app_id, self.cluster, namespace,
                                                 self.ip)
        try:
            code, body = http_request(url, timeout=3, headers=self._signHeaders(url))
            if code == 200:
                data = json.loads(body)
                if self.last_release_key == data["releaseKey"]:
                    return None
                self.last_release_key = data["releaseKey"]
                data = data["configurations"]
                self._update_cache_and_file(data, namespace)
            else:
                return None
        except Exception as e:
            Logger.error(str(e))
            return None
