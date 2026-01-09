import asyncio

from nonebot import get_driver, logger
from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")
require("nonebot_plugin_waiter")
require("nonebot_plugin_localstore")

from .config import ConfigModel, config
from .consts import AUTHOR, DESCRIPTION, NAME
from .handlers import load_handlers
from .sticker_pack import pack_manager
from .utils.operation import format_op

__version__ = "0.2.8"
__plugin_meta__ = PluginMetadata(
    name="PJSK表情生成",
    description=DESCRIPTION,
    usage="""
🚀 常用指令
• pjsk / arc
  └─ 唤起菜单，交互式生成
• pjsk / arc [序号] [文本]
  └─ 直接生成
  示例：`pjsk 1 早上好`
  示例：`arc 0 晚上好`

🛠️ 样式微调 (追加在指令后)
• -s [数值]：调整字号 (支持^相对值)
• -x / -y [数值]：调整横/纵坐标
• -c [颜色]：文本颜色 (如 red/#FF0)
• -r [角度]：旋转角度
• -w [数值]：描边宽度

> 示例：`pjsk 1 测试 -s 60 -c blue`
> 更多用法请发送: meme-stickers
""",
    type="application",
    homepage="https://github.com/lgc-NB2Dev/nonebot-plugin-meme-stickers",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License": "MIT", "Author": AUTHOR},
)


load_handlers()


driver = get_driver()


@driver.on_startup
async def _():
    pack_manager.reload(clear_updating_flags=True)

    if config.auto_update:

        async def do_update():
            logger.info("Updating packs")
            op, _ = await pack_manager.update_all(force=config.force_update)
            logger.success("Update finished")
            for x in format_op(op).splitlines():
                logger.success(x)

        asyncio.create_task(do_update())
