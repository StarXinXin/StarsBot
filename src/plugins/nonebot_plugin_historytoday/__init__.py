import os
from datetime import datetime

from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot_plugin_alconna.uniseg import UniMessage

import utils.AdminTool as at
from src.plugins.nonebot_plugin_historytoday.getdata import get_events_on_day


from pathlib import Path

import nonebot
from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from utils.FileUtils import ensure_file_exists, read_json_file
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_historytoday",
    description="历史上的今天",
    usage="QQ群聊或私聊中发送/历史上的今天",
    config=Config,
)

from ..nonebot_plugin_menu import is_function_normal

config = get_plugin_config(Config)

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)


catch_str = on_keyword({'/历史上的今天'})


@catch_str.handle()
async def send_img(bot: Bot, event: Event, state: T_State, true=True):
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "历史上的今天"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if at.is_group_in_whitelist(parts[1]):
                    now = datetime.now()
                    month = str(now.month).zfill(2)
                    day = str(now.day).zfill(2)
                    events_msg = get_events_on_day(month, day)
                    chuli = events_msg.replace(" [1]","").replace("[","").replace("]","").replace(".baseInfoWrap{display:inline-block;","").rstrip('\n')
                    await UniMessage(chuli).send(reply_to=true)
            else:
                now = datetime.now()
                month = str(now.month).zfill(2)
                day = str(now.day).zfill(2)
                events_msg = get_events_on_day(month, day)
                chuli = events_msg.replace(" [1]", "").replace("[", "").replace("]", "").replace(
                    ".baseInfoWrap{display:inline-block;", "").rstrip('\n')
                await UniMessage(chuli).send(reply_to=true)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)