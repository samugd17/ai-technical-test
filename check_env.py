from dotenv import load_dotenv
import os

def set_up_env():

    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY is not set in the environment variables.')
    print('OPENAI_API_KEY ready to use')

    return api_key
