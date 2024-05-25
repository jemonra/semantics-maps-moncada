class CaptionRefinementPrompt:

    SYSTEM_PROMPT = """Identify and describe objects in scenes. 
    Input and output must be in JSON format. 
    The input field 'captions' contains a list of image captions aiming to identify objects. 
    Output 'summary' as a concise description of the identified object(s). 
    An object mentioned multiple times is likely accurate. If various objects are repeated and a container/surface is noted such as a shelf or table, assume the (repeated) objects are on that container/surface. 
    For unrelated, non-repeating (or empty) captions, summarize as 'conflicting (or empty) captions about [objects]' and set 'object_tag' to 'invalid'. 
    Output 'possible_tags' listing potential object categories. 
    Set 'object_tag' as the conclusive identification. 
    Focus on indoor object types, as the input captions are from indoor scans."""

    EXAMPLE_1 = """
        "id": 1,
        "captions": [
        "a jacket hanging on a wall, either on a hook or a rack.",
        "a jacket, which is hanging on a wall or a rack.",
        "a jacket, which is either being worn or draped over a person's shoulders.",
        "a sweater, which is hanging on a clothes hanger.",
        "a hooded jacket, which is either hanging on a hook or draped over a shower rail.",
        "a mannequin, which is wearing a yellow shirt and a red jacket.",
        "a jacket, which is hanging on a hook or a rack.",
        "a hooded sweatshirt, which is either being held by someone or hanging on a hook or a rack.",
        "a hanger with a yellow and black jacket hanging on it.",
        "a yellow and black striped umbrella.",
        "a hanging coat, which is either yellow or red depending on the specific description.",
        "a cat.",
        "a person wearing a yellow and red jacket."
        ]
        }"
        """

    RESPONSE_1 = """{
        "summary": "a jacket hanging on a rack",
        "possible_tags": ["jacket", "sweater", "hooded jacket", "hooded sweatshirt", "coat", "hanging clothing", "hanger", "wall", "rack"],
        "object_tag": "hanging jacket"
        }"""

    EXAMPLE_2 = """{
        "id": 12,
        "captions": [
        "a bookshelf filled with books",
        "a bicycle helmet"
        ]
        }"""

    RESPONSE_2 = """{
        "summary": "conflicting captions of a bookshelf and a bicycle helmet",
        "possible_tags": ["bookshelf", "bicycle helmet", "helmet", "bookcase", "book", "books", "shelf", "shelves"],
        "object_tag": "invalid"
        }"""

    EXAMPLE_3 = """{
        "id": 304,
        "captions": [
        "a pair of scissors.",
        "a sewing machine.",
        "a white shelf or rack, which is filled with various boxes and files.",
        "a white shelf or bookshelf that is filled with various items."
        ]
        }"""

    RESPONSE_3 = """{
        "summary": "a white shelf or rack filled with various items",
        "possible_tags": ["shelf", "rack", "bookshelf", "bookcase", "box", "file", "scissors", "sewing machine"],
        "object_tag": "shelf"
        }"""

    EXAMPLE_4 = """{
        "id": 433,
        "captions": [
        "a white toilet.",
        "a pile of various exercise equipment, including a set of tennis balls.",
        "a white table.",
        "a barbell.",
        "a microwave.",
        "a tall, thin black bottle.",
        "a barbell, which is situated on a table.",
        "a pile of various exercise equipment, including a bench, situated in a room with desks and a whiteboard.",
        "a tall vase or pitcher.",
        "a tennis ball.",
        "a shirt with a space design on it.",
        "a tennis ball.",
        "a gray shirt with the NASA logo on it."
        ]
        }"""

    RESPONSE_4 = """{
        "summary": "a white table containing a barbell and possibly with some other exercise equipment",
        "possible_tags": ["exercise equipment", "tennis ball", "barbell", "bench", "table", "microwave", "bottle", "vase", "pitcher", "shirt"],
        "object_tag": "white table"
        }"""

    EXAMPLE_5 = """{
        "id": 231,
        "captions": [
            "a teddy bear.",
            "a doorknob.",
            "a television set.",
            "a laptop computer."
        ]
        }"""

    RESPONSE_5 = """{
        "summary": "conflicting captions of a teddy bear, a doorknob, a television set, and a laptop computer",
        "possible_tags": ["teddy bear", "doorknob", "television set", "laptop computer", "computer"],
        "object_tag": "invalid"
        }"""

    def __init__(self):
        self.system_prompt = self.SYSTEM_PROMPT
        self.examples = list()
        self.examples.append((self.EXAMPLE_1, self.RESPONSE_1))
        self.examples.append((self.EXAMPLE_2, self.RESPONSE_2))
        self.examples.append((self.EXAMPLE_3, self.RESPONSE_3))
        self.examples.append((self.EXAMPLE_4, self.RESPONSE_4))
        self.examples.append((self.EXAMPLE_5, self.RESPONSE_5))

    def get_prompt_as_text(self, captions_dict_str):

        # Include instruction
        prompt_text = f"### INSTRUCTION ###\n{self.system_prompt}\n"
        prompt_text += "Examples of the whole process are provided below\n"

        # Include examples
        for example_idx, (example, response) in enumerate(self.examples):
            prompt_text += f"## EXAMPLE {example_idx} INPUT ##\n{example}\n"
            prompt_text += f"## EXAMPLE {example_idx} OUTPUT ##\n{response}\n"

        # Include input
        prompt_text += f"### REAL INPUT ###\n{captions_dict_str}\n"

        return prompt_text
