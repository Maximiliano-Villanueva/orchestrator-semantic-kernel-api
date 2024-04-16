# Standard imports
import copy

from abc import ABCMeta
from typing import Annotated, Optional, Dict, Any

# Internal imports
from app.infrastructure.common.entities import Plugin
from app.infrastructure.common.entities import Question
from app.infrastructure.modules.requester.requester import Requester
from app.infrastructure.utils import custom_logs


logger = custom_logs.getLogger('OrchestratorPlugin')


class PluginMeta(ABCMeta):
    """
    Metaclass that captures the class name of subclasses and is compatible with ABC.
    """
    def __new__(cls, name, bases, dct):
        dct['_class_name'] = name.lower()  # Store the class name in the class dictionary.
        return super().__new__(cls, name, bases, dct)


class OrchestratorPlugin(metaclass=PluginMeta):
    """
    Abstract base class for orchestrator plugins, using PluginMeta.
    """
    
    def get_plugin_conf(self, question: Annotated[Question, "The question object requested"]) -> Annotated[Plugin, "The configuration for the plugin"]:
        """
        Retrieve the configuration for the plugin, looking for a plugin
        whose name matches this class's name.
        """
        plugin_name = self._class_name.lower()
        for plugin in question.plugins:
            if plugin.name.lower() == plugin_name:
                return plugin
        return None

    def send_request_plugin(self, question: Annotated[Question, "List the incidences"], headers: Optional[Annotated[dict, "Headers for the request"]] = {}) -> Annotated[Dict[Any, Any], "Response from microservice"]:
        """
        Default request to all microservices
        """

        plugin_conf: Plugin = self.get_plugin_conf(question)
        formated_question = copy.deepcopy(question)
        formated_question.plugins = [plugin_conf]

        url = plugin_conf.url
        
        logger.debug(f"requesting to{url}, with data: {question.model_dump_json()}")
        result = Requester.post(url=url, data=formated_question.model_dump_json(), headers=headers, is_json=False)
        if result.status_code != 200:
            return {"detail": result.reason, "status_code": result.status_code, "text": result.text}
        return result.json()