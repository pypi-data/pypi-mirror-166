from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from pydantic import EmailStr as EmailStr

class CustomError(BaseModel):
    message: str
    reasons: List[str]

class HttpSuccess(BaseModel):
    ok: str

class HttpError(BaseModel):
    status_code: int
    error: CustomError

class RoleEnum(str, Enum):
    user: str
    admin: str

class JwtParam(BaseModel):
    email: EmailStr
    first_name: str
    role: RoleEnum

class StatusEnum(str, Enum):
    created: str
    accepted: str
    wip: str
    implemented: str
    rejected: str

class TypeEnum(str, Enum):
    feature: str
    bug: str

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
