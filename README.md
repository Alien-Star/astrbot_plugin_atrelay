# 📬 艾特群友转发

<span style="font-size: 18px; font-weight: 500;"></span>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="版本">
  <img src="https://img.shields.io/badge/AstrBot-%3E%3D4.17.0-green.svg" alt="AstrBot版本">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="许可证">
</p>

<p align="center">
  <b>🤖 私聊指挥机器人 · 👥 艾特群友发消息 · ⚡ 精准转发 · 🎯 支持 @ 功能</b>
</p>

---

## ✨ 功能亮点

<table style="width: 100%; border: none; border-collapse: collapse;">
  <tr>
    <td style="width: 33%; padding: 12px; background: #f6f8fa; border-radius: 8px; border: 1px solid #e1e4e8; margin-left: 12px;">
      <div style="font-size: 24px; margin-bottom: 8px;">👥</div>
      <div style="font-weight: 600; margin-bottom: 4px;">精准艾特</div>
      <div style="font-size: 14px; color: #57606a;">可指定艾特某人，消息直达</div>
    </td>
    <td style="width: 33%; padding: 12px; background: #f6f8fa; border-radius: 8px; border: 1px solid #e1e4e8; margin-left: 12px;">
      <div style="font-size: 24px; margin-bottom: 8px;">⚡</div>
      <div style="font-weight: 600; margin-bottom: 4px;">轻量简洁</div>
      <div style="font-size: 14px; color: #57606a;">纯消息转发，无复杂依赖</div>
    </td>
  </tr>
</table>

---

## 📖 使用方法

<div style="background: #f6f8fa; padding: 16px; border-radius: 8px; border: 1px solid #e1e4e8; margin: 16px 0;">
  <div style="font-weight: 600; margin-bottom: 8px;">📋 指令格式</div>
  <code style="background: #fff; padding: 8px 12px; display: block; border-radius: 6px; border: 1px solid #d0d7de; font-size: 16px;">
    /send 群号 [@用户] 要发送的内容
  </code>
  <div style="margin-top: 8px; font-size: 14px; color: #57606a;">
    💡 说明：[@用户] 为可选参数，不填则只发消息不艾特
  </div>
</div>

### 🎯 实际例子

<table style="width: 100%; border-collapse: collapse;">
  <thead>
    <tr style="background: #f6f8fa; border-bottom: 2px solid #d0d7de;">
      <th style="padding: 10px; text-align: left;">你发送的消息</th>
      <th style="padding: 10px; text-align: left;">机器人的动作</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom: 1px solid #e1e4e8;">
      <td style="padding: 10px;"><code>试一下帮我去群821047000里告诉群主，让他也早点睡</code></td>
      <td style="padding: 10px;">➡️ 在群 <code>821047000</code> 中 <code>@1347536076</code> 并发送「早点休息吧，万华镜的光都快熄了。」</td>
    </tr>
    <tr style="border-bottom: 1px solid #e1e4e8;">
      <td style="padding: 10px;"><code>去群里发一句晚安</code></td>
      <td style="padding: 10px;">➡️ 往群 <code>123456789</code> 发送「晚安。」（不艾特）</td>
    </tr>
  </tbody>
</table>

---

## 🎯 适用场景

<ul style="list-style-type: none; padding: 0;">
  <li style="margin-bottom: 12px; padding: 8px 12px; background: #f6f8fa; border-radius: 8px; border: 1px solid #e1e4e8;">
    <span style="font-weight: 600;">👤 不想进群</span> — 人不在群里，但需要往群里发消息或艾特某人
  </li>
  <li style="margin-bottom: 12px; padding: 8px 12px; background: #f6f8fa; border-radius: 8px; border: 1px solid #e1e4e8;">
    <span style="font-weight: 600;">📢 定向通知</span> — 精准艾特特定成员，避免群消息骚扰
  </li>
  <li style="margin-bottom: 12px; padding: 8px 12px; background: #f6f8fa; border-radius: 8px; border: 1px solid #e1e4e8;">
    <span style="font-weight: 600;">🤖 自动化配合</span> — 搭配定时任务插件，实现自动提醒指定成员
  </li>
</ul>

---

## ⚠️ 注意事项

<div style="background: #fff8c5; padding: 16px; border-radius: 8px; border: 1px solid #f0b400; margin: 16px 0;">
  <table style="width: 100%; border-collapse: collapse;">
    <tr>
      <td style="padding: 8px; width: 30%; font-weight: 600;">✅ 机器人必须在群内</td>
      <td style="padding: 8px;">否则消息发送失败</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: 600;">✅ 仅私聊生效</td>
      <td style="padding: 8px;">群聊里发指令不会触发</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: 600;">✅ @功能支持</td>
      <td style="padding: 8px;">可精准艾特指定 QQ 用户</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: 600;">⚠️ 纯文本仅支持</td>
      <td style="padding: 8px;">暂不支持图片、表情等（@除外）</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: 600;">🔧 平台目前无法自动适配</td>
      <td style="padding: 8px;">仅支持QQ群</td>
    </tr>
  </table>
</div>

---

## 📦 安装方式

<div style="display: flex; gap: 20px; margin: 20px 0;">
  <div style="flex: 1; padding: 16px; background: #f6f8fa; border-radius: 8px; border: 1px solid #e1e4e8;">
    <div style="font-weight: 600; font-size: 18px; margin-bottom: 12px;">📡 从 GitHub 安装</div>
    <ol style="margin: 0; padding-left: 20px;">
      <li style="margin-bottom: 8px;">复制仓库地址：<br><code>https://github.com/Alien-Star/astrbot_plugin_atrelay</code></li>
      <li style="margin-bottom: 8px;">AstrBot WebUI → 插件管理 → 从 Git 安装</li>
      <li>粘贴地址，点击安装</li>
    </ol>
  </div>
  <div style="flex: 1; padding: 16px; background: #f6f8fa; border-radius: 8px; border: 1px solid #e1e4e8;">
    <div style="font-weight: 600; font-size: 18px; margin-bottom: 12px;">📂 手动安装</div>
    <ol style="margin: 0; padding-left: 20px;">
      <li style="margin-bottom: 8px;">在 <code>data/plugins/</code> 下创建 <code>astrbot_plugin_atrelay</code></li>
      <li style="margin-bottom: 8px;">将 <code>main.py</code> 和 <code>metadata.yaml</code> 放入该文件夹</li>
      <li>在 WebUI 中重载插件</li>
    </ol>
  </div>
</div>

---

## 🔄 版本更新

<table style="width: 100%; border-collapse: collapse;">
  <thead>
    <tr style="background: #f6f8fa; border-bottom: 2px solid #d0d7de;">
      <th style="padding: 8px; text-align: left;">版本</th>
      <th style="padding: 8px; text-align: left;">更新内容</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom: 1px solid #e1e4e8;">
      <td style="padding: 8px;"><code>v1.0.0</code></td>
      <td style="padding: 8px;">🚀 修复返回错误bug</td>
    </tr>
    <tr style="border-bottom: 1px solid #e1e4e8;">
      <td style="padding: 8px;"><code>v0.3.5</code></td>
      <td style="padding: 8px;">✨ 支持 @ 功能，消息构建优化</td>
    </tr>
    <tr style="border-bottom: 1px solid #e1e4e8;">
      <td style="padding: 8px;"><code>v0.3.0</code></td>
      <td style="padding: 8px;">🎯 删除/send 功能，通过LLM调用工具完成消息转发</td>
    </tr>
    <tr style="border-bottom: 1px solid #e1e4e8;">
      <td style="padding: 8px;"><code>v0.1.1</code></td>
      <td style="padding: 8px;">🚀 初始版本，基础 /send 转发功能</td>
    </tr>
  </tbody>
</table>

---

<div align="center" style="margin: 30px 0; padding: 20px; background: #f6f8fa; border-radius: 8px; border: 1px solid #e1e4e8;">
  <div style="font-size: 14px; color: #57606a; margin-bottom: 10px;">📄 MIT License © Alien-Star</div>
  <div>
    <span style="background: #21262d; color: #fff; padding: 4px 12px; border-radius: 20px; font-size: 14px;">
      ⭐ 如果对你有帮助，欢迎给个 Star
    </span>
  </div>
</div>
