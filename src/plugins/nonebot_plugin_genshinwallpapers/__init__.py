from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot_plugin_alconna import UniMessage

from utils.AdminTool import is_group_in_whitelist
from utils.FileUtils import read_json_file, ensure_file_exists
from utils.Network import make_request, timeout_callback
from .config import Config

__plugin_meta__ = PluginMetadata(
    name=" nonebot_plugin_genshinwallpapers",
    description="",
    usage="",
    config=Config,
)

from ..nonebot_plugin_menu import is_function_normal

config = get_plugin_config(Config)

GenshinImpactWallpapers = on_command(
    "GenshinImpactWallpapers",
    aliases={"/原神壁纸"},
    priority=5,
    block=True,
)


@GenshinImpactWallpapers.handle()
async def _(bot: Bot, event: Event, state: T_State):
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "原神壁纸"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    response = make_request('https://api.lolimi.cn/API/yuan/api.php', timeout=100,
                                            on_timeout=timeout_callback)
                    if response.status_code == 200:
                        # GameId = str(generate_random_number(5))
                        data = response.json()
                        text = data['text']
                        if text:
                            await GenshinImpactWallpapers.finish(MessageSegment.image(text), reply_message=True)
                        else:
                            await UniMessage("无法解析数据或数据不完整，请稍后再试。").send(reply_to=True)
                    else:
                        await UniMessage("无法获取数据，请稍后再试。").send(reply_to=True)
            else:
                response = make_request('https://api.lolimi.cn/API/yuan/api.php', timeout=100,
                                        on_timeout=timeout_callback)
                if response.status_code == 200:
                    # GameId = str(generate_random_number(5))
                    data = response.json()
                    text = data['text']
                    if text:
                        await GenshinImpactWallpapers.finish(MessageSegment.image(text), reply_message=True)
                    else:
                        await UniMessage("无法解析数据或数据不完整，请稍后再试。").send(reply_to=True)
                else:
                    await UniMessage("无法获取数据，请稍后再试。").send(reply_to=True)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)
