from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.utils import PortkeyApiPaths, GenericResponse


class MainFiles(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        file,
        purpose,
        **kwargs
    ) -> GenericResponse:

        response = self.openai_client.files.create(file=file, purpose=purpose, **kwargs)
        return response

    def list(
        self,
        **kwargs
    ) -> GenericResponse:

        response = self.openai_client.files.list(**kwargs)
        return response
    
    def retrieve(
        self,
        file_id,
        **kwargs
    ) -> GenericResponse:

        response = self.openai_client.files.retrieve(
            file_id=file_id, **kwargs)
        return response
    
    def delete(
        self,
        file_id,
        **kwargs
    ) -> GenericResponse:

        response = self.openai_client.files.delete(
            file_id=file_id, **kwargs)
        return response
    
    def retrieveContent(
        self,
        file_id,
        **kwargs
    ) -> GenericResponse:

        response = self.openai_client.files.retrieveContent(
            file_id=file_id, **kwargs)
        return response


class AsyncMainFiles(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        file,
        purpose,
        **kwargs
    ) -> GenericResponse:

        response = await self.openai_client.files.create(file=file, purpose=purpose, **kwargs)
        return response

    async def list(
        self,
        **kwargs
    ) -> GenericResponse:

        response = await self.openai_client.files.list(**kwargs)
        return response
    
    async def retrieve(
        self,
        file_id,
        **kwargs
    ) -> GenericResponse:

        response = await self.openai_client.files.retrieve(
            file_id=file_id, **kwargs)
        return response
    
    async def delete(
        self,
        file_id,
        **kwargs
    ) -> GenericResponse:

        response = await self.openai_client.files.delete(
            file_id=file_id, **kwargs)
        return response
    
    async def retrieveContent(
        self,
        file_id,
        **kwargs
    ) -> GenericResponse:

        response = await self.openai_client.files.retrieveContent(
            file_id=file_id, **kwargs)
        return response