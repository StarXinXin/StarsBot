from nonebot import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot_plugin_alconna.uniseg import UniMessage

import utils.AdminTool as at

from pathlib import Path

import nonebot
from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

# from .config import Config
#
# __plugin_meta__ = PluginMetadata(
#     name="nonebot_plugin_whitelist",
#     description="群白名单和管理员白名单管理",
#     usage="详细请看README.md文件",
#     config=Config,
# )
#
# config = get_plugin_config(Config)

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)

AddAGroupWhitelist = on_keyword({'/添加群白名单'})
RemoveAGroupWhitelist = on_keyword({'/移除群白名单'})
AddAdminWhitelist = on_keyword({'/添加管理员'})
RemoveAdminWhitelist = on_keyword({'/移除管理员'})

Menu = on_keyword({'/白名单配置'})
@Menu.handle()
async def menu(bot: Bot, event: Event, state: T_State):
    ids = event.get_session_id()
    parts = ids.split('_')
    if ids.startswith("group"):
        if at.is_group_in_whitelist(parts[1]):
            user = event.get_user_id()
            if at.is_admin_in_whitelist(user):
                await UniMessage(
                    "星辰Bot白名单配置\n\n"
                    "1：/添加群白名单 + 空格 + 群号\n"
                    "2：/移除群白名单 + 空格 + 群号\n"
                    "3：/添加管理员 + 空格 + 管理员ID\n"
                    "4：/移除管理员 + 空格 + 管理员ID\n\n"
                    "指令“1,2”在群里可直接发送：\n"
                    "/添加群白名单\n"
                    "/移除群白名单\n"
                    "填写群号的为私聊，因为无法自动识别"
                ).send(reply_to=True)
            else:
                await Menu.finish(f"你是管理员么？就查看白名单配置", reply_message=True)
    else:
        user = event.get_user_id()
        if at.is_admin_in_whitelist(user):
            await UniMessage(
                "星辰Bot白名单配置\n\n"
                "1：/添加群白名单 + 空格 + 群号\n"
                "2：/移除群白名单 + 空格 + 群号\n"
                "3：/添加管理员 + 空格 + 管理员ID\n"
                "4：/移除管理员 + 空格 + 管理员ID\n\n"
                "指令“1,2”在群里可直接发送：\n"
                "/添加群白名单\n"
                "/移除群白名单\n"
                "填写群号的为私聊，因为无法自动识别"
            ).send(reply_to=True)
        else:
            await Menu.finish(f"你是管理员么？就查看白名单配置", reply_message=True)

@AddAGroupWhitelist.handle()
async def add_group_whitelist(bot: Bot, event: Event, state: T_State, true=True):
    ids = event.get_session_id()
    # 只对于群聊信息进行响应
    if ids.startswith("group"):
        parts = ids.split('_')
        user = event.get_user_id()
        if at.is_admin_in_whitelist(user):
            if at.is_group_in_whitelist(parts[1]):
                await UniMessage(f"群 {parts[1]} 已在星辰Bot白名单中").send(reply_to=true)
            else:
                at.add_to_group_whitelist(parts[1])
                await UniMessage(f"群 {parts[1]} 已加入星辰Bot白名单").send(reply_to=true)
        else:
            await AddAGroupWhitelist.finish(f"你是管理员么？就添加群白名单", reply_message=true)
    else:
        get_msg = str(event.get_message())
        if ' ' in get_msg[8:]:
            content = get_msg[9:].strip()
        else:
            content = get_msg[8:].strip()
            
        if not content:
            await UniMessage(
                "当前非群聊状态\n"
                "添加白名单，请使用：\n\n"
                "/添加群白名单 + 空格 + 群号\n"
                "/添加群白名单 + 群号"
            ).send(reply_to=true)
        else:
            user = event.get_user_id()
            if at.is_admin_in_whitelist(user):
                try:
                    group_id = int(content)  # 尝试将content转换为整数
                    if at.is_group_in_whitelist(str(group_id)):
                        await UniMessage(f"群 {group_id} 已在星辰Bot白名单中").send(reply_to=true)
                    else:
                        at.add_to_group_whitelist(str(group_id))
                        await UniMessage(f"群 {group_id} 已加入星辰Bot白名单").send(reply_to=true)
                except ValueError:  # 如果content不能转换为整数，捕获ValueError
                    await UniMessage("请输入有效的管理员ID（仅数字）").send(reply_to=True)

            else:
                await AddAGroupWhitelist.finish(f"你是管理员么？就添加群白名单", reply_message=true)


@RemoveAGroupWhitelist.handle()
async def remove_group_whitelist(bot: Bot, event: Event, state: T_State, true=True):
    ids = event.get_session_id()
    # 只对于群聊信息进行响应
    if ids.startswith("group"):
        parts = ids.split('_')
        user = event.get_user_id()
        if at.is_admin_in_whitelist(user):
            if at.is_group_in_whitelist(parts[1]):
                at.remove_from_group_whitelist(parts[1])
                await UniMessage(f"群 {parts[1]} 已从白名单中移除").send(reply_to=true)
            else:
                await UniMessage(f"群 {parts[1]} 不在白名单中").send(reply_to=true)
        else:
            await RemoveAGroupWhitelist.finish(f"你是管理员么？就移除群白名单")
    else:
        get_msg = str(event.get_message())

        if ' ' in get_msg[8:]:
            content = get_msg[9:].strip()  
        else:
            content = get_msg[8:].strip()

        if not content:
            await UniMessage(
                "当前非群聊状态\n"
                "请使用以下两条指令移除群白名单 ：\n\n"
                "1：/移除群白名单 + 空格 + 群号\n"
                "2：/移除群白名单 + 群号"
            ).send(reply_to=True)
        else:
            user = event.get_user_id()
            if at.is_admin_in_whitelist(user):
                try:
                    group_id = int(content)  # 尝试将content转换为整数
                    if at.is_group_in_whitelist(str(group_id)):  # 注意这里传入的是整数而不是字符串
                        at.remove_from_group_whitelist(str(group_id))
                        await UniMessage(f"群 {group_id} 已从白名单中移除").send(reply_to=True)
                    else:
                        await UniMessage(f"群 {group_id} 不在白名单中").send(reply_to=True)
                except ValueError:  # 如果content不能转换为整数，捕获ValueError
                    await UniMessage("请输入有效的群号（仅数字）").send(reply_to=True)
            else:
                await RemoveAGroupWhitelist.finish(f"你是管理员么？就移除群白名单")


@AddAdminWhitelist.handle()
async def add_admin_whitelist(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())

    # 移除命令后的第一个空格（如果存在）
    content = get_msg[8:].lstrip() if ' ' in get_msg[7:] else get_msg[7:].strip()

    if not content:
        await UniMessage(
            "请使用以下的指令添加管理员：\n\n"
            "1：/添加管理员 + 空格 + 管理员ID\n"
            "2：/添加管理员 + 管理员ID"
        ).send(reply_to=True)
    else:
        user = event.get_user_id()
        if at.is_admin_in_whitelist(user):  # 确保user也是字符串类型
            try:
                user_id = int(content)  # 尝试将content转换为整数
                if at.is_admin_in_whitelist(str(user_id)):  # 注意这里传入的是整数而不是字符串
                    await UniMessage(f"管理员 {content} 已在星辰Bot白名单中").send(reply_to=True)
                else:
                    at.add_to_admin_whitelist(str(user_id))
                    await UniMessage(f"管理员 {content} 已加入星辰Bot白名单").send(reply_to=True)
            except ValueError:  # 如果content不能转换为整数，捕获ValueError
                await UniMessage("请输入有效的管理员ID（仅数字）").send(reply_to=True)
        else:
            await UniMessage("你是管理员么？就添加管理员白名单").send(reply_to=True)


@RemoveAdminWhitelist.handle()
async def remove_admin_whitelist(bot: Bot, event: Event, state: T_State):
    get_msg = str(event.get_message())

    if ' ' in get_msg[7:]:
        content = get_msg[8:].strip()  
    else:
        content = get_msg[7:].strip()

    if not content:
        await UniMessage(
            "请使用以下的指令添加管理员：\n\n"
            "1：/移除管理员 + 空格 + 管理员ID\n"
            "2：/移除管理员 + 管理员ID"
        ).send(reply_to=True)
    else:
        user = event.get_user_id()
        if at.is_admin_in_whitelist(user):
            try:
                admin_id = int(content)  # 尝试将content转换为整数
                if at.is_admin_in_whitelist(str(admin_id)):  # 注意这里传入的是整数而不是字符串
                    at.remove_from_admin_whitelist(str(admin_id))  # 同样，这里传入的是整数
                    await UniMessage(f"管理员 {admin_id} 已从白名单中移除").send(reply_to=True)
                else:
                    await UniMessage(f"管理员 {admin_id} 并不在白名单中").send(reply_to=True)
            except ValueError:  # 如果content不能转换为整数，捕获ValueError
                await UniMessage("请输入有效的管理员ID（仅数字）").send(reply_to=True)
        else:
            await UniMessage("你是管理员么？就添加管理员白名单").send(reply_to=True)
