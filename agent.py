import os
from dotenv import load_dotenv
from groq import Groq
import platform
from config import Config

load_dotenv()

class AIAgent:
    def __init__(self):
        # Looks for GROQ_API_KEY inside your .env file automatically
        self.client = Groq()

    def get_system_context(self):
        """Gathers OS, shell, and directory context to pass to the AI."""
        return {
            "os": platform.system(),
            "release": platform.release(),
            "cwd": os.getcwd(),
            "shell": os.environ.get("SHELL", Config.UNKNOWN_SHELL)
        }

    def ask_groq(self, user_prompt):
        context = self.get_system_context()
        system_instruction = (
            Config.SYSTEM_INSTRUCTION_PREFIX +
            f"- Operating System: {context['os']} ({context['release']})\n"
            f"- Current Directory: {context['cwd']}\n"
            f"- User's Shell: {context['shell']}\n" +
            Config.SYSTEM_INSTRUCTION_SUFFIX
        )
        
        try:
            # Uses the OpenAI-standard chat completion format
            response = self.client.chat.completions.create(
                model=Config.MODEL_NAME,  # High quality, ultra-fast free model
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=Config.TEMPERATURE  # Keep it deterministic so it doesn't hallucinate random characters
            )
            return response.choices[0].message.content.strip()
        except Exception as api_error:
            return f"{Config.ERROR_PREFIX}{api_error}"
