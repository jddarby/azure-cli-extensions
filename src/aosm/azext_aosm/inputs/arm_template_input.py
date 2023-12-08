from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any, Dict

from azext_aosm.inputs.base_input import BaseInput
@dataclass
class ArmTemplateInput(BaseInput):

    template_path: Path

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
