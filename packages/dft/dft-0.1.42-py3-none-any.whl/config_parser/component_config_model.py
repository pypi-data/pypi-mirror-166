from config_parser.base_config_model import BaseConfigModel
from config_parser.component_details_config_models.component_relationship_config_model import \
    ComponentRelationshipConfigModel
from config_parser.component_details_config_models.input_component_config_model import InputComponentConfigModel
from config_parser.component_details_config_models.output_component_config_model import OutputComponentConfigModel
from config_parser.component_details_config_models.text_box_component_config_model import TextBoxComponentConfigModel
from config_parser.config_parser_enums.parameter_names import ParameterNames


class ComponentConfigModel(BaseConfigModel):
    def __init__(self, yaml_object: dict):
        super().__init__(yaml_object)
        self.supported_types = ["input", "chart", "output", "text_box"]
        self.available_sizes = ["xs", "s", "m", "l", "xl"]

    def get_optional_params(self):
        return {
            ParameterNames.relationships: self.set_relationships,
            ParameterNames.size: self.set_size
        }

    def get_required_params(self):
        return {
            ParameterNames.type: self.set_type,
            ParameterNames.component_config: self.set_component_config
        }

    def set_type(self, value):
        if value not in self.supported_types:
            raise ValueError("Unsupported component type")

        self.type = value

    def set_component_config(self, value):
        if self.type == "input":
            self.component_config = InputComponentConfigModel(value)
        if self.type == "chart" or self.type == "output":
            self.component_config = OutputComponentConfigModel(value)
        if self.type == "text_box":
            self.component_config = TextBoxComponentConfigModel(value)

    def set_relationships(self, value):
        if not isinstance(value, list):
            raise ValueError("Relationships must be a list")
        relationships = []
        for item in value:
            relationships.append(ComponentRelationshipConfigModel(item))
        self.relationships = relationships

    def set_size(self, value):
        if value not in self.available_sizes:
            raise ValueError("Unknown component size")
        self.size = value
