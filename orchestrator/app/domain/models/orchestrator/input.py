# Standard imports
from typing import Annotated, Any, Optional, Dict
from dataclasses import dataclass

from app.infrastructure.common.entities import Question


@dataclass
class RequestQuestion:
    question: Annotated[Question, "OpenAI Api Key"]
    extra: Optional[Annotated[Dict[Any, Any], "org id"]]