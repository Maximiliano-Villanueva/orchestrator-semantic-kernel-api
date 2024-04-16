from typing import Annotated, Dict, List
from semantic_kernel.functions import kernel_function

from app.infrastructure.common.entities import Question
from app.infrastructure.utils import custom_logs


logger = custom_logs.getLogger(__name__)


class Cities:

    def __init__(self):
        pass

    @kernel_function(
        description="Get the cities based on locations (for example countries or continents), population, etc..",
        name="get_cities"
    )
    def get_cities(self, filter: Annotated[Dict[str, str], "filters in dict format with the information to filter. Here are some examples {'population': 'max(population)', 'continent': 'Europe'}. {'population': '>5000'}"]) -> Annotated[List[str], "List of cities"]:
        logger.debug(f"requesting cities with filter {filter}")
        return ['Barcelona']
