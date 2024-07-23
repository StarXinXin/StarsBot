import json

from nonebot import get_plugin_config
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot_plugin_alconna import UniMessage, Emoji

from utils.AdminTool import is_group_in_whitelist
from utils.FileUtils import ensure_file_exists, file_exists, delete_folder, write_json_to_file, read_json_file
from utils.Network import make_request, timeout_callback
from .config import Config

__plugin_meta__ = PluginMetadata(name="nonebot_plugin_textualfault",
                                 description="小游戏，文本找茬，从一堆文本中找出不一样的文本", usage="/文本找茬",
                                 config=Config, )

from ..nonebot_plugin_menu import is_function_normal

config = get_plugin_config(Config)

TextualFaultFinding = on_command("/文本找茬", priority=0, block=True)


@TextualFaultFinding.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State, content: Message = CommandArg()):
    filepath = f"Profile/Menu/Game/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "文本找茬"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    content = content.extract_plain_text()
                    gid = event.get_session_id()
                    group_file = f"Profile/GameData/TextualFault/Group/"
                    group_file_path = f"Profile/GameData/TextualFault/Group/Config.json"
                    if not content:
                        await UniMessage(Emoji("187") + " 要玩游戏吗？发送以下指令即可开始玩耍哦\n\n" + Emoji(
                            "187") + " 开始游戏：\n" + Emoji("187") + " /文本找茬 开始游戏\n\n" + Emoji(
                            "187") + " 结束游戏：\n" + Emoji("187") + " /文本找茬 结束游戏\n\n" + Emoji(
                            "187") + " 提示：\n" + Emoji("187") + " /文本找茬 提示\n\n" + Emoji(
                            "187") + " 回答：\n" + Emoji("187") + "/文本找茬 答案 + 你的答案").send(reply_to=True)
                    elif content == "开始游戏":
                        if file_exists(group_file_path):
                            await UniMessage(Emoji("187") + " 游戏已开始，请勿重复开始游戏\n"
                                                            "如果你想结束游戏\n"
                                                            "请输入/文本找茬 结束游戏").send(reply_to=True)
                        else:
                            文本接口1 = "https://www.oexan.cn/API/Find_fault_with_words.php"
                            图片接口2 = "https://api.andeer.top/API/private_img_find_different.php"
                            response = make_request(图片接口2, timeout=100, on_timeout=timeout_callback)
                            if response.status_code == 200:
                                # GameId = str(generate_random_number(5))
                                data = response.json()
                                pic = data['data']['image']
                                point = data['data']['point']
                                if pic and point:
                                    write_json_to_file({"Data": {"Answer": point}}, group_file_path)
                                    image = MessageSegment.image(pic) + MessageSegment.text("\n"
                                                                                            f"示例回答：\n"
                                                                                            f"/文本找茬 答案a2")
                                    await TextualFaultFinding.finish(image, reply_message=True)
                                else:
                                    await UniMessage("无法解析数据或数据不完整，请稍后再试。").send(reply_to=True)
                            else:
                                await UniMessage("无法获取数据，请稍后再试。").send(reply_to=True)
                    elif content == "结束游戏":
                        if file_exists(group_file_path):
                            delete_folder(group_file)
                            await UniMessage(Emoji("187") + " 游戏已结束").send(reply_to=True)
                        else:
                            await UniMessage(Emoji("187") + " 游戏未开始，请先开始游戏").send(reply_to=True)
                    elif content == "提示":
                        await UniMessage(Emoji("187") + " 好像游戏太简单了，不能提示。").send(reply_to=True)
                    else:
                        if file_exists(group_file_path):
                            user_answer = content.split("答案", 1)[1].strip()
                            with open(group_file_path, 'r') as file:
                                game_data = json.load(file)
                                correct_answer = game_data['Data']['Answer']

                            if user_answer == correct_answer:
                                await UniMessage(Emoji("320") + "恭喜你，挑战成功！").send(reply_to=True)
                                if file_exists(group_file_path):
                                    delete_folder(group_file)
                            else:
                                await UniMessage(Emoji("344") + "很遗憾，挑战失败，再试一次").send(reply_to=True)
                        else:
                            await UniMessage(Emoji("187") + " 游戏未开始，请先开始游戏").send(reply_to=True)
            else:
                content = content.extract_plain_text()
                gid = event.get_session_id()
                private_file = f"Profile/GameData/TextualFault/Private"
                private_file_path = f"Profile/GameData/TextualFault/Private/Config.json"
                if not content:
                    await UniMessage(
                        Emoji("187") + " 要玩游戏吗？发送以下指令即可开始玩耍哦\n\n" + Emoji("187") + " 开始游戏：\n" + Emoji(
                            "187") + " /文本找茬 开始游戏\n\n" + Emoji("187") + " 结束游戏：\n" + Emoji(
                            "187") + " /文本找茬 结束游戏\n\n" + Emoji("187") + " 提示：\n" + Emoji(
                            "187") + " /文本找茬 提示\n\n" + Emoji("187") + " 回答：\n" + Emoji(
                            "187") + "/文本找茬 答案 + 你的答案").send(reply_to=True)
                elif content == "开始游戏":
                    if file_exists(private_file_path):
                        await UniMessage(Emoji("187") + " 游戏已开始，请勿重复开始游戏\n"
                                                        "如果你想结束游戏\n"
                                                        "请输入/文本找茬 结束游戏").send(reply_to=True)
                    else:
                        文本接口1 = "https://www.oexan.cn/API/Find_fault_with_words.php"
                        图片接口2 = "https://api.andeer.top/API/private_img_find_different.php"
                        response = make_request(图片接口2, timeout=100, on_timeout=timeout_callback)
                        if response.status_code == 200:
                            # GameId = str(generate_random_number(5))
                            data = response.json()
                            pic = data['data']['image']
                            point = data['data']['point']
                            if pic and point:
                                write_json_to_file({"Data": {"Answer": point}}, private_file_path)
                                image = MessageSegment.image(pic) + MessageSegment.text("\n"
                                                                                        f"示例回答：\n"
                                                                                        f"/文本找茬 答案a2")
                                await TextualFaultFinding.finish(image, reply_message=True)
                            else:
                                await UniMessage("无法解析数据或数据不完整，请稍后再试。").send(reply_to=True)
                        else:
                            await UniMessage("无法获取数据，请稍后再试。").send(reply_to=True)
                elif content == "结束游戏":
                    if file_exists(private_file_path):
                        delete_folder(private_file)
                        await UniMessage(Emoji("187") + " 游戏已结束").send(reply_to=True)
                    else:
                        await UniMessage(Emoji("187") + " 游戏未开始，请先开始游戏").send(reply_to=True)
                elif content == "提示":
                    await UniMessage(Emoji("187") + " 好像游戏太简单了，不能提示。").send(reply_to=True)
                else:
                    if file_exists(private_file_path):
                        user_answer = content.split("答案", 1)[1].strip()
                        with open(private_file_path, 'r') as file:
                            game_data = json.load(file)
                            correct_answer = game_data['Data']['Answer']

                        if user_answer == correct_answer:
                            await UniMessage(Emoji("320") + "恭喜你，挑战成功！").send(reply_to=True)
                            if file_exists(private_file_path):
                                delete_folder(private_file)
                        else:
                            await UniMessage(Emoji("344") + "很遗憾，挑战失败，再试一次").send(reply_to=True)
                    else:
                        await UniMessage(Emoji("187") + " 游戏未开始，请先开始游戏").send(reply_to=True)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)
