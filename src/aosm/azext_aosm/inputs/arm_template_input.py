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
            self._generate_schema_from_params(arm_template_schema, data["parameters"])
        else:
            print(
                "No parameters found in the template provided. "
                "Your NFD will have no deployParameters"
            )

        return arm_template_schema

    def _generate_schema_from_params(
        self, schema: Dict[str, Any], parameters: Dict[str, Any]
    ) -> None:
        """Generate the schema from the parameters."""
        for key, value in parameters.items():
            if "defaultValue" not in value:
                schema["required"].append(key)
            if value["type"] in ("object", "secureObject"):
                schema["properties"][key] = {
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
                if "properties" in value:
                    self._generate_schema_from_params(
                        schema["properties"][key], value["properties"]
                    )
            else:
                schema["properties"][key] = {"type": value["type"]}
