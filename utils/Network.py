import requests
from nonebot_plugin_alconna import UniMessage
from requests.exceptions import Timeout


def make_request(url, headers=None, data=None, timeout=100, on_timeout=None):
    try:
        response = requests.post(url, headers=headers, data=data, timeout=timeout)
        # 这里假设使用POST请求，你也可以根据需要修改为GET或其他HTTP方法
        return response
    except Timeout:
        if on_timeout:
            on_timeout()
        return None


async def timeout_callback():
    await UniMessage("请求超时,无法获取数据，请稍后再试。").send(reply_to=True)