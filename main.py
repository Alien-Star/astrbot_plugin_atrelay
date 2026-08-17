"""
astrbot_plugin_atrelay — 艾特群友转发

通过私聊自然语言指挥机器人在 QQ 群内 @ 群友发消息、向指定 QQ 发送私聊消息。
支持群号 / 群名、QQ 号 / 群昵称匹配。
"""

from __future__ import annotations

import json
import re
import time
from typing import Any

from astrbot.api import AstrBotConfig, logger
from astrbot.api.event import AstrMessageEvent, MessageChain, filter
from astrbot.api.message_components import At, Plain
from astrbot.api.provider import LLMResponse, ProviderRequest
from astrbot.api.star import Context, Star, register

try:
    from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import (
        AiocqhttpMessageEvent,
    )
except Exception:  # pragma: no cover - 仅在缺少 aiocqhttp 平台时兜底
    AiocqhttpMessageEvent = None  # type: ignore[assignment]


# 工具结果里的成功/失败标记，用于在 on_llm_response 中精简回复
_SUCCESS_MARKERS = ("消息已成功发送到群", "已成功向")
_ERROR_MARKERS = ("发送失败", "私聊发送失败")

# 系统提示词中追加的工具使用规则
_PRIVACY_INSTRUCTION = """\
【消息转发工具使用规则】
当用户要求你去其他地方(群聊或私聊)发送消息时：
1. 不要生成消息内容预览，不要在回复里提前透露将要发送的内容。
2. 优先调用工具完成发送，工具返回结果后再生成简短、友好的回复(放在 content 字段)。
3. 工具调用失败时，可直接输出工具返回的错误信息。
4. 用户提供群名而非群号时，先调用 get_group_id_by_name 获取群号；
   用户提供昵称/群备注而非 QQ 号时，先调用 get_user_id_by_name 获取 QQ 号；
   获取到 ID 后再执行发送。
5. 当用户要求私聊发送时，调用 send_to_private_user 工具。
6. 群聊发送时调用 send_to_group_tool 工具，at_user 参数为可选，仅在用户明确要求 @ 某人时填写。
7. message 参数中只放纯文本内容，不要包含 [at:xxx]、[face:xx] 等标记，@ 功能由 at_user 参数控制。"""


def _is_aiocqhttp(event: AstrMessageEvent) -> bool:
    """判断当前事件是否来自 aiocqhttp(OneBot) 平台。"""
    return AiocqhttpMessageEvent is not None and isinstance(
        event, AiocqhttpMessageEvent
    )


def _build_target_umo(event: AstrMessageEvent, message_type: str, target_id: str) -> str:
    """根据当前事件构造目标 unified_msg_origin。

    UMO 格式: <platform_id>:<MessageType>:<session_id>
    group_id 对应 GroupMessage；user_id 对应 FriendMessage。
    """
    platform_id = event.get_platform_id()
    return f"{platform_id}:{message_type}:{target_id}"


def _is_valid_qq_id(value: str) -> bool:
    """校验 QQ 号 / 群号格式(非空纯数字)。"""
    return bool(value) and str(value).isdigit()


# 匹配 LLM 可能生成的多余 at 标记，如 [at:123456] 或 [at:qq=123456] 等
_AT_TAG_RE = re.compile(r"\[at[^\]]*\]", re.IGNORECASE)
# 匹配 QQ 表情标记 [face:xx] 等其他可能被 LLM 误生成的标签
_EXTRA_TAG_RE = re.compile(r"\[(?:at|face|cq(?:code)?|reply|image)[^\]]*\]", re.IGNORECASE)


def _clean_message_text(text: str) -> str:
    """清洗 LLM 生成的消息文本，去除误加的 [at:xxx] 等标记。

    LLM 在生成需要 @ 的消息时，有时会自行补上 [at:123456] 这类文本标记，
    而代码已经通过 At 组件实现了真正的 @，这些文本标记会造成重复显示。
    """
    if not text:
        return text
    cleaned = _AT_TAG_RE.sub("", text)
    # 合并因删除标记而产生的多余空格
    cleaned = re.sub(r" {2,}", " ", cleaned).strip()
    return cleaned


@register("astrbot_plugin_atrelay", "AlienStar", "艾特群友转发", "2.0.0")
class AtRelayPlugin(Star):
    """通过私聊指挥机器人在群内/私聊中转发消息，支持 @ 与群名/昵称匹配。"""

    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config or {}
        logger.info("AtRelayPlugin 已加载")

    # ------------------------------------------------------------------
    # LLM 钩子
    # ------------------------------------------------------------------

    @filter.on_llm_request()
    async def on_llm_request_hook(self, event: AstrMessageEvent, req: ProviderRequest):
        """在 LLM 请求前追加消息转发工具使用规则。

        仅当用户消息中疑似出现「发送/转发/告诉/@/私聊」等意图词时才注入，
        避免污染所有正常对话。
        """
        if not self.config.get("enable_llm_prompt_injection", True):
            return

        message_str = event.message_str
        trigger_keywords = (
            "发消息", "发个", "发送", "转发", "告诉", "通知",
            "艾特", "@", "私聊", "群里发", "群里说", "群发",
        )
        if not any(kw in message_str for kw in trigger_keywords):
            return

        if req.system_prompt:
            req.system_prompt += "\n" + _PRIVACY_INSTRUCTION
        else:
            req.system_prompt = _PRIVACY_INSTRUCTION
        logger.debug("已追加消息转发工具使用规则到系统提示词")

    @filter.on_llm_response()
    async def on_llm_response_hook(self, event: AstrMessageEvent, resp: LLMResponse):
        """精简 LLM 对工具调用结果的回复，去除冗余信息。

        仅当回复中包含工具返回的成功/失败标记时才做精简，
        避免误伤正常对话。
        """
        if not self.config.get("enable_response_simplification", True):
            return

        original = resp.completion_text or ""
        if not original.strip():
            resp.completion_text = "抱歉，我无法处理这个请求（模型响应为空）。"
            logger.warning("LLM 返回空回复，已替换为默认提示")
            return

        # 仅在包含工具结果标记时精简
        if not any(marker in original for marker in _SUCCESS_MARKERS + _ERROR_MARKERS):
            return

        lines = original.strip().split("\n")
        for line in lines:
            stripped = line.strip()
            if any(
                marker in stripped
                for marker in _SUCCESS_MARKERS + _ERROR_MARKERS
            ):
                logger.debug(f"精简回复: {original!r} -> {stripped!r}")
                resp.completion_text = stripped
                return

    # ------------------------------------------------------------------
    # LLM 工具
    # ------------------------------------------------------------------

    @filter.llm_tool(name="send_to_group_tool")
    async def send_to_group_tool(
        self,
        event: AstrMessageEvent,
        group_id: str,
        message: str,
        at_user: str = "",
    ):
        '''向指定群聊发送消息，可选择 @ 群内某个成员。

        Args:
            group_id(string): 目标群号
            message(string): 要发送的消息文本内容
            at_user(string): 需要 @ 的用户 QQ 号，不填则不 @ 任何人
        '''
        logger.info(f"send_to_group_tool: group_id={group_id}, at_user={at_user}")

        # 1. 校验群号
        if not _is_valid_qq_id(group_id):
            return "❌ 发送失败：群号格式不正确，请提供纯数字群号。"

        # 2. 校验 at_user（若提供）
        if at_user and not _is_valid_qq_id(at_user):
            return "❌ 发送失败：要 @ 的 QQ 号格式不正确。"

        try:
            # 3. 前置检查：机器人是否在该群
            if _is_aiocqhttp(event):
                try:
                    group_list = await event.bot.api.call_action("get_group_list")
                    joined_ids = {str(g["group_id"]) for g in group_list}
                    if group_id not in joined_ids:
                        return f"❌ 发送失败：机器人不在群 {group_id} 中。"
                except Exception as e:
                    logger.warning(f"获取群列表失败，将尝试直接发送: {e}")

            # 4. 构造消息链
            clean_message = _clean_message_text(message)
            chain: list = []
            if at_user:
                chain.append(At(qq=at_user))
                chain.append(Plain(" "))
            chain.append(Plain(clean_message))

            # 5. 发送
            target_umo = _build_target_umo(event, "GroupMessage", group_id)
            await self.context.send_message(target_umo, MessageChain(chain))
            return f"✅ 消息已成功发送到群 {group_id}"

        except Exception as e:
            logger.error(f"send_to_group_tool 发送失败: {e}", exc_info=True)
            return f"❌ 发送失败：{e}"

    @filter.llm_tool(name="send_to_private_user")
    async def send_to_private_user(
        self, event: AstrMessageEvent, user_id: str, message: str
    ):
        '''向指定 QQ 用户发送私聊消息。

        Args:
            user_id(string): 目标 QQ 号
            message(string): 要发送的消息文本内容
        '''
        logger.info(f"send_to_private_user: user_id={user_id}")

        if not _is_valid_qq_id(user_id):
            return "❌ 私聊发送失败：QQ 号格式不正确，请提供纯数字 QQ 号。"

        try:
            target_umo = _build_target_umo(event, "FriendMessage", user_id)
            clean_message = _clean_message_text(message)
            await self.context.send_message(
                target_umo, MessageChain([Plain(clean_message)])
            )
            return f"✅ 已成功向 {user_id} 发送私聊消息"
        except Exception as e:
            logger.error(f"send_to_private_user 发送失败: {e}", exc_info=True)
            return f"❌ 私聊发送失败：{e}"

    @filter.llm_tool(name="get_group_id_by_name")
    async def get_group_id_by_name(
        self, event: AstrMessageEvent, group_name: str
    ):
        '''根据群名关键词模糊匹配，返回匹配到的群号。

        Args:
            group_name(string): 群名关键词
        '''
        if not _is_aiocqhttp(event):
            return "❌ 当前平台不支持获取群列表。"

        try:
            group_list = await event.bot.api.call_action("get_group_list")
            for g in group_list:
                if group_name in str(g.get("group_name", "")):
                    return str(g["group_id"])
            return f"❌ 未找到名称包含「{group_name}」的群。"
        except Exception as e:
            logger.error(f"get_group_id_by_name 失败: {e}", exc_info=True)
            return f"❌ 获取群列表失败：{e}"

    @filter.llm_tool(name="get_user_id_by_name")
    async def get_user_id_by_name(
        self,
        event: AstrMessageEvent,
        nickname: str,
        group_id: str = "",
    ):
        '''根据群内昵称或群名片模糊匹配，返回匹配到的 QQ 号。

        Args:
            nickname(string): 用户昵称或群名片关键词
            group_id(string): 群号，不填则默认使用当前消息所在的群
        '''
        if not _is_aiocqhttp(event):
            return "❌ 当前平台不支持获取群成员列表。"

        # 优先用传入的 group_id，否则回退到当前群
        target_gid = group_id or event.get_group_id() or ""
        if not _is_valid_qq_id(target_gid):
            return "❌ 未指定群号且当前不在群聊环境中，无法查询成员。"

        try:
            members = await event.bot.api.call_action(
                "get_group_member_list", group_id=target_gid
            )
            for m in members:
                nick = str(m.get("nickname", ""))
                card = str(m.get("card", ""))
                if nickname in nick or nickname in card:
                    return str(m["user_id"])
            return f"❌ 在群 {target_gid} 中未找到昵称包含「{nickname}」的成员。"
        except Exception as e:
            logger.error(f"get_user_id_by_name 失败: {e}", exc_info=True)
            return f"❌ 获取群成员失败：{e}"

    @filter.llm_tool(name="get_specified_group_members")
    async def get_specified_group_members(
        self,
        event: AstrMessageEvent,
        group_id: str = "",
        keyword: str = "",
    ) -> str:
        '''获取指定群聊的成员列表。

        Args:
            group_id(string): 目标群号，不填时默认使用当前群
            keyword(string): 搜索关键词，匹配昵称、群名片或 QQ 号；为空则返回全部成员
        '''
        start_time = time.time()

        # 优先用传入的 group_id，否则回退到当前群
        target_gid = group_id or event.get_group_id() or ""
        if not _is_valid_qq_id(target_gid):
            return json.dumps(
                {"status": "error", "message": "未指定群号且当前不在群聊环境中，无法查询成员。"},
                ensure_ascii=False,
            )

        if not _is_aiocqhttp(event):
            return json.dumps(
                {"status": "error", "message": "当前平台协议暂不支持获取群成员。"},
                ensure_ascii=False,
            )

        try:
            raw_members = await event.bot.api.call_action(
                "get_group_member_list", group_id=target_gid
            )
            if not raw_members:
                return json.dumps(
                    {"status": "error", "message": "无法获取成员列表或机器人权限不足。"},
                    ensure_ascii=False,
                )

            role_map = {"owner": "群主", "admin": "管理员", "member": "成员"}
            formatted: list[dict[str, Any]] = []

            for m in raw_members:
                user_id = str(m.get("user_id", ""))
                nickname = m.get("nickname", "")
                card = m.get("card", "")
                role = m.get("role", "member")

                # 关键词过滤
                if keyword:
                    search_blob = f"{user_id}{nickname}{card}"
                    if keyword not in search_blob:
                        continue

                formatted.append(
                    {
                        "user_id": user_id,
                        "nickname": nickname,
                        "group_card": card if card else "无",
                        "role": role_map.get(role, "成员"),
                    }
                )

            output = {
                "status": "success",
                "group_id": target_gid,
                "count": len(formatted),
                "members": formatted,
            }
            logger.debug(
                f"群成员查询成功：耗时 {time.time() - start_time:.2f}s，"
                f"共 {len(formatted)} 人"
            )
            return json.dumps(output, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"get_specified_group_members 异常: {e}", exc_info=True)
            return json.dumps(
                {"status": "error", "message": f"系统内部异常: {e}"},
                ensure_ascii=False,
            )
