
from llm.gemini_provider import GoogleGeminiProvider

GOOGLE_GEMINI_CREDENTIALS_FILE_PATH = "./credentials/concept-graphs-moncada-a807e893ef12.json"
GOOGLE_GEMINI_PROJECT_ID = "concept-graphs-moncada"
GOOGLE_GEMINI_PROJECT_LOCATION = "us-central1"

if __name__ == "__main__":

    llm_service = GoogleGeminiProvider(credentials_file=GOOGLE_GEMINI_CREDENTIALS_FILE_PATH,
                                       project_id=GOOGLE_GEMINI_PROJECT_ID,
                                       project_location=GOOGLE_GEMINI_PROJECT_LOCATION,
                                       model_name=GoogleGeminiProvider.GEMINI_1_0_PRO_VISION)
    while True:
        prompt = input("Write a prompt!")
        print(llm_service.generate_text(prompt))
