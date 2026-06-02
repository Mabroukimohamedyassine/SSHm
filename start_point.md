# Project Start Point

## What This Project Does
This script is a CLI loop that takes user input (single line by default, multi-line via trailing `\`), sends it to Groq’s chat completion API with system context, and returns a raw terminal command. It then asks for confirmation and executes the command locally, printing stdout/stderr and the exit status.

## What Has Been Implemented So Far
- **Module imports and environment loading**: Loads `dotenv` to pull `GROQ_API_KEY` from a `.env` file and imports `platform`, `subprocess`, and OS helpers needed for environment context and command execution. This sets up configuration and system introspection for later steps.
- **`get_system_context()`**: Collects OS name, OS release, current working directory, and shell from `SHELL`. This context is injected into the system prompt so the model emits commands compatible with the user’s environment.
- **`make_client()`**: Instantiates a `Groq` client, relying on environment variables loaded by `dotenv`. This isolates client creation from the main loop.
- **`ask_groq(client, user_prompt, context)`**: Builds a system instruction that forces the model to return only a raw command, includes environment context, and requests deterministic output with `temperature=0.0`. It calls `client.chat.completions.create(...)` using `model="llama-3.3-70b-versatile"` and returns the assistant message content. On API errors, it returns a string prefixed with `# Error`, which downstream logic checks.
- **`execute_safely(command)`**: Validates the command, handles error strings from the API, prints the generated command, and asks the user for confirmation. If confirmed, it runs the command with `subprocess.run(..., shell=True, text=True, capture_output=True)` and prints stdout/stderr along with success/failure status. If the user declines, it cancels execution.
- **`main()`**: Creates the Groq client, captures system context once, prints a welcome banner, and enters an infinite loop. It reads multi-line user input until a blank line, skips empty input, exits on `exit`/`quit`, calls `ask_groq`, and then calls `execute_safely`. It handles `KeyboardInterrupt` to exit cleanly and prints any unexpected exception message.
- **Entry point guard**: `if __name__ == "__main__": main()` ensures the CLI runs only when executed directly.

## Current State
- **Working / fully implemented**: Environment loading, context collection, Groq API call, command display/confirmation, and command execution with output/error reporting. The CLI loop, multi-line input collection, and exit handling are all implemented.
- **Partially implemented or stubbed out**: None indicated in `main.py`.
- **TODOs or placeholders**: None present in `main.py`.

## Key Design Decisions
- Uses Groq’s chat completions API via the `groq` client, with a fixed model (`llama-3.3-70b-versatile`) and deterministic output (`temperature=0.0`).
- Forces output to be a raw command via a strict system prompt and includes OS/shell/CWD to tailor commands to the local environment.
- Requires explicit user confirmation before executing any generated command and captures stdout/stderr for visibility.

## How to Resume
1. Read `main.py` from top to bottom to understand the context capture, Groq call, and execution flow.
2. After reviewing the original flow, the code was reorganized into separate modules: `config.py` (constants), `agent.py` (Groq client + prompt/context), `user_input.py` (multi-line input and command parsing), `executor.py` (command confirmation and execution), and `session.py` (main loop), with `main.py` now only invoking `Session().run()`. The earlier single-file OOP refactor is preserved in `main_v1.py`.
3. Ensure dependencies are installed (`python-dotenv`, `groq`) and a `.env` file provides `GROQ_API_KEY`.
