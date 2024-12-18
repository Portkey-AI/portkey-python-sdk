import json
from typing import Any, AsyncIterator, Dict, Iterable, Iterator, List, Optional, Union
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from ..._vendor.openai._types import NotGiven, NOT_GIVEN

# from portkey_ai.api_resources.utils import TextCompletionChunk
from portkey_ai.api_resources.types.complete_type import (
    TextCompletion,
    TextCompletionChunk,
)
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource


class Completion(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.client = client

    def stream_create(  # type: ignore[return]
        self,
        model,
        prompt,
        stream,
        temperature,
        max_tokens,
        top_p,
        best_of,
        echo,
        frequency_penalty,
        logit_bias,
        logprobs,
        n,
        presence_penalty,
        seed,
        stop,
        suffix,
        user,
        stream_options,
        **kwargs,
    ) -> Union[TextCompletion, Iterator[TextCompletionChunk]]:
        with self.openai_client.with_streaming_response.completions.create(
            model=model,
            prompt=prompt,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            best_of=best_of,
            echo=echo,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            logprobs=logprobs,
            n=n,
            presence_penalty=presence_penalty,
            seed=seed,
            stop=stop,
            suffix=suffix,
            user=user,
            stream_options=stream_options,
            extra_body=kwargs,
        ) as response:
            for line in response.iter_lines():
                json_string = line.replace("data: ", "")
                json_string = json_string.strip().rstrip("\n")
                if json_string == "":
                    continue
                elif json_string == "[DONE]":
                    break
                elif json_string != "":
                    json_data = json.loads(json_string)
                    json_data = TextCompletionChunk(**json_data)
                    yield json_data
                else:
                    return ""

    def normal_create(
        self,
        model,
        prompt,
        stream,
        temperature,
        max_tokens,
        top_p,
        best_of,
        echo,
        frequency_penalty,
        logit_bias,
        logprobs,
        n,
        presence_penalty,
        seed,
        stop,
        suffix,
        user,
        stream_options,
        **kwargs,
    ) -> TextCompletion:
        response = self.openai_client.with_raw_response.completions.create(
            model=model,
            prompt=prompt,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            best_of=best_of,
            echo=echo,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            logprobs=logprobs,
            n=n,
            presence_penalty=presence_penalty,
            seed=seed,
            stop=stop,
            suffix=suffix,
            user=user,
            stream_options=stream_options,
            extra_body=kwargs,
        )
        data = TextCompletion(**json.loads(response.text))
        data._headers = response.headers
        return data

    def create(
        self,
        *,
        model: Optional[str] = "portkey-default",
        prompt: Union[
            str, List[str], Iterable[int], Iterable[Iterable[int]], None
        ] = None,
        stream: Union[bool, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        max_tokens: Union[int, NotGiven] = NOT_GIVEN,
        top_p: Union[bool, NotGiven] = NOT_GIVEN,
        best_of: Union[int, NotGiven] = NOT_GIVEN,
        echo: Union[bool, NotGiven] = NOT_GIVEN,
        frequency_penalty: Union[float, NotGiven] = NOT_GIVEN,
        logit_bias: Union[Dict[str, int], NotGiven] = NOT_GIVEN,
        logprobs: Union[int, NotGiven] = NOT_GIVEN,
        n: Union[int, NotGiven] = NOT_GIVEN,
        presence_penalty: Union[float, NotGiven] = NOT_GIVEN,
        seed: Union[int, NotGiven] = NOT_GIVEN,
        stop: Union[Optional[str], List[str], None, NotGiven] = NOT_GIVEN,
        suffix: Union[str, NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        stream_options: Optional[Any] = NOT_GIVEN,
        **kwargs,
    ) -> Union[TextCompletion, Iterator[TextCompletionChunk]]:
        if stream is True:
            return self.stream_create(
                model=model,
                prompt=prompt,
                stream=stream,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                best_of=best_of,
                echo=echo,
                frequency_penalty=frequency_penalty,
                logit_bias=logit_bias,
                logprobs=logprobs,
                n=n,
                presence_penalty=presence_penalty,
                seed=seed,
                stop=stop,
                suffix=suffix,
                user=user,
                stream_options=stream_options,
                **kwargs,
            )
        else:
            return self.normal_create(
                model=model,
                prompt=prompt,
                stream=stream,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                best_of=best_of,
                echo=echo,
                frequency_penalty=frequency_penalty,
                logit_bias=logit_bias,
                logprobs=logprobs,
                n=n,
                presence_penalty=presence_penalty,
                seed=seed,
                stop=stop,
                suffix=suffix,
                user=user,
                stream_options=stream_options,
                **kwargs,
            )


class AsyncCompletion(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def stream_create(
        self,
        model,
        prompt,
        stream,
        temperature,
        max_tokens,
        top_p,
        best_of,
        echo,
        frequency_penalty,
        logit_bias,
        logprobs,
        n,
        presence_penalty,
        seed,
        stop,
        suffix,
        user,
        stream_options,
        **kwargs,
    ) -> Union[TextCompletion, AsyncIterator[TextCompletionChunk]]:
        async with self.openai_client.with_streaming_response.completions.create(
            model=model,
            prompt=prompt,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            best_of=best_of,
            echo=echo,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            logprobs=logprobs,
            n=n,
            presence_penalty=presence_penalty,
            seed=seed,
            stop=stop,
            suffix=suffix,
            user=user,
            stream_options=stream_options,
            extra_body=kwargs,
        ) as response:
            async for line in response.iter_lines():
                json_string = line.replace("data: ", "")
                json_string = json_string.strip().rstrip("\n")
                if json_string == "":
                    continue
                elif json_string == "[DONE]":
                    break
                elif json_string != "":
                    json_data = json.loads(json_string)
                    json_data = TextCompletionChunk(**json_data)
                    yield json_data
                else:
                    pass

    async def normal_create(
        self,
        model,
        prompt,
        stream,
        temperature,
        max_tokens,
        top_p,
        best_of,
        echo,
        frequency_penalty,
        logit_bias,
        logprobs,
        n,
        presence_penalty,
        seed,
        stop,
        suffix,
        user,
        stream_options,
        **kwargs,
    ) -> TextCompletion:
        response = await self.openai_client.with_raw_response.completions.create(
            model=model,
            prompt=prompt,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            best_of=best_of,
            echo=echo,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            logprobs=logprobs,
            n=n,
            presence_penalty=presence_penalty,
            seed=seed,
            stop=stop,
            suffix=suffix,
            user=user,
            stream_options=stream_options,
            extra_body=kwargs,
        )
        data = TextCompletion(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def create(
        self,
        *,
        model: Optional[str] = "portkey-default",
        prompt: Union[
            str, List[str], Iterable[int], Iterable[Iterable[int]], None
        ] = None,
        stream: Union[bool, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        max_tokens: Union[int, NotGiven] = NOT_GIVEN,
        top_p: Union[bool, NotGiven] = NOT_GIVEN,
        best_of: Union[int, NotGiven] = NOT_GIVEN,
        echo: Union[bool, NotGiven] = NOT_GIVEN,
        frequency_penalty: Union[float, NotGiven] = NOT_GIVEN,
        logit_bias: Union[Dict[str, int], NotGiven] = NOT_GIVEN,
        logprobs: Union[int, NotGiven] = NOT_GIVEN,
        n: Union[int, NotGiven] = NOT_GIVEN,
        presence_penalty: Union[float, NotGiven] = NOT_GIVEN,
        seed: Union[int, NotGiven] = NOT_GIVEN,
        stop: Union[Optional[str], List[str], None, NotGiven] = NOT_GIVEN,
        suffix: Union[str, NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        stream_options: Optional[Any] = NOT_GIVEN,
        **kwargs,
    ) -> Union[TextCompletion, AsyncIterator[TextCompletionChunk]]:
        if stream is True:
            return self.stream_create(
                model=model,
                prompt=prompt,
                stream=stream,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                best_of=best_of,
                echo=echo,
                frequency_penalty=frequency_penalty,
                logit_bias=logit_bias,
                logprobs=logprobs,
                n=n,
                presence_penalty=presence_penalty,
                seed=seed,
                stop=stop,
                suffix=suffix,
                user=user,
                stream_options=stream_options,
                **kwargs,
            )
        else:
            return await self.normal_create(
                model=model,
                prompt=prompt,
                stream=stream,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                best_of=best_of,
                echo=echo,
                frequency_penalty=frequency_penalty,
                logit_bias=logit_bias,
                logprobs=logprobs,
                n=n,
                presence_penalty=presence_penalty,
                seed=seed,
                stop=stop,
                suffix=suffix,
                user=user,
                stream_options=stream_options,
                **kwargs,
            )
