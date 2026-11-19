# CodeCritique AI

A local command-line code review tool built with Python, Pydantic (v2), and the OpenAI Python SDK targeting a local `llama.cpp` server. Paste a multi-line code snippet in the terminal to receive a structured review covering a summary, severity score, identified bugs and fixes, refactored code, and a test skeleton.

## Project Structure

- `models.py` — Pydantic schemas (`BugItem` and `CodeReviewReport`) for validating structured model output.
- `engine.py` — Configures the local `llama.cpp` client (`http://localhost:8080/v1`), sends prompts with low temperature (`0.2`), strips markdown fences, and parses/validates the JSON response.
- `main.py` — Interactive CLI that reads multi-line input until `RUN` and formats the review report in the terminal.

## Prerequisites

- Python 3.9+
- Dependencies: `pydantic`, `openai`
- A local `llama.cpp` server running on port `8080` with a loaded model (e.g., `smollm2-1.7b-instruct`).

## Usage

1. Start your local `llama.cpp` server on `http://localhost:8080`.
2. Run the CLI:
   ```bash
   python main.py
