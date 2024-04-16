# Standard imports
import time
import logging

# Third-party imports
import requests
from typing import Any, Annotated, Type, Optional, Dict

from app.infrastructure.modules.observability import MethodObservability


class Requester(metaclass=MethodObservability):
    # TODO: turn this into a normal class for better testing.
    """
    A class to perform HTTP GET and POST requests.
    """
    @staticmethod
    def get(url: Annotated[str, "The URL to send the GET request to"], 
            headers: Annotated[Optional[Dict[str, str]], "Optional HTTP headers for the GET request"] = None) -> Annotated[requests.Response, "The response object from the GET request"]:
        """
        Sends a GET request to a specified URL with optional headers.

        Args:
            url (str): The URL to send the GET request to.
            headers (Optional[Dict[str, str]]): Optional HTTP headers for the GET request.

        Returns:
            requests.Response: The response object from the GET request.
        """
        return requests.get(url, headers=headers)

    @staticmethod
    def post(url: Annotated[str, "The URL to send the POST request to"], 
             data: Annotated[Dict[str, Any], "The data to send in the POST request"], 
             is_json: Annotated[Optional[bool], "Whether the data is sent as JSON"] = False, 
             headers: Annotated[Optional[Dict[str, str]], "Optional HTTP headers for the POST request"] = None) -> Annotated[requests.Response, "The response object from the POST request"]:
        """
        Sends a POST request to a specified URL with given data, with an option to send as JSON, and includes optional headers.

        Args:
            url (str): The URL to send the POST request to.
            data (Dict[str, Any]): The data to send in the POST request.
            is_json (Optional[bool]): Whether the data is sent as JSON.
            headers (Optional[Dict[str, str]]): Optional HTTP headers for the POST request.

        Returns:
            requests.Response: The response object from the POST request.
        """
        if is_json:
            return requests.post(url, json=data, headers=headers)
        else:
            return requests.post(url, data=data, headers=headers)