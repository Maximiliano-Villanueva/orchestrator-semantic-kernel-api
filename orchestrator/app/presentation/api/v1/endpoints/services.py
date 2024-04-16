# Standard imports
import os

from typing import Union, Annotated

# Internal imports
from app.infrastructure.utils import custom_logs
from app.presentation.api.models import (
    SuccesfulResponse,
    ContextResponse,
    ErrorResponse
)
from app.presentation.api.models import (
    Plugin,
    OrchestratorQuestion
)
from app.application.services.sk_orchestrator import SKernelOrchestrator
from app.application.models.sk_orchestrator_config import SKOrchestratorConfig

from app.domain.services.orchestrator import OrchestratorPlanningService

from app.presentation.api.exceptions.orchestrator import (
    InitializationError,
    InvalidOrchestrator,
    OrchestratorReponseInvalid
)
from app.application.exceptions import OrchestratorNotInitialized
from app.domain.models import RequestQuestion


# Initialize logger
logger = custom_logs.getLogger("orchestrator_endpoint")


async def orchestrate(question: OrchestratorQuestion) -> Annotated[Union[ContextResponse, ErrorResponse], "Response obtained from orchestration"]:
    """
    Provide the service for orchestration

    raises:
        - InvalidOrchestrator
        - InitializationError
    """
    orchestrator: OrchestratorPlanningService = None
    
    # Get the orchestrator
    # TODO: factory
    if question.orchestrator_type == SKernelOrchestrator.name:
        config = SKOrchestratorConfig(openai_api_key=os.getenv("OPENAI_API_KEY"), org_id=os.getenv("ORG_ID"))
        orchestrator = SKernelOrchestrator(config=config)
    else:
        raise InvalidOrchestrator
    
    try:
        # Initialize the orchestrator
        await orchestrator.initialize()

        # Create and execute plan
        request_extra = {"headers": {"Authorization": ""}}
        
        response = await orchestrator.orchestrate(question=RequestQuestion(question.to_question(), request_extra))

        # Check if all fields are present
        if not isinstance(response, dict):
            logger.error(response)
            logger.exception()
            raise OrchestratorReponseInvalid
        
        if all(field_name in response for field_name in ContextResponse.__annotations__):
            return ContextResponse(**response)
        elif all(field_name in response for field_name in ErrorResponse.__annotations__):
            return ErrorResponse(**response)

    except OrchestratorNotInitialized:
        raise InitializationError