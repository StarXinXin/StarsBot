import json
import os

def is_valid_number(s):
    """检查字符串是否为有效的数字"""
    return s.isdigit()

def create_directories(path):
    """创建目录，如果它们不存在"""
    os.makedirs(os.path.dirname(path), exist_ok=True)

def get_valid_numbers(prompt):
    """获取有效的数字列表，并将其转换为字符串列表"""
    while True:
        ids = input(prompt).split()
        valid_ids = []
        for id in ids:
            if is_valid_number(id):
                valid_ids.append(str(id))  # 将数字转换为字符串
            else:
                print(f"警告: '{id}' 不是有效的数字。")
        if valid_ids:
            return valid_ids
        else:
            print("没有有效的输入，请重新输入。")

def write_to_json(file_path, data):
    """将数据写入JSON文件"""
    create_directories(file_path)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"数据已成功保存到 {file_path}")

def main():
    # 群白名单处理
    group_whitelist = get_valid_numbers("请输入群号ID，使用空格隔开: ")
    write_to_json('Profile/Whitelist/GroupWhitelist.json', group_whitelist)

    # 管理员白名单处理
    admin_whitelist = get_valid_numbers("请输入管理员QQ号，使用空格隔开: ")
    write_to_json('Profile/Whitelist/AdminWhitelist.json', admin_whitelist)

if __name__ == "__main__":
    main()
