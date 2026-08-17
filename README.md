# 📬 艾特群友转发

<p align="center">
<img src="https://img.shields.io/badge/version-2.0.0-blue.svg" alt="版本">
<img src="https://img.shields.io/badge/AstrBot-%3E%3D4.5.0-green.svg" alt="AstrBot版本">
<img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="许可证">
</p>

<p align="center">
<b>🤖 私聊指挥机器人 · 👥 艾特群友发消息 · ⚡ 精准转发 · 🎯 支持 @ 功能 · 🌍 自然语言调用</b>
</p>

---

## ✨ 功能亮点

| 功能 | 说明 |
|------|------|
| 👥 精准艾特 | 可指定艾特某人，消息直达 |
| ⚡ 轻量简洁 | 纯消息转发，无复杂依赖 |
| 🗣️ 自然语言 | 支持群名/昵称识别，无需记群号 |
| 💬 私聊推送 | 支持机器人主动向指定 QQ 发送私聊消息 |
| 👤 群成员查询 | 支持按关键词检索群内成员 |

## 📖 使用方法

直接用自然语言私聊机器人即可，例如：

```
帮我到群里发一句晚安
去 123456789 群里告诉 987654321 早点睡
去"摸鱼交流群"告诉"小明"记得开会
给 987654321 发个私聊说生日快乐
```

> 💡 机器人会自动识别群号 / 群名、QQ 号 / 昵称，并调用对应工具完成转发。

## 🛠️ LLM 工具

本插件向 LLM 注册以下工具：

| 工具名 | 功能 |
|--------|------|
| `send_to_group_tool` | 向指定群聊发送消息，可选 @ 群友 |
| `send_to_private_user` | 向指定 QQ 发送私聊消息 |
| `get_group_id_by_name` | 根据群名关键词模糊匹配群号 |
| `get_user_id_by_name` | 根据群内昵称/群名片匹配 QQ 号 |
| `get_specified_group_members` | 获取指定群聊成员列表 |

## ⚙️ 插件配置

在 WebUI「插件管理」中可配置：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `enable_llm_prompt_injection` | `true` | 是否在 LLM 请求中注入消息转发工具使用规则 |
| `enable_response_simplification` | `true` | 是否精简 LLM 对工具调用结果的回复 |

## 🎯 适用场景

- **👤 不想进群** — 人不在群里，但需要往群里发消息或艾特某人
- **📢 定向通知** — 精准艾特特定成员，避免群消息骚扰
- **🤖 自动化配合** — 搭配定时任务插件，实现自动提醒指定成员
- **💬 私聊推送** — 支持机器人主动向指定 QQ 发送私聊消息
- **🗣️ 自然交互** — 不用记群号/QQ号，群名昵称直接使用

## ⚠️ 注意事项

| 项目 | 说明 |
|------|------|
| ✅ 机器人必须在群内 | 否则群消息发送失败 |
| ✅ 仅私聊生效 | 群聊里发指令不会触发转发 |
| ✅ @功能支持 | 可精准艾特指定 QQ 用户 |
| ⚠️ 纯文本 | 暂不支持图片、表情等（@除外） |
| 🔧 平台限制 | 仅支持 QQ（aiocqhttp / OneBot 协议） |

## 📦 安装方式

### 📡 从 GitHub 安装

1. 复制仓库地址：`https://github.com/Alien-Star/astrbot_plugin_atrelay`
2. AstrBot WebUI → 插件管理 → 从 Git 安装
3. 粘贴地址，点击安装

### 📂 手动安装

1. 在 `data/plugins/` 下创建 `astrbot_plugin_atrelay`
2. 将 `main.py`、`metadata.yaml`、`_conf_schema.json` 放入该文件夹
3. 在 WebUI 中重载插件

## 🔄 版本更新

| 版本 | 更新内容 |
|------|----------|
| `v2.0.0` | 🔄 完整重构：修复群成员查询 bug、系统提示词污染、回复误截断；新增配置项；移除死代码 |
| `v1.1.0` | 🆕 新增私聊发送、群名/昵称匹配工具；支持自然语言调用 |
| `v1.0.0` | 🚀 修复返回错误 bug；新增群成员查询、群聊发送工具 |
| `v0.3.5` | ✨ 支持 @ 功能，消息构建优化 |
| `v0.3.0` | 🎯 删除 /send 功能，通过 LLM 调用工具完成消息转发 |
| `v0.1.1` | 🚀 初始版本，基础 /send 转发功能 |

---

<div align="center">

📄 MIT License © Alien-Star

⭐ 如果对你有帮助，欢迎给个 Star

</div>
