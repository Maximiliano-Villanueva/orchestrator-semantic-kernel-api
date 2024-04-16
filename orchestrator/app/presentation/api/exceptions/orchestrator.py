from typing import Optional


class InvalidOrchestrator(Exception):

    default_message: str = "Type of orchestrtor not allowed"

    def __init__(self, message: Optional[str] = None):
        """
        Initialize the custom exception.

        Args:
            message (str, optional): The error message. Defaults to None.
        """
        if message:
            super().__init__(message if message else self.default_message)


class InitializationError(Exception):
    default_message: str = "Something went wrong initializating the orchestrator. "

    def __init__(self, message: Optional[str] = None):
        """
        Initialize the custom exception.

        Args:
            message (str, optional): The error message. Defaults to None.
        """
        if message:
            super().__init__(message if message else self.default_message)


class OrchestratorReponseInvalid(Exception):
    default_message: str = "Unexpected answer from one or more sources."

    def __init__(self, message: Optional[str] = None):
        """
        Initialize the custom exception.

        Args:
            message (str, optional): The error message. Defaults to None.
        """
        if message:
            super().__init__(message if message else self.default_message)