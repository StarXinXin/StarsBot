from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot_plugin_alconna.uniseg import UniMessage

import utils.AdminTool as at
from utils.FileUtils import ensure_file_exists, read_json_file
from utils.RedirectResolverHttpx import RedirectResolverHttpx



from pathlib import Path

import nonebot
from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_60sworld",
    description="六十秒读懂世界",
    usage="QQ群聊或私聊中发送/60s世界",
    config=Config,
)

from ..nonebot_plugin_menu import is_function_normal

config = get_plugin_config(Config)

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)


catch_str = on_keyword({'/60s世界'})


@catch_str.handle()
async def _(bot: Bot, event: Event, state: T_State):
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "60s世界"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if at.is_group_in_whitelist(parts[1]):
                    image_url = RedirectResolverHttpx().resolve_redirect("http://api.jun.la/60s.php?format=image")
                    await bot.finish(MessageSegment.image(str(image_url)), reply_message=True)
            else:
                image_url = RedirectResolverHttpx().resolve_redirect("http://api.jun.la/60s.php?format=image")
                await bot.finish(MessageSegment.image(str(image_url)), reply_message=True)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)