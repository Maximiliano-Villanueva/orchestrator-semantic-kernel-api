# Standard
from typing import Annotated, Dict, List, Optional

# Third party
from app.infrastructure.modules.semantic_kernel_impl.plugins.ServiceDesk.ServiceDesk import ServiceDesk
import semantic_kernel as sk

from semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import OpenAIChatCompletion
from semantic_kernel.functions.kernel_plugin import KernelPlugin
from semantic_kernel.prompt_template.input_variable import InputVariable

# Internal
from app.infrastructure.modules.semantic_kernel_impl.custom_implementations.kernel import CustomKernel


def get_kernel_router(api_key: Annotated[str, "OpenAI api key"],
                      org_id: Annotated[Optional[str], "org id"],
                      service_id: Annotated[Optional[str], "service id for the planner"],
                      ai_model_id: Annotated[Optional[str], "openai model version"]) -> Annotated[sk.Kernel, "Kernel instance"]:
    """
    Initialize the kernel for planning purposes.
    """

    kernel = CustomKernel()
   
    kernel.add_service(
        OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=ai_model_id,
            api_key=api_key,
        )
    )

    return kernel


def load_question_updater_plugin(kernel: Annotated[sk.Kernel, "kernel instance from semantic kernel"]) -> Annotated[List[KernelPlugin], "Hidden plugins loaded"]:
    """
    Load plugins that are meant to be used internaly
    """
    prompt = """
        I have the following Question:
        {{$question}}.

        And the following context:
        {{$previous_output}}

        I need you to return the same question updated based on the context provided.
        If the context is not useful return the same input question.
        Use only the information provided and nothing more.
        Do not include anything but the question generated in your response.

    """

    prompt_template_config = sk.PromptTemplateConfig(
        template=prompt,
        name="question_update",
        template_format="semantic-kernel",
        input_variables=[
            InputVariable(name="question", description="Question to update", is_required=True),
            InputVariable(name="previous_output", description="Output from last function", is_required=True)
        ],
    )

    question_updater = kernel.create_function_from_prompt(
        function_name="question_updater",
        plugin_name="question_updater",
        prompt_template_config=prompt_template_config,
    )

    return [question_updater]
