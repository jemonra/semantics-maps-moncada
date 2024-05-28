
from abc import ABC, abstractmethod


class ClassicalPrompt(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_prompt_template(self):
        pass

    def get_prompt_as_text(self, **prompt_data_dict):

        prompt_text = self.get_prompt_template()

        # Substitute keys in prompt_data_dict
        for key in prompt_data_dict:
            prompt_text = prompt_text.replace(
                "{{"+key+"}}", prompt_data_dict[key])

        # print("prompt_text:", prompt_text)
        return prompt_text
