# ARCHITECTURE.md

# Athena Architecture

## Overview

Athena is an event-driven Personal Chief of Staff.

Every interaction begins with an event, is coordinated by the **Athena Kernel**, delegated to the appropriate departments, executed through integrations when necessary, and finally stored as knowledge for future interactions.

Athena is designed around **coordination**, not monolithic intelligence.

The Kernel does not "think."

The Kernel coordinates specialists.

---

# Design Philosophy

Athena follows one simple lifecycle.

```text
Event
    ↓
Understand
    ↓
Gather Context
    ↓
Plan
    ↓
Execute
    ↓
Learn
    ↓
Respond
```

Every workflow, regardless of complexity, follows this lifecycle.

---

# High-Level Architecture

```text
                         USER

                           │
                           ▼

              Conversation Interfaces

 WhatsApp │ Web │ Mobile │ Voice │ Future Clients

                           │
                           ▼

                   Event Dispatcher

                           │
                           ▼

═══════════════════════════════════════════════
                 ATHENA KERNEL
═══════════════════════════════════════════════

Receives Events

Coordinates Departments

Executes Workflows

Maintains System State

═══════════════════════════════════════════════

        │
        ├─────────────────────────────┐
        │                             │
        ▼                             ▼

 Planning Department

 Memory Department

 Context Department

 Communication Department

 Action Department

 Scheduler

═══════════════════════════════════════════════

               │
               ▼

         Integration Layer

 Google Calendar
 Google Drive
 Google Sheets
 GitHub
 OpenRouter
 WhatsApp
 Email
 Future Services

               │
               ▼

          External Systems
```

---

# Athena Kernel

The Athena Kernel is the heart of the system.

It is responsible for coordinating every request inside Athena.

The Kernel never performs business logic itself.

Instead, it delegates work to specialized departments.

Responsibilities include:

* Receiving events
* Selecting workflows
* Coordinating departments
* Managing execution order
* Maintaining runtime state
* Producing final responses

The Kernel is intentionally lightweight.

---

# Departments

The Kernel coordinates several specialized departments.

Each department has a single responsibility.

---

## Planning Department

Responsible for deciding what should happen.

Responsibilities include:

* Prioritization
* Planning
* Recommendations
* Responsibility evaluation
* Daily planning

The Planning Department never communicates directly with external services.

---

## Memory Department

Responsible for long-term memory.

Examples:

* Preferences
* Conversation history
* Important facts
* Learned behavior
* User-specific information

The Memory Department determines what should be remembered and how it should be retrieved.

---

## Context Department

Responsible for building Athena's understanding of the current situation.

It gathers information from:

* Responsibilities
* Calendar
* Projects
* Documents
* People
* Goals
* Memory

Instead of returning isolated facts, the Context Department constructs a complete picture of the user's current state.

Example:

User asks:

> Can I game tonight?

Context does not simply return:

* 3 tasks
* 1 meeting

Instead it produces:

* Everything due today is complete.
* Tomorrow has one assignment.
* No remaining commitments tonight.

The Planning Department then uses this context to make recommendations.

---

## Communication Department

Responsible for conversation.

Responsibilities include:

* Intent recognition
* Conversation management
* Response generation
* Clarification questions
* Natural language formatting

The Communication Department never decides what actions to perform.

---

## Action Department

Responsible for executing work.

Examples:

* Create reminders
* Generate briefings
* Update spreadsheets
* Create calendar events
* Move documents
* Send notifications

The Action Department performs work.

It does not decide whether work should happen.

---

## Scheduler

Generates recurring events.

Examples:

* Morning briefing
* Reminder checks
* Daily reflection
* Synchronization
* Health monitoring

The Scheduler creates Events.

It never performs business logic.

---

# Integration Layer

The Integration Layer connects Athena to external systems.

Examples:

* WhatsApp
* Google Calendar
* Google Drive
* Google Sheets
* GitHub
* OpenRouter
* Email

Responsibilities:

* Authentication
* API communication
* Data normalization
* Error handling

Integrations never contain business logic.

They simply translate between Athena and external services.

---

# Information Flow

Every request follows the same execution path.

```text
Event

↓

Kernel

↓

Workflow Selection

↓

Relevant Departments

↓

Action Department

↓

Integration Layer (if needed)

↓

Knowledge Update

↓

Response
```

This execution flow remains identical whether the request originated from a user, a scheduler, or an external integration.

---

# Separation of Responsibilities

The architecture intentionally separates decision making from execution.

Planning Department

↓

Decides.

---

Context Department

↓

Builds understanding.

---

Memory Department

↓

Remembers.

---

Communication Department

↓

Communicates.

---

Action Department

↓

Executes.

---

Integration Layer

↓

Interacts with external services.

---

Kernel

↓

Coordinates everything.

Nothing more.

---

# Extensibility

Athena should grow by adding new departments, workflows, operations, or integrations without requiring changes to the Kernel.

Examples

Adding Slack

→ New Integration

Adding Gmail

→ New Integration

Adding Finance Tracking

→ New Workflow

Adding Voice

→ New Conversation Interface

Adding Local LLM

→ Replace or extend the OpenRouter integration.

The Kernel remains stable.

---

# Design Goals

Athena should remain:

* Event-driven
* Modular
* Provider-independent
* Easy to extend
* Easy to reason about
* Easy to test

As Athena grows, complexity should increase inside departments—not inside the Kernel.

---

# Final Principle

The Athena Kernel coordinates.

Departments specialize.

Integrations communicate.

Knowledge persists.

Together, they allow Athena to function as a single, coherent Personal Chief of Staff rather than a collection of disconnected AI features.
