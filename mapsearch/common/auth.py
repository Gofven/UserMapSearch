from abc import ABC, abstractmethod
from typing import Any, Optional

from django.http import HttpRequest
from ninja.errors import logger
from ninja.security import HttpBearer

from backend import settings
from mapsearch.user.models import User


# HttpBearer with async support, it's identical to django ninja HttpBearer, just with "async" calls instead
class AsyncHttpBearer(HttpBearer, ABC):
    async def __call__(self, request: HttpRequest) -> Optional[Any]:
        headers = request.headers
        auth_value = headers.get(self.header)

        if not auth_value:
            return None

        parts = auth_value.split(" ")

        if parts[0].lower() != self.openapi_scheme:
            if settings.DEBUG:
                logger.error(f"Unexpected auth - '{auth_value}'")

            return None

        token = " ".join(parts[1:])
        return await self.authenticate(request, token)

    @abstractmethod
    async def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        pass  # pragma: no cover


class UserAuth(AsyncHttpBearer):
    async def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        user = await User.objects.aget(api_key=token)

        return user