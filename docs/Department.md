# DEPARTMENTS.md

# Athena Departments

## Purpose

Athena is organized into specialized departments.

Each department owns a single responsibility.

Departments do not perform each other's work.

The Athena Kernel coordinates collaboration between departments.

---

# Organizational Structure

```text
Athena Kernel

├── Planning Department

├── Memory Department

├── Context Department

├── Communication Department

├── Action Department

└── Scheduler
```

---

# Planning Department

## Mission

Decide what Athena should do.

Planning focuses on reasoning rather than execution.

---

### Responsibilities

* Prioritize responsibilities
* Generate daily plans
* Recommend next actions
* Evaluate urgency
* Balance workload
* Select workflows

---

### Inputs

* Context
* Responsibilities
* Goals
* Calendar
* User request

---

### Outputs

* Decisions
* Recommendations
* Priorities
* Workflow selection

---

### Does NOT

* Execute actions
* Call APIs
* Store memory

---

# Memory Department

## Mission

Maintain Athena's long-term memory.

---

### Responsibilities

* Store memories
* Retrieve memories
* Learn preferences
* Remember projects
* Remember user habits

---

### Inputs

* Conversations
* Workflow results
* User information

---

### Outputs

* Relevant memories
* User preferences
* Historical context

---

### Does NOT

* Plan
* Execute
* Communicate

---

# Context Department

## Mission

Construct Athena's current understanding of the user's world.

---

### Responsibilities

* Gather information
* Connect related concepts
* Build context
* Detect conflicts
* Compute Responsibility State

---

### Inputs

* Responsibilities
* Events
* Memory
* Projects
* Documents
* Goals

---

### Outputs

Current Context

Examples:

* Today's workload
* Remaining commitments
* Calendar conflicts
* Safe to relax
* Urgent responsibilities

---

### Does NOT

* Make decisions
* Execute actions

---

# Communication Department

## Mission

Manage conversations.

---

### Responsibilities

* Understand intent
* Ask clarifying questions
* Generate responses
* Explain decisions
* Maintain conversation flow

---

### Inputs

* User messages
* Planning decisions
* Context

---

### Outputs

Natural language.

---

### Does NOT

* Decide priorities
* Execute work

---

# Action Department

## Mission

Execute work approved by the Planning Department.

---

### Responsibilities

* Create reminders
* Update spreadsheets
* Generate reports
* Schedule calendar events
* Organize documents
* Trigger automations

---

### Inputs

* Planning decisions
* Workflow instructions

---

### Outputs

Completed actions

---

### Does NOT

* Decide whether actions should happen

---

# Scheduler

## Mission

Generate recurring events.

---

### Responsibilities

* Morning briefing
* Reminder checks
* Daily reflection
* Hourly monitoring
* Background synchronization

---

### Outputs

Events

---

### Does NOT

* Execute business logic

---

# Department Collaboration

Departments never communicate directly.

All communication flows through the Athena Kernel.

```text
Planning

↓

Kernel

↓

Context

↓

Kernel

↓

Action
```

This prevents tight coupling between departments.

---

# Department KPIs

Planning

* Better recommendations
* Better prioritization

Memory

* Fewer repeated questions
* Better recall

Context

* Accurate understanding
* Correct Responsibility State

Communication

* Natural conversations
* Clear explanations

Action

* Successful automations
* Reliable execution

Scheduler

* Timely event generation

---

# Design Philosophy

Athena is one employee.

Departments are internal specializations.

The user should never know which department performed the work.

The user only interacts with Athena.
