from abc import ABC, abstractmethod
from typing import Literal

import aiohttp

from errors import InvalidRequestError, InvalidTokenError, ForbiddenError


class BaseHttpExecutor(ABC):
    def __init__(
        self,
        headers: dict
    ):
        self.__headers = headers

    async def make_request(
        self,
        url: str,
        method: Literal["get", "post"] = "post",
        load_response_body: bool = True,
        **kwargs
    ) -> (aiohttp.ClientResponse, dict):
        async with aiohttp.ClientSession() as session:
            async with getattr(session, method)(
                url=url,
                headers=self.__headers,
                **kwargs
            ) as resp:
                self._check_response_status(resp)

                return resp, await resp.json() if load_response_body else {}

    @abstractmethod
    def _check_response_status(self, response: aiohttp.ClientResponse) -> None:
        raise NotImplementedError


class YoomoneyHttpExecutor(BaseHttpExecutor):
    def _check_response_status(self, response: aiohttp.ClientResponse) -> None:
        match response.status:
            case 200:
                return
            case 400:
                raise InvalidRequestError
            case 401:
                raise InvalidTokenError
            case 403:
                raise ForbiddenError
