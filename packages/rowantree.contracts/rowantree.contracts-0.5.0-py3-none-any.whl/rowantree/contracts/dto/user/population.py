from pydantic import BaseModel


class UserPopulation(BaseModel):
    population: int
