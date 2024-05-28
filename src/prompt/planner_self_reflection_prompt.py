class PlannerSelfReflectionPrompt:

    PROMPT_TEMPLATE = """
    ### CONTEXT ###
    We have received a response from another LLM tasked with interpreting and answering questions about a 3D scene described in a JSON format. Your task is to reflect on this response, providing constructive feedback to help refine and improve it.

    The ORIGINAL INSTRUCTION was:
    The input to the model is a 3D scene described in a JSON format (### 3D SCENE ###). Each entry in the JSON describes one object in the scene, with the following five fields:

    "id": a unique object id
    "bbox_extent": extents of the 3D bounding box for the object
    "bbox_center": centroid of the 3D bounding box for the object
    "object_tag": a brief (but sometimes inaccurate) tag categorizing the object
    "caption": a brief caption for the object
    Once you have parsed the JSON and are ready to answer questions about the scene, say "I'm ready".

    The user will then begin to ask questions, and the task is to answer various user queries about the 3D scene. For each user question, respond with a JSON dictionary with the following fields:

    "inferred_query": your interpretation of the user query in a succinct form
    "relevant_objects": list of relevant object ids for the user query (if applicable)
    "query_achievable": whether or not the user specified query is achievable using the objects and descriptions provided in the 3D scene.
    "final_relevant_objects": A final list of objects relevant to the user-specified task. Sort all objects in this list such that the most relevant object is listed first, followed by the second most relevant, and so on.
    "explanation": A brief explanation of what the most relevant object(s) is(are), and how they achieve the user-specified task.
    
    The 3D SCENE was:
    {{semantic_map}}

    The ORIGINAL RESPONSE was:
    {{planner_response}}
    
    ### INSTRUCTION ###
    Your task is to:
    - Carefully review the original response for correctness, relevance, and clarity.
    - Provide constructive criticism, focusing on areas where the response could be improved.
    - Offer specific suggestions for how to refine the response, ensuring it better meets the requirements and addresses any potential issues.
    
    REFLECTION TASK
    Correctness:
    - Are the inferred query and relevant objects accurately identified?
    - Is the query achievable status appropriately determined?
    - Is the explanation logically sound and coherent?
    Relevance:
    - Are all relevant objects identified, and are they sorted by relevance accurately?
    - Are any crucial objects or details omitted?
    Clarity:
    - Is the response clear and easy to understand?
    - Are there any ambiguities or vague descriptions?
    
    CRITIQUE TEMPLATE
    Please review the response carefully for correctness, relevance, and clarity, and provide constructive criticism for how to improve it. Follow the structure provided below:

    Correctness:
    [Your comments on correctness]
    Relevance:
    [Your comments on relevance]
    Clarity:
    [Your comments on clarity]
    
    SUGGESTIONS FOR IMPROVEMENT
    Based on your critique, please suggest specific improvements. These can include corrections to factual errors, inclusion of missing relevant objects, reordering of objects by relevance, or clarifications to enhance understanding.
    """

    def get_prompt_as_text(self, semantic_map_str, planner_response):

        prompt_text = self.PROMPT_TEMPLATE
        prompt_text = prompt_text.replace(
            "{{semantic_map}}", semantic_map_str)
        prompt_text = prompt_text.replace(
            "{{planner_response}}", planner_response)

        return prompt_text
