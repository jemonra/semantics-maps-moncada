from prompt.classical_prompt import ClassicalPrompt


class PlannerCorrectionPrompt(ClassicalPrompt):

    PROMPT_TEMPLATE = """
    ### CONTEXT ###
    We have received two responses from other LLMs. The first one was tasked with interpreting and answering questions about a 3D scene described in a JSON format. The second one was tasked with reflecting on the first response, providing constructive feedback to help refine and improve it.
    
    ### FIRST LLM RESPONSE ###
    
    The INSTRUCTION was:
    | The input to the model is a 3D scene described in a JSON format (### 3D SCENE ###). Each entry in the JSON describes one object in the scene, with the following five fields:
    | 1. "id": a unique object id
    | 2. "bbox_extent": extents of the 3D bounding box for the object
    | 3. "bbox_center": centroid of the 3D bounding box for the object
    | 4. "object_tag": a brief (but sometimes inaccurate) tag categorizing the object
    | 5. "caption": a brief caption for the object
    | Once you have parsed the JSON and are ready to answer questions about the scene, say "I'm ready".
    | The user will then begin to ask questions, and the task is to answer various user queries about the 3D scene. For each user question, respond with a JSON dictionary with the following fields:
    | 1. "inferred_query": your interpretation of the user query in a succinct form
    | 2. "relevant_objects": list of relevant object ids for the user query (if applicable)
    | 3. "query_achievable": whether or not the user specified query is achievable using the objects and descriptions provided in the 3D scene.
    | 4. "final_relevant_objects": A final list of objects relevant to the user-specified task. Sort all objects in this list such that the most relevant object is listed first, followed by the second most relevant, and so on.
    | 5. "explanation": A brief explanation of what the most relevant object(s) is(are), and how they achieve the user-specified task.
    
    The 3D SCENE was:
    {{semantic_map_str}}

    The RESPONSE was:
    {{planner_response}}

    ### SECOND LLM RESPONSE ###

    The INSTRUCTION was:
    | Your task is to:
    | - Carefully review the original response for correctness, relevance, and clarity.
    | - Provide constructive criticism, focusing on areas where the response could be improved.
    | - Offer specific suggestions for how to refine the response, ensuring it better meets the requirements and addresses any potential issues.
    | REFLECTION TASK
    | Correctness:
    | - Are the inferred query and relevant objects accurately identified?
    | - Is the query achievable status appropriately determined?
    | - Is the explanation logically sound and coherent?
    | Relevance:
    | - Are all relevant objects identified, and are they sorted by relevance accurately?
    | - Are any crucial objects or details omitted?
    | Clarity:
    | - Is the response clear and easy to understand?
    | - Are there any ambiguities or vague descriptions?
    | CRITIQUE TEMPLATE
    | Please review the response carefully for correctness, relevance, and clarity, and provide constructive criticism for how to improve it. Follow the structure provided below:
    | Correctness:
    | [Your comments on correctness]
    | Relevance:
    | [Your comments on relevance]
    | Clarity:
    | [Your comments on clarity]
    | SUGGESTIONS FOR IMPROVEMENT
    | Based on your critique, please suggest specific improvements. These can include corrections to factual errors, inclusion of missing relevant objects, reordering of objects by relevance, or clarifications to enhance understanding.

    The RESPONSE was:
    {{self_reflection_response}}
    
    ### INSTRUCTION ###
    Your task is to apply the feedback provided in the critique to produce a refined and corrected response.
    Note that the response must again be a JSON, with the same keys as the first LLM call, but with the values corrected according to the feedback.
    1. "inferred_query"
    2. "relevant_objects"
    3. "query_achievable"
    4. "final_relevant_objects"
    5. "explanation"
    """
