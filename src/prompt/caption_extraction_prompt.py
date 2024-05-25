
class CaptionExtractionPrompt:

    SYSTEM_PROMPT = "Describe with 2 or 3 sentences maximum the central element of the image"

    def get_prompt_as_text(self):
        return self.SYSTEM_PROMPT
