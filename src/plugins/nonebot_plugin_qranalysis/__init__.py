import os
import pathlib
from io import BytesIO

import requests
import zxing
from PIL import Image
from nonebot import get_plugin_config, on_message
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Bot
from nonebot.internal.rule import Rule
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMessage, Emoji
from pyzbar import pyzbar

from utils.AdminTool import is_group_in_whitelist
from utils.FileUtils import read_json_file, ensure_file_exists
from utils.ImageDownloader import download_file
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_qranalysis",
    description="",
    usage="",
    config=Config,
)

from ..nonebot_plugin_menu import is_function_normal

config = get_plugin_config(Config)


async def group_message_contains_image(event: MessageEvent) -> bool:
    if isinstance(event, GroupMessageEvent) and any(seg.type == 'image' for seg in event.message):
        return True
    return False


revoke_plugin = on_message(rule=Rule(group_message_contains_image))


@revoke_plugin.handle()
async def handle_image_message(bot: Bot, event: GroupMessageEvent):
    filepath = f"Profile/Menu/Function/Fun.json"
    if ensure_file_exists(filepath):
        if is_function_normal(read_json_file(filepath), "二维码解析"):
            ids = event.get_session_id()
            if ids.startswith("group"):
                parts = ids.split('_')
                if is_group_in_whitelist(parts[1]):
                    for seg in event.message:
                        if seg.type == 'image':
                            image_url = seg.data['url']
                            file_path = await download_file(image_url, "Download/Picture", "QRCode缓存.png")
                            if file_path != "":
                                data = ocr_qrcode_zxing(file_path)
                                if data != None:
                                    await UniMessage(Emoji(
                                        "187") + "检测到一张二维码\n已经帮你识别好了\n" + "解析结果：" + data).send(reply_to=True)
                            else:
                                print("图片下载失败")

    else:
        await UniMessage("菜单配置文件丢失").send(reply_to=True)


def ocr_qrcode_zxing(filename):
    """
    使用zxing包识别二维码
    :param filename:
    :return:
    """
    reader = zxing.BarCodeReader()
    # print(reader.zxing_version, reader.zxing_version_info)
    barcode = reader.decode(filename)
    if barcode:
        return barcode.parsed
    else:
        return None


def download_image(image_url, save_dir):
    """
    下载图片并解析是否存在二维码。
    如果存在二维码，将图片保存到指定文件夹并返回解析内容，否则返回 None。
    """
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    barcodes = pyzbar.decode(image)
    if len(barcodes) > 0:
        filename = os.path.join(save_dir, "qr_code.png")
        pathlib.Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        image.save(filename)
        return barcodes[0].data.decode("utf-8")
    else:
        return None




    # group_id = event.group_id
    # member_info = await bot.get_group_member_info(group_id=group_id, user_id=event.self_id)  # 管理员检测
    # await bot.send(event, member_info['role'])
    # if member_info['role'] != 'admin':
    #     return