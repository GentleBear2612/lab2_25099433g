# import libraries
import os
import sys
import argparse
from typing import List, Dict, Optional

from openai import OpenAI
from dotenv import load_dotenv
from requests import HTTPError

load_dotenv()  # Loads environment variables from .env
# Allow token to be provided via env or CLI --token
env_token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"

# A function to call an LLM model and return the response
def call_llm_model(model, messages, temperature=1.0, top_p=1.0, api_token: str = None):
    """Call the configured LLM and return text. Raises RuntimeError on failures with readable message."""
    token_to_use = api_token or env_token
    if not token_to_use:
        raise RuntimeError("No API token provided. Set GITHUB_TOKEN in the environment or pass --token on the command line.")

    try:
        client = OpenAI(base_url=endpoint, api_key=token_to_use)
        response = client.chat.completions.create(
            messages=messages,
            temperature=temperature, top_p=top_p, model=model)
        return response.choices[0].message.content
    except HTTPError as e:
        # requests HTTPError (if wrapped)
        raise RuntimeError(f"HTTP error when calling LLM API: {e}") from e
    except Exception as e:
        # Generic fallback with readable message
        raise RuntimeError(f"Failed to call LLM API: {e}") from e

# A function to translate to target language
def translate(text: str, target_language: str = "English", model_name: Optional[str] = None, api_token: Optional[str] = None) -> str:
    """Translate text to target language using the configured LLM model."""
    m = model_name or model
    system_prompt = "You are a helpful translator. Translate the user's text into the target language preserving meaning and tone. Reply with translated text only."
    user_prompt = f"Translate to {target_language}:\n\n{text}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    return call_llm_model(m, messages, temperature=0.2, top_p=1.0, api_token=api_token)

# Run the main function if this script is executed
def _parse_args():
    parser = argparse.ArgumentParser(description="Translate text using configured LLM")
    parser.add_argument("--text", "-t", required=False, help="Text to translate. If omitted, read from STDIN.")
    parser.add_argument("--to", default="English", help="Target language (default: English)")
    parser.add_argument("--model", "-m", help="Model name to use (optional)")
    parser.add_argument("--token", help="API token to use (overrides GITHUB_TOKEN env)")
    return parser.parse_args()

def main():
    args = _parse_args()
    try:
        # If --text not provided, read from stdin
        text = args.text
        if not text:
            # Read all from stdin (useful for piping)
            text = sys.stdin.read().strip()
            if not text:
                print("No input text provided. Use --text or pipe text into stdin.", file=sys.stderr)
                return 2

        result = translate(text, target_language=args.to, model_name=args.model, api_token=args.token)
        print(result)
        return 0
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        # Unexpected errors
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 3

if __name__ == "__main__":
    sys.exit(main())