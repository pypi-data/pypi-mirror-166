from typing import ClassVar, Dict, Type

from pydantic import BaseModel
from tygle_docs.types.responses import UpdateResponse


class UpdateRequestBody(BaseModel):
    """
    https://developers.google.com/docs/api/reference/rest/v1/documents/request#request
    """

    response_type: ClassVar[Type[UpdateResponse]] = UpdateResponse
    key: ClassVar[str]

    @property
    def UpdateRequest(self):
        return UpdateRequest(__root__={self.key: self})


class UpdateRequest(BaseModel):
    __root__: Dict[str, UpdateRequestBody]
