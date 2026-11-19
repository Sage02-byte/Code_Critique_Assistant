import json
from openai import OpenAI
from model import CodeReviewReport

client = OpenAI(
    base_url = "http://localhost:8080/v1",
    api_key="sk-no-key-required"
)

def analyze_code_snippet(code_snippet: str, model_name: str = "smollm2-1.7b-instruct") -> CodeReviewReport:

    """
    Sends the code snippet to the local LLM with strict code-review parameters
    and validates the response against the CodeReviewReport Pydantic model.
    """
    # Consists of everything within the Pydantic CodeReviewReport model
    system_prompt = (
        "You are an expert senior software engineer and code reviewer. "
        "Analyze the provided code for bugs, anti-patterns, and performance issues. "
        "You must respond with a valid JSON object that matches the requested schema exactly, "
        "containing these keys: summary (string), severity_score (integer 1-10), "
        "bug_identification (list of objects with line_number, description, fix_suggestion), "
        "refactored_code (string), and suggestion_test (string)."
    )
    
    user_input = f"Please review this code and refactor it:\n\n```python\n{code_snippet}\n```"
    
    try: 
        response = client.chat.completions.create(
        model = model_name,
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],

        # Tuned parameters for code precision and stopping criteria
        temperature = 0.2, # Low temperature for deterministic, accurate code analysis
        top_p= 0.95, # Nucleus sampling for logical token choices
        frequency_penalty = 0.0, # Keep code syntax natural
        presence_penalty = 0.0, # Keep code syntax natural
        max_tokens = 1000, # Allow enough length for code refactoring
        stop = ["<|im_end|>", "####"] # Stop sequence for runaway test
        )
    
        raw_content = response.choices[0].message.content.strip()
    
        if raw_content.startswith("```json"):
            raw_content = raw_content[7:]
        elif raw_content.startswith("```"):
            raw_content = raw_content[3:]
        if raw_content.endswith("```"):
            raw_content = raw_content[:-3]
        raw_content = raw_content.strip()

        '''

        Use of remove.prefix() method and remove.suffix() method can be used
        if you dont want to use index positioning

        raw_content = raw_content.removeprefix("```json").removeprefix("```")
        raw_content = raw_content.removesuffix("```")
        raw_content = raw_content.strip()
        '''

    # Parse JSON and validate through Pydantic

    
        data = json.loads(raw_content) # Pasing everything as Python Dict 
        report= CodeReviewReport(**data)# '**' is dictionary unpacking operator
        return report

    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse model output as JSON. Raw output was:\n{raw_content}\n\nError: {e}")
    except Exception as e:
        raise ValueError(f"An error occurred during local LLM generation: {e}")
