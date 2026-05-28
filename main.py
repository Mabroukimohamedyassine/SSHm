
import sys 
import os
from dotenv import load_dotenv
from groq import Groq
import platform
import subprocess

load_dotenv()

def get_system_context():
    """Gathers OS, shell, and directory context to pass to the AI."""
    return {
        "os": platform.system(),
        "release": platform.release(),
        "cwd": os.getcwd(),
        "shell": os.environ.get("SHELL", "Unknown Shell")
    }

def make_client():
    # Looks for GROQ_API_KEY inside your .env file automatically
    return Groq()

def ask_groq(client, user_prompt, context):
    system_instruction = (
        "You are a cybersecurity engineer and professional pentester. "
        "Respond ONLY with the exact, raw terminal command requested. "
        "Do NOT include explanations, do NOT use markdown format, and do NOT use code blocks.\n\n"
        f"CRITICAL TARGET CONTEXT:\n"
        f"- Operating System: {context['os']} ({context['release']})\n"
        f"- Current Directory: {context['cwd']}\n"
        f"- User's Shell: {context['shell']}\n"
        "Ensure your command is natively compatible with this exact environment."
    )
    
    try:
        # Uses the OpenAI-standard chat completion format
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # High quality, ultra-fast free model
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0  # Keep it deterministic so it doesn't hallucinate random characters
        )
        return response.choices[0].message.content.strip()
    except Exception as api_error:
        return f"# Error contacting Groq API: {api_error}"

def execute_safely(command):
    if not command:
        print("❌ AI returned an empty response.")
        return

    # 2. Handle and display API errors instead of swallowing them
    if command.startswith("# Error"):
        print(f"\n❌ API Issue: {command}")
        return
    # Display the command to the user and ask for confirmation before execution
    print("\n" + "="*40)
    print(f"🤖 AI Generated Command:\n   \033[1;32m{command}\033[0m") 
    print("="*40)
    confirm = input("Do you want to execute this command? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            # Added capture_output=True to grab the results
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            
            # Print standard output (what you normally see when it succeeds)
            if result.stdout:
                print("--- Output ---")
                print(result.stdout.strip())
                print("--------------")
            
            # Print standard error (if something broke)
            if result.stderr:
                print("--- Error Log ---")
                print(result.stderr.strip())
                print("-----------------")
                
            if result.returncode != 0:
                print(f"\n❌ Command failed with error code: {result.returncode}")
            else:
                print(f"\n✅ Command executed successfully.")
                
        except Exception as e:
            print(f"❌ Failed to run command: {e}")
    else:
        print("❌ Execution cancelled by user.")

    

def main(): 
    client = make_client()
    context = get_system_context()
    
    print("Welcome bruv")
    print("Type 'exit' or press Ctrl+C to quit.")
    
    while True:
        try:
            # 1. Get user input safely using input()$
            lines = []
            while True:
                line = input()
                if line.strip() == "":
                    break
                lines.append(line)
            user_prompt = "\n".join(lines).strip()
            # 2. Skip empty lines
            if not user_prompt.strip():
                continue
                
            # 3. Allow the user to exit cleanly
            if user_prompt.strip().lower() in ['exit', 'quit']:
                print("Catch you later.")
                break
                
            print("🧠 Consulting Groq...")
            command = ask_groq(client, user_prompt.strip(), context)
            execute_safely(command)
            
        # 4. Catch Ctrl+C so it doesn't throw that ugly Traceback error you saw
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")



if __name__ == "__main__":
    main()