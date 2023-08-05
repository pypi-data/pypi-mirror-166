from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from tygle_docs.types.enums import ContentAlignment
from tygle_docs.types.resources.models import Dimension


class TableCellStyle(BaseModel):
    """
    https://developers.google.com/docs/api/reference/rest/v1/documents#TableCellStyle
    """

    background_color: Optional[Dict[str, Dict]] = Field(
        None, alias="backgroundColor"
    )  # TODO Type
    border_left: Optional[Dict[str, Any]] = Field(None, alias="borderLeft")  # TODO Type
    border_right: Optional[Dict[str, Any]] = Field(
        None, alias="borderRight"
    )  # TODO Type
    border_top: Optional[Dict[str, Any]] = Field(None, alias="borderTop")  # TODO Type
    border_bottom: Optional[Dict[str, Any]] = Field(
        None, alias="borderBottom"
    )  # TODO Type
    padding_left: Optional[Dimension] = Field(None, alias="paddingLeft")
    padding_right: Optional[Dimension] = Field(None, alias="paddingRight")
    padding_top: Optional[Dimension] = Field(None, alias="paddingTop")
    padding_bottom: Optional[Dimension] = Field(None, alias="paddingBottom")


class TableCellStyleRead(TableCellStyle):
    row_span: int = Field(alias="rowSpan")
    column_span: int = Field(alias="columnSpan")
    content_alignment: ContentAlignment = Field(alias="contentAlignment")


class TableCellStyleWrite(TableCellStyle):
    content_alignment: Optional[ContentAlignment] = Field(
        None, alias="contentAlignment"
    )
