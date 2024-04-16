# Standard imports
import os

# Third-party imports
from fastapi import (
    APIRouter,
    HTTPException,
    status
)

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
    InvalidOrchestrator,
    InitializationError,
    OrchestratorReponseInvalid
)
from app.presentation.api.v1.endpoints.services import orchestrate
from app.application.exceptions import OrchestratorNotInitialized


# Initialize logger
logger = custom_logs.getLogger("orchestrator_endpoint")

router_orchestator = APIRouter(
    prefix="/orchestator", tags=["orchestator"]
)


@router_orchestator.post("", response_model=ContextResponse)
async def question_domain(question: OrchestratorQuestion):
    """
    Entrypoint for any requests that needs to be orquestrated.

    Parameters:
    - question (Question): The query input data.

    Returns:
    - dict: The response dictionary with the answer to the question and the context used to formulate the answer.

    Raises:
    - HTTPException: If there are issues with the query process.
    """

    try:
        response = await orchestrate(question=question)
        if isinstance(response, ErrorResponse):
            raise Exception(str(response))
    except InvalidOrchestrator as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.default_message,
        )
    except (InitializationError, OrchestratorReponseInvalid) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.default_message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    return response
