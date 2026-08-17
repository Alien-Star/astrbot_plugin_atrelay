# 更新日志

## [2.0.0] - 重构版本

### 重构
- 完整重构 `main.py`，统一代码风格与错误处理。
- 修复 `get_specified_group_members` 中群号参数传递错误（原代码在 `group_id` 为空时仍把空值传给 OneBot API，导致查询失败）。
- 修复 `on_llm_request_hook` 关键词匹配过于宽泛（`发`/`讲`/`说` 会命中几乎所有消息）导致系统提示词污染的问题，改为更精确的意图词集合。
- 修复 `on_llm_response_hook` 对包含「发送失败」字样的正常回复误截断的问题。
- 移除从未使用的 `message_relation` 内存字典（死代码）。
- 移除空的 `initialize` / `terminate` 桩方法。
- `at_user` 参数改为可选（原代码在 docstring 中声明为必填）。
- 平台标识改用 `event.get_platform_id()`，不再脆弱地从 `unified_msg_origin` 切割。
- 新增 `_conf_schema.json` 配置：可在 WebUI 开关「系统提示词注入」和「回复精简」。
- `metadata.yaml` 新增 `astrbot_version` 与 `support_platforms` 字段。
- `get_user_id_by_name` / `get_specified_group_members` 支持未传群号时回退到当前群。

### 修复
- 修复 int 类型群号在某些路径下因 `isdigit()` 报错的问题。
- 修复非 aiocqhttp 平台下调用工具时的异常路径。

## [1.1.0] - 2026-04-08
### 新增
- 新增私聊发送工具（send_to_private_user），支持向指定 QQ 号发送私聊消息。
- 新增群名匹配群号工具（get_group_id_by_name）。
- 新增群内昵称 / 备注匹配用户 QQ 工具（get_user_id_by_name）。
- 扩展 LLM 指令，支持通过群名、用户名自然语言触发转发。

### 修复
- 因 group_id.isdigit() 导致 int 类型群号报错问题

## [1.0.0] - 2025-03-17
### 删除
- /send 命令

### 新增
- 添加群成员查询工具（`get_specified_group_members`）。
- 添加向指定群聊发送消息工具（`send_to_group_tool`）。

### 修复
- 修复了未加入群聊时的返回错误
