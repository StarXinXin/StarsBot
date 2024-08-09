from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from urlextract import URLExtract

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_videoparsing",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Bot, Event, MessageEvent
from nonebot.params import CommandArg
import requests

# 定义指令 /视频解析
video_parse = on_command("视频解析", aliases={"视频解析"}, priority=5)

@video_parse.handle()
async def handle_first_receive(bot: Bot, event: Event, content: Message=CommandArg()):
    args = str(event.get_message()).strip()  # 获取用户输入的参数
    if not content.extract_plain_text():
        await video_parse.finish("格式错误，正确格式：\n/视频解析 链接(可以是平台复制时带有文本的链接)")
    else:
        if URLExtract().has_urls(args):

            api_url = "http://api.yujn.cn/api/dspjx.php"
            params = {
                "type": "json",
                "url": URLExtract().find_urls(args)[0]
            }

            try:
                response = requests.get(api_url, params=params, timeout=100)
                if response.status_code == 200:
                    data = response.json()
                    if data["code"] == 200:
                        # 构建消息内容
                        message = (
                            MessageSegment.text("---------") +
                            MessageSegment.face('320') + MessageSegment.text("解析成功") +
                            MessageSegment.face('320') + MessageSegment.text("---------\n") +
                            MessageSegment.text(f"标题: {data['data']['title']}\n") +
                            MessageSegment.text(f"视频源: {data['data']['source']}\n")
                        )

                        # 如果视频链接存在，则输出视频链接
                        if data['data']['video']:
                            message += MessageSegment.text("视频封面：\n") + \
                                       MessageSegment.image(data['data']['img'][0]) + \
                                       MessageSegment.text(f"视频链接: {data['data']['video']}\n\n")
                        # 如果是图集，则输出所有图片
                        else:
                            message += MessageSegment.text("这是一个图集，包含以下图片：\n")
                            for img_url in data['data']['img']:
                                message += MessageSegment.image(img_url) + MessageSegment.text("\n")

                        message += MessageSegment.face('320') + MessageSegment.text("可以直接保存哦") + MessageSegment.face('320')

                        # 发送消息
                        await video_parse.finish(message, reply_message=True)
                    else:
                        await video_parse.finish("解析失败，无法获取视频信息。", reply_message=True)
                else:
                    await video_parse.finish(f"请求失败，状态码: {response.status_code}", reply_message=True)
            except requests.exceptions.Timeout:
                await video_parse.finish("请求超时，请稍后再试。", reply_message=True)

        else:
            await video_parse.finish("请提供一个视频链接！")
