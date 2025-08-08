import pandas as pd
import openai
import json
import time
from check_env import set_up_env

openai.api_key = set_up_env()  # Set up OpenAI API key from environment variables

EVALUATION_PROMPT = """
Evaluate the following AI response to a support ticket.

Criteria:

Content (relevance, accuracy, completeness) → score 1-5

Format (clarity, structure, grammar) → score 1-5

Output ONLY a valid JSON object exactly in this format (no extra text):

    {{
        "content_score": int,
        "content_explanation": "short text",
        "format_score": int,
        "format_explanation": "short text"
    }}

Ticket:
\"\"\"{ticket}\"\"\"

Respuesta:
\"\"\"{reply}\"\"\"
"""


def get_evaluation_from_model(ticket: str, reply: str, retries: int = 3, delay: float = 1.0) -> dict:
    """Get evaluation from OpenAI model for a given ticket and reply."""
    for attempt in range(1, retries + 1):
        try:
            response = openai.chat.completions.create(
                model='gpt-4o',
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a strict and precise evaluator of clear and concise customer support responses.',
                    },
                    {
                        'role': 'user',
                        'content': EVALUATION_PROMPT.format(ticket=ticket, reply=reply),
                    },
                ],
                temperature=0,
            )
            content = response.choices[0].message.content
            evaluation = json.loads(content)
            return evaluation

        except json.JSONDecodeError as e:
            err_msg = f'JSON decode error: {str(e)}'
        except Exception as e:
            err_msg = f'Exception: {str(e)}'

        print(f'Attempt {attempt} failed: {err_msg}')
        if attempt < retries:
            time.sleep(delay)
        else:
            return {
                'content_score': None,
                'content_explanation': err_msg,
                'format_score': None,
                'format_explanation': err_msg,
            }


def evaluate_tickets(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Evaluate each ticket and reply in the dataframe."""
    results = []
    for idx, row in dataframe.iterrows():
        print(f'Evaluating {idx + 1}/{len(dataframe)}...')
        evaluation = get_evaluation_from_model(row['ticket'], row['reply'])
        results.append(evaluation)
        time.sleep(0.5)  # Pause to avoid rate limit

    return add_results_to_dataframe(dataframe, results)


def add_results_to_dataframe(dataframe: pd.DataFrame, results: list) -> pd.DataFrame:
    """Add evaluation results to the dataframe."""
    dataframe['content_score'] = [result['content_score'] for result in results]
    dataframe['content_explanation'] = [result['content_explanation'] for result in results]
    dataframe['format_score'] = [result['format_score'] for result in results]
    dataframe['format_explanation'] = [result['format_explanation'] for result in results]

    return dataframe
