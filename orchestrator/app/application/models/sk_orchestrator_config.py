
# Standard import
import os

from dataclasses import dataclass
from typing import Annotated, Optional

from app.domain.models import OrchestratorConfig


__PLUGIN_PATH__ = os.path.join("semantic_kernel_impl", "plugins")
__PLANNER_ID__ = "orchestrator_planner"
__OPENAI_MODEL_VERSION__ = "gpt-4"


@dataclass
class SKOrchestratorConfig(OrchestratorConfig):
    plugins_path: Optional[Annotated[str, "Path to the plugins folder"]] = __PLUGIN_PATH__
    planner_id: Optional[Annotated[str, "Planner identification inside the kernel"]] = __PLANNER_ID__
    openai_model_version: Optional[Annotated[str, "Version of OpenAI model"]] = __OPENAI_MODEL_VERSION__
