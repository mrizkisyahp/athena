# Getting Started with Athena

Welcome to **Athena**, your AI-powered Personal Chief of Staff! This guide will help you set up and run the project on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.11** (as specified in `pyproject.toml`)
- **uv** (an extremely fast Python package and project manager)

You can install `uv` following the instructions on their [official documentation](https://github.com/astral-sh/uv).

## 1. Environment Setup

Athena requires certain environment variables to be set, particularly for connecting to the LLM (Large Language Model) provider.

1. Create a `.env` file in the root of the project directory.
2. Add the necessary configuration variables. Based on the project structure, it should look something like this:

```env
APP_NAME=Athena
APP_ENV=development

# LLM Configuration (NVIDIA NIM)
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_API_KEY=your_nvidia_api_key_here
LLM_MODEL=minimaxai/minimax-m3
```

Make sure to replace `your_actual_api_key_here` with your real API key.

## 2. Install Dependencies

Since the project uses `uv` for dependency management and contains a `uv.lock` file, you can install all required dependencies and set up the virtual environment with a single command:

```bash
uv sync
```

This command will automatically create a virtual environment (`.venv`) and install all the dependencies specified in `pyproject.toml` and `uv.lock`.

## 3. Run the Application

The application is built with **FastAPI**. To run the development server, you will use `uvicorn`.

Run the following command from the root directory:

```bash
uv run uvicorn app.main:app --reload
```

The `--reload` flag enables auto-reloading so the server will restart whenever you make code changes.

## 4. Access the API

Once the server is running, you can access the API locally:

- **Root Endpoint:** http://127.0.0.1:8000/
- **Health Check:** http://127.0.0.1:8000/health
- **Interactive API Documentation (Swagger UI):** http://127.0.0.1:8000/docs
- **Alternative API Documentation (ReDoc):** http://127.0.0.1:8000/redoc

You can test the chat endpoint by sending a POST request to `/chat` through the Swagger UI at `http://127.0.0.1:8000/docs`.

---
Happy coding with Athena!
