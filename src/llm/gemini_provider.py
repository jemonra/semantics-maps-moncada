import io
from typing import List, Tuple

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
    _COST_PER_INPUT_CHAR = "price_per_input_char"
    _COST_PER_OUTPUT_CHAR = "price_per_output_char"
    _COST_PER_INPUT_IMAGE = "price_per_input_image"

    MODEL_PARAMETERS = {
        GEMINI_1_0_PRO: {
            _MAX_INPUT_TOKENS: 30720,
            _MAX_OUTPUT_TOKENS: 2048,
            _IS_VISION: False,
            _COST_PER_INPUT_CHAR: 0.000000125,
            _COST_PER_OUTPUT_CHAR: 0.000000375
        },
        GEMINI_1_0_PRO_VISION: {
            _MAX_INPUT_TOKENS: 12288,
            _MAX_OUTPUT_TOKENS: 4096,
            _IS_VISION: True,
            _COST_PER_INPUT_CHAR: 0.000000125,
            _COST_PER_OUTPUT_CHAR: 0.000000375,
            _COST_PER_INPUT_IMAGE: 0.0025
        },
        GEMINI_1_5_PRO: {
            _MAX_INPUT_TOKENS: 1048576,
            _MAX_OUTPUT_TOKENS: 8192,
            _IS_VISION: False,
            _COST_PER_INPUT_CHAR: 0.00000125,
            _COST_PER_OUTPUT_CHAR: 0.00000375,
            # TODO: is this model a vision model?
        }
    }

    def __init__(self, credentials_file: str, project_id: str, project_location: str, model_name: str):
        """
        Initialize the GoogleGeminiProvider with the specified credentials, project ID, project location, and model name.

        Args:
            credentials_file (str): Path to the service account credentials file.
            project_id (str): Google Cloud project ID.
            project_location (str): Google Cloud project location.
            model_name (str): Name of the model to be used.
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

    def get_max_input_tokens(self) -> int:
        """
        Retrieve the maximum number of input tokens allowed for the current model.
        """
        return self.MODEL_PARAMETERS[self.model_name][self._MAX_INPUT_TOKENS]

    def get_max_output_tokens(self) -> int:
        """
        Retrieve the maximum number of output tokens allowed for the current model.
        """
        return self.MODEL_PARAMETERS[self.model_name][self._MAX_OUTPUT_TOKENS]

    def is_vision(self) -> bool:
        """
        Determine if the current model supports vision features.
        """
        return self.MODEL_PARAMETERS[self.model_name][self._IS_VISION]

    def get_cost_per_input_char(self) -> float:
        """
        Retrieve the cost per input character for the current model.
        """
        return self.MODEL_PARAMETERS[self.model_name][self._COST_PER_INPUT_CHAR]

    def get_cost_per_output_char(self) -> float:
        """
        Retrieve the cost per output character for the current model.
        """
        return self.MODEL_PARAMETERS[self.model_name][self._COST_PER_OUTPUT_CHAR]

    def get_cost_per_input_image(self) -> float:
        """
        Retrieve the cost per input image for the current model.
        """
        return self.MODEL_PARAMETERS[self.model_name][self._COST_PER_INPUT_IMAGE]

    def get_provider_name(self) -> str:
        return f"Google_{self.model_name}"

    def count_tokens(self, prompt: str) -> int:
        """
        Counts the number of tokens at a prompt
        """
        return self.model.count_tokens(prompt).total_tokens

    def trim_prompt(self, prompt: str):
        """
        Trims the given prompt to fit within the maximum allowed input tokens.

        This method iteratively reduces the length of the prompt until the number of tokens
        is within the acceptable limit defined by the Gemini API.

        Args:
            prompt (str): The input prompt string to be trimmed.

        Returns:
            str: The trimmed prompt string that fits within the maximum allowed input tokens.
        """
        new_prompt = prompt

        n_token = self.count_tokens(new_prompt)
        while n_token > self.get_max_input_tokens():

            n_extra_tokens = n_token - self.get_max_input_tokens()
            n_extra_characters = 15 + n_extra_tokens * 4
            self._info(
                f"Prompt too long({n_token} t, {len(new_prompt)} c), removing {n_extra_tokens} t {n_extra_characters} c")
            # Delete extra tokens (1 token = 4 characters)
            new_prompt = new_prompt[:-n_extra_characters]
            n_token = self.count_tokens(new_prompt)

        return new_prompt

    def calculate_cost(self, input: str, output: str, images: list) -> float:
        """
        Calculates the total cost of the LLM call based on the input text, output text, and number of images.

        Args:
            input (str): The input text string.
            output (str): The output text string generated by the LLM.
            images (list): A list of images associated with the LLM call.

        Returns:
            float: The total cost of the LLM call.
        """
        if self.is_vision():
            images_cost = len(images) * self.get_cost_per_input_image()
        else:
            images_cost = 0
        return len(input) * self.get_cost_per_input_char() + \
            len(output) * self.get_cost_per_output_char() + \
            images_cost

    def generate_text(self, prompt: str) -> Tuple[str, float]:
        prompt = self.trim_prompt(prompt)
        response = self.model.generate_content(prompt)
        try:
            response_text = response.candidates[0].content.parts[0].text
        # VertexAI bug running on conda (https://github.com/googleapis/python-aiplatform/issues/3129)
        except TypeError:
            response_text = response.candidates[0].content.parts[0]._raw_part.text

        response_cost = self.calculate_cost(input=prompt,
                                            output=response_text,
                                            images=[])
        print(f"cost: {response_cost}$")

        return response_text, response_cost

    def pil_image_to_gemini_image(self, pil_image: PILImage.Image) -> GeminiImage:
        """
        Convert a PIL Image to a Gemini Image.

        Args:
            pil_image (PILImage.Image): A PIL Image object to be converted.

        Returns:
            GeminiImage: The converted Gemini Image object.
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
        if not self.is_vision():
            raise NotImplementedError(
                f"Model {self.model_name} does not accept images")

        prompt = self.trim_prompt(prompt)
        combined_prompt = [prompt]

        pil_images = pil_images[:16]  # API limit to 16 images

        for image in pil_images:
            image = self.pil_image_to_gemini_image(image)
            combined_prompt.append(image)

        response = self.model.generate_content(combined_prompt)
        try:
            response_text = response.candidates[0].content.parts[0].text
        # VertexAI bug running on conda (https://github.com/googleapis/python-aiplatform/issues/3129)
        except TypeError:
            response_text = response.candidates[0].content.parts[0]._raw_part.text

        response_cost = self.calculate_cost(input=prompt,
                                            output=response_text,
                                            images=pil_images)
        print(f"cost: {response_cost}$")

        return response_text, response_cost
