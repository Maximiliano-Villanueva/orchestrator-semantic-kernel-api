# Standard imports
from pydantic import BaseModel
from typing import Dict, List, Optional

# Internal
from app.infrastructure.common.entities.plugin import Plugin


class Question(BaseModel):
    user_id: int
    message_id: int  # message storing answer-response tuples in vekai
    chat_id: int
    domain_id: int
    question: str
    plugins: Optional[List[
        Plugin
    ]] = None