from aiogram import Router

from . import commands, inline_mode


def setup_routers() -> Router:
    router = Router()
    router.include_router(commands.router)
    router.include_router(inline_mode.router)

    return router
