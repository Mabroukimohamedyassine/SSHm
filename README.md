# SSHm — AI‑Powered Terminal Assistant (Groq)

SSHm is a Python CLI assistant that turns natural‑language requests into raw terminal commands using Groq’s chat completion API. It injects local system context (OS, shell, CWD) into the prompt, displays the generated command, asks for confirmation, and executes it locally with captured output.

The CLI supports auto mode (AI‑generated commands), manual mode (direct command execution), and multi‑line input for complex prompts. It is designed for quick terminal automation with explicit safety confirmation before executing AI suggestions.

## Features
1. AI command generation via Groq (`llama-3.3-70b-versatile`)
2. Environment-aware prompts (OS, release, CWD, shell)
3. Confirmation gate before executing AI commands
4. Captured output (stdout/stderr) with exit status reporting
5. Manual mode for direct command execution
6. Multi‑line input with `\` continuation
7. Command suggestions and history via `prompt_toolkit`

## Architecture (High-Level)
**Flow:** `UserInput → Session → AIAgent (Groq) → Executor → Terminal`

```mermaid
flowchart LR
  UI[UserInput] --> S[Session]
  S -->|/auto| AG[AIAgent (Groq API)]
  AG --> EX[Executor]
  S -->|/manual| EX
  EX --> SH[Shell / Subprocess]
```

## File / Module Breakdown
| File | Purpose |
| --- | --- |
| `main.py` | Entry point; starts `Session().run()` |
| `session.py` | Main control loop; routes auto/manual execution |
| `agent.py` | Groq client + environment context + prompt building |
| `executor.py` | Command confirmation, execution, output handling |
| `user_input.py` | CLI input, multiline support, mode parsing, history |
| `config.py` | Centralized constants and messages |
| `start_point.md` | Project start documentation and refactor notes |
| `smart_cli_architecture.svg` | Architecture diagram (visual) |
| `test.py` | Prompt toolkit test harness (not production flow) |

## Dependencies
- Python 3.x
- `groq`
- `python-dotenv`
- `prompt_toolkit`

## Setup
Install dependencies:

```bash
pip install groq python-dotenv prompt_toolkit
```

Create a `.env` file at repo root:

```bash
GROQ_API_KEY=your_api_key_here
```

## Configuration
All user-facing messages and prompt policy live in `config.py`. Key config values:
- `MODEL_NAME = "llama-3.3-70b-versatile"`
- `TEMPERATURE = 0.0` (deterministic output)
- System prompt prefix/suffix to enforce raw command output only

## Usage
Start the CLI:

```bash
python main.py
```

### Auto Mode (default)
Use natural language; AI generates a command:

```
/auto list all python files recursively
```

Flow:
1. AI generates a command
2. Command shown for confirmation
3. Enter `y` to execute

### Manual Mode
Bypass the AI and run directly:

```
/manual ls -la
```

Manual mode does not ask for confirmation and uses `subprocess.run(..., shell=True)`.

### Multi‑Line Input
End a line with `\` to continue:

```
/auto find all log files \
and count lines in each
```

Lines are joined with newlines and sent as a single request.

## Safety & Confirmation Behavior
- Auto mode always asks for confirmation before executing.
- Manual mode executes immediately.
- Commands are executed with `shell=True` (consider security implications).

## Error Handling
- API errors are returned as strings beginning with `# Error` and printed.
- Empty responses trigger a specific error message.
- `KeyboardInterrupt` (Ctrl+C) exits cleanly.
- Unexpected exceptions are caught and printed with a generic prefix.

## Development Notes
- The project was refactored from a single-file script into modular components:
  - `agent.py`, `executor.py`, `user_input.py`, `session.py`
- `test.py` is a standalone experiment for `prompt_toolkit` history/completion.
- `start_point.md` includes early design notes and the refactor summary.

## Known Gaps
1. No `requirements.txt` or `pyproject.toml`
2. No automated tests
3. No LICENSE file
