from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any, Dict, Optional

from .base_input_artifact import BaseInputArtifact

@dataclass
class ArmTemplateInputArtifact(BaseInputArtifact):

    template_path: Path
    defaults_path: Optional[Path] = None

    def get_defaults(self):
        # TODO: Implement this
        pass

    def get_schema(self) -> Dict[str, Any]:
        # For ARM templates, the schema is defined by the parameters section
        with open(self.template_path, "r", encoding="utf-8") as _file:
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
