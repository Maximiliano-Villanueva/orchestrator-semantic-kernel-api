# Standard imports
from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Annotated, Dict, Optional

# Internal imports

from app.infrastructure.utils import custom_logs
from app.domain.models import OrchestratorConfig


logger = custom_logs.getLogger(__name__)


class SingletonMeta(ABCMeta):
    """
    Metaclass for creating singleton classes.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
            logger.debug(f"Creating new instance of {cls.__name__}")
        else:
            logger.warning(f"Instance of {cls.__name__} already exists. Returning existing instance.")
        return cls._instances[cls]


class OrchestratorPlanningService(ABC, metaclass=SingletonMeta):
    """
    Abstract base class for an orchestration service based on a planner.
    """
    name: Annotated[str, "Name that identifies the Orchestrator"]
    
    def __init__(self, config: Annotated[OrchestratorConfig, "Configuration for Orchestrator"]):
        self.config = config
        self.initialized = False
        super().__init__()

    @abstractmethod
    async def initialize(self, config: Optional[OrchestratorConfig], **kwargs) -> Any:
        """
        Make any initializations required
        """
        pass

    @abstractmethod
    async def orchestrate(self, *args, **kwargs) -> Annotated[Dict[str, str], "Dictionary representing the response from other microservices"]:
        """
        Perform orchestration based on input
        """
        pass
