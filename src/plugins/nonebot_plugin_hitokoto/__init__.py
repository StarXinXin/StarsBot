import httpx
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Event, Bot
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot_plugin_alconna.uniseg import UniMessage


from pathlib import Path

import nonebot
from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from utils.AdminTool import is_group_in_whitelist
from utils.FileUtils import ensure_file_exists, read_json_file
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_hitokoto",
    description="一言插件，发送关键词即可获得一句话",
    usage="/一言",
    config=Config,
)

from ..nonebot_plugin_menu import is_function_normal

config = get_plugin_config(Config)

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)

hitokoto_matcher = on_command("/一言")

@hitokoto_matcher.handle()
async def _(bot: Bot, event: Event, state: T_State, true=True):
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "一言"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    try:
                        async with httpx.AsyncClient() as client:
                            # timeout = Timeout(10.0, connect=20.0)  # Adjust values as needed
                            response = await client.get("https://v1.hitokoto.cn/?encode=json&c=b&c=c&c=d&c=e&c=h&c=i&c=j&c=k&lang=cn", timeout=100)
                        if response.is_error:
                            await UniMessage("获取一言失败").send(reply_to=true)
                            return
                        data = response.json()
                        msg = data["hitokoto"]
                        add = ""
                        if works := data["from"]:
                            add += f"《{works}》"
                        if from_who := data["from_who"]:
                            add += f"{from_who}"
                        if add:
                            msg += f"\n{add}"
                        await UniMessage(msg).send(reply_to=true)
                    except httpx.ConnectTimeout:
                        await UniMessage("获取一言失败，请求超时").send(reply_to=true)
                    except httpx.ConnectError:
                        await UniMessage("获取一言失败，连接错误").send(reply_to=true)
            else:
                async with httpx.AsyncClient() as client:
                    # timeout = Timeout(10.0, connect=20.0)  # Adjust values as needed
                    response = await client.get(
                        "https://v1.hitokoto.cn/?encode=json&c=b&c=c&c=d&c=e&c=h&c=i&c=j&c=k&lang=cn")
                if response.is_error:
                    await UniMessage("获取一言失败").send(reply_to=true)
                    return
                data = response.json()
                msg = data["hitokoto"]
                add = ""
                if works := data["from"]:
                    add += f"《{works}》"
                if from_who := data["from_who"]:
                    add += f"{from_who}"
                if add:
                    msg += f"\n{add}"
                await UniMessage(msg).send(reply_to=true)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)