from pydantic import BaseModel, field_validator
from typing import Dict
from datetime import datetime
from pydantic import EmailStr


class GetReferal(BaseModel):
    referal_head: str

    def get_referal_link(self) -> Dict[str, str]:
        return {'referal_link': f'http://127.0.0.1:8000/referal/{self.referal_head}'}


class FullReferal(GetReferal):
    id: int
    user_id: int
    life_time: datetime
    user: bool


class EmailRef(BaseModel):
    email: EmailStr


class UserRefered(BaseModel):
    id: int
    login: str
    email: str
    date_registration: datetime

    class Config:
        from_attributes = True
        orm_mode = True
