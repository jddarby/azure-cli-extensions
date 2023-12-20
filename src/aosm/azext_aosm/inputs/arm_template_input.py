import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from azext_aosm.inputs.base_input import BaseInput


@dataclass
class ArmTemplateInput(BaseInput):

    template_path: Path

    def get_defaults(self):
        if self.default_config:
            return self.default_config
        return {}

    def get_schema(self) -> Dict[str, Any]:
        # For ARM templates, the schema is defined by the parameters section
        base_arm_template_schema = r"""
        {
            "$schema": "https://json-schema.org/draft-07/schema#",
            "title": "armTemplateSchema",
            "type": "object",
            "properties": {},
            "required": []
        }
        """
        arm_template_schema = json.loads(base_arm_template_schema)

        with open(self.template_path, "r", encoding="utf-8") as _file:
            data = json.load(_file)

        if "parameters" in data:
            for key, value in data["parameters"].items():
                arm_template_schema["properties"][key] = {"type": value["type"]}
                if "defaultValue" not in value:
                    arm_template_schema["required"].append(key)
        else:
            print(
                "No parameters found in the template provided. "
                "Your NFD will have no deployParameters"
            )

        return arm_template_schema
