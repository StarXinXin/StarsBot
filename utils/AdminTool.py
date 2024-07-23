import os
import json

# Define the profile directory and whitelist files
profile_dir = "Profile/Whitelist"
whitelist_file = os.path.join(profile_dir, "GroupWhitelist.json")
admin_whitelist_file = os.path.join(profile_dir, "AdminWhitelist.json")
designated_admin_id = "1402832033"

# Ensure the profile directory exists
os.makedirs(profile_dir, exist_ok=True)

# Ensure the whitelist files exist and are initialized
def initialize_files():
    if not os.path.exists(whitelist_file):
        with open(whitelist_file, 'w') as file:
            json.dump([], file)
    if not os.path.exists(admin_whitelist_file):
        with open(admin_whitelist_file, 'w') as file:
            json.dump([], file)
        # Add the designated administrator to the admin whitelist

initialize_files()

def load_whitelist(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_whitelist(file_path, whitelist):
    with open(file_path, 'w') as file:
        json.dump(whitelist, file)

def add_to_whitelist(file_path, entry):
    whitelist = load_whitelist(file_path)
    if entry not in whitelist:
        whitelist.append(entry)
        save_whitelist(file_path, whitelist)
        return f"{entry} 已加入白名单"
    else:
        return f"{entry} 已在白名单中"

def remove_from_whitelist(file_path, entry):
    whitelist = load_whitelist(file_path)
    if entry in whitelist:
        whitelist.remove(entry)
        save_whitelist(file_path, whitelist)
        return f"{entry} 已从白名单中移除"
    else:
        return f"{entry} 在白名单中找不到"

def is_in_whitelist(file_path, entry):
    whitelist = load_whitelist(file_path)
    return entry in whitelist

# Group whitelist functions
def add_to_group_whitelist(group_id):
    return add_to_whitelist(whitelist_file, group_id)

def remove_from_group_whitelist(group_id):
    return remove_from_whitelist(whitelist_file, group_id)

def is_group_in_whitelist(group_id: object) -> object:
    return is_in_whitelist(whitelist_file, group_id)

# Admin whitelist functions
def add_to_admin_whitelist(admin_id):
    return add_to_whitelist(admin_whitelist_file, admin_id)

def remove_from_admin_whitelist(admin_id):
    return remove_from_whitelist(admin_whitelist_file, admin_id)

def is_admin_in_whitelist(admin_id):
    return is_in_whitelist(admin_whitelist_file, admin_id)