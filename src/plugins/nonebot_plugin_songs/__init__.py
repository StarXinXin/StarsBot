import json
import os
import re

import requests
from nonebot import get_plugin_config
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent, Message, MessageSegment
from nonebot.params import RegexDict, CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.plugin.on import on_regex, on_command
from nonebot_plugin_alconna import Emoji, UniMessage

from utils.AdminTool import is_group_in_whitelist
from utils.FileUtils import ensure_file_exists, read_json_file
from utils.Network import make_request
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_songs",
    description="QQ音乐点歌[Plus]",
    usage="点歌：/点歌 霜雪千年"
          "播放：/播放 歌曲序号",
    config=Config,
)

from ..nonebot_plugin_menu import is_function_normal

config = get_plugin_config(Config)

SongMenu = on_command(r'/点歌')


@SongMenu.handle()
async def _(bot, event: PrivateMessageEvent | GroupMessageEvent, state, content: Message = CommandArg()) -> None:
    if not content.extract_plain_text():
        data = Emoji("187") + ' 点歌说明\n1. 搜索歌曲 /点歌 歌名'
        await UniMessage.send(data, reply_message=True)


SongSearch = on_regex(r'/点歌 (?P<Platform>.+)')


@SongSearch.handle()
async def _(bot, event: PrivateMessageEvent | GroupMessageEvent, state, matched: dict = RegexDict()) -> None:
    platform = matched['Platform']
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "点歌"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    response = make_request(f"https://api.lolimi.cn/API/yiny/?word={platform}")
                    if response.status_code == 200:
                        data = response.json()
                        getData = ""
                        if data["code"] == 200:
                            songs = data["data"]
                            for index, song_info in enumerate(songs, start=1):
                                song = song_info["song"]
                                singer = song_info["singer"]
                                song = re.sub(r'\([^)]*\)', '', song)
                                getData += f"{index}. {song} - {singer}\n"

                            file_path = f"Profile/MusicID/{event.get_user_id()}/ID.json"
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            song_ids = [songs["id"] for songs in data["data"]]
                            with open(file_path, 'w') as f:
                                json.dump(song_ids, f)

                            getData = getData.rstrip('\n')
                            await UniMessage(f"QQ音乐点歌\n\n"
                                             f"{getData}\n\n/播放 序号 ，获取详细信息").send(reply_to=True)
                        else:
                            await UniMessage(f"接口返回错误，代码: {data['code']}").send(reply_to=True)
                    else:
                        await UniMessage(f"请求失败，状态码: {response.status_code}").send(reply_to=True)
            else:
                response = make_request(f"https://api.lolimi.cn/API/yiny/?word={platform}")
                if response.status_code == 200:
                    data = response.json()
                    getData = ""
                    if data["code"] == 200:
                        songs = data["data"]
                        for index, song_info in enumerate(songs, start=1):
                            song = song_info["song"]
                            singer = song_info["singer"]
                            song = re.sub(r'\([^)]*\)', '', song)
                            getData += f"{index}. {song} - {singer}\n"

                        file_path = f"Profile/MusicID/{event.get_user_id()}/ID.json"
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        song_ids = [songs["id"] for songs in data["data"]]
                        with open(file_path, 'w') as f:
                            json.dump(song_ids, f)

                        getData = getData.rstrip('\n')
                        await UniMessage(f"QQ音乐点歌\n\n"
                                         f"{getData}\n\n/播放 序号 ，获取详细信息").send(reply_to=True)
                    else:
                        await UniMessage(f"接口返回错误，代码: {data['code']}").send(reply_to=True)
                else:
                    await UniMessage(f"请求失败，状态码: {response.status_code}").send(reply_to=True)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)

PlaySong = on_regex(r'/播放 (?P<Platform>([1-9]|10))')

@PlaySong.handle()
async def _(bot, event: PrivateMessageEvent | GroupMessageEvent, state, matched: dict = RegexDict()) -> None:
    song_index = int(matched["Platform"]) - 1
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "点歌"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    file_path = f"Profile/MusicID/{event.get_user_id()}/ID.json"
                    if os.path.exists(file_path):
                        with open(file_path, 'r', encoding='utf-8') as file:
                            ids = json.load(file)
                        if 0 <= song_index < len(ids):
                            song_id = ids[song_index]
                            url = f"https://api.lolimi.cn/API/yiny/?q=4&id={song_id}"
                            response = requests.get(url)
                            if response.status_code == 200:
                                data = response.json()
                                if data["code"] == 200:
                                    song_data = data["data"]
                                    await PlaySong.send(
                                        MessageSegment.image(str(song_data["cover"])) + "\n" + MessageSegment.text(
                                            f"歌曲 - 歌手: {song_data["song"]}") + "\n" + MessageSegment.text(
                                            f"是否付费: {song_data["pay"]}") + "\n" + MessageSegment.text(
                                            f"音质: {song_data["quality"]}") + "\n" + MessageSegment.text(
                                            f"时间: {song_data["time"]}") + "\n" + MessageSegment.text(
                                            f"大小: {song_data["size"]}") + "\n" + MessageSegment.text(
                                            f"音乐地址: {song_data["link"]}") + "\n" + MessageSegment.text(
                                            f"下载链接: {song_data["url"]}"),
                                        reply_message=True)
                                    await PlaySong.finish(
                                        MessageSegment.record(str(song_data["url"])), timeout=100)
                                else:
                                    await bot.send(event, "获取歌曲信息失败，请检查ID是否正确", reply_message=True)
                            else:
                                await bot.send(event, "请求失败，请检查网络连接", reply_message=True)
                        else:
                            await bot.send(event, "输入的索引超出范围，请输入1到10之间的数字", reply_message=True)
                    else:
                        await bot.send(event, "未找到歌曲ID文件，请检查文件路径", reply_message=True)
            else:
                file_path = f"Profile/MusicID/{event.get_user_id()}/ID.json"
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        ids = json.load(file)
                    if 0 <= song_index < len(ids):
                        song_id = ids[song_index]
                        url = f"https://api.lolimi.cn/API/yiny/?q=4&id={song_id}"
                        response = requests.get(url)
                        if response.status_code == 200:
                            data = response.json()
                            if data["code"] == 200:
                                song_data = data["data"]
                                await PlaySong.send(
                                    MessageSegment.image(str(song_data["cover"])) + "\n" + MessageSegment.text(
                                        f"歌曲 - 歌手: {song_data["song"]}") + "\n" + MessageSegment.text(
                                        f"是否付费: {song_data["pay"]}") + "\n" + MessageSegment.text(
                                        f"音质: {song_data["quality"]}") + "\n" + MessageSegment.text(
                                        f"时间: {song_data["time"]}") + "\n" + MessageSegment.text(
                                        f"大小: {song_data["size"]}") + "\n" + MessageSegment.text(
                                        f"音乐地址: {song_data["link"]}") + "\n" + MessageSegment.text(
                                        f"下载链接: {song_data["url"]}"),
                                    reply_message=True)
                                await PlaySong.finish(
                                    MessageSegment.record(str(song_data["url"])), timeout=100)
                            else:
                                await bot.send(event, "获取歌曲信息失败，请检查ID是否正确", reply_message=True)
                        else:
                            await bot.send(event, "请求失败，请检查网络连接", reply_message=True)
                    else:
                        await bot.send(event, "输入的索引超出范围，请输入1到10之间的数字", reply_message=True)
                else:
                    await bot.send(event, "未找到歌曲ID文件，请检查文件路径", reply_message=True)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)