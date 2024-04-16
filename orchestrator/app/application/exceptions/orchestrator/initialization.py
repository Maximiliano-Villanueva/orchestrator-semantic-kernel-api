from typing import Optional


class OrchestratorNotInitialized(Exception):
    default_message: str = "Orchestrator has not been initialized. "

    def __init__(self, message: Optional[str] = None):
        """
        Initialize the custom exception.

        Args:
            message (str, optional): The error message. Defaults to None.
        """
        if message:
            super().__init__(message if message else self.default_message)