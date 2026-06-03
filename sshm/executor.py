import subprocess
from .config import Config


class Executor:
    def run(self, command):
        if not command:
            print(Config.EMPTY_RESPONSE_ERROR)
            return

        # 2. Handle and display API errors instead of swallowing them
        if command.startswith("# Error"):
            print(f"{Config.API_ISSUE_PREFIX}{command}")
            return
        # Display the command to the user and ask for confirmation before execution
        print("\n" + Config.COMMAND_SEPARATOR)
        print(f"{Config.GENERATED_COMMAND_PREFIX}{command}{Config.GENERATED_COMMAND_SUFFIX}")
        print(Config.COMMAND_SEPARATOR)
        confirm = input(Config.CONFIRM_PROMPT).strip().lower()
        if confirm == "y":
            try:
                # Added capture_output=True to grab the results
                result = subprocess.run(command, shell=True, text=True, capture_output=True)

                # Print standard output (what you normally see when it succeeds)
                if result.stdout:
                    print(Config.OUTPUT_HEADER)
                    print(result.stdout.strip())
                    print(Config.OUTPUT_FOOTER)

                # Print standard error (if something broke)
                if result.stderr:
                    print(Config.ERROR_HEADER)
                    print(result.stderr.strip())
                    print(Config.ERROR_FOOTER)

                if result.returncode != 0:
                    print(f"{Config.COMMAND_FAILED_PREFIX}{result.returncode}")
                else:
                    print(Config.COMMAND_SUCCESS)

            except Exception as e:
                print(f"{Config.EXECUTION_FAILED_PREFIX}{e}")
        else:
            print(Config.EXECUTION_CANCELLED)

    def run_manual(self, command):
        subprocess.run(command, shell=True)
