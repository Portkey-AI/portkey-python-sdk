from typing import Dict, Literal, Mapping, Union
from typing_extensions import TypeAlias, override

from portkey_ai._vendor.openai._types import Omit


__all__ = ["Metadata", "Headers", "Query", "Body", "PropertyFormat", "PropertyInfo"]

Metadata: TypeAlias = Dict[str, str]
Headers = Mapping[str, Union[str, Omit]]
Query = Mapping[str, object]
Body = object

PropertyFormat = Literal["iso8601", "base64", "custom"]


class PropertyInfo:
    alias: Union[str, None]
    format: Union[PropertyFormat, None]
    format_template: Union[str, None]
    discriminator: Union[str, None]

    def __init__(
        self,
        *,
        alias: Union[str, None] = None,
        format: Union[PropertyFormat, None] = None,
        format_template: Union[str, None] = None,
        discriminator: Union[str, None] = None,
    ) -> None:
        self.alias = alias
        self.format = format
        self.format_template = format_template
        self.discriminator = discriminator

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(alias='{self.alias}', format={self.format}, format_template='{self.format_template}', discriminator='{self.discriminator}')"  # noqa: E501
