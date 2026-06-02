from config import Config
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory

class UserInput:
    def __init__(self):
        self.commands = {"/auto": self.handle_auto, "/exit": self.handle_exit, "/manual": self.handle_manual}
        self.status_completer = WordCompleter(['/auto', '/exit', '/manual'], ignore_case=True)
        self.session_history = InMemoryHistory()  # Persist history across prompts

    def read(self):
        # 1. Get user input safely using prompt_toolkit
        lines = []
        while True:
            prompt_text = "/auto /manual /exit > " if not lines else "... "
            line = prompt(prompt_text, completer=self.status_completer, history=self.session_history)
            if line.strip() == "":
                if not lines:
                    return ""
                break

            if line.endswith("\\"):
                lines.append(line[:-1].rstrip())
                continue

            lines.append(line)
            break
        user_prompt = "\n".join(lines).strip()
        return user_prompt

    def handle_exit(self, user_prompt):
        # 3. Allow the user to exit cleanly
        if user_prompt.strip().lower() in ['exit', 'quit', '/exit']:
            print(Config.EXIT_MESSAGE)
            return True
        return False

    def handle_auto(self, user_prompt):
        if user_prompt.strip().lower().startswith('/auto'):
            parts = user_prompt.strip().split(' ', 1)
            if len(parts) == 2:
                return parts[1]
            return ""
        return user_prompt

    def handle_manual(self, user_prompt):
        if user_prompt.strip().lower().startswith('/manual'):
            parts = user_prompt.strip().split(' ', 1)
            if len(parts) == 2:
                return parts[1]
            return ""
        return user_prompt

    def parse(self, user_prompt):
        if user_prompt.strip().startswith("/"):
            command = user_prompt.strip().split()[0]
            if command in self.commands:
                if command == "/exit":
                    return self.commands[command](user_prompt), None, None
                return False, command, self.commands[command](user_prompt)
        return False, "/auto", self.handle_auto(user_prompt)
