import json
from abc import ABC, abstractmethod
from typing import List, Tuple

from PIL import Image

from prompt.caption_extraction_prompt import CaptionExtractionPrompt
from prompt.caption_refinement_prompt import CaptionRefinementPrompt
from prompt.planner_correction_prompt import PlannerCorrectionPrompt
from prompt.planner_self_reflection_prompt import PlannerSelfReflectionPrompt


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
    def generate_text(self, prompt: str) -> Tuple[str, float]:
        """
        Abstract method to generate a text response based on the given prompt.

        Args:
            prompt (str): The input prompt string used to generate text.

        Returns:
            Tuple[str, float]: A tuple containing the generated text from the language model 
                               and the cost of the LLM call.
        """
        pass

    @abstractmethod
    def generate_text_with_images(self, prompt: str, pil_images: List[Image.Image]) -> Tuple[str, float]:
        """
        Abstract method to generate text using the LLM based on the provided prompt and images.

        Args:
            prompt (str): The input prompt string used to generate text.
            pil_images (List[str]): List of PIL images to be included in the prompt.

        Returns:
            Tuple[str, float]: A tuple containing the generated text from the language model 
                               and the cost of the LLM call.
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
        start_index = text.find("{")
        end_index = text.rfind("}") + 1

        if start_index != -1 and end_index != -1:
            return text[start_index:end_index]
        else:
            return ""

    def generate_json(self, prompt_text: str, max_attempts: int) -> Tuple[str, float]:
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
        Returns:
            Tuple[str, float]: A tuple containing the first valid JSON response as a string, or the last invalid response if
                               no valid response is generated; and the cost of all the LLM call.
        """
        total_cost = .0
        attempt = 1
        while attempt <= max_attempts:
            try:
                response, cost = self.generate_text(prompt_text)
                total_cost += cost

                # Clean response
                response = self._clean_response(response)
                # Try to parse response
                json.loads(response)

                return response, total_cost  # Return the valid JSON response

            except json.decoder.JSONDecodeError as e:
                self._info(
                    f"Error generating JSON on attempt {attempt}: {str(e)}")
                attempt += 1  # Increment attempt counter

        self._info("Couldn't get a valid JSON response, max attempts exceeded")
        # Returns the last response, potentially invalid if no valid JSON was generated
        return "", total_cost

    def generate_json_with_images(self, prompt_text: str, pil_images: List[Image.Image], max_attempts: int) -> Tuple[str, float]:
        """
        Attempts to generate a valid JSON response from a given text prompt and some images.

        This method repeatedly calls `generate_text_with_images` to generate responses based on the prompt text and
        provided images, then tries to parse and validate these responses as JSON. If a response fails to parse, it retries
        until it either succeeds or reaches the maximum number of attempts allowed.

        Parameters:
            prompt_text (str): The input text prompt used to generate the response.
            pil_images (List[Image.Image]): List of PIL images to be included in the generation process.
            max_attempts (int): The maximum number of attempts to generate a valid JSON response.

        Returns:
            Tuple[str, float]: A tuple containing the first valid JSON response as a string, or the last invalid response if
                               no valid response is generated; and the cost of all the LLM call.
        """
        attempt = 1
        total_cost = .0
        while attempt <= max_attempts:
            try:
                response, cost = self.generate_text_with_images(
                    prompt_text, pil_images)
                total_cost += cost

                # Clean response
                response = self._clean_response(response)
                # Try to parse response
                json.loads(response)
                return response, total_cost  # Return the valid JSON response

            except json.decoder.JSONDecodeError as e:
                self._info(
                    f"Error generating JSON on attempt {attempt}: {str(e)}")
                attempt += 1  # Increment attempt counter

            attempt += 1

        self._info("Couldn't get a valid JSON response, max attempts exceeded")
        return "", total_cost

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

    def planner_self_reflect(self, **prompt_data_dict):
        """
        TODO
        """
        prompt = PlannerSelfReflectionPrompt()
        prompt_text = prompt.get_prompt_as_text(**prompt_data_dict)
        return self.generate_text(prompt_text)

    def planner_correct(self, **prompt_data_dict):
        """
        TODO
        """
        prompt = PlannerCorrectionPrompt()
        prompt_text = prompt.get_prompt_as_text(**prompt_data_dict)
        return self.generate_json(prompt_text,
                                  max_attempts=self.JSON_MAX_ATTEMPTS)
