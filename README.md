# Athena

Athena is an AI-powered Personal Chief of Staff designed to reduce cognitive load, organize responsibilities, and help users make better day-to-day execution decisions.

Rather than acting as a simple chatbot, Athena combines deterministic business logic with large language models to deliver trustworthy, explainable recommendations.

---

## Current Features

### Responsibilities

- Create responsibilities
- Track priorities
- Due dates
- Completion tracking

### Projects

- Organize responsibilities into projects
- Project progress calculation
- Project overview API

### Daily Briefing

- AI-generated daily briefings
- Priority-aware summaries
- Overdue detection

### Advisor Framework

- Availability Advisor
- Capacity Advisor

### Planning Engine

- Deterministic execution planner
- Project-aware planning
- Time-aware workload estimation

### Persistence

- PostgreSQL
- SQLAlchemy
- Alembic migrations

---

## Architecture

FastAPI

↓

Business Services

↓

Domain Models

↓

PostgreSQL

↓

LLM (OpenRouter)

Athena follows a strict architectural principle:

> Deterministic business logic owns decisions.
> The LLM owns communication.

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- OpenRouter
- Structlog

---

## Current Status

Version: v0.1.0

Completed Sprints:

- Sprint 1 — Foundation
- Sprint 2 — Responsibilities
- Sprint 3 — Daily Briefings
- Sprint 4 — PostgreSQL Persistence
- Sprint 5 — Advisor Framework
- Sprint 6 — Projects
- Sprint 7 — Execution Planning
- Sprint 8 — Time Intelligence

---

## Roadmap

Upcoming:

- Sprint 9 — Workload Balancing
- Calendar Integration
- Notifications
- Long-term Memory
- Scheduling Engine