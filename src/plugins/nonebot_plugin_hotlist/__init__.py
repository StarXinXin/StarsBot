import json
import os
import re

import aiohttp
import asyncio
from aiohttp import ClientTimeout
from nonebot import get_plugin_config, on_regex, on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, PrivateMessageEvent
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot_plugin_alconna import UniMessage

from utils.AdminTool import is_group_in_whitelist
from utils.FileUtils import ensure_file_exists, read_json_file
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_hotlist",
    description="获取各平台的热搜榜信息五十条",
    usage="/微博热搜榜"
          "/百度热搜榜"
          "/知乎热搜榜"
          "/抖音热搜榜"
          "/B站热搜榜"
          "/今日头条热搜榜",
    config=Config,
)
import urllib
from urllib import parse

from ..nonebot_plugin_menu import is_function_normal

config = get_plugin_config(Config)
from nonebot import on_regex
from datetime import datetime
from nonebot.params import RegexDict

Menu = on_command("/热搜榜", priority=1, block=True)

HotList = on_regex(r"(/(?P<Platform>(微博|百度|抖音|知乎|B站|今日头条))热搜榜)")
HotListIndex = on_regex(r'/了解(?P<Platform>\d{1,3})')

@Menu.handle()
async def _(event: PrivateMessageEvent | GroupMessageEvent) -> None:
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "热搜榜"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    await Menu.send("你想了解什么平台的新闻呢？\n发送下面的指令即可获得：\n\n/微博热搜榜\n/百度热搜榜\n/知乎热搜榜\n/抖音热搜榜\n/B站热搜榜\n/今日头条热搜榜\n\n"
                                    "发送指令：\n/了解+序号\n例如：/了解1\n获取具体详细内容", reply_message=True)
            else:
                await Menu.send("你想了解什么平台的新闻呢？\n发送下面的指令即可获得：\n\n/微博热搜榜\n/百度热搜榜\n/知乎热搜榜\n/抖音热搜榜\n/B站热搜榜\n/今日头条热搜榜\n\n"
                                "发送指令：\n/了解+序号\n例如：/了解1\n获取具体详细内容", reply_message=True)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)

@HotList.handle()
async def j(foo: PrivateMessageEvent | GroupMessageEvent, matched = RegexDict())-> None:
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "热搜榜"):
            ids = foo.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    data = await fetch_hot_list(matched["Platform"])
                    if data:
                        UrlFile = f"D:/StarsBot/Download/HotList/{foo.get_user_id()}/UrlList.json"
                        event_list = data["data"]["data"]
                        ResultData = f"{matched["Platform"]} {datetime.now().date()} 的热点有：\n\n"
                        sorted_events = sorted(event_list, key=lambda x: x["viewnum"], reverse=True)
                        for index, event in enumerate(sorted_events):
                            rank = index + 1
                            date = event["date"]
                            event_name = event["name"]
                            ResultData += f"{rank}. {event_name}\n"

                        if ResultData.endswith("\n"):
                            ResultData = ResultData[:-1]

                        await HotList.send(ResultData + f"\n\n发送指令：\n/了解+序号\n例如：/了解1\n获取具体详细内容", reply_message=True)

                        # 数据保存部分
                        os.makedirs(os.path.dirname(UrlFile), exist_ok=True)

                        sorted_links = sorted(event_list, key=lambda x: x["viewnum"], reverse=True)
                        sorted_urls = [entry["url"] for entry in sorted_links]

                        with open(UrlFile, "w", encoding="utf-8") as f:
                            json.dump(sorted_urls, f, ensure_ascii=False)
            else:
                data = await fetch_hot_list(matched["Platform"])
                if data:
                    UrlFile = f"D:/StarsBot/Download/HotList/{foo.get_user_id()}/UrlList.json"
                    event_list = data["data"]["data"]
                    ResultData = f"{matched["Platform"]} {datetime.now().date()} 的热点有：\n\n"
                    sorted_events = sorted(event_list, key=lambda x: x["viewnum"], reverse=True)
                    for index, event in enumerate(sorted_events):
                        rank = index + 1
                        date = event["date"]
                        event_name = event["name"]
                        ResultData += f"{rank}. {event_name}\n"

                    if ResultData.endswith("\n"):
                        ResultData = ResultData[:-1]

                    await HotList.send(ResultData + f"\n\n发送指令：\n/了解+序号\n例如：/了解1\n获取具体详细内容",
                                       reply_message=True)

                    # 数据保存部分
                    os.makedirs(os.path.dirname(UrlFile), exist_ok=True)

                    sorted_links = sorted(event_list, key=lambda x: x["viewnum"], reverse=True)
                    sorted_urls = [entry["url"] for entry in sorted_links]

                    with open(UrlFile, "w", encoding="utf-8") as f:
                        json.dump(sorted_urls, f, ensure_ascii=False)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)


@HotListIndex.handle()
async def _(event: PrivateMessageEvent | GroupMessageEvent, matched: dict = RegexDict()) -> None:
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "热搜榜"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    platform_number = int(matched["Platform"])
                    UrlFile = f"D:/StarsBot/Download/HotList/{event.get_user_id()}/UrlList.json"
                    if ensure_file_exists(UrlFile):
                        with open(UrlFile, "r", encoding="utf-8") as f:
                            sorted_urls = json.load(f)

                        if 0 <= platform_number - 1 < len(sorted_urls):
                            selected_url = sorted_urls[platform_number - 1]
                            def encode_chinese(match):
                                return urllib.parse.quote(match.group(0))

                            encoded_url = re.sub(r'[\u4e00-\u9fff]+', encode_chinese, selected_url)
                            await HotListIndex.send(f"链接来啦：\n{encoded_url}", reply_message=True)
                        else:
                            await HotListIndex.send("哎呀，没有这条新闻呢", reply_message=True)
                    else:
                        await HotListIndex.send("哎呀，没有找到配置文件呢", reply_message=True)
            else:
                platform_number = int(matched["Platform"])
                UrlFile = f"D:/StarsBot/Download/HotList/{event.get_user_id()}/UrlList.json"
                if ensure_file_exists(UrlFile):
                    with open(UrlFile, "r", encoding="utf-8") as f:
                        sorted_urls = json.load(f)

                    if 0 <= platform_number - 1 < len(sorted_urls):
                        selected_url = sorted_urls[platform_number - 1]

                        def encode_chinese(match):
                            return urllib.parse.quote(match.group(0))

                        encoded_url = re.sub(r'[\u4e00-\u9fff]+', encode_chinese, selected_url)
                        await HotListIndex.send(f"链接来啦：\n{encoded_url}", reply_message=True)
                    else:
                        await HotListIndex.send("哎呀，没有这条新闻呢", reply_message=True)
                else:
                    await HotListIndex.send("哎呀，没有找到配置文件呢", reply_message=True)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)

async def fetch_hot_list(platform):
    url = {
        "微博": "https://api.hipcapi.com/v3/hot_news/get?route=weibo",
        "百度": "https://api.hipcapi.com/v3/hot_news/get?route=baidu",
        "抖音": "https://api.hipcapi.com/v3/hot_news/get?route=douyin",
        "知乎": "https://api.hipcapi.com/v3/hot_news/get?route=zhihu",
        "B站": "https://api.hipcapi.com/v3/hot_news/get?route=bilibili",
        "今日头条": "https://api.hipcapi.com/v3/hot_news/get?route=toutiao",
        # 添加其他平台的URL
    }[platform]

    async with aiohttp.ClientSession(timeout=ClientTimeout(total=100)) as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    return None
        except asyncio.TimeoutError:
            await HotList.send("服务器请求超时，请稍后再试。", reply_message=True)
            return
