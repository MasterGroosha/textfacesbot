from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import InlineQuery


class FacesMiddleware(BaseMiddleware):
    def __init__(self, faces: list[str]):
        super().__init__()
        self.faces = faces

    async def __call__(
            self,
            handler: Callable[[InlineQuery, Dict[str, Any]], Awaitable[Any]],
            event: InlineQuery,
            data: Dict[str, Any],
    ) -> Any:
        data["faces"] = self.faces
        return await handler(event, data)
