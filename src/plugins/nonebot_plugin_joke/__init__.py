import os

import edge_tts
import nonebot

from nonebot import on_keyword  # 事件响应器函数
from nonebot.typing import T_State  # bot使用的对象和字典
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, Event  # #Message是使用cq码的必要函数
import requests
import json  # 处理api返回的json数据

from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMessage

from utils.AdminTool import is_group_in_whitelist
from utils.FileUtils import ensure_file_exists, read_json_file
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_joke",
    description="返回一个笑话,带语音",
    usage="/笑话"
          "/joke"
          "/讲个笑话",
    config=Config,
)

from ..nonebot_plugin_menu import is_function_normal

config = get_plugin_config(Config)

joke = on_keyword({"/笑话", "/joke", "/讲个笑话"})

@joke.handle()
async def handle_joke(bot: Bot, event: Event, state: T_State, true=False):
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "笑话"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    text = await get_joke()
                    await UniMessage.voice(path=text).send(reply_to=true)
            else:
                text = await get_joke()
                await UniMessage.voice(path=text).send(reply_to=true)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)

async def get_joke(true=True):
    url = 'https://api.vvhan.com/api/text/joke?type=json'
    res = requests.get(url)
    result = json.loads(res.text)
    joke = result['data']['content']
    await UniMessage(joke).send(reply_to=true)
    file_path = f"D:/StarsBot/Download/TTS/TTS.mp3"
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        communicate = edge_tts.Communicate(joke, "zh-CN-YunxiNeural")
        await communicate.save(file_path)
    else:
        communicate = edge_tts.Communicate(joke, "zh-CN-YunxiNeural")
        await communicate.save(file_path)
    return file_path
