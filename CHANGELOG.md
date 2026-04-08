# 更新日志
## [1.0.0] - 2025-03-17
### 删除
- /send 命令

### 新增
- 添加群成员查询工具（`get_specified_group_members`）。
- 添加向指定群聊发送消息工具（`send_to_group_tool`）。

### 修复
- 修复了未加入群聊时的返回错误

## [1.1.0] - 2026-04-08
### 新增
- 新增私聊发送工具（send_to_private_user），支持向指定 QQ 号发送私聊消息。
- 新增群名匹配群号工具（get_group_id_by_name）。
- 新增群内昵称 / 备注匹配用户 QQ 工具（get_user_id_by_name）。
- 扩展 LLM 指令，支持通过群名、用户名自然语言触发转发。

### 修复
- 因group_id.isdigit()导致int类型群号报错问题