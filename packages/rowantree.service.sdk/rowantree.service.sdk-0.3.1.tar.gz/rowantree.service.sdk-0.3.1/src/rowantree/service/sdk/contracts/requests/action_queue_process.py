from pydantic import BaseModel
from rowantree.contracts import ActionQueue


class ActionQueueProcessRequest(BaseModel):
    queue: ActionQueue
