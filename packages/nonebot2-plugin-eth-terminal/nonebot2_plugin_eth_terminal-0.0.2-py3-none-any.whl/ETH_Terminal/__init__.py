from nonebot.adapters.onebot.v11 import GroupMessageEvent
from .utils import check_terminal
from nonebot import on_command


terminal = on_command("ETH", aliases={"eth"}, priority=5)


@terminal.handle()
async def terminal_handle(event: GroupMessageEvent):
    await terminal.finish(await check_terminal())
