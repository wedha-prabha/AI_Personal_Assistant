# AI_Personal_Assistant

A simple personal assistant app built with Python and AI model integrations.

## Live Demo

- Visit the deployed app: https://aipersonalassistantwedha.streamlit.app/

## Setup Instructions

1. Clone the repository.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add required API keys and configuration values.
5. Launch the app:

```bash
python app.py
```

## Architecture Overview

- `app.py` drives the main application flow and integrates the assistant UI with backend services.
- `models/` contains model wrappers and API clients for interacting with AI providers.
- `memory/` stores conversational context and chat history to preserve state between interactions.
- `guardrails/` provides input validation and safety checks to keep responses constrained.
- `observability/` collects logs and diagnostics for monitoring app behavior and failures.
- `evaluation/` contains scripts for testing and validating prompts and model output.

## Decisions and Tradeoffs

- Chosen Python for simplicity and rapid iteration with existing AI client libraries.
- Separated concerns into folders for models, memory, and guardrails to keep the codebase modular.
- Used local file-based memory instead of a database to reduce deployment complexity.
- Focused on a lightweight architecture over full production readiness, so logging and error handling are minimal.

## What I Would Improve With More Time

- Replace file-based memory with a persistent database or vector store for larger context and better retrieval.
- Add a more robust UI/UX, including clearer conversation controls and message formatting.
- Implement stronger guardrails and rate limiting for safe model usage.
- Add automated tests for core workflows and model integrations.
- Improve deployment automation and environment configuration documentation.

## Project Structure

- `app.py` - main application entrypoint
- `requirements.txt` - Python dependencies
- `deployment/` - deployment-related files
- `evaluation/` - evaluation scripts and prompts
- `guardrails/` - safety and validation logic
- `memory/` - chat and memory persistence utilities
- `models/` - model wrappers and API clients
- `observability/` - logging and diagnostics
- `reports/` - generated reports and outputs
- `tools/` - helper tools and utilities

## Notes

- Configure API keys and environment variables in a `.env` file.
- This repository is designed for experimentation with AI assistants and local model connectors.
