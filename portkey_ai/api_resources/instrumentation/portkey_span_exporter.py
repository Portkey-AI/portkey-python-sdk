import json
from typing import Any, Collection
from opentelemetry.sdk.trace.export import SpanExporter, Span

from portkey_ai.api_resources.apis.logger import Logger
from portkey_ai.utils import string_to_uuid_v3


class PortkeySpanExporter(SpanExporter):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def transform_span_to_log(self, span: Span) -> dict:
        log = {
            "metadata": {
                "traceId": string_to_uuid_v3(span.context.trace_id),
                "spanId": span.context.span_id,
                "spanName": span.name,
                "parentSpanId": (span.parent.span_id if span.parent else None),
                "startTime": span.start_time,
                "endTime": span.end_time,
            },
            "request": {
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "body": json.loads(span.to_json()),
            },
            "response": {
                "status": 200,
                "headers": {"Content-Type": "application/json"},
                "body": {},
                "response_time": (span.end_time - span.start_time) * 10**-6,
            },
        }
        print(log)
        return log

    def export(self, spans: Collection[Span], **kwargs: Any) -> int:
        logger = Logger(api_key=self.api_key)
        logs = []
        for span in spans:
            logs.append(self.transform_span_to_log(span))
        try:
            logger.log(logs)
        except Exception as e:
            raise e

        return super().export(spans, **kwargs)
