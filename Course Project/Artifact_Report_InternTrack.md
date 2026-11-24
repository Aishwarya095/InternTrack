# KLE Technological University, Hubballi
### School of Computer Science & Engineering (AI)
### Semester VII | Academic Year 2026–27
---
## Artifact Report
# InternTrack: Autonomous Internship Application & Tracking Portal
### A Human-Governed, Evidence-Grounded Lifecycle System built through the 14-Lab Agentic AI Worklet Method
**Artifact 10 · Agentic AI (26ECAC401) · Team 11 · Division B**

| No. | Student Name | USN | Division | Role in Project |
|:---:|:---|:---:|:---:|:---|
| 1 | **Prerna A** | `01FE23BCI037` | Division B | System Architecture & LangGraph State Machine |
| 2 | **Aishwarya B A** | `01FE23BCI095` | Division B | Agent Swarms, Verification Runner & Deployment |
| 3 | **Sonu Vaishnavi** | `01FE23BCI093` | Division B | Memory Engine, Skills & Grounding Agent |
| 4 | **Nischita N** | `01FE23BCI106` | Division B | Governance, Safety Gates & Audit Trail |

| Item | Link |
|:---|:---|
| **GitHub Repository** | [https://github.com/Aishwarya095/InternTrack](https://github.com/Aishwarya095/InternTrack) |
| **Live Application** | [https://interntrack-pv3r.onrender.com](https://interntrack-pv3r.onrender.com) |

---

## Contents
1. **Abstract**
2. **Introduction and Problem Statement**
   - 2.1 Background
   - 2.2 Problem Statement
   - 2.3 Scope
3. **Objectives**
4. **Expectations and Coverage**
5. **System Architecture**
   - 5.1 Layered Architecture
   - 5.2 Agent Graph
   - 5.3 Implemented Runtime Graph
   - 5.4 Pipeline Protocol (Step-by-Step)
   - 5.5 Data Model
   - 5.6 Eligibility & Priority Verification
   - 5.7 Vacancy Management & Atomic Decrements
   - 5.8 Draft Generation, Progress Journals & Evaluation
   - 5.9 Grounding and Validation
   - 5.10 Approval State Machine and Governance
   - 5.11 Module and Project Structure
   - 5.12 Team Task Allocation and Project Plan
6. **Technology Stack**
7. **Implementation Against Each Expectation**
   - 7.1 Agents
   - 7.2 Skills
   - 7.3 MCP
   - 7.4 OpenCLA / OpenClaw Runtime
   - 7.5 Swarms
   - 7.6 Deep Research
   - 7.7 Cloud SDLC
8. **Supporting Capabilities**
   - 8.1 Typed Tools
   - 8.2 Memory and Retrieval
   - 8.3 LangGraph Node Graph
   - 8.4 Safety and Governance
   - 8.5 Domain Specialisation
9. **End-to-End Walkthrough**
10. **Lab-wise Coverage (Labs 1–14)**
11. **Assignments (Labs 1–14: 28 Graded Tasks)**
12. **Repository and Run Steps**
   - 12.1 Project Code Layout
   - 12.2 Run Locally
   - 12.3 Cloud Deployment Run
13. **Results**
14. **Conclusion and Future Enhancements**
15. **References**
- **Appendix A: Setup and Execution Guide**
- **Appendix B: Master Verification Runner Script**
- **Appendix C: Specification Coverage Checklist**

---

## 1. Abstract
In higher education technical curricula, 8th-semester industry internships carry mandatory academic weight (**12 credits under AICTE / NEP 2020**). However, the manual administration of this lifecycle presents critical bottlenecks: students discover corporate openings through fragmented spreadsheets; coordinators spend weeks manually cross-checking CGPA thresholds and backlogs; off-campus progress journals lack in-semester visibility; and final grading paperwork lacks an auditable trail.

This report presents **InternTrack (powered by AURA)**, an autonomous, regulatory-compliant multi-agent lifecycle system that turns student internship applications into verified, scheduled placements, tracks weekly progress journals, and computes credit clearance. The system is built as a coordinator plus specialist agents orchestrated with **LangGraph**, utilizing typed deterministic tools, 6 reusable schema-validated skills, two-tier memory (session draft state + episodic SQLite audit history), and a governed MCP-style gateway.

It runs inside an OpenClaw-style governed agent runtime equipped with execution step budgets, a complete cryptographic audit log (SHA-256 hash chaining), and crash-recovery checkpoints. A strict **Human-in-the-Loop** principle is enforced: AI agents propose, screen, and rank, but only authenticated faculty coordinators and Heads of Department (HODs) hold authority to sanction placements and award academic credits. Rejection requires a mandatory written justification to eliminate arbitrary actions. All 14 course laboratory milestones are fully realized, backed by **81 automated acceptance tests passing with a 100% pass rate**, deployed live on Render Cloud.

---

## 2. Introduction and Problem Statement

### 2.1 Background
Agentic AI systems transcend stateless conversational chatbots: they pursue an autonomous goal over multiple iterative steps, call typed tools to interact with live databases and APIs, maintain persistent episodic memory, and coordinate heterogeneous specialist agents. The Agentic AI course (26ECAC401) develops these foundations across fourteen hands-on labs. Team 11 applied this methodology to the **Internship Application & Tracking Portal (Chapter 10 Capstone Worklet)**.

### 2.2 Problem Statement
University faculty coordinators, departmental heads, and students face five recurring operational failures:
1. **Scattered Opportunity Discovery:** Students rely on unvetted, informal channels; vacancies and eligibility requirements are opaque.
2. **Inconsistent Eligibility Checks:** CGPA cutoffs, active backlogs, and academic credits are checked manually across disparate spreadsheets, leading to human error.
3. **Overbooking & Seat Clashes:** In-demand corporate seats (e.g. Infosys, TCS, Google) are over-allocated when multiple faculty members review applications concurrently without synchronized vacancy locks.
4. **Zero In-Semester Progress Visibility:** Once a student joins an off-campus enterprise, mentors have no structured, verifiable mechanism to track weekly work logs, milestones, or industry supervisor assessments.
5. **Unverifiable Final Evaluations:** End-of-semester credit awarding relies on rushed paper evaluations lacking an auditable paper trail.

**Problem Statement:** Design and implement an autonomous agentic system that manages the complete 8th-semester internship lifecycle—discovery &rarr; eligibility verification &rarr; multi-preference matching &rarr; coordinator/HOD sanction &rarr; journal tracking &rarr; final credit evaluation—while guaranteeing that no consequential action is taken without explicit human approval and that every system event is cryptographically auditable.

### 2.3 Scope
The system covers engineering undergraduate students (tested across a cohort of 65 authentic KLE Tech profiles), 55 corporate opportunities (20 Top MNCs, 5 grading test fixtures, 30 live Indeed postings), a 4-tier preference submission model, weekly progress journal reviews, and final rubric grading.

---

## 3. Objectives
1. **Autonomous Preference Optimization:** Convert plain-English student career goals into a structured 4-tier company preference application using a Clarify–Plan–Revise loop.
2. **Deterministic Eligibility Tooling:** Enforce academic policies (CGPA &ge; threshold, backlogs == 0) via typed database tools rather than non-deterministic LLM prompts.
3. **Multi-Agent Swarm Concurrency:** Parallelize candidate evaluation across preferences using LangGraph Fan-Out / Fan-In worker swarms.
4. **Strict Human-in-the-Loop Governance:** Enforce mandatory interrupt gates (`PAUSED_FOR_COORDINATOR_APPROVAL`) before committing placements or awarding credits.
5. **Real-Time Dynamic Vacancy Locking:** Implement atomic database decrements preventing seat overbooking.
6. **Deep Grounding & Evidence Citations:** Ground all company recommendations in verified career portals and AICTE minimum stipend floors.
7. **Operational Resilience & Self-Healing:** Implement circuit breakers, targeted regrading, and failure retry budgets.
8. **Cloud Deployment:** Deploy a production web application with zero-downtime automated CI/CD.

---

## 4. Expectations and Coverage
| # | Course Expectation | Evaluation Criteria | InternTrack Implementation | Section |
|:---:|:---|:---|:---|:---:|
| **1** | **Assignment Submission** | On time, complete, meets specification | 28 graded lab assignments (Labs 1–14, 2 per lab) with code & verified outputs | Sec. 11 |
| **2** | **GitHub Repo Readiness** | Clean structure, documentation, commit history | Comprehensive repository with run guides, tests, and CI/CD automation | Sec. 12 |
| **3** | **Agents** | Clear goals, typed tools, goal completion | Coordinator Agent + 7 specialized sub-agents | Sec. 7.1 |
| **4** | **Skills** | Schema-typed, reusable procedural modules | 6 reusable skills with Pydantic v2 validation contracts | Sec. 7.2 |
| **5** | **MCP** | Standardized gateway with governance | Governed MCP gateway with 11 capabilities, bearer auth, and scoping | Sec. 7.3 |
| **6** | **OpenCLA / OpenClaw Runtime** | Execution budgets, audit logging, crash recovery | Governed runtime: max 50 steps, JSONL audit trail, and atomic checkpoints | Sec. 7.4 |
| **7** | **Swarms** | Parallel agent coordination, merge & critique | Lab 8 LangGraph parallel fan-out swarm across 4 student preferences | Sec. 7.5 |
| **8** | **Deep Research** | Grounded in evidence, hallucination rejection | Indeed live job scraping + verified catalog grounding with AICTE stipend verification | Sec. 7.6 |
| **9** | **Cloud SDLC** | Build, test suite, and cloud deployment | 81/81 automated acceptance tests passing; live deployment on Render Cloud | Sec. 7.7 |

---

## 5. System Architecture

### 5.1 Layered Architecture
The platform is organized into six clean, decoupled architectural layers:
```
┌────────────────────────────────────────────────────────────────────────┐
│ L1: Presentation Layer — Responsive Web Dashboard & 14-Lab Studio      │
│ (Operational Dashboard, Form, Matcher, Queues, Journals, Audit UI)     │
├────────────────────────────────────────────────────────────────────────┤
│ L2: Coordination Layer — LangGraph StateGraph & Governed Runtime       │
│ (State Machine, Conditional Edges, Step Budgets, Human Gate Interrupt) │
├────────────────────────────────────────────────────────────────────────┤
│ L3: Agents & Skills Layer — Multi-Agent Swarm & Schema-Typed Skills     │
│ (Coordinator, Profiler, Matcher, Validator, Swarm Workers, Specialists)│
├────────────────────────────────────────────────────────────────────────┤
│ L4: Connector Layer — Governed Model Context Protocol (MCP) Gateway    │
│ (Typed RPC surface, Bearer Token Auth, Role-Based Scoping & Redaction) │
├────────────────────────────────────────────────────────────────────────┤
│ L5: Governance & Audit Layer — Human Approval Gate & Hash-Chained Log  │
│ (Coordinator Desk, HOD Sanction, Mandatory Rejection Reasons, Rollback)│
├────────────────────────────────────────────────────────────────────────┤
│ L6: Data Persistence Layer — SQLite3 Relational Engine & Fixture Store │
│ (Students, Opportunities, Submissions, Journals, Evaluations, Audit)   │
└────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Agent Graph
The Coordinator agent orchestrates specialized workers:
- **Student Profiler:** Ingests USN, fetches verified academic history, and extracts resume skills.
- **Eligibility Agent:** Evaluates hard university constraints (CGPA cutoff, active backlogs, earned credits).
- **Parallel Swarm Workers:** Concurrently evaluate preference slots 1 through 4.
- **Barrier Reducer:** Aggregates worker outputs and resolves ranking conflicts.
- **Governance Gatekeeper:** Enforces human authorization before executing atomic state changes.

### 5.3 Implemented Runtime Graph (LangGraph)
In code (`aura/lab8_langgraph.py`), the workflow executes as an explicit 17-node directed graph:
```
[Intake Node] ──► [Planner Node] ──► [Profile Extraction]
                                             │
                                             ▼
                             [Parallel Swarm Fan-Out]
                             ├── Worker 1: Preference 1
                             ├── Worker 2: Preference 2
                             ├── Worker 3: Preference 3
                             └── Worker 4: Preference 4
                                             │
                                             ▼
                                   [Fan-In Barrier Merge]
                                             │
                                             ▼
                                   [Constraint Validator]
                                        │          ▲
                                 (Pass) │          │ (Fail - Bounded Retry)
                                        ▼          │
                        [PAUSED_FOR_COORDINATOR_APPROVAL]
                                        │ (Human Review)
                        ┌───────────────┴───────────────┐
                        ▼                               ▼
                 [Approve Node]                  [Reject Node]
                        │                               │
                 (Atomic Decrement)              (Feedback Log)
                        │                               │
                        ▼                               ▼
                 [Publish Node] ────────────────► [Terminal End]
```

### 5.4 Pipeline Protocol (Step-by-Step)
1. **Intake & Clarify:** Ingests student USN or unstructured query; asks clarifying questions if incomplete.
2. **Profile & Memory Recall:** Retrieves verified academic credentials and checks historical rejections.
3. **Parallel Swarm Evaluation:** Spawns 4 concurrent workers to verify company eligibility and seat availability.
4. **Barrier Aggregation & Critique:** Merges worker outputs and scores candidate fit.
5. **Validation Gate:** Asserts all preconditions (valid CGPA, non-negative vacancies).
6. **Human Gate Breakpoint:** Suspends execution at `PAUSED_FOR_COORDINATOR_APPROVAL`.
7. **Coordinator Sign-Off:** Faculty reviews candidate packet; rejection requires mandatory justification.
8. **Atomic Commit & Publish:** Decrements opportunity vacancy and publishes confirmed placement record.

### 5.5 Data Model (Core Entities)
Defined using Pydantic v2 models in `core/models.py`:
- `StudentProfile`: USN, full name, branch, semester, CGPA, backlogs, skills, placement status.
- `Opportunity`: Opportunity ID, company, title, domain, min CGPA, total vacancies, filled vacancies, available vacancies, status (`PUBLISHED`, `CLOSED`).
- `StudentSubmission`: Submission ID, student USN, preferences 1–4, status (`DRAFT`, `SUBMITTED`, `COORDINATOR_APPROVED`, `REJECTED`, `CONFIRMED`).
- `ProgressReport`: Report ID, internship ID, reporting period, hours logged, work completed, mentor comments, status.
- `Evaluation`: Evaluation ID, mentor score (40), presentation score (30), report score (30), total score (100), academic credits (12), grade.
- `AuditEvent`: Event ID, timestamp, actor, action, previous state, new state, cryptographic hash.

### 5.6 Eligibility & Priority Verification
Eligibility scoring follows deterministic institutional rules:
- **Baseline Requirement:** `CGPA >= min_cgpa AND active_backlogs == 0`.
- **Pre-Placed Bypass:** Students holding verified campus offers (`PLACED_COMPANY`) bypass open pool matching.
- **Vacancy Invariant:** `available_vacancies = total_vacancies - filled_vacancies >= 0`.

### 5.7 Vacancy Management & Atomic Decrements
To prevent race conditions, vacancy decrements execute inside single SQLite transactions:
```sql
UPDATE opportunities
SET filled_vacancies = filled_vacancies + 1,
    available_vacancies = available_vacancies - 1
WHERE id = ? AND available_vacancies > 0;
```
If `available_vacancies` reaches 0, the opportunity status shifts to `CLOSED`.

### 5.8 Module and Project Structure
| Module / Folder | Responsibility |
|:---|:---|
| `Course Project/Codebase/server.py` | Central REST API server & HTTP request dispatcher |
| `Course Project/Codebase/aura/` | Multi-agent implementations for Labs 1 to 14 |
| `Course Project/Codebase/database/` | SQLite schema DDL, DB connection manager, seed scripts |
| `Course Project/Codebase/workflows/` | Student profiles, submissions, vacancy management, tracking |
| `Course Project/Codebase/static/` | Responsive web dashboard UI, CSS styles, JavaScript controllers |
| `Course Project/Codebase/tests/` | Unit, integration, and master acceptance test suites |
| `Assignments/` | Standalone source code & test runners for all 28 course assignments |

### 5.9 Team Task Allocation
| Team Member | Functional Area | Specific Deliverables |
|:---|:---|:---|
| **Prerna A** | System Architecture & Graph Execution | LangGraph StateGraph design, conditional edge routing, Labs 1, 7, and 14 |
| **Aishwarya B A** | Agent Swarms, Verification & Deployment | Lab 8 parallel swarm, master verification runner (81 tests), Render deployment |
| **Sonu Vaishnavi** | Memory Systems, Skills & Grounding | Dual-tier memory, 6 reusable typed skills, Lab 9 deep research |
| **Nischita N** | Governance, Safety Gates & Audit Trail | Human-in-the-loop gates, PII redactor, SHA-256 audit log, rollback engine |

---

## 6. Technology Stack
| Area | Technology | Used For |
|:---|:---|:---|
| **Programming Language** | Python 3.11+ | Backend server, agent logic, testing harnesses |
| **Agent Orchestration** | LangGraph (`StateGraph`) | Cyclical multi-agent state machines, parallel fan-out, interrupts |
| **Web & REST Framework** | Python Native HTTP / REST API | High-throughput, zero-dependency REST dispatcher |
| **Data Validation** | Pydantic v2 | Schema enforcement, typed tool contracts, skill I/O |
| **Database Engine** | SQLite3 (WAL Mode) | Relational persistence with foreign keys and strict constraints |
| **Frontend Architecture** | HTML5, Modern CSS3, Vanilla JS | Reactive, zero-dependency web dashboard and 14-Lab Studio |
| **Testing Harness** | Python `unittest` | Automated acceptance test suites across all 14 labs |
| **Cloud Hosting** | Render Cloud Platform | Containerized production deployment with automated CI/CD |

---

## 7. Implementation Against Each Expectation

### 7.1 Agents (Expectation 3)
The system deploys a Coordinator Agent (`AURA`) commanding 7 specialized worker agents. Each agent operates with a bounded system prompt, explicit typed tools, and structured Pydantic inputs/outputs.
- *Evidence:* `Course Project/Codebase/aura/coordinator.py`, `lab2_tools.py`, `lab13_specialists.py`.

### 7.2 Skills (Expectation 4)
Repeatable business procedures are encapsulated into 6 reusable skills extending `BaseSkill`. Each skill enforces input validation and returns checkable schemas:
1. `InternshipPlanSkill`: Generates 4-month academic blueprints.
2. `ApplicationValidatorSkill`: Verifies institutional eligibility constraints.
3. `OpportunityMatchingSkill`: Computes semantic skill-gap matches.
4. `DocumentFormatterSkill`: Formats official ATS resumes and PDF dossiers.
5. `ProgressJournalSkill`: Validates weekly journal compliance.
6. `EvaluationRubricSkill`: Implements the 100-point academic grading rubric.
- *Evidence:* `Course Project/Codebase/aura/lab3_skills.py`.

### 7.3 MCP Gateway (Expectation 5)
External systems (college ERP, student records, live job boards) are accessed through a unified Model Context Protocol (MCP) gateway (`mcp_connector`). The gateway enforces Bearer token authentication, role scoping (`STUDENT`, `COORDINATOR`, `HOD`), and token redaction in logs.
- *Evidence:* `Course Project/Codebase/aura/lab5_connector.py`.

### 7.4 OpenCLA / OpenClaw-Style Governed Runtime (Expectation 6)
Agents execute inside a sandboxed runtime container that enforces:
- **Run Budgets:** Limits execution to 50 steps, 20 LLM calls, and 300 seconds.
- **Audit Logging:** Every state transition is recorded in an append-only JSONL log with SHA-256 hash chaining.
- **Checkpointing:** State snapshots enable crash recovery without repeating completed steps.
- *Evidence:* `Course Project/Codebase/aura/lab6_runtime.py`.

### 7.5 Multi-Agent Swarms (Expectation 7)
Lab 8 implements parallel agent swarms. When a student submits 4 preferences, the coordinator spawns 4 worker agents across parallel threads. Each worker checks company eligibility and vacancies concurrently. A barrier reducer merges outputs and resolves ranking conflicts.
- *Evidence:* `Course Project/Codebase/aura/lab8_langgraph.py`.

### 7.6 Deep Research & Evidence Grounding (Expectation 8)
Job recommendations must be grounded in verified evidence. The system queries active postings via live Indeed scraping and verifies them against the institutional catalog. Postings lacking verified URLs or offering stipends below the AICTE floor are rejected.
- *Evidence:* `Course Project/Codebase/aura/lab9_grounding.py`, `external_research.py`.

### 7.7 Cloud SDLC (Expectation 9)
All features are developed under test-driven green gate validation. The repository includes automated acceptance test suites for all 14 labs. Pushes to `main` trigger automated cloud deployment on Render.
- *Evidence:* `run_master_verification_1_to_14.py`, `https://interntrack-pv3r.onrender.com`.

---

## 8. Supporting Capabilities

### 8.1 Typed Tools
12 deterministic tools extend `BaseTool` with strict Pydantic argument schemas: `get_student_profile`, `list_opportunities`, `check_eligibility`, `decrement_vacancy`, `submit_application`, `coordinator_review`, `hod_sanction`, `log_journal`, `evaluate_student`, `get_audit_log`, `sync_indeed`, `rollback_state`.

### 8.2 Memory and Retrieval
- **Short-Term Session Memory:** `SessionState` maintains transient conversational context.
- **Long-Term Episodic Storage:** SQLite database tracks student application histories, rejection feedback, and supervisor reviews.
- **Lexical/Semantic Retrieval:** Cosine similarity over TF-IDF vectors matches student skills to job descriptions.

### 8.3 LangGraph Node Graph
State orchestration uses LangGraph's native `StateGraph` with typed states, conditional routing edges, parallel fan-out branches, and interrupt checkpoints.

### 8.4 Safety and Governance
- **Human-in-the-Loop:** Placement approvals and credit sign-offs require authenticated human credentials.
- **Mandatory Rejection Reasons:** Coordinators cannot reject an application without providing justification.
- **PII Masking:** Student phone numbers and emails are automatically redacted before external processing.
- **Atomic Rollback:** Faculty can revert the system to a previous release version in one click.

### 8.5 Domain Specialisation
Pluggable specialist agents enforce formal invariants across technical disciplines:
- Python AI/ML Specialist (PyTorch, KV-Cache)
- C/POSIX Systems Specialist (Valgrind-clean memory, semaphores)
- SQL/DBMS Specialist (3NF normalization, index optimization)
- Java Enterprise Specialist (Spring Boot 3, `@Transactional` boundaries)

---

## 9. End-to-End Walkthrough
1. **Student Ingestion:** Student *Ananya Sharma* (`1KG21CS008`) accesses the portal.
2. **Resume Generation:** System fetches verified academic data (CGPA 9.1, B.E. CSE) and generates an ATS-standard resume.
3. **Skills Auto-Matching:** System compares resume skills against 54 active opportunities; identifies *Infosys InStep* (83% match).
4. **Preference Submission:** Student submits 4 preferences (Infosys, TCS, Bosch, Google).
5. **Swarm Auto-Ranking:** Lab 8 parallel swarm evaluates all 4 preferences concurrently and ranks them optimally.
6. **Coordinator Gate:** Execution pauses at `PAUSED_FOR_COORDINATOR_APPROVAL`.
7. **Coordinator Sign-Off:** Faculty coordinator reviews candidate packet and clicks Approve.
8. **Atomic Vacancy Decrement:** Infosys available vacancies decrement from 6 to 5 seats.
9. **Progress Journal Tracking:** Student logs weekly journal reports during the internship.
10. **Final Evaluation:** Evaluator grades final viva and report (94/100, S Grade); 12 academic credits are officially awarded.

---

## 10. Lab-wise Coverage (Labs 1–14)
| Lab | Topic | Implementation Mechanism | Status |
|:---:|:---|:---|:---:|
| **1** | **Agent vs Chatbot** | Goal-driven Clarify &rarr; Plan &rarr; Revise loop with multi-round feedback | **PASS (100%)** |
| **2** | **Tool-Using Agent** | Typed database tools for student profile & vacancy lookups | **PASS (100%)** |
| **3** | **Skill Creation** | 6 schema-validated skills (`InternshipPlan`, `ApplicationValidator`, etc.) | **PASS (100%)** |
| **4** | **Memory & Retrieval** | Two-tier memory: working session draft + long-term episodic history | **PASS (100%)** |
| **5** | **MCP Connector** | Governed gateway with 11 capabilities, bearer auth & RBAC | **PASS (100%)** |
| **6** | **Controlled Runtime** | Step budgets (max 50), cryptographic audit logging & checkpoints | **PASS (100%)** |
| **7** | **Agentic Node Graph** | 17-node LangGraph StateGraph with conditional edges & human gate | **PASS (100%)** |
| **8** | **Parallel Swarm** | Concurrent fan-out worker swarm across 4 student preferences | **PASS (100%)** |
| **9** | **Deep Research** | Indeed live job scraping + verified catalog grounding with AICTE floor | **PASS (100%)** |
| **10** | **Cloud Operations** | Circuit breaker, self-healing targeted repair & retry budgets | **PASS (100%)** |
| **11** | **Agentic SDLC** | Spec-driven build factory with automated green-gate acceptance testing | **PASS (100%)** |
| **12** | **Safety & Governance** | PII redactor, mandatory rejection reasons & 1-click atomic rollback | **PASS (100%)** |
| **13** | **Discipline Specialists** | Pluggable domain specialists for AI/ML, Systems, SQL, and Java | **PASS (100%)** |
| **14** | **Capstone Final** | Unified cloud portal managing complete lifecycle & 12 credit clearance | **PASS (100%)** |

---

## 11. Assignments (Labs 1–14: 28 Graded Tasks)
All 28 graded assignments from the Agentic AI Lab Guide were implemented as standalone Python programs with `# [A1]` / `# [A2]` tags:
| Lab | Reference Program | Assignment 1 (A1) | Assignment 2 (A2) |
|:---:|:---|:---|:---|
| **1** | Planner Agent | Multi-round user plan revision | Scheduling conflict detection & reporting |
| **2** | Tool Calling Agent | Draft-only notification tool | 3-tool chain: fetch &rarr; filter &rarr; evaluate |
| **3** | Reusable Skills | Best-supported claim selector | Low-evidence input rejection handling |
| **4** | Two-Tier Memory | Multi-topic session isolation | Memory retention & staleness warnings |
| **5** | Governed MCP Server | Discoverable capability directory | Scoped secure file/profile reader |
| **6** | Agent Runtime | Per-user session rate limiter | Audit logging & failure escalation |
| **7** | Graph Workflow | Security-scan validation node | Bounded retry loop before escalation |
| **8** | Swarm Coordination | Multi-role budget conflict resolver | Distributed role-based critique |
| **9** | Grounding Engine | Contradictory source conflict detection | Source-quality confidence weighting |
| **10** | Resilience & Repair | Connection-pool exhaustion recovery | Safe self-healing targeted regrading |
| **11** | SDLC Factory | Automated PDF report generator | Deliberate fault injection caught by tests |
| **12** | Governance Gates | Financial/credit ceiling enforcement | Audit rollback after invalid proposals |
| **13** | Domain Specialists | Predictive maintenance load forecaster | Multi-reading trend escalation handler |
| **14** | Help-Desk Capstone | Secure password-reset routing skill | Adversarial prompt-injection defense |

---

## 12. Repository and Run Steps

### 12.1 Project Code Layout
```
InternTrack/
├── Assignments/             # 28 graded standalone assignments (Labs 1 to 14)
├── Course Project/
│   ├── Codebase/
│   │   ├── aura/            # Labs 1 to 14 multi-agent implementations
│   │   ├── core/            # Authentication, PII masking, audit logging
│   │   ├── database/        # SQLite schema DDL, seed data, initial catalog
│   │   ├── static/          # Responsive web UI, CSS styles, JavaScript
│   │   ├── tests/           # Acceptance test suites
│   │   ├── workflows/       # Business workflows for students, reviews, tracking
│   │   ├── server.py        # Central REST API server & HTTP dispatcher
│   │   └── run_master_verification_1_to_14.py # 81-test master runner
│   ├── Artifact_Report_InternTrack.md   # Complete Technical Report (Markdown)
│   └── Artifact_Report_InternTrack.docx # Formatted Official Technical Report
├── requirements.txt         # Production dependencies
└── README.md                # Project landing documentation & quickstart
```

### 12.2 Run Locally
```bash
# 1. Clone repository
git clone https://github.com/Aishwarya095/InternTrack.git
cd InternTrack

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start backend server
cd "Course Project/Codebase"
python server.py

# 4. Open in browser: http://localhost:8000
```

### 12.3 Run Master Verification Test Suite
```bash
cd "Course Project/Codebase"
python run_master_verification_1_to_14.py
```

### 12.4 Cloud Deployment Run
Open live instance: [https://interntrack-pv3r.onrender.com](https://interntrack-pv3r.onrender.com)

---

## 13. Results

### 13.1 Key Performance Indicators (KPIs)
| Objective / KPI | Target | Measured Result | Status |
|:---|:---:|:---:|:---:|
| **Automated Test Pass Rate** | 100% | **81 / 81 Tests Passed (100.0%)** | **MET** |
| **Master Test Execution Time** | < 90s | **60.3s across all 14 Labs** | **MET** |
| **Student Profiles Seeded** | &ge; 50 | **65 authentic KLE Tech profiles** | **MET** |
| **Corporate Opportunities Catalog**| &ge; 30 | **55 opportunities (20 MNCs, 5 Fixtures, 30 Live)** | **MET** |
| **Consequential Actions without Human Approval** | 0 | **0 (Strictly gated at Human Breakpoint)** | **MET** |
| **Vacancy Overbooking Rate** | 0% | **0% (Atomic transactional locks)** | **MET** |
| **Cloud Service Uptime** | 99% | **Live & operational on Render** | **MET** |

### 13.2 Master Lab Acceptance Results
```
================================================================================
INTERNTRACK (AURA) — MASTER VERIFICATION RUNNER FOR LABS 1 TO 14
Institution: KLE Technological University, Hubli
Course: 26ECAC401 Agentic AI — 15 Worklets / 14-Lab Build Book (Chapter 10)
================================================================================
[*] Labs 1-7 (Main Acceptance Suite)              | Tests: 13 | Passed: 13 | Status: PASS (100% OK)
[*] Lab 8 (Parallel Swarm & Human Gate)           | Tests: 13 | Passed: 13 | Status: PASS (100% OK)
[*] Lab 9 (Deep Research & Grounding)             | Tests:  9 | Passed:  9 | Status: PASS (100% OK)
[*] Lab 10 (Ops Resilience & Self-Healing)        | Tests:  9 | Passed:  9 | Status: PASS (100% OK)
[*] Lab 11 (SDLC Factory & Green Gate)            | Tests:  9 | Passed:  9 | Status: PASS (100% OK)
[*] Lab 12 (Safety, Masking & Rollback)           | Tests:  9 | Passed:  9 | Status: PASS (100% OK)
[*] Lab 13 (Discipline Specialists & Invariants)  | Tests:  9 | Passed:  9 | Status: PASS (100% OK)
[*] Lab 14 (Capstone Team-Owned System)           | Tests: 10 | Passed: 10 | Status: PASS (100% OK)
================================================================================
GRAND TOTAL: 81 Tests Run across all 14 Labs
             81 Passed | 0 Failed | 0 Errors
OVERALL PASS RATE: 100.0%
================================================================================
```

---

## 14. Conclusion and Future Enhancements
InternTrack demonstrates the complete 14-lab Agentic AI methodology applied to higher education internship lifecycle management. By coupling LangGraph state machine orchestration with deterministic database tooling, parallel swarms, operational resilience, and strict Human-in-the-Loop governance, the platform resolves long-standing administrative bottlenecks. Academic integrity is preserved by code-level side-effect guards: AI agents propose, screen, and rank, but human faculty members hold exclusive authority to sanction placements and award academic credits.

### Future Enhancements:
1. **Automated WhatsApp/SMS Coordinator Alerts:** Integrate webhooks to notify coordinators of pending approvals.
2. **Weekly Video Journal Analysis:** Implement multimodal vision models to verify student video presentations during remote internships.
3. **Federated University Multi-Tenancy:** Expand database schemas to support cross-university consortiums and statewide placement boards.

---

## 15. References
1. Agentic AI 14-Lab Worklet Build Book, Chapter 10 — Internship Application & Tracking Portal.
2. S. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020.
3. S. Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models," in *Proc. ICLR*, 2023.
4. LangGraph Documentation — StateGraph, Reducers, and Checkpointing (`langchain-ai.github.io/langgraph`).
5. Model Context Protocol (MCP) Specification, Anthropic, 2024.
6. AICTE National Internship Policy & NEP 2020 Guidelines for 8th Semester Academic Credits.
7. OWASP Top 10 for Large Language Model Applications, OWASP Foundation, 2024.
