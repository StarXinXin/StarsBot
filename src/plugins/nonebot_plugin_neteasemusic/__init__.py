import json
import os
import re
from pathlib import Path
import requests
from nonebot.plugin.on import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event

import nonebot
from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna.uniseg import UniMessage

from utils.AdminTool import is_group_in_whitelist
from utils.ImageDownloader import download_file
from utils.RedirectResolverHttpx import RedirectResolverHttpx
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_neteasemusic",
    description="网易云音乐点歌",
    usage="点歌：/点歌+霜雪千年"
          "播放：/播放+歌曲序号",
    config=Config,
)

from .tools.getmusicid import get_song_id_at_index

from utils.FileUtils import check_files_in_directory, delete_folder, ensure_file_exists, read_json_file
from ..nonebot_plugin_menu import is_function_normal

config = get_plugin_config(Config)

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)

Song = on_command("/点歌")


@Song.handle()
async def _(bot: Bot, event: Event, state: T_State, true=False):
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "点歌"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    get_msg = str(event.get_message())
                    if ' ' in get_msg[3:]:
                        content = get_msg[4:].strip()
                    else:
                        content = get_msg[3:].strip()
                    if content == "":
                        await UniMessage("请输入查询歌曲\n"
                                         "例如：/点歌 霜雪千年").send(reply_to=true)
                    else:
                        url = f"https://dev.iw233.cn/Music1/"

                        payload = f"input={content}&filter=name&type=netease&page=1"
                        headers = {
                            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
                            'Accept': "application/json, text/javascript, */*; q=0.01",
                            'Accept-Encoding': "gzip, deflate, br, zstd",
                            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                            'X-Requested-With': "XMLHttpRequest",
                            'Origin': "https://dev.iw233.cn",
                            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
                        }

                        response = requests.post(url, data=payload, headers=headers)
                        data = response.json()

                        result = []
                        for i, song in enumerate(data["data"], start=1):
                            title = re.sub(r'\s*\（[^)]*\）', '', song["title"])
                            author = re.sub(r'\s*\（[^)]*\）', '', song["author"])

                            title2 = re.sub(r'\s*\([^)]*\)', '', title)
                            author2 = re.sub(r'\s*\([^)]*\)', '', author)

                            result.append(f"{i}. {title2} - {author2}")

                        output = "\n".join(result)

                        file_path = f"Profile/MusicID/{event.get_user_id()}/ID.json"
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        song_ids = [song["songid"] for song in data["data"]]
                        with open(file_path, 'w') as f:
                            json.dump(song_ids, f)

                        await UniMessage(f"1网易云点歌\n\n"
                                         f"{output}\n\n请发送：/播放+序号 ，获取详细信息").send(reply_to=true)

            else:
                get_msg = str(event.get_message())
                if ' ' in get_msg[3:]:
                    content = get_msg[4:].strip()
                else:
                    content = get_msg[3:].strip()
                if not content:
                    await UniMessage("请输入查询歌曲\n"
                                     "例如：/点歌 霜雪千年").send(reply_to=true)
                url = f"https://dev.iw233.cn/Music1/"

                payload = f"input={content}&filter=name&type=netease&page=1"
                headers = {
                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
                    'Accept': "application/json, text/javascript, */*; q=0.01",
                    'Accept-Encoding': "gzip, deflate, br, zstd",
                    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                    'X-Requested-With': "XMLHttpRequest",
                    'Origin': "https://dev.iw233.cn",
                    'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
                }

                response = requests.post(url, data=payload, headers=headers)
                data = response.json()

                result = []
                for i, song in enumerate(data["data"], start=1):
                    title = re.sub(r'\s*\（[^)]*\）', '', song["title"])
                    author = re.sub(r'\s*\（[^)]*\）', '', song["author"])

                    title2 = re.sub(r'\s*\([^)]*\)', '', title)
                    author2 = re.sub(r'\s*\([^)]*\)', '', author)

                    result.append(f"{i}. {title2} - {author2}")

                output = "\n".join(result)

                file_path = f"Profile/MusicID/{event.get_user_id()}/ID.json"
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                song_ids = [song["songid"] for song in data["data"]]
                with open(file_path, 'w') as f:
                    json.dump(song_ids, f)

                await UniMessage(f"1网易云点歌\n\n"
                                 f"{output}\n\n请发送：/播放+序号 ，获取详细信息").send(reply_to=true)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)


weather = on_command("/播放")


@weather.handle()
async def send_menu(bot: Bot, event: Event, state: T_State, true=True):
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "点歌"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    get_msg = str(event.get_message())
                    if ' ' in get_msg[3:]:
                        content = get_msg[4:].strip()
                    else:
                        content = get_msg[3:].strip()
                    if content == "":
                        await UniMessage("请输入查询歌曲").send(reply_to=true)
                    else:
                        file_path = f"Profile/MusicID/{event.get_user_id()}/ID.json"  # 示例相对路径，根据实际情况修改
                        song_id = get_song_id_at_index(file_path, int(content) - 1)
                        if song_id is not None:
                            await UniMessage.at(event.get_user_id()).text(" 服务器正在处理的音频，请耐心等待").send(
                                reply_to=true)
                            Url = f"https://api.injahow.cn/meting/?server=netease&type=url&id={song_id}"
                            Redirect = RedirectResolverHttpx().resolve_redirect(Url)
                            file_path = f"./Download/Music/{event.get_user_id()}"
                            if check_files_in_directory(file_path):
                                if delete_folder(file_path):
                                    file_path = await download_file(Redirect, file_path, "Music.mp3")
                                    if file_path != "":
                                        msg = f"Download/Music/{event.get_user_id()}/Music.mp3"
                                        await UniMessage.voice(path=str(msg)).send()
                                    else:
                                        await UniMessage("音频下载失败了呢，到底是为什么？ ").send(reply_to=true)

                            else:
                                file_path = await download_file(Redirect, file_path, "Music.mp3")
                                if file_path != "":
                                    msg = f"Download/Music/{event.get_user_id()}/Music.mp3"
                                    await UniMessage.voice(path=str(msg)).send()
                                else:
                                    await UniMessage("音频下载失败了呢，到底是为什么？ ").send(reply_to=true)
                        else:
                            await UniMessage.at(event.get_user_id()).text(f" 好像并没有这首歌呀").send(reply_to=true)
            else:
                get_msg = str(event.get_message())
                if ' ' in get_msg[3:]:
                    content = get_msg[4:].strip()
                else:
                    content = get_msg[3:].strip()
                if content == "":
                    await UniMessage("请输入查询地点").send(reply_to=true)
                else:
                    file_path = f"Profile/MusicID/{event.get_user_id()}/ID.json"
                    try:
                        song_id = get_song_id_at_index(file_path, int(content)-1)
                        if song_id is not None:
                            Url = f"https://api.injahow.cn/meting/?server=netease&type=url&id={song_id}"
                            Redirect = RedirectResolverHttpx().resolve_redirect(Url)
                            file_path = f"./Download/Music/{event.get_user_id()}"
                            if check_files_in_directory(file_path):
                                if delete_folder(file_path):
                                    file_path = await download_file(Redirect, file_path, "Music.mp3")
                                    if file_path != "":
                                        msg = f"Download/Music/{event.get_user_id()}/Music.mp3"
                                        await UniMessage.voice(path=str(msg)).send()
                                    else:
                                        await UniMessage("音频下载失败了呢，到底是为什么？ ").send(reply_to=true)

                            else:
                                file_path = await download_file(Redirect, file_path, "Music.mp3")
                                if file_path != "":
                                    msg = f"Download/Music/{event.get_user_id()}/Music.mp3"
                                    await UniMessage.voice(path=str(msg)).send()
                                else:
                                    await UniMessage("音频下载失败了呢，到底是为什么？ ").send(reply_to=true)
                        else:
                            await UniMessage(f"好像并没有这首歌呀").send(reply_to=true)
                    except ValueError:
                        await UniMessage(f"好像并没有这首歌呀").send(reply_to=true)
                    except IndexError:
                        await UniMessage(f"错误：选择超出范围").send(reply_to=true)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)