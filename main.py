from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain, At
from astrbot.api import logger

@register("at_relay", "AlienStar", "艾特群友", "0.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("send")
    @filter.event_message_type(filter.EventMessageType.PRIVATE_MESSAGE)
    async def send_to_group(self, event: AstrMessageEvent):
        """
        私聊指令：/send 群号 要说的话
        示例：/send 441262019 博客别忘了
        """
        # 获取用户输入
        text = event.message_str.strip()
        
        # 解析指令：/send 群号 消息
        parts = text.split(maxsplit=2)  # 只分割前两部分，后面的全是消息
        if len(parts) < 3:
            yield event.plain_result("格式错误！正确格式：/send 群号 要说的话")
            return
        
        group_id = parts[1]
        message = parts[2]
        
        if not message:
            yield event.plain_result("格式错误！请填写要发送的内容")
            return
        
        logger.info(f"收到私聊指令：向群 {group_id} 发送消息：{message}")
        
        # 获取群对象
        group = await event.get_group(group_id)
        if not group:
            yield event.plain_result(f"❌ 群 {group_id} 不存在或机器人未加入该群")
            return
        
        # 构建消息链（纯文本）
        message_chain = [Plain(message)]
        
        # 在目标群发送消息
        try:
            await group.send_message(message_chain)
            yield event.plain_result(f"✅ 消息已发送到群 {group_id}")
        except Exception as e:
            logger.error(f"发送失败：{e}")
            yield event.plain_result(f"❌ 发送失败：{str(e)}")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
