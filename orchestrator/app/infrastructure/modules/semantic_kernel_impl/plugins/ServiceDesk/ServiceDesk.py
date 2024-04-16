# Standard imports
from typing import Any, Annotated, Dict, Union, Optional

# Third party
from semantic_kernel.functions import kernel_function

# Internal imports
from app.infrastructure.modules.semantic_kernel_impl.plugins.orchestrator_plugins import OrchestratorPlugin
from app.infrastructure.utils import custom_logs
from app.infrastructure.common.entities import Question


logger = custom_logs.getLogger("ServiceDeskPlugin")


class ServiceDesk(OrchestratorPlugin):

    def __init__(self):
        pass
    
    @kernel_function(
        description="Get and list incidences using the ticketing service ServiceDesk",
        name="get_incidences"
    )
    def get_incidences(self, question: Union[Annotated[str, "List the incidences"], Annotated[Question, "List the incidences"]],
                       headers: Annotated[Optional[Dict[str, str]], "Headers to send to request"] = dict()) -> Annotated[Dict[Any, Any], "List of incidences"]:
        if not isinstance(question, Question):
            raise Exception("No service desk plugin was specified")
        
        result = self.send_request_plugin(question=question, headers=headers)
        return result
