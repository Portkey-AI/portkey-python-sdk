from typing import Any, Dict, List, Literal, Optional, Union
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.user_invite_type import (
    UserInviteResponse,
    UserInviteRetrieveAllResponse,
    UserInviteRetrieveResponse,
    UserRetrieveAllResponse,
    UserRetrieveResponse,
    WorkspaceMemberGetResponse,
    WorkspaceMemberListResponse,
    WorkspacesAddResponse,
    WorkspacesGetResponse,
    WorkspacesListResponse,
    WorkspacesUpdateResponse,
)
from portkey_ai.api_resources.utils import GenericResponse
from portkey_ai.api_resources.utils import PortkeyApiPaths


class Admin(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)
        self.users = Users(client)
        self.workspaces = Workspaces(client)


class Users(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)
        self.invites = Invites(client)

    def get(self, *, user_id: str) -> UserRetrieveResponse:
        return self._get(
            f"{PortkeyApiPaths.USER_API}/{user_id}",
            params=None,
            body=None,
            cast_to=UserRetrieveResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        page_size: Optional[int] = None,
        current_page: Optional[int] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
    ) -> UserRetrieveAllResponse:
        query = {
            "pageSize": page_size,
            "currentPage": current_page,
            "email": email,
            "role": role,
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

    def delete(self, *, user_id: str) -> Any:
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

    def add(
        self,
        *,
        email: Optional[str] = None,
        role: Optional[str] = None,
        workspaces: Optional[List[Dict[str, Any]]] = None,
        workspace_api_key_details: Optional[Dict[str, Any]] = None,
    ) -> UserInviteResponse:
        body = {
            "email": email,
            "role": role,
            "workspaces": workspaces,
            "workspace_api_key_details": workspace_api_key_details,
        }
        return self._post(
            f"{PortkeyApiPaths.INVITE_API}",
            body=body,
            params=None,
            cast_to=UserInviteResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def get(self, *, invite_id: str) -> UserInviteRetrieveResponse:
        return self._get(
            f"{PortkeyApiPaths.INVITE_API}/{invite_id}",
            params=None,
            body=None,
            cast_to=UserInviteRetrieveResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
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

    def delete(self, *, invite_id: str) -> Any:
        return self._delete(
            f"{PortkeyApiPaths.INVITE_API}/{invite_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class Workspaces(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)
        self.users = WorkspacesUsers(client)

    def add(
        self,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        defaults: Optional[Dict[str, Any]] = None,
        users: Optional[List[str]] = None,
    ) -> WorkspacesAddResponse:
        body = {
            "name": name,
            "description": description,
            "defaults": defaults,
            "users": users,
        }
        return self._post(
            f"{PortkeyApiPaths.WORKSPACE_API}",
            body=body,
            params=None,
            cast_to=WorkspacesAddResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def get(self, *, workspace_id: str) -> WorkspacesGetResponse:
        return self._get(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}",
            params=None,
            body=None,
            cast_to=WorkspacesGetResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        page_size: Optional[int] = None,
        current_page: Optional[int] = None,
    ) -> WorkspacesListResponse:
        query = {
            "pageSize": page_size,
            "currentPage": current_page,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.WORKSPACE_API}?{query_string}",
            params=None,
            body=None,
            cast_to=WorkspacesListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        workspace_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        defaults: Optional[Dict[str, Any]] = None,
    ) -> WorkspacesUpdateResponse:
        body = {
            "name": name,
            "description": description,
            "defaults": defaults,
        }
        return self._put(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}",
            body=body,
            params=None,
            cast_to=WorkspacesUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        *,
        workspace_id: Optional[str],
        name: Optional[str] = None,
    ) -> Any:
        body = {
            "workspace_id": workspace_id,
            "name": name,
        }
        return self._delete(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class WorkspacesUsers(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def add(
        self,
        *,
        workspace_id: Optional[str] = None,
        users: Optional[List[Dict[str, str]]] = None,
    ) -> Any:
        body = {
            "workspace_id": workspace_id,
            "users": users,
        }
        return self._post(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/users",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def get(
        self,
        *,
        workspace_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> WorkspaceMemberGetResponse:
        return self._get(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/users/{user_id}",
            params=None,
            body=None,
            cast_to=WorkspaceMemberGetResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        workspace_id: Optional[str] = None,
        page_size: Optional[int] = None,
        current_page: Optional[int] = None,
        email: Optional[str] = None,
        role: Optional[Union[Literal["admin", "manager", "member"], str]] = None,
    ) -> WorkspaceMemberListResponse:
        query = {
            "page_size": page_size,
            "current_page": current_page,
            "email": email,
            "role": role,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/user?{query_string}",
            params=None,
            body=None,
            cast_to=WorkspaceMemberListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        workspace_id: Optional[str] = None,
        user_id: Optional[str] = None,
        role: Optional[Union[Literal["admin", "manager", "member"], str]] = None,
    ) -> Any:
        body = {
            "user_id": user_id,
            "role": role,
        }
        return self._put(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/users/{user_id}",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        *,
        workspace_id: Optional[str],
        user_id: Optional[str] = None,
    ) -> Any:
        return self._delete(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/users/{user_id}",
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
        self.workspaces = AsyncWorkspaces(client)


class AsyncUsers(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.invites = AsyncInvites(client)

    async def get(self, *, user_id: str) -> UserRetrieveResponse:
        return await self._get(
            f"{PortkeyApiPaths.USER_API}/{user_id}",
            params=None,
            body=None,
            cast_to=UserRetrieveResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        page_size: Optional[int] = None,
        current_page: Optional[int] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
    ) -> UserRetrieveAllResponse:
        query = {
            "pageSize": page_size,
            "currentPage": current_page,
            "email": email,
            "role": role,
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

    async def delete(self, *, user_id: str) -> Any:
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

    async def add(
        self,
        *,
        email: Optional[str] = None,
        role: Optional[str] = None,
        workspaces: Optional[List[Dict[str, Any]]] = None,
        workspace_api_key_details: Optional[Dict[str, Any]] = None,
    ) -> UserInviteResponse:
        body = {
            "email": email,
            "role": role,
            "workspaces": workspaces,
            "workspace_api_key_details": workspace_api_key_details,
        }
        return await self._post(
            f"{PortkeyApiPaths.INVITE_API}",
            body=body,
            params=None,
            cast_to=UserInviteResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def get(self, *, invite_id: str) -> UserInviteRetrieveResponse:
        return await self._get(
            f"{PortkeyApiPaths.INVITE_API}/{invite_id}",
            params=None,
            body=None,
            cast_to=UserInviteRetrieveResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
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

    async def delete(self, *, invite_id: str) -> Any:
        return await self._delete(
            f"{PortkeyApiPaths.INVITE_API}/{invite_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncWorkspaces(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.users = AsyncWorkspacesUsers(client)

    async def add(
        self,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        defaults: Optional[Dict[str, Any]] = None,
        users: Optional[List[str]] = None,
    ) -> WorkspacesAddResponse:
        body = {
            "name": name,
            "description": description,
            "defaults": defaults,
            "users": users,
        }
        return await self._post(
            f"{PortkeyApiPaths.WORKSPACE_API}",
            body=body,
            params=None,
            cast_to=WorkspacesAddResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def get(self, *, workspace_id: str) -> WorkspacesGetResponse:
        return await self._get(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}",
            params=None,
            body=None,
            cast_to=WorkspacesGetResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        page_size: Optional[int] = None,
        current_page: Optional[int] = None,
    ) -> WorkspacesListResponse:
        query = {
            "pageSize": page_size,
            "currentPage": current_page,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.WORKSPACE_API}?{query_string}",
            params=None,
            body=None,
            cast_to=WorkspacesListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        workspace_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        defaults: Optional[Dict[str, Any]] = None,
    ) -> WorkspacesUpdateResponse:
        body = {
            "name": name,
            "description": description,
            "defaults": defaults,
        }
        return await self._put(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}",
            body=body,
            params=None,
            cast_to=WorkspacesUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        *,
        workspace_id: Optional[str],
        name: Optional[str] = None,
    ) -> Any:
        body = {
            "workspace_id": workspace_id,
            "name": name,
        }
        return await self._delete(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncWorkspacesUsers(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    def add(
        self,
        *,
        workspace_id: Optional[str] = None,
        users: Optional[List[Dict[str, str]]] = None,
    ) -> Any:
        body = {
            "workspace_id": workspace_id,
            "users": users,
        }
        return self._post(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/users",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def get(
        self,
        *,
        workspace_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> WorkspaceMemberGetResponse:
        return self._get(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/users/{user_id}",
            params=None,
            body=None,
            cast_to=WorkspaceMemberGetResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        workspace_id: Optional[str] = None,
        page_size: Optional[int] = None,
        current_page: Optional[int] = None,
        email: Optional[str] = None,
        role: Optional[Union[Literal["admin", "manager", "member"], str]] = None,
    ) -> WorkspaceMemberListResponse:
        query = {
            "page_size": page_size,
            "current_page": current_page,
            "email": email,
            "role": role,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/user?{query_string}",
            params=None,
            body=None,
            cast_to=WorkspaceMemberListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        workspace_id: Optional[str] = None,
        user_id: Optional[str] = None,
        role: Optional[Union[Literal["admin", "manager", "member"], str]] = None,
    ) -> Any:
        body = {
            "user_id": user_id,
            "role": role,
        }
        return self._put(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/users/{user_id}",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        *,
        workspace_id: Optional[str],
        user_id: Optional[str] = None,
    ) -> Any:
        return self._delete(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/users/{user_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
