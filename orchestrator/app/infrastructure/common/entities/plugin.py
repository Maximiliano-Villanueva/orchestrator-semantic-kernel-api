from pydantic import BaseModel
from typing import Any, Dict


class Plugin(BaseModel):
    name: str
    url: str
    configuration: Dict[str, Any]