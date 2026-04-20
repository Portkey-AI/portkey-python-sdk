import json
from typing import List, Union
from typing_extensions import Literal

from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.skills_type import (
    Skill,
    SkillDeleted,
    SkillList,
    SkillVersion,
    SkillVersionDeleted,
    SkillVersionList,
)
from ..._vendor.openai._types import NOT_GIVEN, FileTypes, NotGiven, Omit, omit
from ..._vendor.openai._legacy_response import HttpxBinaryResponseContent


class SkillsContent(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def retrieve(
        self,
        skill_id: str,
        *,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> HttpxBinaryResponseContent:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        return self.openai_client.skills.content.retrieve(
            skill_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )


class AsyncSkillsContent(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def retrieve(
        self,
        skill_id: str,
        *,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> HttpxBinaryResponseContent:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        return await self.openai_client.skills.content.retrieve(
            skill_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )


class SkillsVersionsContent(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def retrieve(
        self,
        version: str,
        *,
        skill_id: str,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> HttpxBinaryResponseContent:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        return self.openai_client.skills.versions.content.retrieve(
            version,
            skill_id=skill_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )


class AsyncSkillsVersionsContent(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def retrieve(
        self,
        version: str,
        *,
        skill_id: str,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> HttpxBinaryResponseContent:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        return await self.openai_client.skills.versions.content.retrieve(
            version,
            skill_id=skill_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )


class SkillsVersions(APIResource):
    content: SkillsVersionsContent

    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.content = SkillsVersionsContent(client)

    def create(
        self,
        skill_id: str,
        *,
        default: Union[bool, Omit] = omit,
        files: Union[List[FileTypes], FileTypes, Omit] = omit,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> SkillVersion:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = self.openai_client.with_raw_response.skills.versions.create(
            skill_id,
            default=default,
            files=files,  # type: ignore[arg-type]
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = SkillVersion(**json.loads(response.text))
        data._headers = response.headers
        return data

    def retrieve(
        self,
        version: str,
        *,
        skill_id: str,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> SkillVersion:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = self.openai_client.with_raw_response.skills.versions.retrieve(
            version,
            skill_id=skill_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = SkillVersion(**json.loads(response.text))
        data._headers = response.headers
        return data

    def list(
        self,
        skill_id: str,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> SkillVersionList:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = self.openai_client.with_raw_response.skills.versions.list(
            skill_id,
            after=after,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = SkillVersionList(**json.loads(response.text))
        data._headers = response.headers
        return data

    def delete(
        self,
        version: str,
        *,
        skill_id: str,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> SkillVersionDeleted:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = self.openai_client.with_raw_response.skills.versions.delete(
            version,
            skill_id=skill_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = SkillVersionDeleted(**json.loads(response.text))
        data._headers = response.headers
        return data


class AsyncSkillsVersions(AsyncAPIResource):
    content: AsyncSkillsVersionsContent

    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.content = AsyncSkillsVersionsContent(client)

    async def create(
        self,
        skill_id: str,
        *,
        default: Union[bool, Omit] = omit,
        files: Union[List[FileTypes], FileTypes, Omit] = omit,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> SkillVersion:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = await self.openai_client.with_raw_response.skills.versions.create(
            skill_id,
            default=default,
            files=files,  # type: ignore[arg-type]
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = SkillVersion(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def retrieve(
        self,
        version: str,
        *,
        skill_id: str,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> SkillVersion:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = await self.openai_client.with_raw_response.skills.versions.retrieve(
            version,
            skill_id=skill_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = SkillVersion(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def list(
        self,
        skill_id: str,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> SkillVersionList:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = await self.openai_client.with_raw_response.skills.versions.list(
            skill_id,
            after=after,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = SkillVersionList(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def delete(
        self,
        version: str,
        *,
        skill_id: str,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> SkillVersionDeleted:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = await self.openai_client.with_raw_response.skills.versions.delete(
            version,
            skill_id=skill_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = SkillVersionDeleted(**json.loads(response.text))
        data._headers = response.headers
        return data


class Skills(APIResource):
    content: SkillsContent
    versions: SkillsVersions

    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.content = SkillsContent(client)
        self.versions = SkillsVersions(client)

    def create(
        self,
        *,
        files: Union[List[FileTypes], FileTypes, Omit] = omit,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Skill:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = self.openai_client.with_raw_response.skills.create(
            files=files,  # type: ignore[arg-type]
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = Skill(**json.loads(response.text))
        data._headers = response.headers
        return data

    def retrieve(
        self,
        skill_id: str,
        *,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Skill:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = self.openai_client.with_raw_response.skills.retrieve(
            skill_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = Skill(**json.loads(response.text))
        data._headers = response.headers
        return data

    def update(
        self,
        skill_id: str,
        *,
        default_version: str,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Skill:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = self.openai_client.with_raw_response.skills.update(
            skill_id,
            default_version=default_version,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = Skill(**json.loads(response.text))
        data._headers = response.headers
        return data

    def list(
        self,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> SkillList:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = self.openai_client.with_raw_response.skills.list(
            after=after,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = SkillList(**json.loads(response.text))
        data._headers = response.headers
        return data

    def delete(
        self,
        skill_id: str,
        *,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> SkillDeleted:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = self.openai_client.with_raw_response.skills.delete(
            skill_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = SkillDeleted(**json.loads(response.text))
        data._headers = response.headers
        return data


class AsyncSkills(AsyncAPIResource):
    content: AsyncSkillsContent
    versions: AsyncSkillsVersions

    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.content = AsyncSkillsContent(client)
        self.versions = AsyncSkillsVersions(client)

    async def create(
        self,
        *,
        files: Union[List[FileTypes], FileTypes, Omit] = omit,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Skill:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = await self.openai_client.with_raw_response.skills.create(
            files=files,  # type: ignore[arg-type]
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = Skill(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def retrieve(
        self,
        skill_id: str,
        *,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Skill:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = await self.openai_client.with_raw_response.skills.retrieve(
            skill_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = Skill(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def update(
        self,
        skill_id: str,
        *,
        default_version: str,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Skill:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = await self.openai_client.with_raw_response.skills.update(
            skill_id,
            default_version=default_version,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = Skill(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def list(
        self,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> SkillList:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = await self.openai_client.with_raw_response.skills.list(
            after=after,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = SkillList(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def delete(
        self,
        skill_id: str,
        *,
        timeout: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> SkillDeleted:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        response = await self.openai_client.with_raw_response.skills.delete(
            skill_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = SkillDeleted(**json.loads(response.text))
        data._headers = response.headers
        return data
