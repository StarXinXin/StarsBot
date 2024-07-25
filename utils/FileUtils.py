import os
import json
import shutil
from nonebot import logger


#
def new_file_exists(file_path):
    """
    确保文件存在，如果不存在则创建。
    :param file_path:
    :return:
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump('', file)
        return False

    return True


def ensure_file_exists(file_path: object):
    """
    确保文件存在
    :param file_path:
    :return:
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        return False
    return True

def read_json_file(file_path: object):
    """
    读取JSON文件，并返回其中的数据。
    :param file_path:
    :return:
    """
    try:
        with open(file_path, "r", encoding='utf-8') as f:  # 第一步：打开文件
            data = json.load(f)
            return data
    except FileNotFoundError:
        return ""
    except json.JSONDecodeError:
        return ""
    except Exception as e:
        return ""

def append_to_conversation(event, role, content):
    """
    追加一次对话记录到指定的JSON文件中。
    :param event: 事件对象，应包含get_user_id()方法。
    :param role: 对话角色，如"user"或"assistant"。
    :param content: 对话内容，字符串类型。
    """
    # 构建文件路径
    user_id = event.get_user_id()
    file_path = f"Profile/Chat/{user_id}/Context.json"

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    new_entry = {"role": role, "content": content}
    existing_data = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    raise ValueError("现有数据不是列表。")
            except (json.JSONDecodeError, ValueError) as e:
                logger.trace(f"从中读取 JSON 时出错 {file_path}: {e}")
                existing_data = []

    existing_data.append(new_entry)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)

# 使用示例
# 假设event已经定义好，现在我们要追加一次用户和助手的对话
# event = ...
# append_to_conversation(event, "user", "你好")
# append_to_conversation(event, "assistant", "你好！有什么我可以帮助你的吗？")
def clear_json_file(user_id):
    """
    创建或清空指定用户ID对应的文件，使其成为真正的空文件，没有任何内容。

    :param user_id: 用户ID，用于确定文件路径。
    """
    file_path = f"Profile/Chat/{user_id}/Context.json"
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    open(file_path, 'w').close()


def is_file_empty(user_id):
    """
    判断指定用户ID对应的JSON文件是否为空。

    :param user_id: 用户ID，用于确定文件路径。
    :return: 如果文件为空，返回True；否则返回False。
    """
    file_path = f"Profile/Chat/{user_id}/Context.json"
    if not os.path.exists(file_path):
        return True
    file_size = os.path.getsize(file_path)
    return file_size == 0


def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        logger.trace(f"{folder_path} 已成功删除。")
        return True
    else:
        logger.trace(f"{folder_path} 未找到")
        return False


def check_files_in_directory(directory_path):
    """
    检查目录中是否存在文件。
    :param directory_path:
    :return:
    """
    if os.path.exists(directory_path):
        files = os.listdir(directory_path)
        if len(files) > 0:
            return True
        else:
            return False
    else:
        return False



def file_exists(file_path):
    """
    检查文件是否存在。
    """
    if not os.path.exists(file_path):
        return False
    return True

import json
import os

def write_json_to_file(json_content, file_path):
    """
    将JSON内容写入文件。
    :param json_content:
    :param file_path:
    :return:
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_content, json_file, ensure_ascii=False)


