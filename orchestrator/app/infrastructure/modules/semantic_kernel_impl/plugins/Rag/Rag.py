# Standard imports
from typing import Any, Annotated, Dict, Union, Optional
from semantic_kernel.functions import kernel_function

# Internal imports
from app.infrastructure.common.entities import Question
from app.infrastructure.modules.semantic_kernel_impl.plugins.orchestrator_plugins import OrchestratorPlugin
from app.infrastructure.utils import custom_logs
from app.infrastructure.modules.requester.requester import Requester


logger = custom_logs.getLogger("ServiceDeskPlugin")


class Rag(OrchestratorPlugin):

    def __init__(self):
        pass

    @kernel_function(
        description="Default plugin to call when no other plugin can be used. Any information not provided by other functions are meant to be retrieved from here.",
        name="ask_rag"
    )
    
    def ask_rag(self, question: Union[Annotated[str, "User question"],
                                      Annotated[Question, "User Question"]],
                headers: Annotated[Optional[Dict[str, str]], "Headers to send to request"] = dict()) -> Annotated[Dict[Any, Any], "Response from request"]:
        """
        Request answer from RAG
        """
        # TODO: .env
        url = f"http://localhost:8000/domain"
        logger.info(question)
        logger.info(f"headers: {headers}")
        result = Requester.post(url=url, data=question.model_dump_json(),
                                headers=headers, is_json=False)
        if result.status_code != 200:
            return {"detail": result.reason, "status_code": result.status_code, "text": result.text}
        return result.json()

