# WORKFLOWS.md

# Athena Workflows

## Purpose

This document describes how Athena performs recurring jobs and responds to user requests.

A workflow represents a complete sequence of reasoning and actions required to achieve a meaningful outcome.

Workflows are implementation-independent.

They describe *what should happen*, not *how it is coded*.

---

# Workflow Philosophy

Every workflow follows the same lifecycle.

Understand

↓

Gather Context

↓

Reason

↓

Decide

↓

Act

↓

Update Knowledge

↓

Respond

This sequence should remain consistent across the entire system.

---

# Morning Briefing

## Trigger

Every morning at the configured time.

## Goal

Prepare the user for the day before they ask.

## Workflow

1. Load today's Responsibilities.
2. Load today's Events.
3. Load unfinished work.
4. Detect approaching deadlines.
5. Detect overdue items.
6. Review ongoing Projects.
7. Prioritize today's work.
8. Generate recommendations.
9. Produce concise briefing.
10. Send via WhatsApp.

## Expected Result

The user understands:

* What matters today
* What can wait
* What should happen next

---

# Responsibility Check

## Trigger

User asks:

* "Did I forget something?"
* "Am I okay?"
* "Can I game tonight?"

## Workflow

1. Load Responsibilities.
2. Load today's Events.
3. Calculate Responsibility State.
4. Check for conflicts.
5. Estimate remaining effort.
6. Generate recommendation.
7. Explain reasoning.
8. Respond.

## Expected Result

The user feels reassured through verified information.

---

# Reminder

## Trigger

Scheduled reminder.

## Workflow

1. Verify responsibility status.
2. Determine urgency.
3. Check for conflicts.
4. Decide whether notification is still useful.
5. Send reminder if beneficial.

Athena should avoid reminding users about already-completed work.

---

# Employee Submission

## Trigger

New file detected.

## Workflow

1. Verify employee.
2. Verify project.
3. Record upload.
4. Update spreadsheet.
5. Save document.
6. Update knowledge.
7. Notify user.

---

# Planning Session

## Trigger

User asks:

"What should I do today?"

## Workflow

1. Review Responsibilities.
2. Review Calendar.
3. Estimate workload.
4. Detect priorities.
5. Identify dependencies.
6. Build recommended schedule.
7. Explain recommendations.

---

# Document Summary

## Trigger

User shares document.

## Workflow

1. Read document.
2. Identify purpose.
3. Extract key points.
4. Detect action items.
5. Link to Project.
6. Store summary.
7. Present concise overview.

---

# Knowledge Update

## Trigger

New information becomes available.

## Workflow

1. Observe information.
2. Verify source.
3. Determine relevance.
4. Update related knowledge.
5. Link associated concepts.
6. Store memory.

Athena should continuously improve its understanding of the user's world.

---

# Automation Workflow

## Trigger

Known repetitive process.

## Workflow

1. Detect trigger.
2. Verify permissions.
3. Execute automation.
4. Validate success.
5. Update knowledge.
6. Inform user only if valuable.

---

# Conversation Workflow

## Trigger

Every incoming message.

## Workflow

1. Understand intent.
2. Retrieve context.
3. Determine capability.
4. Gather required knowledge.
5. Decide action.
6. Execute if needed.
7. Update memory.
8. Respond naturally.

Every conversation should leave Athena with a better understanding of the user whenever appropriate.

---

# Reflection Workflow

## Trigger

End of day.

## Workflow

1. Review completed Responsibilities.
2. Review unfinished work.
3. Measure progress toward Goals.
4. Detect recurring patterns.
5. Generate observations.
6. Prepare tomorrow's context.

Reflection exists to improve future planning.

---

# Workflow Design Rules

Every workflow should:

* Minimize user effort.
* Verify before acting.
* Explain important decisions.
* Update knowledge whenever new information is learned.
* Leave the user with greater clarity than before.

---

# Future Workflows

Future capabilities should be introduced as workflows rather than isolated features.

Examples include:

* Email management
* Travel planning
* Financial tracking
* Meeting preparation
* Research assistance
* Voice conversations

Regardless of complexity, every workflow should follow Athena's core lifecycle:

Understand → Gather Context → Reason → Decide → Act → Update Knowledge → Respond.
