from enum import Enum

from app.schemas.response_schema import BaseSchema


class AccessFilesRules(Enum):
    internal = "internal"
    public = "public"
    private = "private"


class NextcloudFilesInSchema(BaseSchema):
    id: int
    file_name: str
    file_path: str
    file_type: str
    size: int
    service_requests_id: int
    access: str = AccessFilesRules
    expire: int | None = 24

    class Config:
        orm_mode = True


class NextcloudFilesUpdateSchema(BaseSchema):

    access: str = AccessFilesRules
    expire: int | None = 24
