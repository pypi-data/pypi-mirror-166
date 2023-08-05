from pydantic import BaseModel


class Merchant(BaseModel):
    name: str
