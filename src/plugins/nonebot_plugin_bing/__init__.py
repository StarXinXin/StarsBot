from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot_plugin_alconna.uniseg import UniMessage

import utils.AdminTool as at
from utils.FileUtils import read_json_file, ensure_file_exists
from utils.RedirectResolverHttpx import RedirectResolverHttpx



from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config


__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_bing",
    description="获取并Bing每日壁纸。",
    usage="/Bing每日壁纸",
    config=Config,
)

from ..nonebot_plugin_menu import is_function_normal

config = get_plugin_config(Config)


Bing = on_keyword({'/Bing每日壁纸'})


@Bing.handle()
async def _(bot: Bot, event: Event, state: T_State, true=False):
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "Bing每日壁纸"):
            image_url = RedirectResolverHttpx().resolve_redirect("https://jkapi.com/api/bing_img?type=")
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if at.is_group_in_whitelist(parts[1]):
                    await Bing.finish(MessageSegment.image(str(image_url)), reply_message=True)
            else:
                image = MessageSegment.image(str(image_url))
                await Bing.finish(MessageSegment.image(str(image_url)), reply_message=True)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)