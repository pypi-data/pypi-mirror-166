from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr

#
# GENERIC
#


class CustomError(BaseModel):
    message: str
    reasons: List[str]


#
# HTTP
#


class HttpSuccess(BaseModel):
    ok: str


class HttpError(BaseModel):
    status_code: int
    error: CustomError


#
# JWT
#


class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"


class JwtParam(BaseModel):
    email: EmailStr
    first_name: str
    role: RoleEnum


#
# FEATURE REQUEST
#


class StatusEnum(str, Enum):
    created = "created"
    accepted = "accepted"
    wip = "wip"
    implemented = "implemented"
    rejected = "rejected"


class TypeEnum(str, Enum):
    feature = "feature"
    bug = "bug"


class FeatureRequest(BaseModel):
    uuid: Optional[str]
    title: str
    type: TypeEnum
    description: str
    author: EmailStr
    status: StatusEnum


class FeatureRequestList(BaseModel):
    __root__: List[FeatureRequest]


class FeatureRequestMeta(BaseModel):
    uuid: str
    upvote_count: int
    current_user_voted: bool


class FeatureRequestMetaList(BaseModel):
    __root__: List[FeatureRequestMeta]
