from collections import defaultdict
import time
from typing import Any, Dict, List, Optional
from llama_index.core.callbacks.base_handler import (
        BaseCallbackHandler as LlamaIndexBaseCallbackHandler,
    )

from portkey_ai.api_resources.apis.logger import Logger 
from datetime import datetime, timezone
from llama_index.core.callbacks.schema import (
        CBEventType,
        EventPayload
    )
from llama_index.core.utilities.token_counting import TokenCounter


class PortkeyCallbackHandler(LlamaIndexBaseCallbackHandler):
    startTimestamp: int = 0
    endTimestamp: int = 0

    def __init__(
        self,
        api_key: str,
    ) -> None:
        super().__init__(
            event_starts_to_ignore=[],
            event_ends_to_ignore=[],
        )

        self.api_key = api_key

        self.portkey_logger = Logger(api_key=api_key)

        # self.llm_flag_start = False
        # self.embedding_flag_start = False

        # self.llm_flag_stop = False
        # self.embedding_flag_stop = False

        self.start = False
        self.end = False

        self.end_trace_flag = False

        self._token_counter = TokenCounter()
        self.token_embedding = 0
        self.token_llm = 0
        self.token_sum = 0


        # ------------------------------------------------
        self.log_object: Dict[str, Any] = {}
        self.prompt_records: List[str] = []
        self.usage_records: Any = {}
        self.prompt_tokens: int = 0
        self.completion_tokens: int = 0
        self.total_tokens: int = 0
        # ------------------------------------------------

        # ------------------------------------------------
        self.request: Any = {}
        self.requestMethod: str = "POST"            # Done
        self.requestURL: str = ""                   
        self.requestHeaders: Dict[str, Any] = {}    
        self.requestBody: Any = {}                  # Done

        # -----------------------------------------------
        self.response: Any = {}
        self.responseHeaders: Dict[str, Any] = {}   # Nowhere to get this from
        self.responseBody: Any = {}                 # Done
        self.responseStatus: int = 0                # Done
        self.responseTime: int = 0                  # Done

        self.streamingMode: bool = False

        if not api_key:
            raise ValueError("Please provide an API key to use PortkeyCallbackHandler")



    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        """Run when an event starts and return id of event."""

        if(event_type == CBEventType.LLM):
            self.llm_event_start(payload)

        print("on_event_start event_type", event_type)
        print("on_event_start payload", payload)
        print("on_event_start event_id", event_id)
        print("on_event_start parent_id", parent_id)
        print("on_event_start kwargs", kwargs)

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        """Run when an event ends."""

        if(event_type == CBEventType.LLM):
            self.llm_event_stop(payload, event_id)
        
        # if(event_type == CBEventType.EMBEDDING):
        #     self.embedding_event_stop(payload, self.embedding_flag_stop)            
        
        print("on_event_end event_type", event_type)
        print("on_event_end event_id", event_id)
        print("on_event_end payload", payload)


    def start_trace(self, trace_id: Optional[str] = None) -> None:
        """Run when an overall trace is launched."""    
        if not self.start:
            self.startTimestamp = int(datetime.now().timestamp())
            # self.start = True
        print("start_trace trace_id",trace_id)

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        """Run when an overall trace is exited."""
        # self.endTimestamp = int(datetime.now().timestamp())
        # self.responseTime = self.endTimestamp - self.startTimestamp
        # self.total_tokens = self.token_llm + self.token_embedding
        # self.responseStatus = 200
        # self.log_object.update(
        #     {
        #         "requestMethod": self.requestMethod,
        #         "requestURL": self.requestURL,
        #         "requestHeaders": self.requestHeaders,
        #         "requestBody": self.requestBody,
        #         "responseHeaders": self.responseHeaders,
        #         "responseBody": self.responseBody,
        #         "responseStatus": self.responseStatus,
        #         "responseTime": self.responseTime,
        #         "streamingMode": self.streamingMode,
        #     }
        # )
        # print("LOGGER WILL BE CALLED NOW")
        # # self.portkey_logger.log(log_object=self.log_object)
        
        # # self.end_trace_flag = True
        

        print("end_trace trace_id",trace_id)
        print("end_trace trace_map",trace_map)
        print("end_trace total_tokens", self.total_tokens)


    def llm_event_start(self, payload: Any) -> None:

        if EventPayload.MESSAGES in payload:
            messages = payload.get(EventPayload.MESSAGES, {})
            self.prompt_records = [{'role': m.role.value, 'content': m.content} for m in messages]
        
        print("llm_event_start prompt_records: ", self.prompt_records)

        self.request['url'] = payload.get(EventPayload.SERIALIZED, {}).get("base_url", "")
        self.request['method'] = "POST"
        self.requestHeaders["provider"] = "openai"
        self.request['body'] = {'messages':self.prompt_records}
        self.request['body'].update({"model": payload.get(EventPayload.SERIALIZED, {}).get("model", "")})
        self.request['body'].update({"temperature": payload.get(EventPayload.SERIALIZED, {}).get("temperature", "")}) 



        print("llm_event_start REQUEST: ", self.request)




        # if not llm_flag_start and EventPayload.SERIALIZED in payload:
        #     print("llm_event_start llm_flag_start: ", llm_flag_start)
        #     print("llm_event_start payload: ", payload.get(EventPayload.SERIALIZED, {}))
        #     self.requestBody["llm"] = payload.get(EventPayload.SERIALIZED, {})
            
            # self.llm_flag_start = True
        
        return None

    # def embedding_event_start(self, payload: Any, embedding_flag_start: bool) -> None:

    #     if not embedding_flag_start and EventPayload.SERIALIZED in payload:
    #         print("embedding_event_start embedding_flag_start: ", embedding_flag_start)
    #         print("embedding_event_start payload: ", payload.get(EventPayload.SERIALIZED, {}))
    #         self.requestBody["embedding"] = payload.get(EventPayload.SERIALIZED, {})
    #         # self.embedding_flag_start = True

    def llm_event_stop(self, payload: Any, event_id) -> None:

        self.endTimestamp = float(datetime.now().timestamp())
        responseTime = self.endTimestamp - self.startTimestamp

        data = payload.get(EventPayload.RESPONSE, {})
        # print("llm_event_stop BODY: ", data)
        chunks = payload.get(EventPayload.MESSAGES, {})
        self.token_llm = self._token_counter.estimate_tokens_in_messages(chunks)

        self.response['status'] = 200
        self.response['body'] = {'choices': [{
            "index":0,
            "message": {
                "role": data.message.role.value,
                "content": data.message.content
            },
            "logprobs": data.logprobs,
            "finish_reason": "done"
        }]}
        self.response['body'].update({'usage': {'total_tokens': self.token_llm}})
        self.response['body'].update({'id': event_id})
        self.response['body'].update({'created':int(time.time())})
        self.response['body'].update({'model': data.raw.get("model", "")})
        self.response['responseTime'] = int(responseTime * 1000)


        self.log_object.update(
            {
                "requestMethod": self.request['method'],
                "requestURL": self.request['url'],
                "requestHeaders": self.requestHeaders,
                "requestBody": self.request['body'],
                "responseHeaders": self.responseHeaders,
                "responseBody": self.response['body'],
                "responseStatus": self.response['status'],
                "responseTime": self.response['responseTime'] ,
                "streamingMode": self.streamingMode,
            }
        )

        self.portkey_logger.log(log_object=self.log_object)

        print("llm_event_stop RESPONSE: ", self.response)

        return None
