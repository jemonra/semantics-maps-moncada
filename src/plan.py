
import argparse
import json
import os

from dotenv import load_dotenv

from llm.llm_service import LLMService
from llm.openai_provider import OpenAIProvider
from prompt.planner_prompt import PlannerPrompt
from utils.file_utils import load_json


def print_llm_response(llm: LLMService, response: str):
    print(f"[{llm.get_provider_name()}] {response}")


def main(args):

    # Load the .env file
    load_dotenv()

    # Get ChatGPT instance
    llm = OpenAIProvider(openai_api_key=os.getenv("OPENAI_API_KEY"),
                         model_name=OpenAIProvider.GPT_3_5_TURBO,
                         max_output_tokens=4096)

    # Load semantic map
    semantic_map = load_json(file_path=args.semantic_map_path)
    semantic_map_str = json.dumps(semantic_map)

    # Start conversation
    planner_prompt = PlannerPrompt()
    planner_prompt_text = planner_prompt.get_prompt_as_text(
        semantic_map_str=semantic_map_str)

    # First message
    planner_conversation_history, planner_response = llm.chat(
        planner_prompt_text, [], None)  # empty conversation_history
    print_llm_response(llm, planner_response)

    while (True):
        user_input = input("Input: ")

        # Get planner response
        planner_conversation_history, planner_response = llm.chat(initial_prompt_text=planner_prompt,
                                                                  conversation_history=planner_conversation_history,
                                                                  user_input=user_input)
        print("######### ORIGINAL RESPONSE #########")
        print_llm_response(llm, planner_response)

        # Self reflect the response
        self_reflection_response = llm.planner_self_reflect(semantic_map_str=semantic_map,
                                                            planner_response=planner_response)
        print("######### SELF-REFLECTION RESPONSE #########")
        print_llm_response(llm, self_reflection_response)

        # Correct the response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TODO: program description")

    parser.add_argument("--semantic-map-path",
                        "-s",
                        type=str,
                        required=True,
                        help="Path to the semantic map JSON")

    args = parser.parse_args()

    main(args)
