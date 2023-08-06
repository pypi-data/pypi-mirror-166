""" User Event Definition """

from typing import Optional

from pydantic import BaseModel


class UserEvent(BaseModel):
    """
    UserEvent DTO
    Defines an event of a user.
    In practice this is a state change for the user as a result of an in-world story or encounter.

    Attributes
    ----------
    title: str
        The title of the event.
    text: Optional[list[str]]
        The optional list of text(s) of event.  The set of entries are ment to be rendered sequentially user-side.
    reward: Optional[dict[str, int]]
        The optional list of rewards (positive deltas to apply to the user)
    curse: Optional[dict[str, int]]
        The optional list of curses (negative deltas to apply to the user)
    """

    title: str
    text: Optional[list[str]]
    reward: Optional[dict[str, int]]
    curse: Optional[dict[str, int]]
