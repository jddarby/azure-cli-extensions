from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseInput(ABC):
    """
    Base class for all inputs.

    :param artifact_name: The name of the artifact.
    :type artifact_name: str
    :param artifact_version: The version of the artifact.
    :type artifact_version: str
    :param default_config_path: The path to the default configuration file for the input. Defaults to None.
    :type default_config_path: Optional[str]
    """

    def __init__(
        self,
        artifact_name: str,
        artifact_version: str,
        default_config_path: Optional[str] = None,
    ):
        self.artifact_name = artifact_name
        self.artifact_version = artifact_version
        self.default_config_path = default_config_path

    @abstractmethod
    def get_defaults(self) -> Dict[str, Any]:
        """
        Abstract method to get the default values for the input.

        :return: A dictionary containing the default values.
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """
        Abstract method to get the schema for the input.

        :return: A dictionary containing the schema.
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError
