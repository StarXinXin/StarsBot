import json
import random
from typing import Union


def At(data: str) -> Union[list[str], list[int], list]:
    """
    检测at了谁，返回[qq, qq, qq,...]
    包含全体成员直接返回['all']
    如果没有at任何人，返回[]
    :param data: event.json
    :return: list
    """
    try:
        qq_list = []
        data = json.loads(data)
        for msg in data['message']:
            if msg['type'] == 'at':
                if 'all' not in str(msg):
                    qq_list.append(int(msg['data']['qq']))
                else:
                    return ['all']
        return qq_list
    except KeyError:
        return []


from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from nonebot.params import EventMessage


async def message_at_rule(event: GroupMessageEvent, message: Message = EventMessage()):
    return await extract_member_at(event.group_id, message=message) or event.reply


from typing import Set

from nonebot.adapters.onebot.v11 import Message, Bot


async def extract_member_at(
        group_id: int, message: Message, bot: Bot = None
) -> Set[str]:
    """提取消息中被艾特人的QQ号
    参数:
        message: 消息对象
    返回:
        被艾特集合
    """
    qq_list = (
        await bot.get_group_member_list(group_id=group_id) if bot is not None else None
    )
    result = {
        segment.data["qq"]
        for segment in message
        if segment.type == "at" and "qq" in segment.data
    }
    if "all" in result and qq_list is not None:
        result.remove("all")
        result |= {str(member["user_id"]) for member in qq_list}
    return result



def hum_convert(value):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f%s" % (value, units[i])
        value = value / size




def generate_random_number(num_digits):
    if num_digits <= 0:
        raise ValueError("位数必须为正数")
    range_start = 10**(num_digits-1)
    range_end = (10**num_digits)-1
    return random.randint(range_start, range_end)

