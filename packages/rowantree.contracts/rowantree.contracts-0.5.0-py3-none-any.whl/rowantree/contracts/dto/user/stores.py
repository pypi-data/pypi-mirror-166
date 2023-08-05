from pydantic import BaseModel

from .store import UserStore


class UserStores(BaseModel):
    stores: list[UserStore]
