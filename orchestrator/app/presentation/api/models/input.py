# Standard imports
from typing import Annotated, Optional
from pydantic import Field

# Internal imports
from app.infrastructure.common.entities import (
    Question,
    Plugin
)


class OrchestratorQuestion(Question):
    orchestrator_type: Annotated[Optional[str], "Type of orchestrator"] = Field(default="semantic_kernel", description="Specific orchestrator type: current options are: ['semantic_kernel']")

    def to_question(self) -> Question:
        """
        Converts an instance of OrchestratorQuestion to a Question instance by using the dict method to extract fields
        and removing the additional fields specific to OrchestratorQuestion.

        Returns:
            Question: A new instance of Question with the same properties as the OrchestratorQuestion instance,
            excluding the orchestrator-specific properties.
        """
        data = self.model_dump()  # Convert all attributes to a dictionary
        data.pop('orchestrator_type', None)  # Remove the attribute not present in Question
        return Question(**data)