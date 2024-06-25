from typing import Any, Optional
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.user_invite_type import (
    UserInviteResponse,
    UserInviteRetrieveAllResponse,
    UserInviteRetrieveResponse,
    UserRetrieveAllResponse,
    UserRetrieveResponse,
)
from portkey_ai.api_resources.utils import GenericResponse
from portkey_ai.api_resources.utils import PortkeyApiPaths


class Admin(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)
        self.users = Users(client)


class Users(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)
        self.invites = Invites(client)

    def retrieve(self, *, user_id: str) -> UserRetrieveResponse:
        return self._get(
            f"{PortkeyApiPaths.USER_API}/{user_id}",
            params=None,
            body=None,
            cast_to=UserRetrieveResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve_all(
        self,
        *,
        page_size: Optional[int] = None,
        current_page: Optional[int] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> UserRetrieveAllResponse:
        query = {
            "pageSize": page_size,
            "currentPage": current_page,
            "email": email,
            "role": role,
            "userId": user_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.USER_API}?{query_string}",
            params=None,
            body=None,
            cast_to=UserRetrieveAllResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(self, *, user_id: str, role: str) -> Any:
        body = {"role": role}
        return self._put(
            f"{PortkeyApiPaths.USER_API}/{user_id}",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def remove(self, *, user_id: str) -> Any:
        return self._delete(
            f"{PortkeyApiPaths.USER_API}/{user_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class Invites(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(self, *, email: str, role: str) -> UserInviteResponse:
        body = {"email": email, "role": role}
        return self._post(
            f"{PortkeyApiPaths.INVITE_API}",
            body=body,
            params=None,
            cast_to=UserInviteResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(self, *, invite_id: str) -> UserInviteRetrieveResponse:
        return self._get(
            f"{PortkeyApiPaths.INVITE_API}/{invite_id}",
            params=None,
            body=None,
            cast_to=UserInviteRetrieveResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve_all(
        self,
        *,
        page_size: Optional[int] = None,
        current_page: Optional[int] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        status: Optional[str] = None,
    ) -> UserInviteRetrieveAllResponse:
        query = {
            "pageSize": page_size,
            "currentPage": current_page,
            "email": email,
            "role": role,
            "status": status,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.INVITE_API}?{query_string}",
            params=None,
            body=None,
            cast_to=UserInviteRetrieveAllResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def remove(self, *, invite_id: str) -> Any:
        return self._delete(
            f"{PortkeyApiPaths.INVITE_API}/{invite_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncAdmin(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.users = AsyncUsers(client)


class AsyncUsers(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.invites = AsyncInvites(client)

    async def retrieve(self, *, user_id: str) -> UserRetrieveResponse:
        return await self._get(
            f"{PortkeyApiPaths.USER_API}/{user_id}",
            params=None,
            body=None,
            cast_to=UserRetrieveResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve_all(
        self,
        *,
        page_size: Optional[int] = None,
        current_page: Optional[int] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> UserRetrieveAllResponse:
        query = {
            "pageSize": page_size,
            "currentPage": current_page,
            "email": email,
            "role": role,
            "userId": user_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.USER_API}?{query_string}",
            params=None,
            body=None,
            cast_to=UserRetrieveAllResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(self, *, user_id: str, role: str) -> Any:
        body = {"role": role}
        return await self._put(
            f"{PortkeyApiPaths.USER_API}/{user_id}",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def remove(self, *, user_id: str) -> Any:
        return await self._delete(
            f"{PortkeyApiPaths.USER_API}/{user_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncInvites(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def create(self, *, email: str, role: str) -> UserInviteResponse:
        body = {"email": email, "role": role}
        return await self._post(
            f"{PortkeyApiPaths.INVITE_API}",
            body=body,
            params=None,
            cast_to=UserInviteResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(self, *, invite_id: str) -> UserInviteRetrieveResponse:
        return await self._get(
            f"{PortkeyApiPaths.INVITE_API}/{invite_id}",
            params=None,
            body=None,
            cast_to=UserInviteRetrieveResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve_all(
        self,
        *,
        page_size: Optional[int] = None,
        current_page: Optional[int] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        status: Optional[str] = None,
    ) -> UserInviteRetrieveAllResponse:
        query = {
            "pageSize": page_size,
            "currentPage": current_page,
            "email": email,
            "role": role,
            "status": status,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.INVITE_API}?{query_string}",
            params=None,
            body=None,
            cast_to=UserInviteRetrieveAllResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def remove(self, *, invite_id: str) -> Any:
        return await self._delete(
            f"{PortkeyApiPaths.INVITE_API}/{invite_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
