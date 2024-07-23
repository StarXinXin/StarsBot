import json
from pathlib import Path

import nonebot
from nonebot import get_plugin_config, Bot, on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent
import httpx
from nonebot.plugin import PluginMetadata
from nonebot.params import EventMessage
from nonebot_plugin_alconna import UniMessage,Emoji
from nonebot.rule import to_me

from utils.AdminTool import is_group_in_whitelist
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_chat",
    description="聊天插件",
    usage="At机器人加问题即可聊天",
    config=Config,
)

from utils.FileUtils import ensure_file_exists, read_json_file, append_to_conversation, new_file_exists, \
    clear_json_file, is_file_empty
from ..nonebot_plugin_menu import is_function_normal

config = get_plugin_config(Config)

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)

ai_talk = on_message(rule=to_me())


@ai_talk.handle()
async def _(bot: Bot, event: GroupMessageEvent, message=EventMessage(), true=True):
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "AI聊天"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    msg = str(event.json())
                    data = json.loads(msg)
                    result = ""
                    file_path = f"Profile/Chat/{event.get_user_id()}/Context.json"
                    for message in data['original_message']:
                        if message['type'] == 'at':
                            result += message['data']['qq']
                            if result == "1874671495":
                                get_msg = str(event.get_message())
                                if get_msg == "":
                                    # await UniMessage("@我干嘛呀，要跟我聊天吗，至少聊什么，你要告诉我吧").send(reply_to=true)
                                    await UniMessage("@我干嘛呀，要跟我聊天吗，至少聊什么，你要告诉我吧" + Emoji("344")).send(reply_to=true)
                                    return
                                elif get_msg == "清除上下文":
                                    clear_json_file(event.get_user_id())
                                    if is_file_empty(event.get_user_id()):
                                        await UniMessage("已清除上下文").send(reply_to=true)
                                    else:
                                        await UniMessage("上下文清除失败").send(reply_to=true)
                                else:
                                    result = ensure_file_exists(file_path)
                                    if result:
                                        content = read_json_file(file_path)
                                        if content == "":
                                            try:
                                                url = "https://openai.lbbai.cc/v1/chat/completions"

                                                payload = json.dumps({
                                                    "messages": [{"role": "user", "content": get_msg}],
                                                    "stream": False,
                                                    "model": "gpt-3.5-turbo",
                                                    "temperature": 0.7,
                                                    "presence_penalty": 0
                                                })

                                                headers = {
                                                    'Reqable-Id': "reqable-id-5954cd0e-4e49-4fe4-b4f1-c5c51dc67cf6",
                                                    # 'User-Agent': "Reqable/2.11.1",
                                                    'Content-Type': "application/json",
                                                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
                                                }
                                                response = httpx.post(url, content=payload, headers=headers, timeout=100)
                                                data = response.json()
                                                first_choice_message = data['choices'][0]['message']['content']
                                                # sub_json = data['choices'][0]['message']
                                                # await UniMessage(json.dumps(sub_json, ensure_ascii=False)).send(
                                                #     reply_to=true)

                                                append_to_conversation(event, "user", get_msg)
                                                append_to_conversation(event, "assistant", first_choice_message)

                                                await UniMessage(first_choice_message).send(
                                                    reply_to=true)
                                            except httpx.ReadTimeout:
                                                await UniMessage("出错了：读取操作超时，请检查网络连接或稍后重试。").send(
                                                    reply_to=true)
                                            except httpx.ConnectError:
                                                await UniMessage("出错了：连接失败，请联系管理员检查网络连接或稍后重试。").send(
                                                    reply_to=True)
                                        else:
                                            content = read_json(file_path)
                                            append_conversation(content, "user", get_msg)

                                            try:
                                                url = "https://openai.lbbai.cc/v1/chat/completions"

                                                payload = json.dumps({
                                                    "messages": content,
                                                    "stream": False,
                                                    "model": "gpt-3.5-turbo",
                                                    "temperature": 0.7,
                                                    "presence_penalty": 0
                                                })

                                                headers = {
                                                    'Reqable-Id': "reqable-id-5954cd0e-4e49-4fe4-b4f1-c5c51dc67cf6",
                                                    'Content-Type': "application/json",
                                                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
                                                }

                                                response = httpx.post(url, content=payload, headers=headers, timeout=100)
                                                data = response.json()
                                                first_choice_message = data['choices'][0]['message']['content']

                                                # Append the assistant's response to the conversation history
                                                append_conversation(content, "assistant", first_choice_message)

                                                # Save the updated conversation history
                                                write_json(file_path, content)

                                                await UniMessage(first_choice_message).send(reply_to=True)

                                            except httpx.ReadTimeout:
                                                await UniMessage("出错了：读取操作超时，请检查网络连接或稍后重试。").send(
                                                    reply_to=True)
                                            except httpx.ConnectError:
                                                await UniMessage("出错了：连接失败，请联系管理员检查网络连接或稍后重试。").send(
                                                    reply_to=True)
                                    else:
                                        try:
                                            url = "https://openai.lbbai.cc/v1/chat/completions"

                                            payload = json.dumps({
                                                "messages": [{"role": "user", "content": get_msg}],
                                                "stream": False,
                                                "model": "gpt-3.5-turbo",
                                                "temperature": 0.7,
                                                "presence_penalty": 0
                                            })

                                            headers = {
                                                'Reqable-Id': "reqable-id-5954cd0e-4e49-4fe4-b4f1-c5c51dc67cf6",
                                                # 'User-Agent': "Reqable/2.11.1",
                                                'Content-Type': "application/json",
                                                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
                                            }
                                            response = httpx.post(url, content=payload, headers=headers, timeout=100)
                                            data = response.json()
                                            first_choice_message = data['choices'][0]['message']['content']


                                            append_to_conversation(event, "user", get_msg)
                                            append_to_conversation(event, "assistant", first_choice_message)

                                            await UniMessage(first_choice_message).send(
                                                    reply_to=true)
                                        except httpx.ReadTimeout:
                                            await UniMessage("出错了：读取操作超时，请检查网络连接或稍后重试。").send(
                                                reply_to=True)
                                        except httpx.ConnectError:
                                            await UniMessage("出错了：连接失败，请联系管理员检查网络连接或稍后重试。").send(
                                                reply_to=True)

                        # await UniMessage(result + ": " + get_msg).send(reply_to=true)

                # await UniMessage("").send(reply_to=true)
                # msg = str(event.json())
                # data = json.loads(msg)
                # result = ""
                # file_path = f"Profile/Chat/{event.get_user_id()}/Context.json"
                # for message in data['original_message']:
                #     if message['type'] == 'at':
                #         result += message['data']['qq']
                #         if result == "1874671495":
                #             get_msg = str(event.get_message())
                #             if get_msg == "":
                #                 await UniMessage("@我干嘛呀，要跟我聊天吗，至少聊什么，你要告诉我吧" + Emoji("344")).send(reply_to=true)
                #                 return
                #             elif get_msg == "清除上下文":
                #                 clear_json_file(event.get_user_id())
                #                 if is_file_empty(event.get_user_id()):
                #                     await UniMessage("已清除上下文").send(reply_to=true)
                #                 else:
                #                     await UniMessage("上下文清除失败").send(reply_to=true)
                #             else:
                #                 result = ensure_file_exists(file_path)
                #                 if result:
                #                     content = read_json_file(file_path)
                #                     if content == "":
                #
                #                         url = "https://openai.lbbai.cc/v1/chat/completions"
                #
                #                         payload = json.dumps({
                #                             "messages": [{"role": "user", "content": get_msg}],
                #                             "stream": False,
                #                             "model": "gpt-3.5-turbo",
                #                             "temperature": 0.7,
                #                             "presence_penalty": 0
                #                         })
                #
                #                         headers = {
                #                             'Reqable-Id': "reqable-id-5954cd0e-4e49-4fe4-b4f1-c5c51dc67cf6",
                #                             # 'User-Agent': "Reqable/2.11.1",
                #                             'Content-Type': "application/json",
                #                             'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
                #                         }
                #                         response = httpx.post(url, content=payload, headers=headers)
                #                         data = response.json()
                #                         first_choice_message = data['choices'][0]['message']['content']
                #                         # sub_json = data['choices'][0]['message']
                #                         # await UniMessage(json.dumps(sub_json, ensure_ascii=False)).send(
                #                         #     reply_to=true)
                #
                #                         append_to_conversation(event, "user", get_msg)
                #                         append_to_conversation(event, "assistant", first_choice_message)
                #
                #                         await UniMessage(first_choice_message).send(
                #                             reply_to=true)
                #                     else:
                #                         try:
                #                             with open(file_path, 'r') as file:
                #                                 messages = json.load(file)
                #
                #                             url = "https://openai.lbbai.cc/v1/chat/completions"
                #
                #                             payload = json.dumps({
                #                                 "messages": messages,
                #                                 "stream": False,
                #                                 "model": "gpt-3.5-turbo",
                #                                 "temperature": 0.7,
                #                                 "presence_penalty": 0
                #                             })
                #
                #                             headers = {
                #                                 'Reqable-Id': "reqable-id-5954cd0e-4e49-4fe4-b4f1-c5c51dc67cf6",
                #                                 'Content-Type': "application/json",
                #                                 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
                #                             }
                #
                #                             # 使用httpx发送POST请求，并设置超时时间以避免长时间等待
                #                             response = httpx.post(url, content=payload, headers=headers,
                #                                                   timeout=10)  # 例如，设置超时时间为10秒
                #                             data = response.json()
                #                             first_choice_message = data['choices'][0]['message']['content']
                #                             # sub_json = data['choices'][0]['message']
                #                             # await UniMessage(json.dumps(sub_json, ensure_ascii=False)).send(
                #                             #     reply_to=true)
                #
                #                             append_to_conversation(event, "user", get_msg)
                #                             append_to_conversation(event, "assistant", first_choice_message)
                #
                #                             await UniMessage(first_choice_message).send(
                #                                 reply_to=true)
                #                         except httpx.ReadTimeout:
                #                             await UniMessage("出错了：读取操作超时，请检查网络连接或稍后重试。").send(
                #                                 reply_to=true)
                #                 else:
                #                     url = "https://openai.lbbai.cc/v1/chat/completions"
                #
                #                     payload = json.dumps({
                #                         "messages": [{"role": "user", "content": get_msg}],
                #                         "stream": False,
                #                         "model": "gpt-3.5-turbo",
                #                         "temperature": 0.7,
                #                         "presence_penalty": 0
                #                     })
                #
                #                     headers = {
                #                         'Reqable-Id': "reqable-id-5954cd0e-4e49-4fe4-b4f1-c5c51dc67cf6",
                #                         # 'User-Agent': "Reqable/2.11.1",
                #                         'Content-Type': "application/json",
                #                         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
                #                     }
                #                     response = httpx.post(url, content=payload, headers=headers)
                #                     data = response.json()
                #                     first_choice_message = data['choices'][0]['message']['content']
                #
                #                     append_to_conversation(event, "user", get_msg)
                #                     append_to_conversation(event, "assistant", first_choice_message)
                #
                #                     await UniMessage(first_choice_message).send(
                #                             reply_to=true)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)



def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def append_conversation(event, role, content):
    event.append({"role": role, "content": content})