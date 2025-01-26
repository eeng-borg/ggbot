from typing import TypedDict


class TimeData(TypedDict):

    hour: int
    minute: int
    day: int
    month: int
    year: int


class CommandData(TypedDict):
    "Types for command data dictionary"
    user: str
    command: str
    input: str
    time: TimeData


class KorniszonData(CommandData):
    "Extended command data specific to Korniszon, including a score."
    score: float