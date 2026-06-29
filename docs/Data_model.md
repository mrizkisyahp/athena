# DATA_MODEL.md

# Athena Data Model

## Purpose

This document defines the core data objects used by Athena.

The Data Model translates the conceptual Knowledge Model into concrete application objects.

It remains independent of any database technology or programming language.

---

# Design Philosophy

Athena stores concepts, not integrations.

For example:

* A Google Calendar event becomes an **Event**.
* A Google Drive file becomes a **Document**.
* A GitHub issue becomes a **Responsibility**.

The provider is metadata.

The concept is the data.

---

# Core Objects

## Responsibility

Represents anything the user is responsible for.

### Attributes

* id
* title
* description
* status
* priority
* due_date
* estimated_effort
* created_at
* updated_at

### Relationships

* belongs to one Project
* may involve many People
* may reference many Documents
* may generate many Reminders
* may contribute to many Goals

---

## Project

Groups related responsibilities.

### Attributes

* id
* name
* description
* status
* created_at

### Relationships

* contains Responsibilities
* contains Documents
* contains Notes
* contains Events

---

## Event

Represents something occurring at a specific time.

### Attributes

* id
* title
* start_time
* end_time
* location
* status

### Relationships

* belongs to Project
* involves People
* may create Responsibilities
* may reference Documents

---

## Person

Represents an individual known to Athena.

### Attributes

* id
* name
* role
* contact_information

### Relationships

* participates in Events
* owns Responsibilities
* creates Documents

---

## Document

Represents stored information.

### Attributes

* id
* title
* type
* source
* location
* created_at

### Relationships

* belongs to Project
* supports Responsibilities
* references People

---

## Note

Represents information worth remembering.

### Attributes

* id
* title
* content
* category
* created_at

### Relationships

* belongs to Project
* may reference Responsibilities
* may reference People

---

## Goal

Represents a long-term objective.

### Attributes

* id
* title
* description
* target_date
* status

### Relationships

* contains Responsibilities
* influences Planning

---

## Reminder

Represents a scheduled notification.

### Attributes

* id
* scheduled_time
* status
* repeat_rule

### Relationships

* belongs to one Responsibility
* may relate to one Event

---

## Conversation

Represents a communication session.

### Attributes

* id
* platform
* started_at
* updated_at

### Relationships

* contains Messages
* may create Responsibilities
* may create Notes

---

## Message

Represents a single exchanged message.

### Attributes

* id
* sender
* content
* timestamp
* attachments

### Relationships

* belongs to Conversation

---

# Cross-Object Relationships

```text
Project
│
├── Responsibilities
│       ├── Reminders
│       ├── Documents
│       └── People
│
├── Events
│
├── Notes
│
└── Goals

Conversation
└── Messages
```

---

# Derived Objects

These are computed, not stored directly.

## Responsibility State

Examples:

* Clear
* Attention Needed
* Critical

Computed from:

* Responsibilities
* Events
* Priorities
* Deadlines

---

## Daily Briefing

Generated from:

* Responsibilities
* Calendar
* Goals
* Context

---

## Weekly Review

Generated from:

* Completed Responsibilities
* Progress
* Goals
* Notes

---

# Design Principles

The Data Model should remain:

* Provider-independent
* Human-readable
* Stable over time
* Easy to extend
* Consistent with the Knowledge Model

Database tables, APIs, and programming languages should adapt to this model—not the other way around.
