import json
from typing import Any, Sequence
from opentelemetry.sdk.trace.export import (
    SpanExporter,
    SpanExportResult,
    ReadableSpan,
)

from portkey_ai.api_resources.apis.logger import Logger
from portkey_ai.utils import string_to_uuid


class PortkeySpanExporter(SpanExporter):
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def transform_span_to_log(self, span: ReadableSpan) -> dict:
        start_time = span.start_time
        end_time = span.end_time
        response_time: float
        if start_time and end_time:
            response_time = (end_time - start_time) * 10**-6
        else:
            response_time = 0
        log = {
            "metadata": {
                "traceId": string_to_uuid(span.context.trace_id),
                "spanId": span.context.span_id,
                "spanName": span.name,
                "parentSpanId": (span.parent.span_id if span.parent else None),
                "startTime": start_time,
                "endTime": end_time,
                "_logType": "opentelemetry",
                "_source": (
                    span.attributes.get("_source", "unknown")
                    if span.attributes
                    else "unknown"
                ),
                "framework.version": (
                    span.attributes.get("framework.version", "unknown")
                    if span.attributes
                    else "unknown"
                ),
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
                "response_time": response_time,
            },
        }
        return log

    def export(self, spans: Sequence[ReadableSpan], **kwargs: Any) -> SpanExportResult:
        logger = Logger(api_key=self.api_key, base_url=self.base_url)
        logs = []
        for span in spans:
            logs.append(self.transform_span_to_log(span))
        try:
            logger.log(logs)
        except Exception:
            return SpanExportResult.FAILURE

        return SpanExportResult.SUCCESS
