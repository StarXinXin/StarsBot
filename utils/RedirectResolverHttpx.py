import httpx
from nonebot_plugin_alconna import UniMessage
from nonebot.log import logger

class RedirectResolverHttpx:
    def __init__(self, allow_redirects=True):
        self.client = httpx.Client(follow_redirects=allow_redirects, timeout=100)
        self.client.max_redirects = 30  # 防止无限重定向

    def resolve_redirect(self, url, event=None):
        """
        使用httpx获取URL的最终重定向地址。

        :param url: 需要解析重定向的原始URL
        :return: 最终重定向的URL或原始URL（如果没有重定向）
        """
        try:
            response = self.client.head(url)
            return response.url
        except httpx.RequestError as e:
            logger.log(f"解决重定向时出错： {e}")
            return None
        except httpx.ConnectTimeout as e:
            send_error_message()
            return None


async def send_error_message():
    await UniMessage("重定向请求超时").send()

# 使用示例
# if __name__ == "__main__":
#     resolver = RedirectResolverHttpx()
#     original_url = "http://api.jun.la/60s.php?format=image"
#     final_url = resolver.resolve_redirect(original_url)
#     print(f"The final URL is: {final_url}")
