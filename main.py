from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
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
    async def say_to_group(self, event: AstrMessageEvent, group_id: str, target: str, message: str):
        """
        私聊指令：/tell 群号 @目标QQ或@昵称 要说的话
        示例：/tell 123456789 @12345678 你好呀
        """
        # 记录日志
        logger.info(f"收到私聊指令：向群 {group_id} 中的 {target} 发送消息：{message}")
        
        # 解析目标：判断是QQ号还是@昵称
        at_target = None
        if target.startswith('@'):
            # 可能是@QQ号或@昵称
            target_content = target[1:]  # 去掉@符号
            if target_content.isdigit():
                # 是QQ号，直接使用
                at_target = At(qq=target_content)
            else:
                # 是昵称，需要先获取群成员列表再匹配
                # 这里简化处理：先获取群信息，再尝试匹配
                yield event.plain_result(f"暂不支持通过昵称@人，请使用QQ号。")
                return
        else:
            yield event.plain_result(f"格式错误，请在目标前加@，例如：@12345678")
            return
        
        # 获取群信息
        group = await event.get_group(group_id)
        if not group:
            yield event.plain_result(f"群 {group_id} 不存在或机器人未加入该群。")
            return
        
        # 构建消息链：先@目标，再发文本
        message_chain = [
            at_target,
            Plain(f" {message}")  # 注意@后面加个空格，避免@和文字连在一起
        ]
        
        # 在目标群发送消息
        try:
            await group.send_message(message_chain)
            yield event.plain_result(f"消息已发送到群 {group_id}，已@ {target}")
        except Exception as e:
            logger.error(f"发送失败：{e}")
            yield event.plain_result(f"发送失败：{str(e)}")


    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
