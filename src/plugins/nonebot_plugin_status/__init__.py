from datetime import datetime
import platform
import time

import psutil
from nonebot import get_plugin_config, on_command
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMessage, Emoji

from utils.AdminTool import is_group_in_whitelist
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_status",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

Stutas = on_command("status", aliases={"/运行状态", "/状态", "/运行"}, priority=1)

@Stutas.handle()
async def _(bot, event):
    ids = event.get_session_id()
    if ids.startswith("group"):
        parts = ids.split('_')
        if is_group_in_whitelist(parts[1]):
            cpu = (str(psutil.cpu_percent(1))) + '%'
            boot_time = psutil.boot_time()
            boot_datetime = datetime.fromtimestamp(boot_time)
            now = datetime.now()
            uptime = now - boot_datetime
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"{days}天{hours}小时{minutes}分钟{seconds}秒"

            text = (f'✨星辰Bot - 运行状态✨\n\n'
                    # f"✨ 开机时间：{datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"✨ 已运行：{uptime_str}\n"
                    f'✨ 服务器系统名称: { platform.system()}\n'
                    f'✨ 操作系统版本: {platform.version()}\n'
                    f'✨ Python版本: {platform.python_version()}\n'
                    f'✨ Python解释器名称: {platform.python_implementation()}\n'
                    u"✨ CPU使用率: %s" % cpu)
            await UniMessage(text).send(reply_to=True)
    else:
        cpu = (str(psutil.cpu_percent(1))) + '%'
        boot_time = psutil.boot_time()
        boot_datetime = datetime.fromtimestamp(boot_time)
        now = datetime.now()
        uptime = now - boot_datetime
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{days}天{hours}小时{minutes}分钟{seconds}秒"

        text = (f'✨星辰Bot - 运行状态✨\n\n'
                # f"✨ 开机时间：{datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"✨ 已运行：{uptime_str}\n"
                f'✨ 服务器系统名称: {platform.system()}\n'
                f'✨ 操作系统版本: {platform.version()}\n'
                f'✨ Python版本: {platform.python_version()}\n'
                f'✨ Python解释器名称: {platform.python_implementation()}\n'
                u"✨ CPU使用率: %s" % cpu)
        await UniMessage(text).send(reply_to=True)