from app.infrastructure.modules.semantic_kernel_impl.plugins.Rag.Rag import Rag
from app.infrastructure.common.entities.question import Question

import pytest
from unittest.mock import patch

from app.infrastructure.modules.requester.requester import Requester

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
    headers = {"test-header": "test-value"}
    questions = [Question(**json_data)]

    return questions, [headers]*len(questions)

questions, headers = create_dummy_questions()
print(headers)

plugin = Rag()
parametrization_data_rag = [(questions[i], headers[i], plugin.ask_rag) for i in range(len(questions))]


@pytest.mark.parametrize(
    "question, headers, plugin_func",
    parametrization_data_rag,
)
@pytest.mark.asyncio
async def test_plugin_request(question, headers, plugin_func):
    """
    Test plans genereated
    """
    expected_response = {"answer": "test answer", "context": ["test context"]}
    class DummyOutput:
        
        output = expected_response

        def json(self):
            return self.output

    response = plugin_func(question, headers)

    with patch('app.infrastructure.modules.requester.requester.Requester.post', return_value=DummyOutput()) as mock_post:
        response = plugin_func(question, headers)
        print("--------------------------------------")
        print("--------------------------------------")
        print("--------------------------------------")
        print(response)
        print("--------------------------------------")
        print("--------------------------------------")
        print("--------------------------------------")
        mock_post.assert_called_once()  # Optional, ensures the post method was called once.
        assert response == expected_response
