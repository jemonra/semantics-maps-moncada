import io
from typing import List

import google.cloud.aiplatform as aiplatform
import google.oauth2.service_account
from PIL import Image as PILImage
from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview.generative_models import Image as GeminiImage

from llm.llm_service import LLMService


class GoogleGeminiProvider(LLMService):

    GEMINI_1_0_PRO = "gemini-1.0-pro"
    GEMINI_1_0_PRO_VISION = "gemini-1.0-pro-vision"
    GEMINI_1_5_PRO = "gemini-1.5-pro-preview-0409"

    _MAX_INPUT_TOKENS = "max_input_tokens"
    _MAX_OUTPUT_TOKENS = "max_output_tokens"
    _IS_VISION = "is_vision"

    MODEL_PARAMETERS = {
        GEMINI_1_0_PRO: {
            _MAX_INPUT_TOKENS: 30720,
            _MAX_OUTPUT_TOKENS: 2048,
            _IS_VISION: False
        },
        GEMINI_1_0_PRO_VISION: {
            _MAX_INPUT_TOKENS: 12288,
            _MAX_OUTPUT_TOKENS: 4096,
            _IS_VISION: True
        },
        GEMINI_1_5_PRO: {
            _MAX_INPUT_TOKENS: 1048576,
            _MAX_OUTPUT_TOKENS: 8192,
            _IS_VISION: False
        }
    }

    def __init__(self, credentials_file: str, project_id: str, project_location: str, model_name: str, ):
        """
        TODO
        """
        credentials = (
            google.oauth2.service_account.Credentials.from_service_account_file(
                filename=credentials_file
            )
        )
        aiplatform.init(project=project_id,
                        location=project_location,
                        credentials=credentials)

        self.model_name = model_name
        self.model = GenerativeModel(model_name=model_name)

    def get_max_input_tokens(self):
        """
        Retrieve the maximum number of input tokens allowed for the current model.
        """
        return self.MODEL_PARAMETERS[self.model_name][self._MAX_INPUT_TOKENS]

    def get_max_output_tokens(self):
        """
        Retrieve the maximum number of output tokens allowed for the current model.
        """
        return self.MODEL_PARAMETERS[self.model_name][self._MAX_OUTPUT_TOKENS]

    def is_vision(self):
        """
        Determine if the current model supports vision features.
        """
        return self.MODEL_PARAMETERS[self.model_name][self._IS_VISION]

    def get_provider_name(self) -> str:
        """
        TODO
        """
        return f"Google_{self.model_name}"

    def count_tokens(self, prompt: str) -> int:
        """
        TODO
        """
        n_tokens = self.model.count_tokens(prompt).total_tokens
        print(n_tokens)
        return n_tokens

    def trim_prompt(self, prompt: str) -> str:
        """
        TODO
        """
        new_prompt = prompt

        n_token = self.count_tokens(new_prompt)
        while n_token > self.get_max_input_tokens():

            n_extra_tokens = n_token - self.get_max_input_tokens()
            n_extra_characters = 15 + n_extra_tokens * 4
            self._info(
                f"Prompt too long({n_token} t, {len(new_prompt)} c), removing {n_extra_tokens} t {n_extra_characters} c"
            )
            # Delete extra tokens (1 token = 4 characters)
            new_prompt = new_prompt[:-n_extra_characters]
            n_token = self.count_tokens(new_prompt)

        return new_prompt

    def generate_text(self, prompt: str) -> str:
        """
        TODO
        """
        prompt = self.trim_prompt(prompt)
        response = self.model.generate_content(prompt)
        response = response.candidates[0].content.parts[0].text
        return response

    def pil_image_to_gemini_image(self, pil_image: PILImage.Image):
        """
        TODO
        """
        # Create a bytes buffer
        img_byte_arr = io.BytesIO()

        # Save PIL image to bytes buffer in PNG format (or JPEG if preferred)
        pil_image.save(img_byte_arr, format='PNG')

        # Get the bytes data from the buffer
        img_bytes = img_byte_arr.getvalue()

        # Create a Gemini Image object using the bytes data
        return GeminiImage.from_bytes(img_bytes)

    def generate_text_with_images(self, prompt: str, pil_images: List[PILImage.Image]) -> str:
        """
        TODO
        """
        if not self.is_vision():
            raise NotImplementedError(
                f"Model {self.model_name} doesn't accept images")

        prompt = self.trim_prompt(prompt)
        combined_prompt = [prompt]
        for image in pil_images[:16]:  # API limit to 16 images

            image = self.pil_image_to_gemini_image(image)
            combined_prompt.append(image)
        response = self.model.generate_content(combined_prompt)
        try:
            response_text = response.candidates[0].content.parts[0].text
        # VertexAI bug running on conda (https://github.com/googleapis/python-aiplatform/issues/3129)
        except TypeError:
            response_text = response.candidates[0].content.parts[0]._raw_part.text

        return response_text
