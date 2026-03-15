from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.event import MessageChain
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain, At
from astrbot.api import logger

@register("at_relay", "AlienStar", "艾特群友", "0.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command("send")
    @filter.event_message_type(filter.EventMessageType.PRIVATE_MESSAGE)
    async def send_to_group(self, event: AstrMessageEvent):
        """
        私聊指令：/send 群号 要说的话
        示例：/send 441262019 博客别忘了
        """
        # 解析指令
        text = event.message_str.strip()
        parts = text.split(maxsplit=2)
        if len(parts) < 3:
            yield event.plain_result("格式错误！正确格式：/send 群号 要说的话")
            return
        
        group_id = parts[1]
        message = parts[2]
        
        logger.info(f"收到私聊指令：向群 {group_id} 发送消息：{message}")
        
        # 从当前私聊的 unified_msg_origin 获取平台
        current_umo = event.unified_msg_origin
        logger.info(f"当前私聊 UMO: {current_umo}")
        
        # 格式: "bot:FriendMessage:1347536076"
        # 提取平台部分（第一个冒号之前）
        platform = current_umo.split(':')[0]  # 得到 "bot"
        
        # 构造群聊的 unified_msg_origin
        # 关键：群聊的消息类型是 "GroupMessage"
        target_umo = f"{platform}:GroupMessage:{group_id}"
        
        logger.info(f"目标群聊 UMO: {target_umo}")
        # yield event.plain_result(f"调试信息：当前私聊UMO = {current_umo}")  # 直接发给你看
        # yield event.plain_result(f"调试信息：当前目标群聊UMO = {target_umo}")  # 直接发给你看
        # 构建消息链
        message_chain = MessageChain().message(message)
        
        # 发送消息（使用文档标准API）
        try:
            await self.context.send_message(target_umo, message_chain)
            yield event.plain_result(f"✅ 消息已发送到群 {group_id}")
        except Exception as e:
            logger.error(f"发送失败：{e}")
            yield event.plain_result(f"❌ 发送失败：{str(e)}")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
