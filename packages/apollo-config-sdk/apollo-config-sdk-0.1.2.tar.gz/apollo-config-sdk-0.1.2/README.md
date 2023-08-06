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