
# Standard imports
import os
import json
import importlib.util

from typing import Any, Annotated, Optional, Tuple, Dict

# Third party
from semantic_kernel.planners.basic_planner import Plan

# Internal imports
from app.application.models import SKOrchestratorConfig
from app.domain.services.orchestrator import OrchestratorPlanningService
from app.infrastructure.utils import custom_logs
from app.infrastructure.utils.initializer import get_kernel_router, load_question_updater_plugin
from app.infrastructure.modules.semantic_kernel_impl.custom_implementations.planner import CustomBasicPlanner
from app.infrastructure.common.entities import Question
from app.application.exceptions import OrchestratorNotInitialized
from app.domain.models import RequestQuestion


logger = custom_logs.getLogger("SKernelOrchestrator")


class SKernelOrchestrator(OrchestratorPlanningService):
    """
    Implementation of Orchestrator using semantic kernel.
    """
    config: Annotated[SKOrchestratorConfig, "Orchestrator configuration object"]
    name: Annotated[str, "Name that identifies the Orchestrator"] = "semantic_kernel"

    def __init__(self, config: Annotated[SKOrchestratorConfig, "Configuration for Orchestrator"]):
        super().__init__(config=config)

    async def initialize(self, config: Optional[SKOrchestratorConfig] = None, **kwargs) -> Any:
        """
        Make any initializations required
        """
        # If it has already been initialized and no other config is provided skip this step
        if not config and self.initialized:
            return

        config = config if config else self.config

        self.kernel = get_kernel_router(config.openai_api_key,
                                        org_id=config.org_id,
                                        service_id=config.planner_id,
                                        ai_model_id=config.openai_model_version)

        self._init_plugins()
        self.planner = CustomBasicPlanner(service_id=config.planner_id)
        self.initialized = True

    async def orchestrate(self, question: Annotated[RequestQuestion, "Question to answer"], **kwargs) -> Annotated[Dict[str, str], "Result of plan execution as response to the original question."]:
        """
        Perform orchestration based on input.

        raises:
            - OrchestratorNotInitialized
        """
        plan = await self._create_plan(question=question)
        result = await self._execute_plan(plan=plan, question=question)
        return result

    def _init_plugins(self):
        """
        Load plugins dinamicaly
        """
        self._load_native_plugins()
        self._load_prompt_plugins()

    def _load_prompt_plugins(self):
        """
        Load prompt plugins to the kernel
        """
        load_question_updater_plugin(kernel=self.kernel)
        
    def _load_native_plugins(self):
        """
        Load native function plugins.
        """
        plugin_directory = os.path.join("app", "infrastructure", "modules", self.config.plugins_path)

        for plugin_subdir in os.listdir(plugin_directory):
            plugin_path = os.path.join(plugin_directory, plugin_subdir)
            if os.path.isdir(plugin_path):  # Ensure it's a directory
                cls, cfg = self._load_plugin_and_config(plugin_path)
                if cls and cfg:
                    logger.debug(f"Successfully loaded {cls.__name__} and its config from {plugin_subdir}.")
                    self.kernel.import_plugin_from_object(cls(), plugin_name=cfg["plugin_name"], plugin_description=cfg["plugin_description"])

    def _load_plugin_and_config(self, plugin_dir: Annotated[str, "The directory path of the plugin."]) -> Tuple[Optional[Any], Optional[dict]]:
        """
        Dynamically loads a Python class and its corresponding config.json
        from a given plugin directory.

        Args:
        - plugin_dir: The directory path of the plugin.

        Returns:
        A tuple containing the loaded class (None if not found or error) and
        the loaded config dictionary (None if not found or error).
        """

        # Initialize return values
        loaded_class = None
        config = None

        # Define paths and check for file existence
        py_files = [f for f in os.listdir(plugin_dir) if f.endswith('.py') and not f.startswith('__')]
        config_path = os.path.join(plugin_dir, 'config.json')

        if not py_files or not os.path.exists(config_path):
            logger.debug(f"Skipping {plugin_dir}: does not contain both a Python file and config.json.")
            return loaded_class, config

        # Load the class from the first Python file found
        py_file = py_files[0]  # Assuming one Python file per plugin directory
        module_name = py_file[:-3]  # Strip .py extension

        try:
            module_path = os.path.join(plugin_dir, py_file)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, module_name):
                loaded_class = getattr(module, module_name)
            else:
                logger.warning(f"No class named {module_name} found in {py_file}.")
        except Exception as e:
            logger.warning(f"Could not load class from {py_file}: {e}")

        # Load the config.json file
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
        except Exception as e:
            logger.warning(f"Could not load config from {config_path}: {e}")

        return loaded_class, config
        
    async def _create_plan(self, question: Annotated[RequestQuestion, "Question to answer"]):
        """
        Creates a plan based on the given question.
        
        return: The plan to execute.

        raises:
            - OrchestratorNotInitialized
        """
        if self.planner:
            plan: Plan = await self.planner.create_plan(question.question, kernel=self.kernel)
        else:
            raise OrchestratorNotInitialized
        return plan

    async def _execute_plan(self, plan: Annotated[Plan, "Plan generated previously"],
                            question: Annotated[RequestQuestion, "Question to answer"]) -> Annotated[Dict[str, str], "Result of plan execution as response to the original question."]:
        """
        Executes a plan.

        return: The result of executing the plan.

        raises:
            - OrchestratorNotInitialized
        """
        if self.planner:
            result = await self.planner.execute_plan(plan=plan, kernel=self.kernel, question=question.question, **question.extra)
        else:
            raise OrchestratorNotInitialized
        return result
