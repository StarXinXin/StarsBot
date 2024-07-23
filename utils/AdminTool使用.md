
# 将组添加到白名单中
```python
result = at.add_to_group_whitelist("group_399960298")
print(result)  # 输出：“条目group_399960298已加入白名单”或“条目group_399960298已在白名单中”。
```

# 从白名单中移除群组
```python
result = at.remove_from_group_whitelist("group_399960298")
print(result)  # 输出：“group_399960298从白名单中移除条目”或“在白名单中找不到group_399960298条目”。
```

# 检查群组是否在白名单中
```python
group_id_to_check = "group_399960298"
if at.is_group_in_whitelist(group_id_to_check):
    print(f"Group {group_id_to_check} is in the whitelist.")  # Output if true
else:
    print(f"Group {group_id_to_check} is not in the whitelist.")  # Output if false
```

# 将管理员添加到白名单
```python
result = at.add_to_admin_whitelist("admin_12345")
print(result)  # Output: "Entry admin_12345 added to whitelist." or "Entry admin_12345 is already in the whitelist."
```

# 从白名单中移除管理员
```python
result = at.remove_from_admin_whitelist("admin_12345")
print(result)  # Output: "Entry admin_12345 removed from whitelist." or "Entry admin_12345 not found in the whitelist."
```

# 检查管理员是否在白名单中
```python
admin_id_to_check = "admin_12345"
if at.is_admin_in_whitelist(admin_id_to_check):
    print(f"Admin {admin_id_to_check} is in the whitelist.")  # Output if true
else:
    print(f"Admin {admin_id_to_check} is not in the whitelist.")  # Output if false
```
