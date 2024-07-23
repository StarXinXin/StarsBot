import re
import warnings

from nonebot import on_keyword, on_regex, on_request, on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, GroupRequestEvent, PrivateMessageEvent
from nonebot.permission import *
from nonebot.typing import T_State
from nonebot_plugin_alconna import Emoji
from nonebot_plugin_alconna.uniseg import UniMessage

from utils.AdminTool import is_admin_in_whitelist, is_group_in_whitelist

warnings.filterwarnings("ignore")

# 撤回消息
che = on_keyword({''})  # 填入禁用词
qtk = on_regex(pattern=r'^/开启全禁$')
qtg = on_regex(pattern=r'^/关闭全禁$')
jy = on_keyword({'/禁'})
jj = on_keyword({'/解'})
group_remove = on_keyword({'/踢'})
group_sq = on_request()
agree_apply = on_regex(pattern=r'^/同意申请$')
disagree_apply = on_regex(pattern=r'^/拒绝申请$')

Menu = on_command("/群管菜单", priority=1, block=True)


@Menu.handle()
async def _(event: PrivateMessageEvent | GroupMessageEvent) -> None:
    await UniMessage("✨群管菜单✨\n\n"
                     "禁言(全体)" + Emoji("187") +
                     "\n/开启全禁\n"
                     "/关闭全禁\n\n"
                     "禁言(个人)" + Emoji("187") +
                     "\n/禁 @需禁言的人 时间\n"
                     "/解 @需解禁的人\n"
                     "Tip: 禁言时间单位为分钟\n\n"
                     "功能" + Emoji("187") +
                     "\n/踢 @需踢出的人\n\n"
                     "新人进群管理" + Emoji("187") +
                     "\n/同意申请\n"
                     "/拒绝申请").send(reply_to=True)


# @che.handle()
# async def c(bot: Bot, event: GroupMessageEvent, state: T_State):
#     mid = event.message_id
#     group = event.group_id
#     qq = event.user_id
#     sj = 300
#     await bot.delete_msg(message_id=mid)
#     await bot.set_group_ban(group_id=group, user_id=qq, duration=sj)
#     await che.finish(message=f'@{qq} 你的发言可能包含敏感词汇，这里禁言5分钟警告一下')


@qtk.handle()
async def j(bot: Bot, event: GroupMessageEvent, state: T_State):
    group = event.group_id
    ids = event.get_session_id()
    if ids.startswith("group"):
        parts = ids.split('_')
        user = event.get_user_id()
        if is_admin_in_whitelist(user):
            if is_group_in_whitelist(parts[1]):
                await bot.set_group_whole_ban(group_id=group, enable=True)
                await UniMessage(f"已经为您开启全体禁言").send(reply_to=True)
        else:
            await UniMessage(f"你没有资格命令我！").send(reply_to=True)
    else:
        await UniMessage(f"该功能无法在私聊中使用").send(reply_to=True)


@qtg.handle()
async def g(bot: Bot, event: GroupMessageEvent, state: T_State):
    group = event.group_id  # 获取当前群号
    ids = event.get_session_id()
    if ids.startswith("group"):
        parts = ids.split('_')
        user = event.get_user_id()
        if is_admin_in_whitelist(user):
            if is_group_in_whitelist(parts[1]):
                await bot.set_group_whole_ban(group_id=group, enable=False)
                await UniMessage(f"已经为您关闭全体禁言").send(reply_to=True)
        else:
            await UniMessage(f"你没有资格命令我！").send(reply_to=True)
    else:
        await UniMessage(f"该功能无法在私聊中使用").send(reply_to=True)


@jy.handle()
async def sj(bot: Bot, event: GroupMessageEvent, state: T_State):
    data = str(event.message)
    qq2 = event.user_id  # 获取用户id
    qq = re.findall(r'qq=(.+?)]', data)
    qq = int(qq[0])
    sj1 = re.findall(r'] (.+)', data)
    sj = sj1[0]
    sj = int(sj) * 60
    ids = event.get_session_id()
    if ids.startswith("group"):
        parts = ids.split('_')
        user = event.get_user_id()
        if is_admin_in_whitelist(user):
            if is_group_in_whitelist(parts[1]):
                await bot.set_group_ban(group_id=event.group_id, user_id=qq, duration=sj)
                await UniMessage(f"已经为“{qq}”禁言{sj1[0]}分钟").send(reply_to=True)
        else:
            await UniMessage(f"你没有资格命令我！").send(reply_to=True)
    else:
        await UniMessage(f"该功能无法在私聊中使用").send(reply_to=True)


@jj.handle()
async def sj(bot: Bot, event: GroupMessageEvent, state: T_State):
    data = str(event.message)
    qq = re.findall(r'qq=(.+?)]', data)
    qq = int(qq[0])
    ids = event.get_session_id()
    if ids.startswith("group"):
        parts = ids.split('_')
        user = event.get_user_id()
        if is_admin_in_whitelist(user):
            if is_group_in_whitelist(parts[1]):
                await bot.set_group_ban(group_id=event.group_id, user_id=qq, duration=0)
                await UniMessage(f"已解除“{qq}”的禁言").send(reply_to=True)
        else:
            await UniMessage(f"你没有资格命令我！").send(reply_to=True)
    else:
        await UniMessage(f"该功能无法在私聊中使用").send(reply_to=True)


@group_sq.handle()
async def sq(bot: Bot, event: GroupRequestEvent, state: T_State):
    qq_id = event.user_id
    message = event.comment  # 获取验证信息
    global flag_id
    flag_id = event.flag  # 申请进群的flag
    global type_id
    type_id = event.sub_type  # 请求信息的类型
    ids = event.get_session_id()
    if ids.startswith("group"):
        parts = ids.split('_')
        if is_group_in_whitelist(parts[1]):
            await UniMessage(f"用户 {qq_id} 申请进群\n验证消息：{message}\n同意/拒绝申请").send(reply_to=True)


@agree_apply.handle()
async def sn(bot: Bot, event: GroupMessageEvent, state: T_State):
    if event.sender.role == "admin" or event.sender.role == "owner":
        await bot.set_group_add_request(flag=flag_id, sub_type=type_id, approve=True)
    else:
        await UniMessage(f"你没有资格命令我！").send(reply_to=True)


@disagree_apply.handle()
async def sn(bot: Bot, event: GroupMessageEvent, state: T_State):
    if event.sender.role == "admin" or event.sender.role == "owner":
        await bot.set_group_add_request(flag=flag_id, sub_type=type_id, approve=False,
                                        reason='')
        await UniMessage(f"机器人自动审批，如有误判请联系群主或其他管理员").send(reply_to=True)
    else:
        await UniMessage(f"你没有资格命令我！").send(reply_to=True)


@group_remove.handle()
async def move(bot: Bot, event: GroupMessageEvent, state: T_State):
    if event.sender.role == "admin" or event.sender.role == "owner":
        data = str(event.message)
        group_id = event.group_id
        qq_id = re.findall(r'qq=(.+?)]', data)
        qq_id = qq_id[0]
        await bot.set_group_kick(group_id=group_id, user_id=qq_id, reject_add_request=False)
        await UniMessage(f'已将QQ:{qq_id}移除群聊').send(reply_to=True)
    else:
        await UniMessage(f"你没有资格命令我！").send(reply_to=True)
