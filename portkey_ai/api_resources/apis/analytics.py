from typing import Any, Literal, Union
from portkey_ai._vendor.openai import NOT_GIVEN, NotGiven
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.analytics_type import (
    AnalyticsGraphResponse,
    AnalyticsGroupResponse,
    AnalyticsSummaryResponse,
)

ANALYTICS_API_PATH = "/analytics"


class AnalyticsGraphs(APIResource):
    """Analytics Graphs API for retrieving time-series analytics data."""

    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def _build_query_string(
        self,
        time_of_generation_min: str,
        time_of_generation_max: str,
        total_units_min: Union[int, NotGiven] = NOT_GIVEN,
        total_units_max: Union[int, NotGiven] = NOT_GIVEN,
        cost_min: Union[float, NotGiven] = NOT_GIVEN,
        cost_max: Union[float, NotGiven] = NOT_GIVEN,
        status_code: Union[str, NotGiven] = NOT_GIVEN,
        virtual_keys: Union[str, NotGiven] = NOT_GIVEN,
        configs: Union[str, NotGiven] = NOT_GIVEN,
        workspace_slug: Union[str, NotGiven] = NOT_GIVEN,
        api_key_ids: Union[str, NotGiven] = NOT_GIVEN,
        ai_org_model: Union[str, NotGiven] = NOT_GIVEN,
        prompt_slug: Union[str, NotGiven] = NOT_GIVEN,
        metadata: Union[str, NotGiven] = NOT_GIVEN,
        cache_status: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> str:
        query = {
            "time_of_generation_min": time_of_generation_min,
            "time_of_generation_max": time_of_generation_max,
            "total_units_min": total_units_min,
            "total_units_max": total_units_max,
            "cost_min": cost_min,
            "cost_max": cost_max,
            "status_code": status_code,
            "virtual_keys": virtual_keys,
            "configs": configs,
            "workspace_slug": workspace_slug,
            "api_key_ids": api_key_ids,
            "ai_org_model": ai_org_model,
            "prompt_slug": prompt_slug,
            "metadata": metadata,
            "cache_status": cache_status,
            **kwargs,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        return urlencode(filtered_query)

    def requests(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get requests analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/requests?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def cost(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get cost analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/cost?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def latency(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get latency analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/latency?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def tokens(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get tokens analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/tokens?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def users(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get users analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/users?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def users_requests(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get users/requests analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/users/requests?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def errors(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get errors analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/errors?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def errors_rate(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get errors rate analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/errors/rate?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def errors_stacks(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get errors stacks analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/errors/stacks?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def errors_status_codes(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get errors status codes analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/errors/status-codes?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def requests_rescued(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get rescued requests analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/requests/rescued?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def cache_hit_rate(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get cache hit rate analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/cache/hit-rate?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def cache_latency(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get cache latency analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/cache/latency?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def feedbacks(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get feedbacks analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/feedbacks?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def feedbacks_scores(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get feedback scores analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/feedbacks/scores?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def feedbacks_weighted(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get weighted feedbacks analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/feedbacks/weighted?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def feedbacks_ai_models(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get feedbacks by AI models analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/graphs/feedbacks/ai-models?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AnalyticsGroups(APIResource):
    """Analytics Groups API for retrieving grouped analytics data."""

    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def _build_query_string(
        self,
        time_of_generation_min: str,
        time_of_generation_max: str,
        columns: Union[str, NotGiven] = NOT_GIVEN,
        include_total: Union[bool, NotGiven] = NOT_GIVEN,
        current_page: Union[int, NotGiven] = NOT_GIVEN,
        page_size: Union[int, NotGiven] = NOT_GIVEN,
        order_by: Union[str, NotGiven] = NOT_GIVEN,
        order_by_type: Union[Literal["asc", "desc"], NotGiven] = NOT_GIVEN,
        virtual_keys: Union[str, NotGiven] = NOT_GIVEN,
        configs: Union[str, NotGiven] = NOT_GIVEN,
        workspace_slug: Union[str, NotGiven] = NOT_GIVEN,
        api_key_ids: Union[str, NotGiven] = NOT_GIVEN,
        ai_org_model: Union[str, NotGiven] = NOT_GIVEN,
        prompt_slug: Union[str, NotGiven] = NOT_GIVEN,
        metadata: Union[str, NotGiven] = NOT_GIVEN,
        cache_status: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> str:
        query = {
            "time_of_generation_min": time_of_generation_min,
            "time_of_generation_max": time_of_generation_max,
            "columns": columns,
            "include_total": include_total,
            "current_page": current_page,
            "page_size": page_size,
            "order_by": order_by,
            "order_by_type": order_by_type,
            "virtual_keys": virtual_keys,
            "configs": configs,
            "workspace_slug": workspace_slug,
            "api_key_ids": api_key_ids,
            "ai_org_model": ai_org_model,
            "prompt_slug": prompt_slug,
            "metadata": metadata,
            "cache_status": cache_status,
            **kwargs,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        return urlencode(filtered_query)

    def users(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGroupResponse:
        """Get analytics grouped by users."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/groups/users?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGroupResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def ai_models(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGroupResponse:
        """Get analytics grouped by AI models."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/groups/ai-models?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGroupResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def workspaces(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGroupResponse:
        """Get analytics grouped by workspaces."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/groups/workspaces?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGroupResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def metadata(
        self,
        *,
        metadata_key: str,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGroupResponse:
        """Get analytics grouped by metadata key."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/groups/metadata/{metadata_key}?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGroupResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def group_by(
        self,
        *,
        group_by: Literal[
            "ai_service",
            "model",
            "status_code",
            "api_key",
            "config",
            "workspace",
            "provider",
            "prompt",
        ],
        time_of_generation_min: str,
        time_of_generation_max: str,
        columns: Union[str, NotGiven] = NOT_GIVEN,
        include_total: Union[bool, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> AnalyticsGroupResponse:
        """Get analytics grouped by specified dimension."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            columns=columns,
            include_total=include_total,
            **kwargs,
        )
        return self._get(
            f"{ANALYTICS_API_PATH}/groups/{group_by}?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGroupResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AnalyticsSummary(APIResource):
    """Analytics Summary API for retrieving summary analytics data."""

    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def cache(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        workspace_slug: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> AnalyticsSummaryResponse:
        """Get cache summary analytics."""
        query = {
            "time_of_generation_min": time_of_generation_min,
            "time_of_generation_max": time_of_generation_max,
            "workspace_slug": workspace_slug,
            **kwargs,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{ANALYTICS_API_PATH}/summary/cache?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsSummaryResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class Analytics(APIResource):
    """Analytics API for retrieving analytics data from Portkey."""

    graphs: AnalyticsGraphs
    groups: AnalyticsGroups
    summary: AnalyticsSummary

    def __init__(self, client: APIClient) -> None:
        super().__init__(client)
        self.graphs = AnalyticsGraphs(client)
        self.groups = AnalyticsGroups(client)
        self.summary = AnalyticsSummary(client)


class AsyncAnalyticsGraphs(AsyncAPIResource):
    """Async Analytics Graphs API for retrieving time-series analytics data."""

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    def _build_query_string(
        self,
        time_of_generation_min: str,
        time_of_generation_max: str,
        total_units_min: Union[int, NotGiven] = NOT_GIVEN,
        total_units_max: Union[int, NotGiven] = NOT_GIVEN,
        cost_min: Union[float, NotGiven] = NOT_GIVEN,
        cost_max: Union[float, NotGiven] = NOT_GIVEN,
        status_code: Union[str, NotGiven] = NOT_GIVEN,
        virtual_keys: Union[str, NotGiven] = NOT_GIVEN,
        configs: Union[str, NotGiven] = NOT_GIVEN,
        workspace_slug: Union[str, NotGiven] = NOT_GIVEN,
        api_key_ids: Union[str, NotGiven] = NOT_GIVEN,
        ai_org_model: Union[str, NotGiven] = NOT_GIVEN,
        prompt_slug: Union[str, NotGiven] = NOT_GIVEN,
        metadata: Union[str, NotGiven] = NOT_GIVEN,
        cache_status: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> str:
        query = {
            "time_of_generation_min": time_of_generation_min,
            "time_of_generation_max": time_of_generation_max,
            "total_units_min": total_units_min,
            "total_units_max": total_units_max,
            "cost_min": cost_min,
            "cost_max": cost_max,
            "status_code": status_code,
            "virtual_keys": virtual_keys,
            "configs": configs,
            "workspace_slug": workspace_slug,
            "api_key_ids": api_key_ids,
            "ai_org_model": ai_org_model,
            "prompt_slug": prompt_slug,
            "metadata": metadata,
            "cache_status": cache_status,
            **kwargs,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        return urlencode(filtered_query)

    async def requests(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get requests analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/requests?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def cost(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get cost analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/cost?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def latency(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get latency analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/latency?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def tokens(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get tokens analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/tokens?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def users(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get users analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/users?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def users_requests(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get users/requests analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/users/requests?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def errors(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get errors analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/errors?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def errors_rate(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get errors rate analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/errors/rate?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def errors_stacks(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get errors stacks analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/errors/stacks?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def errors_status_codes(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get errors status codes analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/errors/status-codes?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def requests_rescued(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get rescued requests analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/requests/rescued?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def cache_hit_rate(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get cache hit rate analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/cache/hit-rate?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def cache_latency(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get cache latency analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/cache/latency?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def feedbacks(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get feedbacks analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/feedbacks?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def feedbacks_scores(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get feedback scores analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/feedbacks/scores?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def feedbacks_weighted(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get weighted feedbacks analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/feedbacks/weighted?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def feedbacks_ai_models(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGraphResponse:
        """Get feedbacks by AI models analytics graph data."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/graphs/feedbacks/ai-models?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGraphResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncAnalyticsGroups(AsyncAPIResource):
    """Async Analytics Groups API for retrieving grouped analytics data."""

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    def _build_query_string(
        self,
        time_of_generation_min: str,
        time_of_generation_max: str,
        columns: Union[str, NotGiven] = NOT_GIVEN,
        include_total: Union[bool, NotGiven] = NOT_GIVEN,
        current_page: Union[int, NotGiven] = NOT_GIVEN,
        page_size: Union[int, NotGiven] = NOT_GIVEN,
        order_by: Union[str, NotGiven] = NOT_GIVEN,
        order_by_type: Union[Literal["asc", "desc"], NotGiven] = NOT_GIVEN,
        virtual_keys: Union[str, NotGiven] = NOT_GIVEN,
        configs: Union[str, NotGiven] = NOT_GIVEN,
        workspace_slug: Union[str, NotGiven] = NOT_GIVEN,
        api_key_ids: Union[str, NotGiven] = NOT_GIVEN,
        ai_org_model: Union[str, NotGiven] = NOT_GIVEN,
        prompt_slug: Union[str, NotGiven] = NOT_GIVEN,
        metadata: Union[str, NotGiven] = NOT_GIVEN,
        cache_status: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> str:
        query = {
            "time_of_generation_min": time_of_generation_min,
            "time_of_generation_max": time_of_generation_max,
            "columns": columns,
            "include_total": include_total,
            "current_page": current_page,
            "page_size": page_size,
            "order_by": order_by,
            "order_by_type": order_by_type,
            "virtual_keys": virtual_keys,
            "configs": configs,
            "workspace_slug": workspace_slug,
            "api_key_ids": api_key_ids,
            "ai_org_model": ai_org_model,
            "prompt_slug": prompt_slug,
            "metadata": metadata,
            "cache_status": cache_status,
            **kwargs,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        return urlencode(filtered_query)

    async def users(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGroupResponse:
        """Get analytics grouped by users."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/groups/users?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGroupResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def ai_models(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGroupResponse:
        """Get analytics grouped by AI models."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/groups/ai-models?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGroupResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def workspaces(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGroupResponse:
        """Get analytics grouped by workspaces."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/groups/workspaces?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGroupResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def metadata(
        self,
        *,
        metadata_key: str,
        time_of_generation_min: str,
        time_of_generation_max: str,
        **kwargs: Any,
    ) -> AnalyticsGroupResponse:
        """Get analytics grouped by metadata key."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/groups/metadata/{metadata_key}?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGroupResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def group_by(
        self,
        *,
        group_by: Literal[
            "ai_service",
            "model",
            "status_code",
            "api_key",
            "config",
            "workspace",
            "provider",
            "prompt",
        ],
        time_of_generation_min: str,
        time_of_generation_max: str,
        columns: Union[str, NotGiven] = NOT_GIVEN,
        include_total: Union[bool, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> AnalyticsGroupResponse:
        """Get analytics grouped by specified dimension."""
        query_string = self._build_query_string(
            time_of_generation_min=time_of_generation_min,
            time_of_generation_max=time_of_generation_max,
            columns=columns,
            include_total=include_total,
            **kwargs,
        )
        return await self._get(
            f"{ANALYTICS_API_PATH}/groups/{group_by}?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsGroupResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncAnalyticsSummary(AsyncAPIResource):
    """Async Analytics Summary API for retrieving summary analytics data."""

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def cache(
        self,
        *,
        time_of_generation_min: str,
        time_of_generation_max: str,
        workspace_slug: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> AnalyticsSummaryResponse:
        """Get cache summary analytics."""
        query = {
            "time_of_generation_min": time_of_generation_min,
            "time_of_generation_max": time_of_generation_max,
            "workspace_slug": workspace_slug,
            **kwargs,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{ANALYTICS_API_PATH}/summary/cache?{query_string}",
            params=None,
            body=None,
            cast_to=AnalyticsSummaryResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncAnalytics(AsyncAPIResource):
    """Async Analytics API for retrieving analytics data from Portkey."""

    graphs: AsyncAnalyticsGraphs
    groups: AsyncAnalyticsGroups
    summary: AsyncAnalyticsSummary

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.graphs = AsyncAnalyticsGraphs(client)
        self.groups = AsyncAnalyticsGroups(client)
        self.summary = AsyncAnalyticsSummary(client)
