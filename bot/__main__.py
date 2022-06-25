import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.telegram import TelegramAPIServer
from aiogram.dispatcher.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from aiohttp import web

from bot.config_reader import config
from bot.handlers import setup_routers


async def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    root_router = setup_routers()
    dp.include_router(root_router)

    if config.custom_bot_api:
        bot.session.api = TelegramAPIServer.from_base(config.custom_bot_api, is_local=True)

    # Set commands in the UI
    await bot.set_my_commands(
        commands=[BotCommand(command="start", description="Help and source code")],
        scope=BotCommandScopeAllPrivateChats()
    )

    try:
        if not config.webhook_domain:
            await bot.delete_webhook(drop_pending_updates=config.drop_pending_updates)
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        else:
            # Turn off aiohttp logs
            aiohttp_logger = logging.getLogger("aiohttp.access")
            aiohttp_logger.setLevel(logging.CRITICAL)

            # Set webhook
            await bot.set_webhook(
                url=config.webhook_domain + config.webhook_path,
                drop_pending_updates=config.drop_pending_updates,
                allowed_updates=dp.resolve_used_update_types()
            )

            # Prepare our webhook application
            app = web.Application()
            SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=config.webhook_path)
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, host=config.app_host, port=config.app_port)
            await site.start()

            # The infinite loop so the bot will work
            await asyncio.Event().wait()
    finally:
        await bot.session.close()


asyncio.run(main())
