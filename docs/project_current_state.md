# Athena - Project Current State

## Overview
**Athena** is an AI-powered "Personal Chief of Staff" designed to reduce cognitive load by managing responsibilities, organizing information, and automating repetitive tasks. The project is built using Python 3.11, FastAPI, and `uv` for dependency management.

## Architecture
The application is structured modularly:
* **Bootstrap (`app/bootstrap/container.py`)**: A simple dependency injection container that instantiates and holds singleton instances of core services (Kernel, Communication Department, Responsibilities Service, LLM Client).
* **Kernel (`app/kernel/kernel.py`)**: The central coordinator that routes user intents to the appropriate departments. It currently manages communication via the `CommunicationDepartment`.
* **Departments (`app/departments/`)**: Domain-specific logic. 
  * `CommunicationDepartment`: Handles conversational AI interactions.
* **Integrations (`app/integrations/llm.py`)**: The LLM client abstraction. It uses the `openai` Python package but is provider-agnostic. It is currently configured to connect to NVIDIA NIM using the `minimaxai/minimax-m3` model.
* **Services (`app/responsibilities/`)**: Handles the business logic for task/responsibility management without knowing about HTTP layers or the LLM.
* **Schemas (`app/schemas/`)**: Pydantic models for request/response validation (e.g., `TaskResponse`, `TodayResponse`, `SuccessResponse`). Contains a `mappers.py` file to cleanly map internal domain models to API responses.

## Current Features & Endpoints
The FastAPI application (`app/main.py`) exposes the following endpoints:

### System
* **`GET /`**: Welcome message.
* **`GET /health`**: API health and environment status.

### AI Communication
* **`POST /chat`**: Takes a user message and returns an LLM-generated reply via the Athena Kernel.

### Task Management (Sprint 2)
* **`POST /tasks`**: Creates a new responsibility (Task). Requires a title, and optionally accepts description, priority, and due_date.
* **`GET /tasks`**: Returns a list of all tasks ever created in the system.
* **`PATCH /tasks/{task_id}/complete`**: Marks a specific task as completed. Returns a `SuccessResponse` or a 404 error if the task is not found.
* **`GET /today`**: Categorizes incomplete and completed tasks relevant to the current day.

## Known Issues (Pending Fixes)
There are two known bugs currently affecting the `/today` endpoint:
1. **The Schema Bug**: The `TodayResponse` schema defines `completed_today` as an integer (`int`). This means the API only returns a count of completed tasks, preventing frontend clients from rendering the actual details of the tasks completed today.
2. **The Timezone Bug**: The backend filters tasks using `datetime.utcnow().date()`. For users in timezones ahead of UTC (e.g., GMT+7), local "today" tasks are treated by the server as being due "tomorrow" because the UTC date lags behind. This causes tasks due today to completely vanish from the `/today` endpoint.

## Development Setup
* **Package Manager**: `uv`
* **Local Run Command**: `uv run uvicorn app.main:app --reload`
* **Environment Variables**: Managed via `.env` (loaded into `app/config/settings.py` via `pydantic-settings`). Includes keys like `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL`.
