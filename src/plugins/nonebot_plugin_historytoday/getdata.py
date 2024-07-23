import re
import httpx
from datetime import datetime

def remove_html_tags(text):
    """使用正则表达式移除HTML标签"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def get_events_on_day(month: str, day: str) -> str:
    """
    根据给定的月份和日期，从百度百科获取历史上的事件信息。

    参数:
    month (str): 月份，格式为两位数字字符串。
    day (str): 日期，格式为两位数字字符串。

    返回:
    str: 包含历史事件信息的消息字符串。
    """
    url = f"https://baike.baidu.com/cms/home/eventsOnHistory/{month}.json"
    response = httpx.get(url)
    if response.status_code == 200:
        data = response.json()
        events_on_day = data[month].get(f"{month}{day}", [])
        msg = ""
        for event in events_on_day:
            title = remove_html_tags(event['title'])
            desc = remove_html_tags(event['desc'])
            msg += f"{event['year']} - {title}\n{desc}\n\n"

        return msg

    else:
        return f"Request failed with status code {response.status_code}"
