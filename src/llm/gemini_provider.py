import io
from pathlib import Path
from typing import List

import google.cloud.aiplatform as aiplatform
import google.oauth2.service_account
from PIL import Image as PILImage
from vertexai.preview.generative_models import GenerativeModel, Image as GeminiImage

from llm.llm_service import LLMService


class GoogleGeminiProvider(LLMService):

    GEMINI_1_0_PRO = "gemini-1.0-pro"
    GEMINI_1_0_PRO_VISION = "gemini-1.0-pro"

    VISION_MODELS = (GEMINI_1_0_PRO_VISION,)

    def __init__(self, credentials_file: str, project_id: str, project_location: str, model_name: str):
        """
        TODO: create python docstrings
        """
        credentials = (
            google.oauth2.service_account.Credentials.from_service_account_file(
                filename=credentials_file
            )
        )
        aiplatform.init(project=project_id,
                        location=project_location, credentials=credentials)

        self.model_name = model_name
        self.model = GenerativeModel(
            model_name=model_name
        )

    def get_provider_name(self) -> str:
        return f"Google_{self.model_name}"

    def generate_text(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)

        try:
            response_text = response.candidates[0].content.parts[0].text
        # VertexAI bug running on conda (https://github.com/googleapis/python-aiplatform/issues/3129)
        except TypeError:
            response_text = response.candidates[0].content.parts[0]._raw_part.text
        return response_text

    def pil_image_to_gemini_image(pil_image: PILImage.Image):
        # Create a bytes buffer
        img_byte_arr = io.BytesIO()

        # Save PIL image to bytes buffer in PNG format (or JPEG if preferred)
        pil_image.save(img_byte_arr, format='PNG')

        # Get the bytes data from the buffer
        img_bytes = img_byte_arr.getvalue()

        # Create a Gemini Image object using the bytes data
        return GeminiImage(img_bytes)

    def generate_text_with_images(self, prompt: str, pil_images: List[PILImage.Image]) -> str:
        if self.model_name not in self.VISION_MODELS:
            raise NotImplementedError(
                f"Model {self.model_name} doesn't accept images")

        combined_prompt = [prompt]
        for image in pil_images[:16]:  # Limit to 16 images (API limit)

            image = self.pil_image_to_gemini_image(image)
            combined_prompt.append(image)
        response = self.model.generate_content(combined_prompt)
        try:
            response_text = response.candidates[0].content.parts[0].text
        # VertexAI bug running on conda (https://github.com/googleapis/python-aiplatform/issues/3129)
        except TypeError:
            response_text = response.candidates[0].content.parts[0]._raw_part.text

        return response_text
