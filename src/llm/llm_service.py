import json
import os
from abc import ABC, abstractmethod
from typing import List

from PIL import Image

from prompt.caption_extraction_prompt import CaptionExtractionPrompt
from prompt.caption_refinement_prompt import CaptionRefinementPrompt


class LLMService(ABC):

    JSON_MAX_ATTEMPTS = 10

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Abstract method to get the name of the LLM service provider.

        Returns:
            str: The name of the LLM service provider.
        """
        pass

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """
        Abstract method to generate a text response based on the given prompt.

        Args:
            prompt (str): The input prompt string used to generate text.

        Returns:
            str: The generated text from the language model.
        """
        pass

    @abstractmethod
    def generate_text_with_images(self, prompt: str, pil_images: List[Image.Image]) -> str:
        """
        Abstract method to generate text using the LLM based on the provided prompt and images.

        Args:
            prompt (str): The input prompt string used to generate text.
            pil_images (List[str]): List of PIL images to be included in the prompt.

        Returns:
            str: The generated text from the model.
        """
        pass

    def _info(self, message: str):
        """
        Prints an informational message prefixed with the provider name.

        Args:
            message (str): The message to be printed.

        Returns:
            None
        """
        print(f"[{self.get_provider_name()}] {message}")

    def _clean_response(self, text: str) -> str:
        """
        Extract the JSON-like portion from the model's response by finding the text
        between the first occurrence of "{ " and the last occurrence of "}".

        Args:
            text (str): The text containing the model's response.

        Returns:
            str: The extracted text that is likely in JSON format.
        """
        # Remove backticks, "json" at the start and end
        start_index = text.find("{")
        # Include the closing bracket in the substring
        end_index = text.rfind("}") + 1

        # Extract and return the substring between these indicess
        if start_index != -1 and end_index != -1:
            return text[start_index:end_index]
        else:
            return ""

    def generate_json(self, prompt_text: str, max_attempts: int) -> str:
        """
        Attempts to generate a valid JSON response from a given text prompt.

        This method repeatedly calls `generate_text` to generate responses based on the prompt text,
        then tries to parse and validate these responses as JSON. If a response fails to parse, it retries
        until it either succeeds or reaches the maximum number of attempts allowed.

        Args:
            prompt_text (str): The input text prompt used to generate the response.
            max_attempts (int): The maximum number of attempts to generate a valid JSON response.

        Returns:
            str: The first valid JSON response as a string, or the last invalid response if no valid response is generated.
        """
        attempt = 1
        while attempt <= max_attempts:
            try:
                response = self.generate_text(prompt_text)
                response = self._clean_response(response)
                json.loads(response)
                return response  # Return the valid JSON response

            except Exception as e:
                self._info(
                    f"Error generating JSON on attempt {attempt}: {str(e)}")
                attempt += 1  # Increment attempt counter

        self._info("Couldn't get a valid JSON response, max attempts exceeded")
        return ""

    def generate_json_with_images(self, prompt_text: str, pil_images: List[Image.Image], max_attempts: int) -> str:
        """
        Attempts to generate a valid JSON response from a given text prompt and associated image paths.

        This method repeatedly calls `generate_text_with_images` to generate responses based on the prompt text and
        provided images, then tries to parse and validate these responses as JSON. If a response fails to parse, it retries
        until it either succeeds or reaches the maximum number of attempts allowed.

        Parameters:
            prompt_text (str): The input text prompt used to generate the response.
            pil_images (List[Image.Image]): List of PIL images to be included in the generation process.
            max_attempts (int): The maximum number of attempts to generate a valid JSON response.

        Returns:
            str: The first valid JSON response as a string, or the last invalid response if no valid response is generated.
        """
        attempt = 1
        while attempt <= max_attempts:
            try:
                response = self.generate_text_with_images(
                    prompt_text, pil_images)
                response = self._clean_response(response)
                json.loads(response)
                return response  # Return the valid JSON response

            except Exception as e:
                self._info(
                    f"Error generating JSON on attempt {attempt}: {str(e)}")
                attempt += 1  # Increment attempt counter

            attempt += 1

        self._info("Couldn't get a valid JSON response, max attempts exceeded")
        return ""

    def extract_captions(self, images):
        """
        TODO
        """

        prompt = CaptionExtractionPrompt()
        prompt_text = prompt.get_prompt_as_text()

        return self.generate_text_with_images(prompt=prompt_text,
                                              pil_images=images)

    def refine_captions(self, captions_dict_str):
        """
        TODO
        """

        prompt = CaptionRefinementPrompt()
        prompt_text = prompt.get_prompt_as_text(captions_dict_str)

        return self.generate_json(prompt_text,
                                  max_attempts=self.JSON_MAX_ATTEMPTS)
