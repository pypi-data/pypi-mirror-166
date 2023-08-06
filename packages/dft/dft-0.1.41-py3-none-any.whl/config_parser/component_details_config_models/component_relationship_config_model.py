from config_parser.base_config_model import BaseConfigModel
from config_parser.component_details_config_models.component_relationship_contract_model import \
    ComponentRelationshipContractModel
from config_parser.config_parser_enums.parameter_names import ParameterNames


class ComponentRelationshipConfigModel(BaseConfigModel):

    def get_required_params(self):
        return {
            ParameterNames.name: self.set_name
        }

    def get_optional_params(self):
        return {
            ParameterNames.application: self.set_application,
            ParameterNames.relationship_contract: self.set_relationship_contract
        }

    def set_name(self, value):
        self.name = value

    def set_application(self, value):
        self.value = value

    def set_relationship_contract(self, value):
        self.relationship_contract = ComponentRelationshipContractModel(value)

