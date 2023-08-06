from config_parser.base_config_model import BaseConfigModel
from config_parser.component_details_config_models.parameter_value_relationship_config_model import \
    ParameterValueRelationshipConfigModel
from config_parser.component_details_config_models.table_input_relationship_model import TableInputRelationshipModel
from config_parser.config_parser_enums.parameter_names import ParameterNames


class ComponentRelationshipContractModel(BaseConfigModel):

    def __init__(self, yaml_object: dict):
        super().__init__(yaml_object)
        self.available_type = ["chart_click", "table_input", "cell_input", "chart_data_input"]

    def get_optional_params(self):
        return {

        }

    def get_required_params(self):
        return {
            ParameterNames.type: self.set_type,
            ParameterNames.config: self.set_config
        }

    def set_type(self, value):
        if value not in self.available_type:
            raise ValueError("Relationship type unknown")

        self.type = value

    def set_config(self, value):
        if self.type == "chart_click" or self.type == "cell_input":
            self.config = ParameterValueRelationshipConfigModel(value)
        elif self.type == "table_input" or self.type == "chart_data_input":
            self.config = TableInputRelationshipModel(value)

