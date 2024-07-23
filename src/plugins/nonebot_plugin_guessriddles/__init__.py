import httpx
import re
import os
import json
from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot_plugin_alconna import UniMessage, Emoji

from utils.AdminTool import is_group_in_whitelist
from utils.FileUtils import ensure_file_exists, read_json_file, file_exists, delete_folder
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_guessriddles",
    description="猜谜语游戏",
    usage="/猜谜语",
    config=Config,
)

from ..nonebot_plugin_menu import is_function_normal

config = get_plugin_config(Config)

GuessRiddle = on_command("/猜谜语", priority=0, block=True)

GROUP_DATA_DIR = "Profile/GameData/GuessRiddle/Group"
PRIVATE_DATA_DIR = "Profile/GameData/GuessRiddle/Private"

GROUP_DATA_FILE = os.path.join(GROUP_DATA_DIR, "CurrentRiddle.json")
PRIVATE_DATA_FILE = os.path.join(PRIVATE_DATA_DIR, "CurrentRiddle.json")


def save_riddle_data(DATA_DIR, DATA_FILE, DATA):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DATA, f, ensure_ascii=False, indent=4)
    else:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DATA, f, ensure_ascii=False, indent=4)

def load_riddle_data(DATA_FILE):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


async def get_riddle():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.andeer.top/API/txt_guess_riddles.php", timeout=100)
        if response.status_code == 200:
            return response.json()
        return None

@GuessRiddle.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State, content: Message = CommandArg()):
    filepath = f"Profile/Menu/Game/Fun.json"
    content = content.extract_plain_text()

    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "猜谜语"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    if not content:
                        await UniMessage(Emoji("187") + " 要玩游戏吗？发送以下指令即可开始玩耍哦\n\n"
                                         + Emoji("187") + " 开始游戏：\n"
                                         + Emoji("187") + " /猜谜语 开始游戏\n\n"
                                         + Emoji("187") + " 结束游戏：\n"
                                         + Emoji("187") + " /猜谜语 结束游戏\n\n"
                                         + Emoji("187") + " 我不会：\n"
                                         + Emoji("187") + " /猜谜语 我不会\n\n"
                                         + Emoji("187") + " 回答：\n"
                                         + Emoji("187") + "/猜谜语 答案 + 你的答案").send(reply_to=True)
                    elif content == "开始游戏":
                        if file_exists(GROUP_DATA_DIR):
                            riddle_data = load_riddle_data(GROUP_DATA_FILE)
                            await UniMessage("你又来了，上一次的题目是:\n\n"
                                             f"谜题：{riddle_data['谜题']}\n提示：{riddle_data['提示']}").send(
                                reply_to=True)
                        else:
                            riddle_data = await get_riddle()
                            if riddle_data and riddle_data['code'] == 200:
                                save_riddle_data(GROUP_DATA_DIR, GROUP_DATA_FILE, riddle_data['data'])
                                await UniMessage(
                                    f"谜题：{riddle_data['data']['谜题']}\n提示：{riddle_data['data']['提示']}").send(
                                    reply_to=True)
                            else:
                                await UniMessage("获取谜题失败，请稍后再试。").send(reply_to=True)
                    elif content == "结束游戏":
                        riddle_data = load_riddle_data(GROUP_DATA_FILE)
                        if riddle_data:
                            if os.path.exists(GROUP_DATA_DIR):
                                delete_folder(GROUP_DATA_DIR)
                            await UniMessage("游戏已结束。").send(reply_to=True)
                        else:
                            await UniMessage("当前没有进行中的游戏。").send(reply_to=True)
                    elif content == "我不会":
                        riddle_data = load_riddle_data(GROUP_DATA_FILE)
                        if riddle_data:
                            if os.path.exists(GROUP_DATA_DIR):
                                delete_folder(GROUP_DATA_DIR)
                            riddle_data = await get_riddle()
                            if riddle_data and riddle_data['code'] == 200:
                                save_riddle_data(GROUP_DATA_DIR, GROUP_DATA_FILE, riddle_data['data'])
                                await UniMessage(Emoji("344") + f"本题的谜底是：{riddle_data['data']['谜底']}\n\n"
                                                                f"下一题是：\n"
                                                                f"谜题：{riddle_data['data']['谜题']}\n提示：{riddle_data['data']['提示']}").send(
                                    reply_to=True)
                        else:
                            await UniMessage("当前没有进行中的游戏。").send(reply_to=True)
                    elif content.startswith("答案"):
                        answer = re.sub(r"^答案\s*", "", content)
                        riddle_data = load_riddle_data(GROUP_DATA_FILE)
                        if riddle_data:
                            if check_answer(answer, riddle_data):
                                if os.path.exists(GROUP_DATA_DIR):
                                    delete_folder(GROUP_DATA_DIR)
                                get_riddle_data = await get_riddle()
                                if get_riddle_data['code'] == 200:
                                    save_riddle_data(GROUP_DATA_DIR, GROUP_DATA_FILE, get_riddle_data['data'])
                                    await UniMessage(Emoji("320") + f"恭喜你，答对了！\n谜底是：{riddle_data['谜底']}\n\n"
                                                                    f"下一题是：\n"
                                                                    f"谜题：{get_riddle_data['data']['谜题']}\n提示：{get_riddle_data['data']['提示']}").send(
                                        reply_to=True)
                            else:
                                await UniMessage(Emoji("344") + "很遗憾，挑战失败，再试一次").send(reply_to=True)
                        else:
                            await UniMessage("当前没有进行中的游戏。").send(reply_to=True)
            else:
                if not content:
                    await UniMessage(Emoji("187") + " 要玩游戏吗？发送以下指令即可开始玩耍哦\n\n"
                                     + Emoji("187") + " 开始游戏：\n"
                                     + Emoji("187") + " /猜谜语 开始游戏\n\n"
                                     + Emoji("187") + " 结束游戏：\n"
                                     + Emoji("187") + " /猜谜语 结束游戏\n\n"
                                     + Emoji("187") + " 我不会：\n"
                                     + Emoji("187") + " /猜谜语 我不会\n\n"
                                     + Emoji("187") + " 回答：\n"
                                     + Emoji("187") + "/猜谜语 答案 + 你的答案").send(reply_to=True)
                elif content == "开始游戏":
                    if file_exists(PRIVATE_DATA_DIR):
                        riddle_data = load_riddle_data(PRIVATE_DATA_FILE)
                        await UniMessage("你又来了，上一次的题目是:\n\n"
                                         f"谜题：{riddle_data['谜题']}\n提示：{riddle_data['提示']}").send(reply_to=True)
                    else:
                        riddle_data = await get_riddle()
                        if riddle_data and riddle_data['code'] == 200:
                            save_riddle_data(PRIVATE_DATA_DIR, PRIVATE_DATA_FILE, riddle_data['data'])
                            await UniMessage(
                                f"谜题：{riddle_data['data']['谜题']}\n提示：{riddle_data['data']['提示']}").send(
                                reply_to=True)
                        else:
                            await UniMessage("获取谜题失败，请稍后再试。").send(reply_to=True)
                elif content == "结束游戏":
                    riddle_data = load_riddle_data(PRIVATE_DATA_FILE)
                    if riddle_data:
                        if os.path.exists(PRIVATE_DATA_DIR):
                            delete_folder(PRIVATE_DATA_DIR)
                        await UniMessage("游戏已结束。").send(reply_to=True)
                    else:
                        await UniMessage("当前没有进行中的游戏。").send(reply_to=True)
                elif content == "我不会":
                    riddle_data = load_riddle_data(PRIVATE_DATA_FILE)
                    if riddle_data:
                        if os.path.exists(PRIVATE_DATA_DIR):
                            delete_folder(PRIVATE_DATA_DIR)
                        riddle_data = await get_riddle()
                        if riddle_data and riddle_data['code'] == 200:
                            save_riddle_data(PRIVATE_DATA_DIR, PRIVATE_DATA_FILE, riddle_data['data'])
                            await UniMessage(Emoji("344") + f"本题的谜底是：{riddle_data['data']['谜底']}\n\n"
                                                            f"下一题是：\n"
                                                            f"谜题：{riddle_data['data']['谜题']}\n提示：{riddle_data['data']['提示']}").send(
                                reply_to=True)
                    else:
                        await UniMessage("当前没有进行中的游戏。").send(reply_to=True)
                elif content.startswith("答案"):
                    answer = re.sub(r"^答案\s*", "", content)
                    riddle_data = load_riddle_data(PRIVATE_DATA_FILE)
                    if riddle_data:
                        if check_answer(answer, riddle_data):
                            if os.path.exists(PRIVATE_DATA_DIR):
                                delete_folder(PRIVATE_DATA_DIR)
                            get_riddle_data = await get_riddle()
                            if  get_riddle_data['code'] == 200:
                                save_riddle_data(PRIVATE_DATA_DIR, PRIVATE_DATA_FILE, get_riddle_data['data'])
                                await UniMessage(Emoji("320") + f"恭喜你，答对了！\n谜底是：{riddle_data['谜底']}\n\n"
                                                                f"下一题是：\n"
                                                                f"谜题：{get_riddle_data['data']['谜题']}\n提示：{get_riddle_data['data']['提示']}").send(
                                    reply_to=True)
                        else:
                            await UniMessage(Emoji("344") + "很遗憾，挑战失败，再试一次").send(reply_to=True)
                    else:
                        await UniMessage("当前没有进行中的游戏。").send(reply_to=True)
        else:
            await UniMessage("功能异常，已被管理员关闭").send(reply_to=True)
    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)

# 假设谜底可能包含括号内的解释，我们提取核心词汇
def check_answer(user_answer, riddle_data):
    """
    检查用户答案是否与谜底匹配。

    :param user_answer: 用户提供的答案字符串
    :param riddle_data: 包含谜底的字典数据
    :return: 如果答案匹配返回True，否则返回False
    """
    # 获取谜底
    full_answer = riddle_data["谜底"]

    # 分割谜底以检查部分匹配
    parts = full_answer.split('（')

    # 检查用户答案是否与谜底或其第一部分相匹配
    if user_answer in parts[0]:
        return True
    else:
        return False

