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
    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息

    @filter.command("tell")
    @filter.event_message_type(filter.EventMessageType.PRIVATE_MESSAGE)  # 只响应私聊
    async def tell_in_group(self, event: AstrMessageEvent):
        """
        私聊指令：/tell 群号 @目标QQ 要说的话
        示例：/tell 123456789 @987654321 明天下午开会
        """
        # 获取用户输入
        text = event.message_str.strip()
        
        # 解析指令：/tell 群号 @QQ 消息
        parts = text.split()
        if len(parts) < 3:
            yield event.plain_result("格式错误！正确格式：/tell 群号 @目标QQ 要说的话")
            return
        
        # 提取群号
        group_id = parts[1]
        
        # 提取@目标和消息
        at_part = parts[2]
        if not at_part.startswith('@'):
            yield event.plain_result("格式错误！请在目标QQ前加@符号")
            return
        
        target_qq = at_part[1:]  # 去掉@符号
        if not target_qq.isdigit():
            yield event.plain_result("格式错误！目标QQ必须是数字")
            return
        
        # 剩余部分是要说的话
        message = ' '.join(parts[3:])
        if not message:
            yield event.plain_result("格式错误！请填写要带的话")
            return
        
        logger.info(f"收到私聊指令：向群 {group_id} 中的 {target_qq} 发送消息：{message}")
        
        # 获取群对象
        group = await event.get_group(group_id)
        if not group:
            yield event.plain_result(f"❌ 群 {group_id} 不存在或机器人未加入该群")
            return
        
        # 构建消息链：@目标 + 消息
        message_chain = [
            At(qq=target_qq),
            Plain(f" {message}")  # 注意@后面加空格，避免连在一起
        ]
        
        # 在目标群发送消息
        try:
            await group.send_message(message_chain)
            yield event.plain_result(f"✅ 消息已发送到群 {group_id}，已@ {target_qq}")
        except Exception as e:
            logger.error(f"发送失败：{e}")
            yield event.plain_result(f"❌ 发送失败：{str(e)}")


    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
