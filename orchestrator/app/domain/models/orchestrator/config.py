# Standard imports
from typing import Annotated, Optional
from dataclasses import dataclass


@dataclass
class OrchestratorConfig:
    openai_api_key: Annotated[str, "OpenAI Api Key"]
    org_id: Optional[Annotated[str, "org id"]]