from nonebot.internal.rule import Rule
from nonebot.matcher import Matcher
from nonebot import on_keyword, on_command, on_regex, on_notice
from nonebot.params import RegexDict
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, PrivateMessageEvent, MessageEvent, \
    PokeNotifyEvent, Message
from nonebot_plugin_alconna import Emoji
from nonebot_plugin_alconna.uniseg import Image, UniMessage

import utils.AdminTool as at
from pathlib import Path

import nonebot
from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from utils.FileUtils import ensure_file_exists, read_json_file
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_menu",
    description="菜单插件通过该插件的关键词获得机器人的菜单",
    usage="QQ群聊或私聊中发送/菜单 or /cd",
    config=Config,
)

config = get_plugin_config(Config)

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)

Menu = on_regex(r'/((菜单|cd))(?P<Platform>\d{1,3})?')
GameMenu = on_regex(r'/((游戏菜单|cd))(?P<Platform>\d{1,3})?')


# Menu = on_command("/菜单", aliases={"/cd"})
AIChat = on_command("/AI聊天")


@Menu.handle()
async def _(event: PrivateMessageEvent | GroupMessageEvent | MessageEvent, matched = RegexDict())-> None:
    ids = event.get_session_id()
    filepath = f"Profile/Menu/Function/Fun.json"
    if ids.startswith("group"):
        parts = ids.split('_')
        if at.is_group_in_whitelist(parts[1]):
            if not matched["Platform"]:
                if ensure_file_exists(filepath):
                    menu_message = generate_menu(read_json_file(filepath), "1")
                await UniMessage(menu_message).send(reply_to=True)
            elif matched["Platform"] == "2":
                if ensure_file_exists(filepath):
                    menu_message = generate_menu(read_json_file(filepath), "2")
                await UniMessage(menu_message).send(reply_to=True)

    else:
        if not matched["Platform"]:
            if ensure_file_exists(filepath):
                menu_message = generate_menu(read_json_file(filepath), "1")
            await UniMessage(menu_message).send(reply_to=True)
        elif matched["Platform"] == "2":
            if ensure_file_exists(filepath):
                menu_message = generate_menu(read_json_file(filepath), "2")
            await UniMessage(menu_message).send(reply_to=True)


@AIChat.handle()
async def send_menu(bot: Bot, event: Event, state: T_State, true=True):
    ids = event.get_session_id()
    if ids.startswith("group"):
        parts = ids.split('_')
        if at.is_group_in_whitelist(parts[1]):
            await UniMessage(f"免费的AI聊天功能，\n@星辰Bot+聊天内容\n即可开启聊天模式，\n@星辰Bot+清除上下文\n结束这次的聊天(清空记忆)\n\nAI自带记忆功能，聊天会被保存哦，以更好地为您服务").send(reply_to=true)
    else:
        await UniMessage(f"欢迎使用星辰Bot\n"
                         f"发送以下指令，获取更多哦~\n\n"
                         f"/一言\n"
                         f"/历史上的今天\n"
                         f"/60s世界\n"
                         f"/天气\n\n"
                         f"特殊功能\n"
                         f"AI聊天\n"
                         ).send(reply_to=true)



@GameMenu.handle()
async def _(event: PrivateMessageEvent | GroupMessageEvent, matched = RegexDict())-> None:
    ids = event.get_session_id()
    gamefilepath = f"Profile/Menu/Game/Fun.json"
    if ids.startswith("group"):
        parts = ids.split('_')
        if at.is_group_in_whitelist(parts[1]):
            if not matched["Platform"]:
                if ensure_file_exists(gamefilepath):
                    menu_message = generate_gamemenu(read_json_file(gamefilepath), "1")
                await UniMessage(menu_message).send(reply_to=True)
            elif matched["Platform"] == "2":
                if ensure_file_exists(gamefilepath):
                    menu_message = generate_gamemenu(read_json_file(gamefilepath), "2")
                await UniMessage(menu_message).send(reply_to=True)

    else:
        if not matched["Platform"]:
            if ensure_file_exists(gamefilepath):
                menu_message = generate_gamemenu(read_json_file(gamefilepath), "1")
            await UniMessage(menu_message).send(reply_to=True)
        elif matched["Platform"] == "2":
            if ensure_file_exists(gamefilepath):
                menu_message = generate_gamemenu(read_json_file(gamefilepath), "2")
            await UniMessage(menu_message).send(reply_to=True)


def generate_menu(json_data, Page):
    commands = json_data["Commands"][Page]
    menu_content = "       ✨星辰Bot✨\n\n"
    if Page == "1":
        for command in commands:
            menu_content += f"/{command}\n"

        menu_content += f"\n         第{Page}页/共2页\n\n"
        menu_content += "       " + Emoji("187") + "其他功能" + Emoji("187") + "\n"
        menu_content += "/游戏菜单\n\n"
        menu_content += "菜单切换：/菜单+数字"
    elif Page == "2":
        for command in commands:
            status = json_data["Config"].get(command, "未知状态")
            menu_content += f"/{command}\n"

        menu_content +=  f"\n         第{Page}页/共2页\n\n"
        menu_content += "菜单切换：/菜单+数字"

    return menu_content


def generate_gamemenu(json_data, Page):
    commands = json_data["Commands"][Page]
    menu_content = "       ✨星辰Bot✨\n\n"
    if Page == "1":
        for command in commands:
            menu_content += f"/{command}\n"

        menu_content += f"\n         第{Page}页/共2页\n\n"
        menu_content += "菜单切换：/菜单+数字"
    elif Page == "2":
        for command in commands:
            status = json_data["Config"].get(command, "未知状态")
            menu_content += f"/{command}\n"

        menu_content += f"\n         第{Page}页/共2页\n\n"
        menu_content += "菜单切换：/菜单+数字"

    return menu_content


def is_function_normal(json_data, function_name):
    status = json_data["Config"].get(function_name)
    if status == "正常":
        return True
    else:
        return False
