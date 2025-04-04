import json
from typing import Any, Dict, Literal, Optional, Union
import httpx

from portkey_ai.api_resources.types.assistant_type import AssistantTool
from .utils import parse_headers
from typing import List
from pydantic import BaseModel, PrivateAttr

__all__ = [
    "Run",
    "Usage",
    "LastError",
    "Function",
    "RequiredActionFunctionToolCall",
    "RequiredActionSubmitToolOutputs",
    "RequiredAction",
    "FunctionDefinition",
    "ToolAssistantToolsCode",
    "ToolAssistantToolsRetrieval",
    "ToolAssistantToolsFunction",
    "Tool",
    "RunList",
    "RunStep",
    "StepDetails",
    "ToolCallsStepDetails",
    "MessageCreationStepDetails",
    "MessageCreation",
    "ToolCall",
    "CodeInterpreter",
    "CodeInterpreterOutput",
    "CodeInterpreterOutputLogs",
    "CodeInterpreterOutputImage",
    "CodeInterpreterOutputImageImage",
    "CodeToolCall",
    "RetrievalToolCall",
    "FunctionToolCall",
    "FunctionParameters",
    "RunStepList",
    "IncompleteDetails",
    "AssistantToolChoice",
    "AssistantToolChoiceFunction",
    "AssistantToolChoiceOption",
    "TruncationStrategy",
    "FileSearchRankingOptions",
    "FileSearchResultContent",
    "FileSearchResult",
    "FileSearch",
    "FileSearchToolCall",
]


class Function(BaseModel, extra="allow"):
    arguments: Optional[str] = None
    name: Optional[str] = None
    output: Optional[str] = None


class FunctionToolCall(BaseModel, extra="allow"):
    id: Optional[str] = None
    function: Optional[Function] = None
    type: Optional[Literal["function"]] = None


class RetrievalToolCall(BaseModel, extra="allow"):
    id: Optional[str] = None
    retrieval: Optional[object] = None
    type: Optional[str] = None


class CodeInterpreterOutputLogs(BaseModel, extra="allow"):
    logs: Optional[str] = None
    type: Optional[str] = None


class CodeInterpreterOutputImageImage(BaseModel, extra="allow"):
    file_id: Optional[str] = None


class CodeInterpreterOutputImage(BaseModel, extra="allow"):
    image: Optional[CodeInterpreterOutputImageImage] = None
    type: Optional[str] = None


CodeInterpreterOutput = Union[CodeInterpreterOutputLogs, CodeInterpreterOutputImage]


class CodeInterpreter(BaseModel, extra="allow"):
    input: Optional[str] = None
    outputs: Optional[List[CodeInterpreterOutput]] = None


class CodeToolCall(BaseModel, extra="allow"):
    id: Optional[str] = None
    code_interpreter: Optional[CodeInterpreter] = None
    type: Optional[str] = None


class FileSearchRankingOptions(BaseModel, extra="allow"):
    ranker: Optional[str] = None
    score_threshold: Optional[float] = None


class FileSearchResultContent(BaseModel, extra="allow"):
    text: Optional[str] = None
    type: Optional[str] = None


class FileSearchResult(BaseModel, extra="allow"):
    file_id: Optional[str] = None
    file_name: Optional[str] = None
    score: Optional[float] = None
    content: Optional[List[FileSearchResultContent]] = None


class FileSearch(BaseModel, extra="allow"):
    ranking_options: Optional[FileSearchRankingOptions] = None
    results: Optional[List[FileSearchResult]] = None


class FileSearchToolCall(BaseModel, extra="allow"):
    id: Optional[str] = None
    file_search: Optional[FileSearch] = None
    type: Optional[str] = None


ToolCall = Union[CodeToolCall, FileSearchToolCall, RetrievalToolCall, FunctionToolCall]


class ToolCallsStepDetails(BaseModel, extra="allow"):
    tool_calls: Optional[List[ToolCall]] = None
    type: Optional[str] = None


class MessageCreation(BaseModel, extra="allow"):
    message_id: Optional[str] = None


class MessageCreationStepDetails(BaseModel, extra="allow"):
    message_creation: Optional[MessageCreation] = None

    type: Optional[str] = None


StepDetails = Union[MessageCreationStepDetails, ToolCallsStepDetails]


class Usage(BaseModel, extra="allow"):
    completion_tokens: Optional[int] = None
    prompt_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class LastError(BaseModel, extra="allow"):
    code: Optional[str] = None
    message: Optional[str] = None


class FunctionRA(BaseModel, extra="allow"):
    arguments: Optional[str] = None
    name: Optional[str] = None


class RequiredActionFunctionToolCall(BaseModel, extra="allow"):
    id: Optional[str] = None
    function: Optional[FunctionRA] = None
    type: Optional[str] = None


class RequiredActionSubmitToolOutputs(BaseModel, extra="allow"):
    tool_calls: Optional[List[RequiredActionFunctionToolCall]] = None


class RequiredAction(BaseModel, extra="allow"):
    submit_tool_outputs: Optional[RequiredActionSubmitToolOutputs] = None
    type: Optional[str] = None


FunctionParameters = Dict[str, object]


class FunctionDefinition(BaseModel, extra="allow"):
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[FunctionParameters] = None


class ToolAssistantToolsCode(BaseModel, extra="allow"):
    type: Optional[str] = None


class ToolAssistantToolsRetrieval(BaseModel, extra="allow"):
    type: Optional[str] = None


class ToolAssistantToolsFunction(BaseModel, extra="allow"):
    function: Optional[FunctionDefinition] = None
    type: Optional[str] = None


Tool = Union[
    ToolAssistantToolsCode, ToolAssistantToolsRetrieval, ToolAssistantToolsFunction
]


class IncompleteDetails(BaseModel, extra="allow"):
    reason: Optional[str] = None


class AssistantToolChoiceFunction(BaseModel, extra="allow"):
    name: Optional[str] = None


class AssistantToolChoice(BaseModel, extra="allow"):
    type: Optional[str] = None

    function: Optional[AssistantToolChoiceFunction] = None


AssistantToolChoiceOption = Union[Optional[str], AssistantToolChoice]


class TruncationStrategy(BaseModel, extra="allow"):
    type: Optional[str] = None
    last_messages: Optional[int] = None


class Run(BaseModel, extra="allow"):
    id: Optional[str] = None
    assistant_id: Optional[str] = None
    cancelled_at: Optional[int] = None
    completed_at: Optional[int] = None
    created_at: Optional[int] = None
    expires_at: Optional[int] = None
    failed_at: Optional[int] = None
    file_ids: Optional[List[str]] = None
    instructions: Optional[str] = None
    last_error: Optional[LastError] = None
    metadata: Optional[object] = None
    model: Optional[str] = None
    object: Optional[str] = None
    required_action: Optional[RequiredAction] = None
    started_at: Optional[int] = None
    status: Optional[str] = None
    thread_id: Optional[str] = None
    tools: Optional[List[AssistantTool]] = None
    usage: Optional[Usage] = None
    incomplete_details: Optional[IncompleteDetails] = None
    max_completion_tokens: Optional[int] = None
    max_prompt_tokens: Optional[int] = None
    parallel_tool_calls: Optional[bool] = None
    tool_choice: Optional[AssistantToolChoiceOption] = None
    truncation_strategy: Optional[TruncationStrategy] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    response_format: Optional[Any] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class RunList(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[Run]] = None
    first_id: Optional[str] = None
    last_id: Optional[str] = None
    has_more: Optional[bool] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class RunStep(BaseModel, extra="allow"):
    id: Optional[str] = None
    assistant_id: Optional[str] = None
    cancelled_at: Optional[int] = None
    completed_at: Optional[int] = None
    created_at: Optional[int] = None
    expired_at: Optional[int] = None
    failed_at: Optional[int] = None
    last_error: Optional[LastError] = None
    metadata: Optional[object] = None
    object: Optional[str] = None
    run_id: Optional[str] = None
    status: Optional[str] = None
    step_details: Optional[StepDetails] = None
    thread_id: Optional[str] = None
    type: Optional[str] = None
    usage: Optional[Usage] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class RunStepList(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[RunStep]] = None
    first_id: Optional[str] = None
    last_id: Optional[str] = None
    has_more: Optional[bool] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
