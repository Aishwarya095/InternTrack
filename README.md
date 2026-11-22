# InternTrack
### Internship Application & Tracking Portal
**Course:** 26ECAC401 Agentic AI — 15 Worklets / 14-Lab Build Book (Chapter 10 Capstone)  
**Institution:** KLE Technological University, Hubballi  

---

## 👥 Team Information — InternTrack Team 11

| Team Member Name | USN | Department & Division | Role in Project |
|---|---|---|---|
| **Prerna A** | `01FE23BCI037` | CSE (AI) — Division B | System Architecture & LangGraph State Machine |
| **Aishwarya B A** | `01FE23BCI095` | CSE (AI) — Division B | Agent Swarms, Verification Runner & Deployment |
| **Sonu Vaishnavi** | `01FE23BCI093` | CSE (AI) — Division B | Memory Engine, Skills & Grounding Agent |
| **Nischita N** | `01FE23BCI106` | CSE (AI) — Division B | Governance, Safety Gates & Audit Trail |

- **Team Name / Number:** InternTrack Team 11  
- **Worklet Title:** InternTrack — AURA-Powered Internship Application & Tracking Portal  
- **Guiding Institutional Principle:** *"Agents draft, screen, analyze, and flag; a named human approves."*  
- **Live Deployment Instance:** [https://interntrack-pv3r.onrender.com](https://interntrack-pv3r.onrender.com)  

---

## 🔗 Quick Navigation Links

- 📂 [**Assignments Folder (Labs 1 to 14)**](./Assignments/) — Standalone code, test scripts, and execution guides for all 14 coursework assignments.
- 📂 [**Course Project Folder**](./Course%20Project/) — Project codebase, original problem statement, and formal final evaluation report.
  - 📄 [Original Problem Statement Document (DOCX)](./Course%20Project/Problem_Statement.docx) · [PDF Version](./Course%20Project/AAI_INTERNSHIP_DOC.pdf)
  - 📄 [Final Course Project Evaluation Report (DOCX)](./Course%20Project/Final_Course_Project_Report.docx)
  - 💻 [Full Course Project Codebase](./Course%20Project/Codebase/)

---

## 📚 Overview of the 14 Course Assignments

The 14 course assignments systematically build the capabilities of the autonomous coordinator-and-worker agent platform:

| # | Assignment Title | Core Concept & Mechanism | Technologies / Tools | Folder Link |
|---|---|---|---|---|
| **01** | **Agent vs Chatbot Concept** | Goal-driven loop & Plan–Act–Observe–Revise cycle vs. stateless conversational chatbot | Python, Pydantic, Rule-based Planner | [Assignment_01](./Assignments/Assignment_01/) |
| **02** | **Tool-Using Agent** | Typed deterministic interfaces & single-point call tracing without hallucinated numbers | SQLite3, Typed Schemas, Call Tracer | [Assignment_02](./Assignments/Assignment_02/) |
| **03** | **Reusable Skills & Rubrics** | Procedural compliance skills & 100-point rubric evaluator for journals and viva | Python Skills, Rubric Matrix, Feedback Generator | [Assignment_03](./Assignments/Assignment_03/) |
| **04** | **Two-Tier Memory & State** | Dual memory: Ephemeral session working state + immutable episodic audit logs | JSON State, SQLite Audit Log, Session Store | [Assignment_04](./Assignments/Assignment_04/) |
| **05** | **Governed Connector** | Unified data access gateway with Bearer authentication and Role-Based Access Control (RBAC) | REST API, Bearer Auth, Token Redaction | [Assignment_05](./Assignments/Assignment_05/) |
| **06** | **Controlled Runtime & Audit Log** | Deterministic pre-execution safety gates & append-only cryptographic event logging | Hash Chaining, SHA-256 Audit Logs, Gatekeeper | [Assignment_06](./Assignments/Assignment_06/) |
| **07** | **Explicit Graph Execution** | LangGraph directed state graph with conditional routing and deterministic joins | LangGraph, StateGraph, Typed State | [Assignment_07](./Assignments/Assignment_07/) |
| **08** | **Parallel Swarm & Human Gate** | Fan-Out / Fan-In multi-agent worker swarm across preferences with Coordinator Gate | Multi-threading, Worker Swarms, Human Gate | [Assignment_08](./Assignments/Assignment_08/) |
| **09** | **Deep Research & Grounding** | Web / document grounding with strict source citation verification to reject hallucinations | Grounding Agent, Cross-Encoder, Citations | [Assignment_09](./Assignments/Assignment_09/) |
| **10** | **Cloud Ops Resilience** | Circuit breaker, exponential backoff retries, and self-healing automated fallback | Circuit Breaker Pattern, Fallback Strategy | [Assignment_10](./Assignments/Assignment_10/) |
| **11** | **Agentic SDLC Factory** | Automated test-driven green gate validation to build, test, and promote agent tools | Unittest, Green Gate Runner, Factory Pattern | [Assignment_11](./Assignments/Assignment_11/) |
| **12** | **Safety Governance & Rollback** | Automated PII masking, safety invariant verification, and atomic snapshot rollback | Regex PII Redactor, Invariant Checker, Rollback | [Assignment_12](./Assignments/Assignment_12/) |
| **13** | **Discipline Specialists** | Specialized domain agents (Coordinator, HoD, Mentor, Dean) enforcing institutional rules | Role-based Subagents, Authority Hierarchies | [Assignment_13](./Assignments/Assignment_13/) |
| **14** | **Capstone Final Integration** | Unified lifecycle platform, live vacancy decrements, 4-tier preferences & full test suite | LangGraph Swarms, SQLite3, FastAPI, Render | [Assignment_14](./Assignments/Assignment_14/) |

---

## 🎯 Detailed Course Project Explanation

### 1. Problem Statement
In higher education institutions, 8th-semester full-time internships carry mandatory academic weight (**12 credits under AICTE / NEP 2020**). However, the manual administration of this lifecycle presents critical bottlenecks:
1. **Scattered Discovery:** Students discover company openings through fragmented word-of-mouth and outdated notice boards.
2. **Inconsistent Eligibility Checks:** CGPA thresholds, active backlogs, and earned credits are checked manually across disparate spreadsheets.
3. **Zero In-Semester Progress Visibility:** Once a student joins an off-campus corporate company, faculty mentors have no real-time tracking of weekly journals, milestones, or mentor check-ins.
4. **Unverifiable Final Evaluations:** Final grading relies on rushed end-of-semester paperwork lacking an auditable paper trail.

### 2. Project Objectives
- Build an enterprise-grade, regulatory-compliant **Internship Application & Tracking Portal (InternTrack / AURA)**.
- Implement an **Autonomous Agent Swarm** to automate student profiling, corporate vacancy matching, progress monitoring, and rubric scoring.
- Enforce strict **Human-in-the-Loop Governance**: Agents propose, screen, and flag, but only named faculty coordinators and HODs approve placements and award academic credits.
- Provide an **Immutable Cryptographic Audit Trail** with atomic state rollback for institutional compliance.

### 3. Agentic Architecture & Approach
The platform is designed around an explicit **LangGraph state machine** orchestrating autonomous worker agents:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      AURA COORDINATOR AGENT                            │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
┌─────────────────────────────────┐         ┌─────────────────────────────────┐
│ Group A: Opportunity Discovery  │         │ Group B: Eligibility Verifier   │
│ - Semantic profile matching     │         │ - Strict CGPA cutoff validation │
│ - Corporate vacancy decrement   │         │ - Backlog & credit constraints  │
└────────────────┬────────────────┘         └────────────────┬────────────────┘
                 │                                           │
                 └────────────────────┬──────────────────────┘
                                      ▼
                       ┌─────────────────────────────┐
                       │ Group C: Application Join   │
                       │ - Verified candidate packet │
                       └──────────────┬──────────────┘
                                      ▼
                       ┌─────────────────────────────┐
                       │ 🛡️ COORDINATOR HUMAN GATE   │
                       │ - Named faculty sign-off    │
                       └──────────────┬──────────────┘
                                      ▼
         ┌────────────────────────────┴──────────────────────────┐
         ▼                                                       ▼
┌─────────────────────────────────┐             ┌─────────────────────────────────┐
│ Group E: Progress Tracking      │             │ Group F: 100-pt Evaluation      │
│ - Bi-weekly journal validation  │             │ - Objective rubric grading      │
│ - Employer attendance checks    │             │ - Final 12-credit certification │
└─────────────────────────────────┘             └─────────────────────────────────┘
```

### 4. Implementation & Tech Stack
- **Core Orchestration:** LangGraph State Machine, Python 3.10+, Pydantic.
- **Backend & API:** Custom Lightweight REST Server / FastAPI architecture, SQLite3 relational database with foreign key constraints.
- **Frontend Portal:** Responsive Vanilla CSS Design System and ES6 reactive web interface.
- **Governance & Safety:** Cryptographic audit logger, Regex-based PII masker, and snapshot-based atomic rollback engine.
- **Verification Suite:** Comprehensive 81-test master verification suite ensuring 100% test pass rate across all 14 labs.

### 5. Key Results & Achievements
- **100% Deterministic Execution:** Zero hallucinations in eligibility decisions; all criteria verified against database records.
- **Complete Test Coverage:** 81 out of 81 automated tests verified across all labs (`run_master_verification_1_to_14.py`).
- **Real-World University Dataset:** Seeded with 65 authentic student profiles, real placement records, and live vacancy counters.
- **Cloud Deployment:** Fully deployed and operational on Render cloud infrastructure.

---

## 🚀 How to Run the Project Directly on GitHub / Locally

### Option A: Run Directly in Browser with GitHub Codespaces
1. Open this repository on GitHub.
2. Press `,` (comma) on your keyboard OR click **Code ➔ Codespaces ➔ Create codespace on main**.
3. In the built-in terminal, start the server:
   ```bash
   cd "Course Project/Codebase"
   python server.py
   ```
4. Click **"Open in Browser"** on the pop-up notification to access the live portal!

### Option B: Run Automated Master Test Suite
In the terminal, run the master verification script:
```bash
cd "Course Project/Codebase"
python run_master_verification_1_to_14.py
```

### Option C: Run Local Instance
```bash
git clone <YOUR_REPO_URL>
cd InternTrack/"Course Project"/Codebase
pip install -r requirements.txt
python server.py
```
Open [http://localhost:8000](http://localhost:8000) in your web browser.
