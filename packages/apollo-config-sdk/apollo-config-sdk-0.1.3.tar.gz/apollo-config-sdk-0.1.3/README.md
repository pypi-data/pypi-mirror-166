# Apollo-Config-Sdk


```python
from apollo_config_sdk.client import ApolloClient

if __name__ == '__main__':
    client = ApolloClient(
        app_id="appid",
        cluster="cluster",
        config_url='config_url',
        secret="secret"
    )

    for i in range(500):
        import time

        time.sleep(1)
        z = client.get_value('key', namespace='namespace')
        print(z)
        pass
```

1. Feature Acceptance Test environment 功能验收测试环境，用于软件测试者测试使用