from config_parser.base_config_model import BaseConfigModel
from config_parser.config_parser_enums.parameter_names import ParameterNames


class TextBoxComponentConfigModel(BaseConfigModel):

    def get_optional_params(self):
        return {}

    def get_required_params(self):
        return {
            ParameterNames.text: self.set_text
        }

    def set_text(self, value):
        self.text = value
