# DATABASE.md

# Athena Database Design

## Purpose

This document defines how Athena persists information.

It translates the Data Model into a relational PostgreSQL schema.

The database exists to store Athena's knowledge reliably, consistently, and efficiently.

Business logic does not belong in the database.

The database stores state.

The Athena Kernel interprets that state.

---

# Database Philosophy

The database should answer:

> "What does Athena know?"

It should never answer:

> "What should Athena do?"

Reasoning belongs inside the Kernel.

---

# Database Technology

Database

PostgreSQL

ORM

SQLAlchemy 2.x

Migration

Alembic

Primary Keys

UUID v7

Time Zone

UTC

Soft Delete

Supported

---

# Audit Fields

Every table contains:

* id
* created_at
* updated_at

Optional:

* deleted_at

These fields are managed automatically.

---

# Core Tables

## users

Purpose

Represents Athena's owner.

Current expectation:

One row.

Designed for future multi-user support.

---

## responsibilities

Stores user responsibilities.

Relationships

* belongs_to Project
* has_many Reminders
* many_to_many Documents
* many_to_many People

---

## projects

Stores projects.

Relationships

* has_many Responsibilities
* has_many Events
* has_many Documents
* has_many Notes

---

## events

Stores scheduled events.

Relationships

* belongs_to Project

---

## reminders

Stores reminder schedules.

Relationships

* belongs_to Responsibility

---

## people

Stores known individuals.

Relationships

* many_to_many Responsibilities
* many_to_many Events

---

## documents

Stores document metadata.

Athena stores references rather than document contents whenever possible.

Relationships

* belongs_to Project
* many_to_many Responsibilities

---

## notes

Stores long-form information.

Relationships

* belongs_to Project

---

## goals

Stores long-term objectives.

Relationships

* many_to_many Responsibilities

---

## conversations

Stores conversations.

Relationships

* has_many Messages

---

## messages

Stores message history.

Relationships

* belongs_to Conversation

---

## memories

Stores long-term learned knowledge.

Examples

* User preferences
* Frequently used information
* Learned habits

This table powers Athena's Memory Department.

---

# Relationship Overview

```text
User
│
├── Projects
│      │
│      ├── Responsibilities
│      │      ├── Reminders
│      │      ├── Documents
│      │      └── People
│      │
│      ├── Events
│      ├── Notes
│      └── Goals
│
├── Conversations
│      └── Messages
│
└── Memories
```

---

# Indexing Strategy

Primary indexes

* UUID
* Foreign Keys

Additional indexes

Responsibilities

* due_date
* priority
* status

Events

* start_time

Messages

* timestamp

Documents

* source

Memories

* category

Indexes should be added only when query patterns justify them.

---

# Data Ownership

Athena stores only what it owns.

External systems remain authoritative.

Example

Google Calendar

Source of truth for Events.

Athena

Stores relationships, summaries, context, and metadata.

---

# Soft Deletes

Important user information should never be permanently deleted immediately.

Soft deletion allows:

* recovery
* auditing
* historical reasoning

Permanent deletion should occur only through explicit maintenance.

---

# Transactions

Every workflow should execute inside a database transaction when multiple related updates occur.

Examples

Employee Upload

↓

Save document

↓

Update responsibility

↓

Create memory

↓

Commit

Failure anywhere rolls back the transaction.

---

# Future Expansion

The schema should support:

* Multi-user
* Multiple workspaces
* Multiple LLM providers
* Additional integrations
* Plugin ecosystem

Without requiring major redesign.

---

# Design Principles

The database exists to preserve knowledge.

It should remain:

* Reliable
* Predictable
* Provider-independent
* Easy to migrate
* Easy to query
* Easy to extend

The Athena Kernel owns business logic.

The database owns persistence.
