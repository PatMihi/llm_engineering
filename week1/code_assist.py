import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI

# constants
MODEL_GPT = 'gpt-4o-mini'
MODEL_LLAMA = 'llama3.2'

# set up environment
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")


#System and user prompts
    
def system_prompt():
    return """You are a coding assistant. You will be provided with a code snippet and your task is to explain the code in detail.\
    The code snippet will be in Python. You should provide a detailed explanation of the code. It should be in a markdown format. \
    It might happen that the code is not correct. In that case, you should provide a detailed explanation of the code and then provide the correct code snippet.\
    If not asked for more, anwer in up to 250 words."""

def user_prompt(code: str) -> str:
    return f"Explain the following code in detail:\n\n{code}\n\n###\n\n"

def code_assist(code, model = 'llama'):
    
    if model == 'gpt':
        openai = OpenAI()
        stream = openai.chat.completions.create(
            model=MODEL_GPT,
            messages=[
                {"role": "system", "content":system_prompt()},
                {"role": "user", "content": user_prompt(code)}
            ],
            stream=True,
        )
    
    elif model == 'llama':
        
        ollama_via_openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
        stream = ollama_via_openai.chat.completions.create(
            model=MODEL_LLAMA,
            messages=[
                {"role": "system", "content":system_prompt},
                {"role": "user", "content": user_prompt(code)}
            ],
            stream=True,
        )
        
    else:
        raise ValueError("Model not available. Please use 'gpt' or 'llama'.")
    
    response = ""
    display_handle = display(Markdown(""), display_id=True)
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        response = response.replace("```","").replace("markdown", "")
        update_display(Markdown(response), display_id=display_handle.display_id)

