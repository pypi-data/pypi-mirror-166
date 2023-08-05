from pydantic import BaseModel


class UserActive(BaseModel):
    active: bool
