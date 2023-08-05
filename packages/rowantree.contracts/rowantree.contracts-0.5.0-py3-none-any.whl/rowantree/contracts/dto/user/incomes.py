from pydantic import BaseModel

from .income import UserIncome


class UserIncomes(BaseModel):
    incomes: list[UserIncome]
