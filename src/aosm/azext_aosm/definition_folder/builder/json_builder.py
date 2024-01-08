from pathlib import Path
from azext_aosm.definition_folder.builder.base_builder import (
    BaseDefinitionElementBuilder,
)


class JSONDefinitionElementBuilder(BaseDefinitionElementBuilder):
    """Bicep definition element builder."""

    json_content: str

    def __init__(
        self, path: Path, json_content: str, only_delete_on_clean: bool = False
    ):
        super().__init__(path, only_delete_on_clean)
        self.json_content = json_content

    def write(self):
        """Write the definition element to disk."""
        self.path.mkdir(exist_ok=True)
        (self.path / "common_deploy.parameters.json").write_text(self.json_content)
