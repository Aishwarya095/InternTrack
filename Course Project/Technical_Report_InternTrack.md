# KLE Technological University, Hubballi
### School of Computer Science & Engineering (AI)
### Semester VII | Academic Year 2026–27
---
## Artifact Report
# InternTrack: Autonomous Internship Application & Tracking Portal
### A Human-Governed, Evidence-Grounded Lifecycle System built through the 14-Lab Agentic AI Worklet Method
**Artifact 10 · Agentic AI (26ECAC401) · Team 11 · Division B**

### Student Details

| No. | Student Name | USN | Division | Role / Project Responsibilities |
|:---:|:---|:---:|:---:|:---|
| 1 | **Prerna A** | `01FE23BCI037` | Division B | System Architecture & LangGraph State Machine |
| 2 | **Aishwarya B A** | `01FE23BCI095` | Division B | Agent Swarms, Verification Runner & Deployment |
| 3 | **Sonu Vaishnavi** | `01FE23BCI093` | Division B | Memory Engine, Skills & Grounding Agent |
| 4 | **Nischita N** | `01FE23BCI106` | Division B | Governance, Safety Gates & Audit Trail |

### Project Links

| Item | Link |
|:---|:---|
| **GitHub repository** | [https://github.com/Aishwarya095/InternTrack](https://github.com/Aishwarya095/InternTrack) |
| **Live application** | [https://interntrack-pv3r.onrender.com/](https://interntrack-pv3r.onrender.com/) |

---

## Table of Contents

- **1. Abstract**
- **2. Introduction and Problem Statement**
- **3. Objectives**
- **4. Expectations and Coverage**
- **5. System Architecture**
- **6. Technology Stack**
- **7. Implementation Against Each Expectation**
- **8. Supporting Capabilities**
- **9. End-to-End Walkthrough**
- **10. Lab-wise Coverage (Labs 1–14)**
- **11. Assignments**
- **12. Repository and Run Steps**
- **13. Results**
- **14. Conclusion and Future Enhancements**
- **15. References**

---

## 1. Abstract

In eighth-semester engineering curricula under NEP 2020, full-time off-campus internships carry 12 mandatory academic credits. Yet across institutional placement ecosystems, internship allocation and governance remain bottlenecked by fragmented workflows: manual Google Forms, error-prone spreadsheet verification of CGPA and backlog statuses, lack of continuous off-campus progress visibility, and last-minute document aggregation without verifiable audit trails.

This report presents **InternTrack powered by AURA**, a human-governed, evidence-grounded agentic AI system engineered to automate the entire 8th-semester internship lifecycle. The system is architected as an autonomous multi-agent hierarchy orchestrated through LangGraph: a Central Coordinator agent directs parallel role swarms for opportunity discovery and eligibility verification, a Skill Matcher that calculates cosine similarity across 100+ technical competencies, and periodic tracking agents that ingest and evaluate bi-weekly student progress journals against real company deliverables.

InternTrack operates within a sandboxed, governed runtime enforcing strict Human-in-the-Loop (HITL) checkpoints: agents autonomously discover, parse, validate, and rank opportunities, but transition to an explicit paused state awaiting mandatory faculty coordinator and HOD sign-offs. Rejections require mandatory justification reasons, and approved allocations trigger atomic database transactions that decrement vacancies in real time (preventing over-allocation). The platform features regex-based PII redaction, cryptographic SHA-256 audit trails, circuit-breaker fault tolerance, and a master test suite of 81 automated acceptance tests passing at 100% across all 14 course labs. InternTrack is deployed live on Render Cloud (https://interntrack-pv3r.onrender.com/) with a production SQLite database pre-seeded with 65 authentic KLE Tech students, 55 corporate opportunities, and 45 longitudinal progress journals.

## 2. Introduction and Problem Statement

### 2.1 Background
Agentic AI represents a fundamental paradigm shift from conversational chatbots to autonomous execution systems. Unlike conversational models that merely respond to localized prompts, agentic systems maintain persistent goals, decompose multi-phase objectives, invoke typed external tools, maintain hierarchical memory across sessions, and coordinate specialized agent swarms to alter real-world environments safely. Across the fourteen hands-on labs of the Agentic AI (26ECAC401) curriculum, our team developed and integrated these foundational principles into a production-grade capstone worklet addressing academic internship operations.

### 2.2 Problem Statement
University internship administration for final-year undergraduate students suffers from four structural points of failure:
- **Fragmented Discovery & Asymmetric Information**: Students discover opportunities through informal channels, unverified WhatsApp broadcasts, and stale bulletin boards, missing high-fit openings aligned with their technical profile.
- **Manual, Inconsistent Eligibility Verification**: Faculty coordinators spend hundreds of hours manually cross-checking university database records (CGPA cutoffs, active academic backlogs, prerequisite departmental credits) against company criteria, leading to human fatigue and compliance errors.
- **Zero Off-Campus Progress Visibility**: Once students depart for 4-to-6 month full-time industry internships, academic departments lose all continuous visibility into student attendance, mentor guidance, and technical deliverables.
- **Unverifiable Last-Minute Evaluation**: Semester-end credit certification relies on rushed paperwork, unverified student claims, and retrospective employer surveys lacking cryptographic or temporal evidence.

### 2.3 Scope
InternTrack addresses the full lifecycle of final-year undergraduate internships: student academic profile ingestion, opportunity scraping and catalog synchronization, automated semantic ATS resume building, multi-preference submission with parallel swarm auto-ranking, dual-gate faculty/HOD approvals, atomic vacancy decrement, bi-weekly progress journal evaluation with LLM evidence grounding, and immutable audit logging. Non-coursework features such as direct corporate payroll disbursement and legal enterprise contract generation remain outside the current academic scope.

## 3. Objectives

- Automate student academic ingestion and ATS resume generation using verified institutional records for 65+ authentic KLE Tech students.
- Implement semantic skill matching and eligibility verification across 50+ corporate opportunities using TF-IDF cosine similarity and deterministic rule gating.
- Orchestrate multi-preference evaluation using LangGraph parallel fan-out swarms and barrier synchronization.
- Enforce strict Human-in-the-Loop (HITL) safety breakpoints requiring faculty coordinator justification and explicit sign-off before state progression.
- Guarantee database integrity through ACID atomic transactions and constraints to prevent negative vacancy race conditions.
- Maintain evidence-grounded progress tracking by evaluating bi-weekly student journals against verified corporate benchmarks.
- Ensure enterprise governance through automated PII redaction, structured error handling with circuit breakers, and an immutable SHA-256 audit trail.
- Deploy the production application live on cloud infrastructure backed by an automated 81-test master verification suite achieving 100% pass rate.

## 4. Expectations and Coverage

The capstone worklet is formally evaluated against nine core technical rubrics. Table 3 maps each expectation to its implementation and corresponding report section.

### Table 3: Capstone Evaluation Rubrics & Coverage

| # | Expectation | What is checked | Covered by | Section |
|:---:|:---|:---|:---|:---:|
| 1 | **Assignment submission** | Complete, on time, meets brief | 28 lab assignments with code & execution output | §11 |
| 2 | **GitHub repo readiness** | README, structure, commits, run steps | Structured repository, automated master verification | §12 |
| 3 | **Agents** | Clear goal, uses tools, completes task | Coordinator + 7 specialized domain agents | §7.1 |
| 4 | **Skills** | Defined, reusable, used by agents | 6 standardized skills with Pydantic schemas | §7.2 |
| 5 | **MCP Gateway** | Servers & tools connected and working | MCP Gateway with 12 typed capability tools | §7.3 |
| 6 | **Governed Runtime** | OpenClaw-style runtime with safety limits | Bounded loop (50 steps), PII redactor, circuit breaker | §7.4 |
| 7 | **Agent Swarms** | Coordinated agents with clear roles | LangGraph Fan-Out / Fan-In parallel swarm | §7.5 |
| 8 | **Deep Research** | Evidence-grounded parsing and evaluation | ATS Resume Matcher + Journal Evidence Grounding | §7.6 |
| 9 | **Cloud SDLC** | Build, test, deployment run in cloud | Render Cloud CI/CD, 81 tests passing 100% | §7.7 |

## 5. System Architecture

### 5.1 Internship Application and Tracking Lifecycle
InternTrack models the entire academic internship progression as an immutable, state-driven lifecycle: `DRAFT` &rarr; `VALIDATING` &rarr; `PAUSED_FOR_COORDINATOR_APPROVAL` &rarr; `APPROVED` / `REJECTED` &rarr; `ALLOCATED` &rarr; `ACTIVE_INTERNSHIP` &rarr; `EVALUATING` &rarr; `COMPLETED`. State progression is strictly monotonic; no candidate can skip directly to `ALLOCATED` without satisfying prerequisite eligibility rules and clearing the coordinator sign-off checkpoint.

### Table 4: Layered System Architecture

| Layer | Architectural Responsibilities |
|:---|:---|
| **Web UI Presentation (Render)** | Responsive Single Page Application (vanilla JS, Tailwind CSS, Lucide icons) providing Student, Coordinator, and HOD dashboards. |
| **FastAPI Application Server** | High-concurrency ASGI REST API exposing endpoints for opportunity lookup, preference intake, coordinator review, and audit streaming. |
| **Governed Agent Runtime** | OpenClaw-inspired execution supervisor enforcing run budgets (50 steps max), regex PII redaction, and circuit breaker resilience. |
| **LangGraph State Engine** | StateGraph coordinating sequential and parallel multi-agent workflows with state checkpoints and human breakpoint interrupts. |
| **Specialist Agent Tier** | Coordinator, Student Profiler, Opportunity Discovery, Eligibility Verifier, Skill Matcher, Approval Router, Tracking Agent. |
| **Skills & Tools Framework** | Reusable domain procedures extending BaseSkill and BaseTool with typed Pydantic validation schemas. |
| **MCP Service Gateway** | Unified JSON-RPC connector interface dispatching live jobs, database operations, and external scraping tools. |
| **Persistence & Audit Storage** | SQLite ACID database with CHECK constraints, foreign key cascades, and SHA-256 cryptographic audit logs. |

## 6. Technology Stack

### Table 5: Comprehensive Technology Stack & Justification

| Area | Technology | Used for |
|:---|:---|:---|
| **Backend Runtime** | `Python 3.10+, FastAPI, Uvicorn` | Core application server, high-throughput REST endpoints, and async worker execution |
| **Agent Orchestration** | `LangGraph (StateGraph, Send API)` | Stateful multi-agent graphs, conditional branching, and parallel fan-out swarms |
| **Data Validation** | `Pydantic v2` | Strict schema enforcement, type validation for tools, and serialized agent state |
| **Database & ORM** | `SQLite 3 with ACID transactions` | Structured relational persistence, atomic seat decrements, and transactional integrity |
| **Vector & NLP Matcher** | `Scikit-Learn, NumPy (TF-IDF)` | Mathematical cosine similarity scoring between student resumes and opportunity catalogs |
| **LLM Intelligence** | `Groq API / Llama-3-70B & Gemini API` | Semantic resume parsing, technical competency extraction, and journal evidence synthesis |
| **Cloud Hosting & CI/CD** | `Render Cloud Platform` | Automated GitHub repository continuous deployment, production web hosting, and SSL |
| **Frontend Interface** | `Vanilla ES6+ JavaScript, Tailwind CSS` | Zero-dependency, high-performance interactive SPA with real-time reactive UI updates |
| **Verification Suite** | `Python unittest & custom runner` | 81 automated acceptance tests across Labs 1 through 14 with 100% pass rate |

## 7. Implementation Against Each Expectation

### 7.1 Agents
> **Expectation: Agents** — Agents have a clear goal, invoke typed tools, and drive tasks to verified completion.

The system implements a hierarchical multi-agent structure led by the Internship Coordinator Agent. The Coordinator decomposes complex requests, dispatches tasks to specialist agents, aggregates candidate preference matrices, and routes exceptions. Each agent executes within a deterministic bounded loop and emits typed AgentOutput schemas.

#### Table 7: Specialist Agents, Goals & Invoked Capabilities

| Agent | Goal / Responsibility | Tools & Skills Used |
|:---|:---|:---|
| **Coordinator Agent** | Supervise lifecycle, dispatch parallel swarms, route human approvals | `CoordinatorGraph, MemoryEngine, AuditLogger` |
| **Student Profiler** | Fetch and validate authentic student academic records and credits | `student_lookup_tool, gpa_verification_tool` |
| **Opportunity Discovery** | Scrape, categorize, and rank active corporate internship openings | `opportunity_search_tool, live_job_sync` |
| **Eligibility Verifier** | Verify CGPA cutoffs, active backlogs, and departmental prerequisites | `eligibility_check_tool, policy_guardrail` |
| **Skill Matcher** | Parse student resume and compute cosine match against job requirements | `skill_extraction_tool, cosine_matcher` |
| **Approval Router** | Gate state progression, enforce mandatory coordinator justification | `approval_gate_tool, atomic_decrement_tool` |
| **Tracking & Evaluation** | Monitor bi-weekly journal submissions and compute progress score | `journal_ingest_tool, evidence_grounder` |

### 7.2 Skills
> **Expectation: Skills** — Skills are modular, reusable, self-contained capabilities with typed schemas.

InternTrack abstracts complex multi-step reasoning into standardized skills extending `BaseSkill`. Each skill publishes `SkillMetadata` (name, description, input/output schemas, operational constraints) registered centrally within a `SkillRegistry`.

#### Table 9: Reusable Standardized Domain Skills

| Skill | Purpose & Execution Logic | Reusability Across Worklet |
|:---|:---|:---|
| **Eligibility Verification** | Deterministic validation of student CGPA >= cutoff and active backlogs == 0 | Used in student submission, preference ranking, and coordinator audit |
| **Semantic Skill Matching** | Extract technical keywords from resume and compute TF-IDF cosine score | Invoked in AI Resume Matcher and parallel preference swarm |
| **Opportunity Auto-Ranking** | Rank corporate openings by composite score (60% skills + 40% CGPA buffer) | Reusable across all student multi-preference applications |
| **Journal Evidence Grounding** | Cross-examine student progress claims against company milestone deliverables | Invoked bi-weekly throughout the 4-month off-campus internship |
| **Immutable Plan Locking** | Generate cryptographic SHA-256 hash of student application state | Re-locked whenever student preferences or coordinator comments change |
| **Format & Reporting** | Generate structured ATS-compliant plain-text and PDF resumes | Used in university career export and coordinator summary desks |

### 7.3 MCP Gateway
> **Expectation: MCP Gateway** — Connectors expose external capabilities through standardized, discoverable interfaces.

External integrations and enterprise tool calls are mediated through a centralized Model Context Protocol (MCP) gateway. The gateway exposes a JSON-RPC 2.0 envelope, enforces parameter validation, prevents unauthorized side effects, and provides a mock/real adapter toggle.

#### Table 11: MCP Gateway Capability Manifest

| Capability Identifier | Connected Subsystem | Side-Effect / Gating Policy |
|:---|:---|:---|
| `opportunity.search` | Opportunity Catalog / Indeed Feed | Read-only; cached queries; circuit-breaker protected |
| `student.lookup_record` | KLE Tech Academic Records DB | Read-only; regex PII masking applied on export |
| `eligibility.verify_rules` | Academic Affairs Policy Engine | Read-only; deterministic rule evaluation |
| `matcher.compute_score` | TF-IDF Vector Matching Engine | Read-only; pure mathematical cosine computation |
| `allocation.atomic_decrement` | SQLite Opportunities DB | Consequential side effect; gated by coordinator approval |
| `audit.write_event` | Cryptographic Audit Logger | Append-only immutable event stream |

### 7.4 OpenCLA / Governed Runtime
> **Expectation: Governed Runtime** — Agents execute in a sandboxed, budget-constrained runtime with crash recovery.

InternTrack executes all agent workflows inside an OpenClaw-inspired governed supervisor. The runtime enforces execution budgets (max 50 iterations, 30s timeout), PII redaction of student contact details, structured audit telemetry, and atomic transaction rollbacks upon unexpected execution failure.

### 7.5 Multi-Agent Swarms (Parallel Fan-Out / Fan-In)
> **Expectation: Swarms** — Autonomous worker agents coordinate concurrently with clear division of labor.

When a student submits four company preferences, evaluating them sequentially introduces excessive latency. InternTrack implements a parallel fan-out swarm using LangGraph's Send API. The coordinator spawns 4 concurrent worker agents that independently check company eligibility, compute skill fit, and verify live seat availability. A barrier synchronization node aggregates the worker evaluations into a single optimal preference matrix.

### 7.6 Deep Research & Evidence Grounding
> **Expectation: Deep Research** — Synthesizes structured outputs strictly grounded in verified source evidence.

In academic internship evaluation, hallucinations can lead to fraudulent credit awards. The Deep Research & Evidence Grounding agent parses bi-weekly student progress journals and validates reported work against industry project milestones. Every credit recommendation must cite verbatim source snippets from student submission logs; unsubstantiated claims are flagged for faculty investigation.

### 7.7 Cloud SDLC & Production Deployment
> **Expectation: Cloud SDLC** — Specification-driven build, automated testing, and verified cloud deployment.

The project adheres to rigorous software engineering practices: a declarative OpenAPI specification, 81 automated acceptance tests covering all 14 course labs, Git version control, and zero-downtime continuous deployment on Render Cloud connected directly to the GitHub main branch.

## 8. Supporting Capabilities

### 8.1 Typed Tools
InternTrack features 12 typed tools extending Pydantic BaseModel schemas. Tool arguments undergo automatic type casting, range checking, and validation before execution. Tools consistently return structured ToolResult objects containing output payloads, error states, and execution latencies.

### 8.2 Memory and Retrieval
The system implements a four-tiered memory architecture:
- **Short-term Session Memory**: Tracks the live LangGraph execution state, candidate preference arrays, and intermediate agent critiques.
- **Long-term Candidate Store**: Persists historical student academic backgrounds, previous project portfolios, and verified transcripts in SQLite.
- **Dynamic Vector Index**: In-memory TF-IDF vector space for real-time mathematical cosine matching across corporate vacancy catalogs.
- **Cryptographic Audit Memory**: Write-once, read-many (WORM) audit journal storing SHA-256 hashed state transitions.

### 8.3 LangGraph State Machine
The primary execution engine is structured as a LangGraph StateGraph comprising 14 discrete nodes: INTAKE &rarr; PARSE_PROFILE &rarr; DISCOVER_OPPORTUNITIES &rarr; FAN_OUT_SWARM &rarr; PARALLEL_WORKERS [1..4] &rarr; BARRIER_AGGREGATION &rarr; ELIGIBILITY_GATE &rarr; PAUSED_FOR_COORDINATOR_APPROVAL &rarr; (Human Gate) &rarr; ATOMIC_ALLOCATION &rarr; JOURNAL_TRACKING &rarr; FINAL_EVALUATION. Conditional edges safely route ineligible students to an advisory revision loop.

### 8.4 Safety, Governance and Human-in-the-Loop
Autonomous agent decision-making is strictly constrained by departmental governance policy. The system incorporates two mandatory safety gates: Coordinator Approval and HOD Departmental Sanction. An agent cannot decrement vacancies or confirm an internship without cryptographic human sign-off. Furthermore, faculty rejections enforce a mandatory text justification field to eliminate arbitrary dismissals.

### 8.5 Domain Specialisation (NEP 2020 Compliance)
InternTrack is specialized for academic engineering regulations under the National Education Policy (NEP 2020) at KLE Technological University. The system encodes institutional rules: minimum 7.0 CGPA for tier-1 MNCs, zero active backlogs at time of departure, mandatory 12-credit capstone allocation, and a minimum 16-week off-campus corporate duration.

## 9. End-to-End Walkthrough

A complete representative execution trace illustrates the seamless coordination across agents, tools, and human gates:
1. **Student Lookup**: Student Ananya Sharma (`1KG21CS008`) is looked up. The Profiler Agent retrieves verified records: CGPA 9.1, B.E. Computer Science, AWS and Java competencies.
2. **ATS Resume Generation**: The Format Skill generates a standardized ATS plain-text and PDF resume; PII masking redacts personal mobile and residential addresses.
3. **Skill Matching**: The Skill Matcher executes TF-IDF cosine comparison across 55 corporate openings. Infosys InStep yields an 83% technical match; missing skills (Python automation) are highlighted for upskilling.
4. **Multi-Preference Submission**: The student selects 4 ranked preferences (Infosys, TCS, Bosch, Google) and submits.
5. **Parallel Swarm Evaluation**: The Coordinator spawns 4 parallel worker agents via LangGraph Send API. Concurrently, worker threads verify company cutoffs and seat availability in 1.4 seconds.
6. **Human Breakpoint Interruption**: The barrier aggregator formats the proposal and transitions state to `PAUSED_FOR_COORDINATOR_APPROVAL`. The agent yields control.
7. **Coordinator Approval & Atomic Decrement**: Faculty Coordinator Dr. Ramesh reviews the verification dossier and clicks Approve. An atomic SQLite transaction decrements available vacancies from 6 to 5.
8. **Off-Campus Tracking & Audit**: Bi-weekly progress journals are ingested, grounded against corporate milestones, and committed to the immutable SHA-256 audit log.

## 10. Lab-wise Coverage (Labs 1–14)

Table 16 details how each of the fourteen curriculum labs is instantiated within the InternTrack production codebase.

### Table 16: Curriculum Lab Mapping & Technical Implementations

| Lab | Curriculum Concept | Implementation in InternTrack Capstone Worklet |
|:---:|:---|:---|
| **Lab 1** | Agent vs Chatbot | Goal-oriented student lifecycle agent with clarify &rarr; validate &rarr; approve execution loops |
| **Lab 2** | Tool-Using Agent | 12 typed tools (student_lookup, eligibility_check, vacancy_decrement) with Pydantic validation |
| **Lab 3** | Skill Creation | 6 reusable skills extending BaseSkill (Eligibility, Matching, Auto-Rank, Plan Lock, Reporting) |
| **Lab 4** | Memory & Retrieval | Session state, long-term student history, dynamic TF-IDF vector index, and audit logs |
| **Lab 5** | MCP Connector | Centralized MCP Gateway dispatching tool calls, JSON-RPC envelopes, and mock/real toggles |
| **Lab 6** | OpenClaw Runtime | Governed runtime with 50-step budget limits, PII redactor, and crash recovery checkpoints |
| **Lab 7** | Agentic Node Graph | LangGraph StateGraph with 14 nodes, conditional branching, and Human-in-the-Loop breakpoint |
| **Lab 8** | Parallel Swarm | Fan-Out / Fan-In multi-agent swarm evaluating 4 company preferences concurrently with barrier sync |
| **Lab 9** | Deep Research | Semantic ATS resume skill matching and evidence-grounded progress journal verification |
| **Lab 10** | Cloud Operations | Circuit breaker fault tolerance, exponential backoff retries, and Render cloud deployment |
| **Lab 11** | Agentic SDLC | Specification-driven design, Pydantic schemas, and 81 automated acceptance tests passing 100% |
| **Lab 12** | Safety & Governance | Dual-gate Human-in-the-Loop approval, mandatory justification reasons, and SHA-256 audit log |
| **Lab 13** | Domain Specialisation | KLE Tech NEP 2020 12-credit capstone internship rules, CGPA cutoffs, and backlog gates |
| **Lab 14** | Capstone Integration | Full end-to-end production deployment with interactive role switcher (Student/Coord/HOD) |

## 11. Assignments

All 28 assignments across the 14 course labs were completed using standard Python libraries, with modifications tagged `# [A1]` and `# [A2]`. Table 17 lists the reference program and corresponding assignment implementations.

### Table 17: Graded Lab Assignments Implementation Matrix

| Lab | Reference Program | Assignment 1 (`# [A1]`) | Assignment 2 (`# [A2]`) |
|:---:|:---|:---|:---|
| **Lab 1** | Study Planner Agent | Two-round iterative feedback refinement | Conflict detection across overlapping commitments |
| **Lab 2** | Campus Data Assistant | Draft-only notification tool with justification | Three-tool execution pipeline (read &rarr; filter &rarr; average) |
| **Lab 3** | Research-Summary Skill | Selection of best-supported claim among competitors | Handling low-evidence input with 'not stated' fallback |
| **Lab 4** | Project Assistant Memory | Multi-topic memory isolation across candidates | Memory retention and policy staleness warnings |
| **Lab 5** | Mini MCP Server | Discoverable list_capabilities tool endpoint | Scoped tool execution restricted to sandboxed directory |
| **Lab 6** | Personal Agent Runtime | Per-session execution rate limiter | Automatic fault escalation to audit log after two failures |
| **Lab 7** | Campus Event App Graph | Security policy compliance verification node | Single-retry builder with automated human escalation |
| **Lab 8** | Hackathon Planner Swarm | Role-based marketing and budget conflict handling | Distributed multi-role peer critique and aggregation |
| **Lab 9** | AI Topic Briefing | Contradictory source detection and reconciliation | Source credibility scoring and weighted synthesis |
| **Lab 10** | Deployment Diagnosis | Database connection pool exhaustion remediation | Safe automated remediation with gated rollback controls |
| **Lab 11** | CSV Export SDLC | PDF export implementation with data lineage | Automated test suite capturing intentional schema defects |
| **Lab 12** | Production Change Guardrails | Cost ceiling control with administrative sign-off | Mandatory policy re-evaluation after 5 proposals |
| **Lab 13** | Predictive Maintenance | Load forecasting domain agent | Escalation trigger based on 3-reading anomaly trends |
| **Lab 14** | Campus Help-Desk | Automated password-reset routing skill | 8-scenario adversarial prompt injection test suite |

## 12. Repository and Run Steps

### 12.1 Project Code Layout

#### Table 18: File & Module Structural Manifest

| Directory / File | Contents & Functional Role |
|:---|:---|
| `Course Project/Codebase/agents/` | CoordinatorAgent, StudentProfiler, EligibilityAgent, MatcherAgent, RouterAgent |
| `Course Project/Codebase/skills/` | BaseSkill, EligibilitySkill, MatchingSkill, RankingSkill, GroundingSkill |
| `Course Project/Codebase/tools/` | 12 typed Pydantic tools for database lookup, rule checking, and vacancy updates |
| `Course Project/Codebase/graphs/` | LangGraph workflow definitions: sequential lifecycle graph and parallel swarm graph |
| `Course Project/Codebase/connectors/` | MCP Gateway implementation with JSON-RPC dispatcher and mock/real toggles |
| `Course Project/Codebase/runtime/` | Governed runtime loop, execution budget supervisor, and PII redactor |
| `Course Project/Codebase/safety/` | Cryptographic audit logging, circuit breaker, and Human-in-the-Loop breakpoint handlers |
| `Course Project/Codebase/frontend/` | Single-page responsive web dashboard (vanilla JS, Tailwind CSS, Lucide icons) |
| `Course Project/Codebase/data/` | SQLite database pre-seeded with 65 students, 55 opportunities, and 45 journals |
| `Course Project/Codebase/tests/` | Unit, integration, and workflow test suites across Labs 1 through 14 |
| `run_master_verification_1_to_14.py` | Master test runner executing all 81 automated acceptance tests with colored summary |

### 12.2 Run Locally

To execute the InternTrack application and run the complete test suite locally:

```bash
# 1. Clone repository and navigate to root
git clone https://github.com/Aishwarya095/InternTrack.git
cd InternTrack

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Master Verification Suite across all 14 Labs
python "Course Project/Codebase/run_master_verification_1_to_14.py"

# 4. Launch Production Application Server
python "Course Project/Codebase/server.py"
```

Access the interactive web dashboard at `http://localhost:8000` in any web browser.

## 13. Results

Table 19 summarizes the empirical results and performance metrics achieved by InternTrack across all core objectives.

### Table 19: Empirical Results & Verification Metrics

| Objective / Key Performance Indicator (KPI) | Empirical Production Result |
|:---|:---|
| **Student Profile & ATS Resume Generation** | 65 authentic KLE Tech students ingested; verified academic profiles & ATS resumes generated instantly. |
| **Corporate Opportunity Catalog** | 55 corporate opportunities active (20 top MNCs, 5 test fixtures, 30 live Indeed postings). |
| **Semantic Skill Match Accuracy** | Cosine matching accurately distinguishes technical fit (e.g. 83% for Ananya Sharma vs Infosys). |
| **Parallel Swarm Latency** | Evaluating 4 preferences concurrently takes 1.4s (vs 5.2s sequential), achieving a 73% latency reduction. |
| **Human-in-the-Loop Safety Enforcement** | 100% of allocations pause at coordinator gate; zero unapproved allocations permitted. |
| **Race Condition & Over-allocation Prevention** | ACID transactions with CHECK constraints prevent negative vacancies; 0 over-allocations across 100 test runs. |
| **Operational Fault Tolerance** | Circuit breaker gracefully falls back to pre-seeded catalog during external network dropouts. |
| **Automated Acceptance Test Pass Rate** | 81 of 81 automated acceptance tests passed across all 14 course labs (100.0% pass rate). |
| **Production Cloud Deployment** | Live on Render Cloud at https://interntrack-pv3r.onrender.com/ with zero downtime. |

## 14. Conclusion and Future Enhancements

InternTrack successfully demonstrates how agentic AI architectures—combining LangGraph state machines, parallel worker swarms, typed tools, and governed runtimes—can replace fragile, manual academic processes with a secure, evidence-grounded lifecycle system. By preserving strict faculty authority through Human-in-the-Loop breakpoints while automating repetitive eligibility checks and semantic skill matching, the platform ensures complete regulatory compliance under NEP 2020 while drastically reducing administrative overhead.

### Future Enhancements
- **Autonomous Industry Mentor Webhook**: Direct integration with corporate slack channels and corporate mentor webhooks for real-time progress validation.
- **WhatsApp Student Notification Bot**: Automated conversational notifications alerting students when coordinator approval is granted or when journal submissions are due.
- **Verifiable Digital Credentials**: Cryptographic issuance of completed 12-credit internship completion certificates on the Polygon blockchain.

## 15. References

- National Education Policy (NEP 2020) Guidelines for Undergraduate Engineering Internships, Ministry of Education, Government of India, 2020.
- Agentic AI Course Curriculum & Lab Guide (26ECAC401), School of Computer Science & Engineering, KLE Technological University, Hubballi, 2026.
- InternTrack: Internship Application and Tracking Portal — AI Solution Direction & Workflow Proposal (Team 11), KLE Technological University, 2026.
- Harrison Chase et al., 'LangGraph: Building Stateful, Multi-Actor Applications with LLMs', LangChain AI Documentation, 2024.
- Anthropic, 'Model Context Protocol (MCP) Specification: Standardizing Tool Calling and Resource Retrieval for AI Agents', 2024.
- Tiangolo et al., 'FastAPI: Modern, High-Performance Web Framework for Building APIs with Python 3.8+', 2024.
- Scikit-Learn Developers, 'Feature Extraction and TF-IDF Vector Spaces', Scikit-Learn Reference Manual, 2023.
- SQLite Development Team, 'ACID Compliance, Write-Ahead Logging, and Integrity Constraints in Embedded Databases', 2024.
