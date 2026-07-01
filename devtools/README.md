# AI Engineering Pipeline

This directory (`devtools/`) contains the infrastructure that powers Athena's AI Engineering Pipeline.

## Constitution v1.0
1. **Human remains accountable:** No AI agent may autonomously merge code, change architecture, or modify the roadmap. The Human Operator (Rizki) always remains in control.
2. **Every AI has one specialty:** Never ask one agent to do everything.
3. **Information only flows forward:** Agents don't skip stages.
4. **Every decision is explainable:** The reasoning behind implementation choices must be logged.
5. **The pipeline is disposable:** This pipeline is development infrastructure, NOT product.

## Architectural Boundary
The `devtools/` package is strictly separated from the main Athena application (`app/`).
**CRITICAL RULE:** Deleting the entire `devtools/` directory must NEVER affect Athena's runtime, APIs, domain model, or production behavior.

## Team Roles
- **Technical Lead (ChatGPT):** Product vision, Architecture, Sprint planning, PR design, Acceptance criteria, Final approval, Roadmap
- **Human Operator (Rizki):** Makes final engineering decisions, Passes work between systems
- **Development Orchestrator (Antigravity):** Coordinates workflow, Delegation, Tracking, Reporting
- **Architect (Kimi):** Architecture
- **Backend Executor (Cohere):** Implementation
- **Database Reviewer (Llama):** Persistence
- **QA Reviewer (GPT-OSS):** Review

## Workflow
Specification 
    ↓ 
Architecture 
    ↓ 
Implementation 
    ↓ 
Review 
    ↓ 
Acceptance
