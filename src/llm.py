# import libraries
import os
import sys
import argparse
from typing import List, Dict, Optional

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from .env
token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"

# A function to call an LLM model and return the response
def call_llm_model(model, messages, temperature=1.0, top_p=1.0):    
    client = OpenAI(base_url=endpoint,api_key=token)
    response = client.chat.completions.create(
        messages=messages,
        temperature=temperature, top_p=top_p, model=model)
    return response.choices[0].message.content

# A function to translate to target language
def translate(text: str, target_language: str = "English", model_name: Optional[str] = None) -> str:
    """Translate text to target language using the configured LLM model."""
    m = model_name or model
    system_prompt = "You are a helpful translator. Translate the user's text into the target language preserving meaning and tone. Reply with translated text only."
    user_prompt = f"Translate to {target_language}:\n\n{text}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    return call_llm_model(m, messages, temperature=0.2, top_p=1.0)

# Run the main function if this script is executed
def _parse_args():
    parser = argparse.ArgumentParser(description="Translate text using configured LLM")
    parser.add_argument("--text", "-t", required=True, help="Text to translate")
    parser.add_argument("--to", default="English", help="Target language (default: English)")
    parser.add_argument("--model", "-m", help="Model name to use (optional)")
    return parser.parse_args()

def main():
    args = _parse_args()
    try:
        result = translate(args.text, target_language=args.to, model_name=args.model)
        print(result)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())