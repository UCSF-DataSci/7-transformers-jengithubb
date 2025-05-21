# utils/one_off_chat.py

import requests
import argparse
import os

def get_response(prompt, model_name="HuggingFaceH4/zephyr-7b-beta", api_key=None):
    """
    Get a response from the model
    
    Args:
        prompt: The prompt to send to the model
        model_name: Name of the model to use
        api_key: API key for authentication (optional for some models)
        
    Returns:
        The model's response
    """
    # TODO: Implement the get_response function
    # Set up the API URL and headers
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    # Create a payload with the prompt
    payload = {"inputs": prompt}
    try:
        # Send the payload to the API
        response = requests.post(api_url, headers=headers, json=payload, timeout=50)
        response.raise_for_status()

        # Extract and return the generated text from the response
        output = response.json()
        if isinstance(output, list) and 'generated_text' in output[0]:
            return output[0]['generated_text']
        elif isinstance(output, dict) and 'generated_text' in output:
            return output['generated_text']
        return str(output)
 # Handle any errors that might occur
    except requests.exceptions.RequestException as e:
        return f"[ERROR] API request failed: {e}"


    #pass

def run_chat(model_name, api_key):
    """Run an interactive chat session"""
    print("Welcome to the Simple LLM Chat! Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
            
        # TODO: Get response from the model
        response = get_response(user_input, model_name=model_name, api_key=api_key)

        # Print the response
        print(f"LLM: {response}")
        
def main():
    parser = argparse.ArgumentParser(description="Chat with an LLM")
    # TODO: Add arguments to the parser
    parser.add_argument("--model", type=str, default="HuggingFaceH4/zephyr-7b-beta", help="Hugging Face model name")
    parser.add_argument("--api_key", type=str, default=os.getenv("HF_API_KEY"), help="Hugging Face API token")

    args = parser.parse_args()
    
    # TODO: Run the chat function with parsed arguments
    run_chat(model_name=args.model, api_key=args.api_key)
    
if __name__ == "__main__":
    main()
