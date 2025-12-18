import os
from pathlib import Path

current_file_path = Path(os.path.abspath(__file__))
root_folder = current_file_path.parent.parent.parent
with open('{}/openai.credential'.format(root_folder), 'r') as file:
    key = file.read()

def get_openai_model_config(model = 'gpt-4o'):
    return {"model": model, "api_key": key}