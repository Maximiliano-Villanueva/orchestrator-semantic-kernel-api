# Standard imports
import inspect

from typing import Union, Any, Dict

# Third party
import semantic_kernel as sk

from semantic_kernel.functions.kernel_plugin import KernelPlugin
from semantic_kernel.exceptions import PluginInvalidNameError, FunctionNameNotUniqueError
from semantic_kernel.functions.kernel_function import KernelFunction
from semantic_kernel.functions.kernel_function_from_method import KernelFunctionFromMethod

from semantic_kernel.connectors.openai_plugin.openai_function_execution_parameters import (
    OpenAIFunctionExecutionParameters,
)

# Internal imports
from app.infrastructure.utils import custom_logs


logger = custom_logs.getLogger(__name__)


class CustomKernel(sk.Kernel):
    def import_plugin_from_object(self, plugin_instance: Union[Any, Dict[str, Any]], plugin_name: str, plugin_description: str = "") -> KernelPlugin:
        """
        Creates a plugin that wraps the specified target object and imports it into the kernel's plugin collection

        Args:
            plugin_instance (Any | Dict[str, Any]): The plugin instance. This can be a custom class or a
                dictionary of classes that contains methods with the kernel_function decorator for one or
                several methods. See `TextMemoryPlugin` as an example.
            plugin_name (str): The name of the plugin. Allows chars: upper, lower ASCII and underscores.

        Returns:
            KernelPlugin: The imported plugin of type KernelPlugin.
        """
        if not plugin_name.strip():
            raise PluginInvalidNameError("Plugin name cannot be empty")
        logger.debug(f"Importing plugin {plugin_name}")

        functions: Dict[str, KernelFunction] = {}

        if isinstance(plugin_instance, dict):
            candidates = plugin_instance.items()
        else:
            candidates = inspect.getmembers(plugin_instance, inspect.ismethod)
        # Read every method from the plugin instance
        for _, candidate in candidates:
            # If the method is a prompt function, register it
            if not hasattr(candidate, "__kernel_function__"):
                continue

            func = KernelFunctionFromMethod(plugin_name=plugin_name, method=candidate)
            if func.name in functions:
                raise FunctionNameNotUniqueError(
                    "Overloaded functions are not supported, " "please differentiate function names."
                )
            functions[func.name] = func
        logger.debug(f"Methods imported: {len(functions)}")

        plugin = KernelPlugin(name=plugin_name, functions=functions, description=plugin_description)
        self.plugins.add(plugin)

        return plugin
    
    async def import_plugin_from_openai(
        self,
        plugin_name: str,
        plugin_description: str,
        plugin_url: str | None = None,
        plugin_str: str | None = None,
        execution_parameters: OpenAIFunctionExecutionParameters | None = None,
    ) -> KernelPlugin:
        plugin: KernelPlugin = await super().import_plugin_from_openai(plugin_name, plugin_url, plugin_str, execution_parameters)
        plugin.description = plugin_description

        return plugin
