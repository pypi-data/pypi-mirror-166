""" UserIncomes Definition """

from pydantic import BaseModel

from .income import UserIncome


class UserIncomes(BaseModel):
    """
    UserIncomes DTO
    Defines a list of user incomes.
    NOTE / TODO:
    This is a unique set of UserIncome objects.

    Due to the legacy implementation this has been brought forward as-is.
    However,
    We want to make this a dictionary in the future given the access pattern (and uniqueness constraint) of the data.
    """

    incomes: list[UserIncome]
