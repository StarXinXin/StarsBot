import json
import os


def load_white_list(file_path):
    """加载白名单，如果文件不存在或无法读取，返回空列表"""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        # print(f"从中加载白名单时出错{file_path}: {e}")
        return ""
def get_or_create_config(ids, token_id):
    """
    获取或创建配置文件
    :param ids:
    :param token_id:
    :return:
    """
    if token_id == "g":
        # 定义配置文件的路径
        config_file_path = f"Profile/Timing/TimeOnHour/{ids.split('_')[1]}/ConfigData.json"

        # 检查文件是否存在
        if not os.path.exists(config_file_path):
            # 如果文件不存在，创建目录和文件，并写入默认内容
            os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
            default_data = {
                "Use": False,
                "Type": "语音"
            }
            with open(config_file_path, 'w') as file:
                json.dump(default_data, file)

        # 读取文件内容
        with open(config_file_path, 'r') as file:
            data = json.load(file)

        return data
    elif token_id == "p":
        # 定义配置文件的路径
        config_file_path = f"Profile/Timing/TimeOnHour/{ids}/ConfigData.json"

        # 检查文件是否存在
        if not os.path.exists(config_file_path):
            # 如果文件不存在，创建目录和文件，并写入默认内容
            os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
            default_data = {
                "Use": False,
                "Type": "语音"
            }
            with open(config_file_path, 'w') as file:
                json.dump(default_data, file)

        # 读取文件内容
        with open(config_file_path, 'r') as file:
            data = json.load(file)

        return data


def update_config_value(file_path, key, new_value):
    # 读取配置文件
    with open(file_path, 'r') as file:
        config = json.load(file)

    # 修改字典中的键值
    if key in config:
        config[key] = new_value

    # 将更新后的字典写回文件
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=2)

def save_white_list(white_list, file_path):
    """
    保存白名单到文件
    :param white_list:
    :param file_path:
    :return:
    """
    with open(file_path, 'w') as file:
        json.dump(white_list, file)

def add_to_white_list(content, file_path):
    """
    添加用户到白名单，如果内容已存在则不进行任何操作
    在写入前确保文件路径的目录和文件存在，若文件不存在则直接创建并写入内容
    :param content: 要添加的内容（应为数字）
    :param file_path: 白名单文件的路径
    :return: 操作结果的消息
    """
    # 验证content是否为数字
    if not str(content).isdigit():
        return "输入的群号无效，请确保群号为纯数字"

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 如果文件不存在，直接创建并写入内容
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([content], file)
        return f"群号 {content} 已加入整点报时白名单"

    # 如果文件存在，按原逻辑处理
    white_list = load_white_list(file_path)
    if content not in white_list:
        white_list.append(content)
        save_white_list(white_list, file_path)
        return f"群号 {content} 已加入整点报时白名单"
    else:
        return f"群号 {content} 已在整点报时白名单中"





def remove_from_white_list(group_id, file_path):
    """
    从白名单中移除用户
    :param user:
    :param group_id:
    :param file_path:
    :return:
    """
    # 验证content是否为数字
    if not str(group_id).isdigit():
        return "输入的群号无效，请确保群号为纯数字"

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("")
    white_list = load_white_list(file_path)
    if group_id in white_list:
        white_list.remove(group_id)
        save_white_list(white_list, file_path)
        return f"群号 {group_id} 已从白名单中移除"
    else:
        return f"群号 {group_id} 好像不在白名单中"

def is_value_in_whitelist(value):
    file_path = 'Profile/Timing/TimeOnHour/WhiteList.json'
    try:
        with open(file_path, 'r') as file:
            whitelist = json.load(file)
        return value in whitelist
    except FileNotFoundError:
        return False
    except Exception as e:
        return False
