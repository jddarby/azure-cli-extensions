from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any, Dict, Optional

from .base_input_artifact import BaseInputArtifact

@dataclass
class ArmTemplateInputArtifact(BaseInputArtifact):

    def get_defaults(self):
        return self.default_config

    def get_schema(self) -> Dict[str, Any]:
        # For ARM templates, the schema is defined by the parameters section
        with open(self.artifact_path, "r", encoding="utf-8") as _file:
            data = json.load(_file)
            if "parameters" in data:
                parameters: Dict[str, Any] = data["parameters"]
            else:
                print(
                    "No parameters found in the template provided. "
                    "Your NFD will have no deployParameters"
                )
                parameters = {}

        return parameters
