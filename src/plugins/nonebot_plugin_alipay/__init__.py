from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Bot, Event, MessageEvent
from nonebot.params import CommandArg

from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot_plugin_alconna import UniMessage

from utils.AdminTool import is_group_in_whitelist
from utils.FileUtils import ensure_file_exists, read_json_file
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_alipay",
    description="酷宝到账音效合成",
    usage="/支付宝到账",
    config=Config,
)

from ..nonebot_plugin_menu import is_function_normal

config = get_plugin_config(Config)


alipay_voice = on_command("/支付宝到账")


@alipay_voice.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State, content: Message=CommandArg()):
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "支付宝到账"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    if not content.extract_plain_text():
                        await alipay_voice.send("请输入金额", reply_message=True)
                    if not content.extract_plain_text().isdigit():
                        await alipay_voice.send("错误的，请输入正确的数字", reply_message=True)
                    if 0.01 <= float(content.extract_plain_text()) <= 999999999999.99:
                        url = f"https://free.wqwlkj.cn/wqwlapi/alipay_yy.php?money={content.extract_plain_text()}"
                        await alipay_voice.send(MessageSegment.record(url))
                    else:
                        await alipay_voice.send("数字大小超出限制，支持范围为0.01~999999999999.99", reply_message=True)
            else:
                if not content.extract_plain_text():
                    await alipay_voice.send("请输入金额", reply_message=True)
                if not content.extract_plain_text().isdigit():
                    await alipay_voice.send("错误的，请输入正确的数字", reply_message=True)
                if 0.01 <= float(content.extract_plain_text()) <= 999999999999.99:
                    url = f"https://free.wqwlkj.cn/wqwlapi/alipay_yy.php?money={content.extract_plain_text()}"
                    await alipay_voice.send(MessageSegment.record(url))
                else:
                    await alipay_voice.send("数字大小超出限制，支持范围为0.01~999999999999.99", reply_message=True)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)
