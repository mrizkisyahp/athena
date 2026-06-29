# KNOWLEDGE_MODEL.md

# Knowledge Model

## Purpose

This document defines how Athena understands the user's world.

It is independent of databases, APIs, or external services.

Every integration (Google Calendar, GitHub, WhatsApp, Google Drive, etc.) should translate into these concepts.

Athena should think in knowledge, not software.

---

# Core Philosophy

Everything Athena knows belongs to one or more concepts.

External services are merely different sources of the same knowledge.

For example:

Google Calendar stores Events.

Google Drive stores Documents.

GitHub stores Projects and Responsibilities.

Athena reasons about Events, Documents, Projects, and Responsibilities—not about Google or GitHub.

---

# Core Concepts

## Responsibility

The most important concept in Athena.

A Responsibility represents anything the user is expected to complete, monitor, or remember.

Examples:

* Assignment
* Meeting preparation
* Employee review
* Pay electricity bill
* Review pull request
* Renew passport
* Buy groceries

A Responsibility may have:

* Due date
* Priority
* Status
* Project
* Related people
* Related documents
* Notes
* Source
* Reminder
* Dependencies

---

## Project

Projects group related responsibilities.

Examples:

* University
* Athena
* Internship
* Personal
* Finance

Projects provide context for planning and prioritization.

---

## Event

An Event represents something that happens at a specific time.

Examples:

* Lecture
* Meeting
* Presentation
* Birthday
* Appointment

Events occupy time.

Responsibilities require work.

A Responsibility may create an Event.

An Event may generate Responsibilities.

---

## Person

Any individual known to Athena.

Examples:

* User
* Employee
* Lecturer
* Friend
* Client

People may own responsibilities, participate in events, create documents, or belong to projects.

---

## Document

Any piece of stored information.

Examples:

* PDF
* Spreadsheet
* Image
* Drive File
* Report
* Receipt
* Presentation

Documents support Responsibilities and Projects.

---

## Conversation

A communication between the user and another person or system.

Examples:

* WhatsApp
* Email
* Discord
* Telegram

Conversations may generate Responsibilities, Decisions, or Notes.

---

## Note

Information worth remembering.

Notes may contain:

* Ideas
* Meeting summaries
* Preferences
* Decisions
* Research

Notes become part of Athena's long-term memory.

---

## Reminder

A Reminder is not a Responsibility.

A Reminder is a scheduled notification about a Responsibility or Event.

Multiple reminders may exist for a single Responsibility.

---

## Goal

A long-term desired outcome.

Examples:

* Graduate university
* Launch Athena
* Save 20 million IDR
* Exercise three times per week

Goals help Athena prioritize Responsibilities over time.

---

# Relationships

Project
├── contains Responsibilities
├── contains Documents
├── contains Notes
└── contains Events

Responsibility
├── belongs to Project
├── may create Event
├── has Reminder(s)
├── references Document(s)
├── involves Person(s)
└── contributes to Goal(s)

Event
├── belongs to Project
├── involves Person(s)
├── may generate Responsibilities
└── may reference Documents

Person
├── participates in Events
├── owns Responsibilities
└── creates Documents

Conversation
├── may create Responsibilities
├── may create Notes
├── may update Projects
└── may trigger Automations

---

# Sources

Knowledge may originate from:

* User conversation
* Google Calendar
* Google Drive
* Google Sheets
* GitHub
* WhatsApp
* Email
* Local storage
* Manual input

The source should never define the knowledge itself.

It only defines where Athena learned it.

---

# Knowledge Lifecycle

Information follows a lifecycle:

Observe

↓

Understand

↓

Store

↓

Relate

↓

Reason

↓

Act

↓

Learn

Athena should continually connect new information with existing knowledge rather than storing isolated facts.

---

# Design Principle

The world is made of concepts.

Software platforms are merely different windows into those concepts.

Athena should always reason about concepts first and integrations second.
