import json
import os
from datetime import datetime

import requests
from nonebot import get_plugin_config, require, get_bots, on_command, on_regex
from nonebot.adapters.onebot.v11 import Bot, Event, Message, PrivateMessageEvent, GroupMessageEvent, MessageSegment
from nonebot.params import CommandArg, RegexDict
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot_plugin_alconna import UniMessage, Emoji

from utils.AdminTool import is_group_in_whitelist, is_admin_in_whitelist
from utils.FileUtils import check_files_in_directory, file_exists
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_timing",
    description="整点报时插件",
    usage="/添加报时白名单"
          "/移除报时白名单"
          "/(打开|关闭)整点报时"
          "/设置报时模式 语音"
          "/设置报时模式 文本",
    config=Config,
)

from .utils import add_to_white_list, remove_from_white_list, load_white_list, update_config_value, \
    get_or_create_config, is_value_in_whitelist

config = get_plugin_config(Config)

SettingsMenu = on_command("/整点报时")


@SettingsMenu.handle()
async def _(bot: Bot, event: Event, state: T_State, true=True):
    ids = event.get_session_id()
    if ids.startswith("group"):
        parts = ids.split('_')
        if is_group_in_whitelist(parts[1]):
            user = event.get_user_id()
            if is_admin_in_whitelist(user):
                await UniMessage(
                    Emoji("187") + " 整点报时功能指令：\n\n"
                    + Emoji("187") + " /添加报时白名单\n"
                    + Emoji("187") + " /移除报时白名单\n"
                    + Emoji("187") + " /设置报时模式 语音\n"
                    + Emoji("187") + " /设置报时模式 文本\n"
                    + Emoji("187") + " /(打开|关闭)整点报时"
                ).send(reply_to=true)
            else:
                await UniMessage(
                    "整点报时，只有Bot管理员才能操作"
                ).send(reply_to=true)
    else:
        user = event.get_user_id()
        if is_admin_in_whitelist(user):
            await UniMessage(
                Emoji("187") + " 整点报时功能指令：\n\n"
                + Emoji("187") + " /添加报时白名单\n"
                + Emoji("187") + " /移除报时白名单\n"
                + Emoji("187") + " /设置报时模式 语音\n"
                + Emoji("187") + " /设置报时模式 文本\n"
                + Emoji("187") + " /(打开|关闭)整点报时"
            ).send(reply_to=true)
        else:
            await UniMessage(
                "整点报时，只有Bot管理员才能操作"
            ).send(reply_to=true)


add_timing_whitelist = on_command("/添加报时白名单", priority=0, block=True)


@add_timing_whitelist.handle()
async def _(bot: Bot, event: Event, state: T_State, true=True, content: Message = CommandArg()):
    ids = event.get_session_id()
    file_path = f"Profile/Timing/TimeOnHour/WhiteList.json"
    if ids.startswith("group"):
        parts = ids.split('_')
        if is_group_in_whitelist(parts[1]):
            user = event.get_user_id()
            if is_admin_in_whitelist(user):
                if not content:
                    await UniMessage(
                        add_to_white_list(str(ids.split("_")[1]), file_path)
                    ).send(reply_to=true)
                else:
                    await UniMessage(
                        add_to_white_list(str(content), file_path)
                    ).send(reply_to=true)
            else:
                await UniMessage(
                    "整点报时，只有Bot管理员才能操作"
                ).send(reply_to=true)
    else:
        user = event.get_user_id()
        if is_admin_in_whitelist(user):
            if not content:
                await UniMessage(
                    "请输入要添加的群号"
                ).send(reply_to=true)
            else:
                await UniMessage(
                    add_to_white_list(str(content), file_path)
                ).send(reply_to=true)
        else:
            await UniMessage(
                "整点报时，只有Bot管理员才能操作"
            ).send(reply_to=true)


remove_timing_whitelist = on_command("/移除报时白名单", priority=0, block=True)


@remove_timing_whitelist.handle()
async def _(bot: Bot, event: Event, state: T_State, true=True, content: Message = CommandArg()):
    ids = event.get_session_id()
    file_path = f"Profile/Timing/TimeOnHour/WhiteList.json"
    if ids.startswith("group"):
        parts = ids.split('_')
        if is_group_in_whitelist(parts[1]):
            user = event.get_user_id()
            if is_admin_in_whitelist(user):
                if not content:
                    await UniMessage(
                        remove_from_white_list(str(ids.split("_")[1]), file_path)
                    ).send(reply_to=true)
                else:
                    await UniMessage(
                        remove_from_white_list(str(content), file_path)
                    ).send(reply_to=true)
        else:
            await UniMessage(
                "整点报时，只有Bot管理员才能操作"
            ).send(reply_to=true)
    else:
        user = event.get_user_id()
        if is_admin_in_whitelist(user):
            if not content:
                await UniMessage(
                    "请输入要移除的群号"
                ).send(reply_to=true)
            else:
                await UniMessage(
                    remove_from_white_list(str(content), file_path)
                ).send(reply_to=true)
        else:
            await UniMessage(
                "整点报时，只有Bot管理员才能操作"
            ).send(reply_to=true)


# set_timing_theme_p = on_regex(r"/设置报时模式 (?P<Platform>(文本|语音)) (?P<Num>\d+)")
set_timing_theme_p = on_regex(r"/设置报时模式 (?P<Platform>(文本|语音))")


@set_timing_theme_p.handle()
async def j(foo: PrivateMessageEvent | GroupMessageEvent, matched=RegexDict()) -> None:
    ids = foo.get_session_id()
    parts = ids.split('_')
    if ids.startswith("group"):
        if is_group_in_whitelist(parts[1]):
            if check_files_in_directory("Profile/Timing/TimeOnHour"):
                data = get_or_create_config(ids, "g")
                config_file_path = f"Profile/Timing/TimeOnHour/{ids.split('_')[1]}/ConfigData.json"
                result = is_value_in_whitelist(parts[1])
                if not result:
                    await OFFON.finish(MessageSegment.face('344') + MessageSegment.text(
                        "该群聊未在白名单中，请添加白名单后重试\n/添加报时白名单"), reply_message=True)
                else:
                    user = foo.get_user_id()
                    if is_admin_in_whitelist(user):
                        if matched["Platform"] == "语音":
                            if data["Type"] == "语音":
                                await UniMessage(
                                    f"群 {ids.split('_')[1]} 当前模式已经为语音模式"
                                ).send(reply_to=True)
                            else:
                                update_config_value(config_file_path, "Type", "语音")
                                await UniMessage(
                                    f"群 {ids.split('_')[1]} 当前模式已设置为：语音"
                                ).send(reply_to=True)
                        elif matched["Platform"] == "文本":
                            if data["Type"] == "文本":
                                await UniMessage(
                                    f"群 {ids.split('_')[1]} 当前模式已经为文本模式"
                                ).send(reply_to=True)
                            else:
                                update_config_value(config_file_path, "Type", "文本")
                                await UniMessage(
                                    f"群 {ids.split('_')[1]} 当前模式已设置为：文本"
                                ).send(reply_to=True)
                        else:
                            await UniMessage(
                                "好像没有这个选项"
                            ).send(reply_to=True)
                    else:
                        await UniMessage(
                            "整点报时，只有Bot管理员才能操作"
                        ).send(reply_to=True)
            else:
                await UniMessage("整点报时功能配置文件异常").send(reply_to=True)
    else:
        await UniMessage("整点报时功能，请在群聊中使用指令").send(reply_to=True)


OFFON = on_regex(r"/(?P<Platform>(打开|关闭))整点报时")


@OFFON.handle()
async def j(foo: PrivateMessageEvent | GroupMessageEvent, matched=RegexDict()) -> None:
    ids = foo.get_session_id()
    parts = ids.split('_')
    if ids.startswith("group"):
        if is_group_in_whitelist(parts[1]):
            if check_files_in_directory("Profile/Timing/TimeOnHour"):
                if file_exists(f"Profile/Timing/TimeOnHour/{ids.split('_')[1]}/ConfigData.json"):
                    config_file_path = f"Profile/Timing/TimeOnHour/{ids.split('_')[1]}/ConfigData.json"
                    data = load_white_list(config_file_path)
                    result = is_value_in_whitelist(parts[1])
                    if not result:
                        await OFFON.finish(MessageSegment.face('344') + MessageSegment.text(
                            "该群聊未在白名单中，请添加白名单后重试\n/添加报时白名单"), reply_message=True)
                    else:
                        user = foo.get_user_id()
                        if is_admin_in_whitelist(user):
                            if matched["Platform"] == "打开":
                                if data["Use"]:
                                    data = MessageSegment.face('320') + MessageSegment.text(
                                        "整点报时已经打开了，不要重复打开哦~")
                                    await OFFON.finish(data, reply_message=True)
                                else:
                                    update_config_value(config_file_path, "Use", True)
                                    data = MessageSegment.face('320') + MessageSegment.text("整点报时已打开，不要忘记时间喔~")
                                    await OFFON.finish(data, reply_message=True)
                            elif matched["Platform"] == "关闭":
                                if not data["Use"]:
                                    data = MessageSegment.face('320') + MessageSegment.text(
                                        "整点报时已经关闭了，不要重复关闭哦~")
                                    await OFFON.finish(data, reply_message=True)
                                else:
                                    update_config_value(config_file_path, "Use", False)
                                    data = MessageSegment.face('320') + MessageSegment.text("整点报时已关闭，欢迎您下次使用~")
                                    await OFFON.finish(data, reply_message=True)
                            else:
                                await UniMessage(
                                    "好像没有这个选项"
                                ).send(reply_to=True)
                        else:
                            await UniMessage("整点报时，只有Bot管理员才能操作").send(reply_to=True)
                else:
                    await UniMessage("请先使用指令：\n\n/设置报时模式 (语音|文本)\n\n初始化配置文件").send(reply_to=True)
            else:
                await UniMessage("整点报时功能配置文件异常").send(reply_to=True)
        else:
            await UniMessage("整点报时功能，请在群聊中使用指令").send(reply_to=True)


# 加载定时器
timing = require("nonebot_plugin_apscheduler").scheduler

# # 设置在早上1:00发送信息
# @timing.scheduled_job("cron", hour='1', minute='00', second='00', id="TimeSignal20")
# async def TimeSignal20():
#     white_list = load_white_list("Profile/Timing/TimeOnHour/WhiteList.json")
#     base_path = "Profile/Timing/TimeOnHour"
#
#     bot, = get_bots().values()
#
#     for folder_name in os.listdir(base_path):
#         folder_path = os.path.join(base_path, folder_name)
#         config_path = os.path.join(folder_path, "ConfigData.json")
#
#         if os.path.isdir(folder_path) and os.path.exists(config_path):
#             config = load_config(config_path)
#
#             if config["Use"] and folder_name in white_list:
#                 if config["Type"] == "语音":
#                     await send_voice_signal(bot, folder_name)
#                 else:
#                     await send_text_signal(bot, folder_name)
async def time_signal_task():
    if check_files_in_directory("Profile/Timing/TimeOnHour"):
        white_list = load_white_list("Profile/Timing/TimeOnHour/WhiteList.json")
        base_path = "Profile/Timing/TimeOnHour"

        bot, = get_bots().values()

        for folder_name in os.listdir(base_path):
            folder_path = os.path.join(base_path, folder_name)
            config_path = os.path.join(folder_path, "ConfigData.json")

            if os.path.isdir(folder_path) and os.path.exists(config_path):
                config = load_white_list(config_path)

                if config["Use"] and folder_name in white_list:
                    if config["Type"] == "语音":
                        await send_voice_signal(bot, folder_name)
                    else:
                        await send_text_signal(bot, folder_name)

# 设置在每个整点发送信息
for hour in range(24):
    timing.scheduled_job("cron", hour=hour, minute=0, second=0, id=f"TimeSignal{hour}")(time_signal_task)

async def send_voice_signal(bot, group_id):
    current_hour = datetime.now().hour
    url = f"https://xiaoapi.cn/API/zs_zdbs.php?h={current_hour}"
    response = requests.get(url, timeout=100)
    if response.status_code == 200:
        data = response.json()
        await bot.send_msg(
            message_type="group",
            group_id=int(group_id),
            message=f'[CQ:record,file={data["mp3"]}]'
        )
    else:
        await UniMessage(f"无法获取数据。状态码：{response.status_code}").send(reply_to=True)


async def send_text_signal(bot, group_id):
    current_hour = datetime.now().hour
    url = f"https://xiaoapi.cn/API/zs_zdbs.php?h={current_hour}"
    response = requests.get(url, timeout=100)
    if response.status_code == 200:
        data = response.json()
        await bot.send_msg(
            message_type="group",
            group_id=int(group_id),
            message=f'现在是：{data["time"]}\n{data["msg"]}'
        )
    else:
        await UniMessage(f"无法获取数据。状态码：{response.status_code}").send(reply_to=True)