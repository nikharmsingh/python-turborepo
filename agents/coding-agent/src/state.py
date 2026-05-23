from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class CodingState(TypedDict):
    messages: Annotated[list, add_messages]
    task: str
    code: str
    review: str
