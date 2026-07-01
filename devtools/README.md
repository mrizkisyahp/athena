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

## Prompt Library
Prompts are version-controlled engineering assets. They are treated as source code, not documentation or logic.
Changes to prompts should be reviewed and merged just like any other implementation change to the codebase. Each prompt defines the strict persona, inputs, and boundaries for an agent in the AI Engineering Pipeline.

## Execution Engine
The `PipelineEngine` is strictly responsible for planning the workflow.
- It determines which agents participate and in what order.
- It does **not** execute agents.
- Networking is intentionally out of scope.
- The Human Operator and Development Orchestrator (Antigravity) remain responsible for actually orchestrating and executing the planned stages.

## Run History
The pipeline remembers every execution via `RunHistory`.
- It is in-memory today.
- Persistence is intentionally deferred.
- It is designed for future auditing and engineering traceability, so the pipeline can answer what happened in past PRs.

## Provider Architecture
The pipeline depends on the `BaseProvider` abstraction.
- Concrete providers live behind this abstraction.
- Networking belongs to implementations, not the engine.
- New providers can be added without modifying the engine.

## Concrete Providers
`BaseProvider` defines the contract for all providers. 
The `NineRouterProvider` is one implementation designed for the 9router service. 
- It is responsible only for transport (translating requests and responses).
- Retries and orchestration are intentionally deferred.
- Provider implementations should remain "boring" translation layers.
- Additional providers can be added without modifying the engine.

## Runtime
The Execution Runtime is the bridge between planning and execution.
- **Runtime** executes.
- **Engine** plans.
- **Provider** communicates.
- **Antigravity** coordinates.
These four responsibilities remain independent. The Runtime is intentionally "dumb" and strictly executes the plan sequentially, halting on any failure.

## Development Lifecycle
The canonical workflow for building Athena is:
1. **Technical Lead** defines the product vision and PR specifications.
2. **Human Operator** passes the work between systems and makes final engineering decisions.
3. **Antigravity (Development Orchestrator)** receives the work and routes it through the pipeline.
4. **Pipeline Engine** plans the exact execution stages.
5. **Specialist Agents** (Architect, Executor, DB Reviewer, QA) execute the stages.
6. **Run History** stores the executed pipeline run for auditing.
7. **Technical Lead Review** accepts or rejects the final output.

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
