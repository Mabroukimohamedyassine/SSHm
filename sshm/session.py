from .agent import AIAgent
from .user_input import UserInput
from .executor import Executor
from .config import Config


class Session:
    def __init__(self):
        self.agent = AIAgent()
        self.input_handler = UserInput()
        self.executor = Executor()

    def run(self):
        print(Config.WELCOME_MESSAGE)
        print(Config.EXIT_HINT)

        while True:
            try:
                user_prompt = self.input_handler.read()
                # 2. Skip empty lines
                if not user_prompt.strip():
                    continue

                should_exit, mode, parsed_prompt = self.input_handler.parse(user_prompt)
                if should_exit:
                    break

                if not parsed_prompt or not parsed_prompt.strip():
                    continue

                if mode == "/manual":
                    self.executor.run_manual(parsed_prompt)
                else:
                    print(Config.CONSULTING_MESSAGE)
                    command = self.agent.ask_groq(parsed_prompt.strip())
                    self.executor.run(command)

            # 4. Catch Ctrl+C so it doesn't throw that ugly Traceback error you saw
            except KeyboardInterrupt:
                print(Config.KEYBOARD_INTERRUPT_MESSAGE)
                break
            except Exception as e:
                print(f"{Config.GENERIC_ERROR_PREFIX}{e}")
