from typing import Annotated, Union
from semantic_kernel.functions import kernel_function

from app.infrastructure.common.entities import Question


class InvoicesDB:

    def __init__(self):
        pass

    @kernel_function(
        description="Retrieve information about invoices and the users related to them.",
        name="get_invoices"
    )
    def get_invoices(self, question: Union[Annotated[str, "The input of the user"], Annotated[Question, "The input of the user"]]) -> Annotated[str, "List of invoices"]:
        data = question
        return f"requested invoices with question: {data}"

    @kernel_function(
        description="Execute write operations on invoices like update, upsert on inserts.",
        name="upsert_invoices"
    )
    def upsert_invoices(self, question: Union[Annotated[str, "The input of the user"], Annotated[Question, "The input of the user"]]) -> Annotated[str, "Boolean telling if the operations was successful"]:
        data = question
        return f"requested write operations on invoices with question: {data}"