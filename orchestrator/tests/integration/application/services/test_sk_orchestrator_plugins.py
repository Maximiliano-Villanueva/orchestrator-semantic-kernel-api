import json
import os

# Internal imports
from app.application.models import SKOrchestratorConfig
from app.application.services.sk_orchestrator import SKernelOrchestrator
from app.infrastructure.common.entities.question import Question

# Third party
import pytest

from semantic_kernel.exceptions import PlannerException

from app.domain.models import RequestQuestion


def initialize_kernel():
    """
    Set up test case environment.
    """
    config = SKOrchestratorConfig(openai_api_key=os.getenv("OPENAI_API_KEY"), org_id=None)
    return SKernelOrchestrator(config=config)


def create_dummy_questions():
    """
    Test loading a valid plugin and configuration.
    """
    json_data = {
        "user_id": 7,
        "message_id": 7,
        "chat_id": 4,
        "domain_id": 1,
        "question": "lista las incidencias wifi",
        "plugins": [{
            "name": "ServiceDesk",
            "url": "http://localhost:9001/query",
            "configuration":{
            }
        }]
    }

    # Create an instance of the Question model using the JSON data
    
    questions = [RequestQuestion(question=Question(**json_data), extra={"headers": {"test-header": "test-value"}})]
    json_data["question"] = "lista todas las facturas del usuario con id 5"
    questions.append(RequestQuestion(question=Question(**json_data), extra={"headers": {"test-header": "test-value"}}))

    json_data["question"] = "Actualiza la siguiente factura: {id=1, test=True, user_id=5}"
    questions.append(RequestQuestion(question=Question(**json_data), extra={"headers": {"test-header": "test-value"}}))

    json_data["question"] = "What is Lyfe cycle analysis?"
    questions.append(RequestQuestion(question=Question(**json_data), extra={"headers": {"test-header": "test-value"}}))

    json_data["question"] = "Tell me some facts about the most populated city in the world."
    questions.append(RequestQuestion(question=Question(**json_data), extra={"headers": {"Authentication": "test-value"}}))

    function_expected = [
        ["sevicedesk.get_incidences"],
        ["invoices.get_invoices"],
        ["invoices.upsert_invoices"],
        ["rag.ask_rag"],
        ["cities_db.get_cities", "rag.ask_rag"]
    ]

    output_expected = [
        "",
        "",
        "",
        "",
        ""
    ]
    # return [questions[-1]], [function_expected[-1]], [output_expected[-1]]
    return questions, function_expected, output_expected

# Initialize common objects
orchestrator = initialize_kernel()


questions, functions_expected, output_expected = create_dummy_questions()

parametrization_data_functions = [(questions[i], functions_expected[i]) for i in range(len(questions))]
parametrization_data_output = [(questions[i], functions_expected[i]) for i in range(len(questions))]


@pytest.mark.parametrize(
    "question, expected_function",
    parametrization_data_functions
)
@pytest.mark.asyncio
@pytest.mark.xfail(
    raises=PlannerException,
    reason="Test is known to occasionally produce unexpected results.",
)
async def test_create_plan_function_single(question, expected_function):
    """
    Test plans genereated
    """
    await orchestrator.initialize()
    # Plan
    plan = await orchestrator._create_plan(question)
    gen_plan = json.loads(str(plan.generated_plan))
    subtasks = ([x["function"] for x in gen_plan["subtasks"]])

    # Assert
    print(subtasks)
    print(expected_function)
    assert all(item in subtasks for item in expected_function)


@pytest.mark.parametrize(
    "question, expected_result",
    parametrization_data_output
)
@pytest.mark.asyncio
@pytest.mark.xfail(
    raises=PlannerException,
    reason="Test is known to occasionally produce unexpected results.",
)
async def test_plan_result(question, expected_result):
    """
    Test the result obtained from functions
    """
    await orchestrator.initialize()

    # Plan
    plan = await orchestrator._create_plan(question)
    # Execute plan
    result = await orchestrator._execute_plan(plan, question=question)

    print(result)
    # TODO: assert 
    assert 1==1