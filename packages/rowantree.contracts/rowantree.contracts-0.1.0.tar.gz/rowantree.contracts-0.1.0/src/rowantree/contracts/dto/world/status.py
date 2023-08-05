from pydantic import BaseModel


class WorldStatus(BaseModel):
    active_players: list[str]
