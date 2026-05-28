import sys 
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def gemini(user_prompt):
    client = genai.Client()
    
    # We strictly instruct the model to return ONLY raw code with zero conversational text
    config = {
        "system_instruction": (
            "You are a cybersecurity engineer and professional pentester. "
            "Respond ONLY with the exact, raw terminal command requested. "
            "Do NOT include explanations, do NOT use markdown format, and do NOT use code blocks."
        )
    }
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", # Using the optimal 2.5-flash model
            config=config,
            contents=user_prompt     # Fixed: changed from 'content' to 'contents'
        )
        return response.text.strip()
    except Exception as api_error:
        return f"# Error contacting API: {api_error}"

def main(): 
    print("Hello, SSHM!")
    try:
        # Simulate some work
        sys.stdout.write(f'wokring... \n')
        for line in sys.stdin:
            x = gemini(line.strip())
            sys.stdout.write(f'{x} => {x}\n')
            os.system(x)
            
    except Exception as e:
        print(f"An error occurred: {e}) ")



if __name__ == "__main__":
    main()