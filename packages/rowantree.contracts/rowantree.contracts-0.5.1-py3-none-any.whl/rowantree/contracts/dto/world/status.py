"""" WorldStatus Definition """
from pydantic import BaseModel


class WorldStatus(BaseModel):
    """
    WorldStatus DTO
    Defines the status of the game world.

    NOTE / TODO:
    Rename active_players to active_users.

    Attributes
    ----------
    active_players: list[str]
        A list of active users.
    """

    active_players: list[str]
