from typing import Any, Dict, List, Literal, Optional, Union
from portkey_ai._vendor.openai import NOT_GIVEN, NotGiven
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

    def list(
        self,
        *,
        page_size: Union[int, str, NotGiven] = NOT_GIVEN,
        current_page: Optional[int] = 0,
        email: Union[str, NotGiven] = NOT_GIVEN,
        role: Union[str, NotGiven] = NOT_GIVEN,
    ) -> UserRetrieveAllResponse:
        query = {
            "pageSize": page_size,
            "currentPage": current_page,
            "email": email,
            "role": role,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
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

    def create(
        self,
        *,
        email: Union[str, NotGiven] = NOT_GIVEN,
        role: Union[str, NotGiven] = NOT_GIVEN,
        workspaces: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        workspace_api_key_details: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
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

    def list(
        self,
        *,
        page_size: Union[int, str, NotGiven] = NOT_GIVEN,
        current_page: Optional[int] = 0,
        email: Union[str, NotGiven] = NOT_GIVEN,
        role: Union[str, NotGiven] = NOT_GIVEN,
        status: Union[str, NotGiven] = NOT_GIVEN,
    ) -> UserInviteRetrieveAllResponse:
        query = {
            "pageSize": page_size,
            "currentPage": current_page,
            "email": email,
            "role": role,
            "status": status,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
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

    def resend(self, *, invite_id: str) -> Any:
        return self._post(
            f"{PortkeyApiPaths.INVITE_API}/{invite_id}/resend",
            body=None,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class Workspaces(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)
        self.users = WorkspacesUsers(client)

    def create(
        self,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        defaults: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        users: Union[List[str], NotGiven] = NOT_GIVEN,
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

    def retrieve(self, *, workspace_id: str) -> WorkspacesGetResponse:
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
        name: Union[str, NotGiven] = NOT_GIVEN,
        page_size: Union[int, str, NotGiven] = NOT_GIVEN,
        current_page: Optional[int] = 0,
        exact_name: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> WorkspacesListResponse:
        query = {
            "name": name,
            "pageSize": page_size,
            "currentPage": current_page,
            "exact_name": exact_name,
            **kwargs,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
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
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        defaults: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
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
        name: Union[str, NotGiven] = NOT_GIVEN,
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

    def create(
        self,
        *,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        users: Union[List[Dict[str, str]], NotGiven] = NOT_GIVEN,
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

    def retrieve(
        self,
        *,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        user_id: Union[str, NotGiven] = NOT_GIVEN,
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
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        page_size: Union[int, str, NotGiven] = NOT_GIVEN,
        current_page: Optional[int] = 0,
        email: Union[str, NotGiven] = NOT_GIVEN,
        role: Union[Literal["admin", "manager", "member"], str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        query = {
            "page_size": page_size,
            "current_page": current_page,
            "email": email,
            "role": role,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/users?{query_string}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        user_id: Union[str, NotGiven] = NOT_GIVEN,
        role: Union[Literal["admin", "manager", "member"], str, NotGiven] = NOT_GIVEN,
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
        user_id: Union[str, NotGiven] = NOT_GIVEN,
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

    async def list(
        self,
        *,
        page_size: Union[int, str, NotGiven] = NOT_GIVEN,
        current_page: Optional[int] = 0,
        email: Union[str, NotGiven] = NOT_GIVEN,
        role: Union[str, NotGiven] = NOT_GIVEN,
    ) -> UserRetrieveAllResponse:
        query = {
            "pageSize": page_size,
            "currentPage": current_page,
            "email": email,
            "role": role,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
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

    async def resend(self, *, invite_id: str) -> Any:
        return await self._post(
            f"{PortkeyApiPaths.INVITE_API}/{invite_id}/resend",
            body=None,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncInvites(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def create(
        self,
        *,
        email: Union[str, NotGiven] = NOT_GIVEN,
        role: Union[str, NotGiven] = NOT_GIVEN,
        workspaces: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        workspace_api_key_details: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
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

    async def list(
        self,
        *,
        page_size: Union[int, str, NotGiven] = NOT_GIVEN,
        current_page: Optional[int] = 0,
        email: Union[str, NotGiven] = NOT_GIVEN,
        role: Union[str, NotGiven] = NOT_GIVEN,
        status: Union[str, NotGiven] = NOT_GIVEN,
    ) -> UserInviteRetrieveAllResponse:
        query = {
            "pageSize": page_size,
            "currentPage": current_page,
            "email": email,
            "role": role,
            "status": status,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
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

    async def create(
        self,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        defaults: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        users: Union[List[str], NotGiven] = NOT_GIVEN,
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

    async def retrieve(self, *, workspace_id: str) -> WorkspacesGetResponse:
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
        name: Union[str, NotGiven] = NOT_GIVEN,
        page_size: Union[int, str, NotGiven] = NOT_GIVEN,
        current_page: Optional[int] = 0,
        exact_name: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> WorkspacesListResponse:
        query = {
            "name": name,
            "pageSize": page_size,
            "currentPage": current_page,
            "exact_name": exact_name,
            **kwargs,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
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
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        defaults: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
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
        name: Union[str, NotGiven] = NOT_GIVEN,
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

    async def create(
        self,
        *,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        users: Union[List[Dict[str, str]], NotGiven] = NOT_GIVEN,
    ) -> Any:
        body = {
            "workspace_id": workspace_id,
            "users": users,
        }
        return await self._post(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/users",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(
        self,
        *,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        user_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> WorkspaceMemberGetResponse:
        return await self._get(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/users/{user_id}",
            params=None,
            body=None,
            cast_to=WorkspaceMemberGetResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        page_size: Union[int, str, NotGiven] = NOT_GIVEN,
        current_page: Optional[int] = 0,
        email: Union[str, NotGiven] = NOT_GIVEN,
        role: Union[Literal["admin", "manager", "member"], str, NotGiven] = NOT_GIVEN,
    ) -> WorkspaceMemberListResponse:
        query = {
            "page_size": page_size,
            "current_page": current_page,
            "email": email,
            "role": role,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/users?{query_string}",
            params=None,
            body=None,
            cast_to=WorkspaceMemberListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        user_id: Union[str, NotGiven] = NOT_GIVEN,
        role: Union[Literal["admin", "manager", "member"], str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        body = {
            "user_id": user_id,
            "role": role,
        }
        return await self._put(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/users/{user_id}",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        *,
        workspace_id: Optional[str],
        user_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        return await self._delete(
            f"{PortkeyApiPaths.WORKSPACE_API}/{workspace_id}/users/{user_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
