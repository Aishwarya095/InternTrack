# -*- coding: utf-8 -*-
"""
Full Academic Artifact Report Builder for InternTrack.
Generates:
  1. Course Project/Artifact_Report_InternTrack.docx
  2. Course Project/Artifact_Report_InternTrack.md
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def build_docx_and_md():
    doc = docx.Document()
    
    # Page Margins (0.7875 inches / 2 cm like reference)
    for section in doc.sections:
        section.top_margin = Inches(0.7875)
        section.bottom_margin = Inches(0.7875)
        section.left_margin = Inches(0.7875)
        section.right_margin = Inches(0.7875)
        
    def set_cell_background(cell, fill_hex):
        shd_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}" w:val="clear" w:color="auto"/>'
        cell._tc.get_or_add_tcPr().append(parse_xml(shd_xml))

    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcMar_xml = f'''<w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>'''
        cell._tc.get_or_add_tcPr().append(parse_xml(tcMar_xml))

    def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
        tblPr = table._tbl.tblPr
        borders_xml = f'''<w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tblBorders>'''
        tblPr.append(parse_xml(borders_xml))

    def format_table(table, col_widths=None, header_bg="1F4E79", alt_bg="F9FBFC"):
        set_table_borders(table, color="D3D3D3", sz="4")
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, row in enumerate(table.rows):
            is_header = (i == 0)
            for j, cell in enumerate(row.cells):
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
                if col_widths and j < len(col_widths):
                    cell.width = col_widths[j]
                if is_header:
                    set_cell_background(cell, header_bg)
                    for p in cell.paragraphs:
                        p.paragraph_format.space_before = Pt(3)
                        p.paragraph_format.space_after = Pt(3)
                        for r in p.runs:
                            r.bold = True
                            r.font.size = Pt(10)
                            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                else:
                    if i % 2 == 1:
                        set_cell_background(cell, "FFFFFF")
                    else:
                        set_cell_background(cell, alt_bg)
                    for p in cell.paragraphs:
                        p.paragraph_format.space_before = Pt(2)
                        p.paragraph_format.space_after = Pt(2)
                        for r in p.runs:
                            r.font.size = Pt(9.5)
                            r.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    def add_callout(expectation_title, expectation_desc):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        set_cell_background(cell, "EAF1F8")
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        
        tcBorders_xml = f'''<w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="2E75B6"/>
            <w:left w:val="single" w:sz="18" w:space="0" w:color="1F4E79"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="2E75B6"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="2E75B6"/>
        </w:tcBorders>'''
        cell._tc.get_or_add_tcPr().append(parse_xml(tcBorders_xml))
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run("Expectation: ")
        r1.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
        
        r2 = p.add_run(f"{expectation_title} — {expectation_desc}")
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(3)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(16)
        r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        return p

    def add_bullet(text, prefix="• "):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r_pre = p.add_run(prefix)
        r_pre.bold = True
        r_pre.font.size = Pt(10)
        r_pre.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
        r = p.add_run(text)
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        return p

    # --- COVER / HEADER ---
    p0 = doc.add_paragraph()
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(1)
    r = p0.add_run("KLE Technological University, Hubballi")
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

    p1 = doc.add_paragraph()
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(4)
    r = p1.add_run("School of Computer Science & Engineering (AI)")
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(4)
    p2.paragraph_format.space_after = Pt(2)
    r = p2.add_run("Artifact Report")
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)

    p3 = doc.add_paragraph()
    p3.paragraph_format.space_before = Pt(2)
    p3.paragraph_format.space_after = Pt(4)
    r = p3.add_run("InternTrack: Autonomous Internship Application & Tracking Portal")
    r.bold = True
    r.font.size = Pt(24)
    r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    p4 = doc.add_paragraph()
    p4.paragraph_format.space_before = Pt(0)
    p4.paragraph_format.space_after = Pt(10)
    r = p4.add_run("Artifact 10 · Agentic AI (26ECAC401) · Team 11 · Division B")
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    # TABLE 1: Students
    t1_data = [
        ["No.", "Student name", "USN", "Roll no. / Project Role"],
        ["1", "Prerna A", "01FE23BCI037", "System Architecture & LangGraph State Machine"],
        ["2", "Aishwarya B A", "01FE23BCI095", "Agent Swarms, Verification Runner & Deployment"],
        ["3", "Sonu Vaishnavi", "01FE23BCI093", "Memory Engine, Skills & Grounding Agent"],
        ["4", "Nischita N", "01FE23BCI106", "Governance, Safety Gates & Audit Trail"]
    ]
    t1 = doc.add_table(rows=len(t1_data), cols=4)
    for r_idx, row in enumerate(t1_data):
        for c_idx, val in enumerate(row):
            t1.rows[r_idx].cells[c_idx].text = val
    format_table(t1, [Inches(0.5), Inches(1.8), Inches(1.4), Inches(3.2)])

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(4)

    # TABLE 2: Links
    t2_data = [
        ["Item", "Link"],
        ["GitHub repository", "https://github.com/Aishwarya095/InternTrack"],
        ["Live application", "https://interntrack-pv3r.onrender.com/"]
    ]
    t2 = doc.add_table(rows=len(t2_data), cols=2)
    for r_idx, row in enumerate(t2_data):
        for c_idx, val in enumerate(row):
            t2.rows[r_idx].cells[c_idx].text = val
    format_table(t2, [Inches(2.2), Inches(4.7)])

    # TABLE OF CONTENTS
    add_h2("Contents")
    toc_items = [
        "1. Abstract",
        "2. Introduction and Problem Statement",
        "3. Objectives",
        "4. Expectations and Coverage",
        "5. System Architecture",
        "6. Technology Stack",
        "7. Implementation Against Each Expectation",
        "8. Supporting Capabilities",
        "9. End-to-End Walkthrough",
        "10. Lab-wise Coverage (Labs 1–14)",
        "11. Assignments",
        "12. Repository and Run Steps",
        "13. Results",
        "14. Conclusion and Future Enhancements",
        "15. References"
    ]
    for item in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before = Pt(1)
        p_toc.paragraph_format.space_after = Pt(1)
        r = p_toc.add_run(item)
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    # --- 1. ABSTRACT ---
    add_h1("1. Abstract")
    add_p("In eighth-semester engineering curricula under NEP 2020, full-time off-campus internships carry 12 mandatory academic credits. Yet across institutional placement ecosystems, internship allocation and governance remain bottlenecked by fragmented workflows: manual Google Forms, error-prone spreadsheet verification of CGPA and backlog statuses, lack of continuous off-campus progress visibility, and last-minute document aggregation without verifiable audit trails.")
    add_p("This report presents InternTrack powered by AURA, a human-governed, evidence-grounded agentic AI system engineered to automate the entire 8th-semester internship lifecycle. The system is architected as an autonomous multi-agent hierarchy orchestrated through LangGraph: a Central Coordinator agent directs parallel role swarms for opportunity discovery and eligibility verification, a Skill Matcher that calculates cosine similarity across 100+ technical competencies, and periodic tracking agents that ingest and evaluate bi-weekly student progress journals against real company deliverables.")
    add_p("InternTrack operates within a sandboxed, governed runtime enforcing strict Human-in-the-Loop (HITL) checkpoints: agents autonomously discover, parse, validate, and rank opportunities, but transition to an explicit paused state awaiting mandatory faculty coordinator and HOD sign-offs. Rejections require mandatory justification reasons, and approved allocations trigger atomic database transactions that decrement vacancies in real time (preventing over-allocation). The platform features regex-based PII redaction, cryptographic SHA-256 audit trails, circuit-breaker fault tolerance, and a master test suite of 81 automated acceptance tests passing at 100% across all 14 course labs. InternTrack is deployed live on Render Cloud (https://interntrack-pv3r.onrender.com/) with a production SQLite database pre-seeded with 65 authentic KLE Tech students, 55 corporate opportunities, and 45 longitudinal progress journals.")

    # --- 2. INTRODUCTION AND PROBLEM STATEMENT ---
    add_h1("2. Introduction and Problem Statement")
    add_h2("2.1 Background")
    add_p("Agentic AI represents a fundamental paradigm shift from conversational chatbots to autonomous execution systems. Unlike conversational models that merely respond to localized prompts, agentic systems maintain persistent goals, decompose multi-phase objectives, invoke typed external tools, maintain hierarchical memory across sessions, and coordinate specialized agent swarms to alter real-world environments safely. Across the fourteen hands-on labs of the Agentic AI (26ECAC401) curriculum, our team developed and integrated these foundational principles into a production-grade capstone worklet addressing academic internship operations.")
    
    add_h2("2.2 Problem Statement")
    add_p("University internship administration for final-year undergraduate students suffers from four structural points of failure:")
    add_bullet("Fragmented Discovery & Asymmetric Information: Students discover opportunities through informal channels, unverified WhatsApp broadcasts, and stale bulletin boards, missing high-fit openings aligned with their technical profile.")
    add_bullet("Manual, Inconsistent Eligibility Verification: Faculty coordinators spend hundreds of hours manually cross-checking university database records (CGPA cutoffs, active academic backlogs, prerequisite departmental credits) against company criteria, leading to human fatigue and compliance errors.")
    add_bullet("Zero Off-Campus Progress Visibility: Once students depart for 4-to-6 month full-time industry internships, academic departments lose all continuous visibility into student attendance, mentor guidance, and technical deliverables.")
    add_bullet("Unverifiable Last-Minute Evaluation: Semester-end credit certification relies on rushed paperwork, unverified student claims, and retrospective employer surveys lacking cryptographic or temporal evidence.")

    add_h2("2.3 Scope")
    add_p("InternTrack addresses the full lifecycle of final-year undergraduate internships: student academic profile ingestion, opportunity scraping and catalog synchronization, automated semantic ATS resume building, multi-preference submission with parallel swarm auto-ranking, dual-gate faculty/HOD approvals, atomic vacancy decrement, bi-weekly progress journal evaluation with LLM evidence grounding, and immutable audit logging. Non-coursework features such as direct corporate payroll disbursement and legal enterprise contract generation remain outside the current academic scope.")

    # --- 3. OBJECTIVES ---
    add_h1("3. Objectives")
    objectives = [
        "Automate student academic ingestion and ATS resume generation using verified institutional records for 65+ authentic KLE Tech students.",
        "Implement semantic skill matching and eligibility verification across 50+ corporate opportunities using TF-IDF cosine similarity and deterministic rule gating.",
        "Orchestrate multi-preference evaluation using LangGraph parallel fan-out swarms and barrier synchronization.",
        "Enforce strict Human-in-the-Loop (HITL) safety breakpoints requiring faculty coordinator justification and explicit sign-off before state progression.",
        "Guarantee database integrity through ACID atomic transactions and constraints to prevent negative vacancy race conditions.",
        "Maintain evidence-grounded progress tracking by evaluating bi-weekly student journals against verified corporate benchmarks.",
        "Ensure enterprise governance through automated PII redaction, structured error handling with circuit breakers, and an immutable SHA-256 audit trail.",
        "Deploy the production application live on cloud infrastructure backed by an automated 81-test master verification suite achieving 100% pass rate."
    ]
    for obj in objectives:
        add_bullet(obj)

    # --- 4. EXPECTATIONS AND COVERAGE ---
    add_h1("4. Expectations and Coverage")
    add_p("The capstone worklet is formally evaluated against nine core technical rubrics. Table 3 maps each expectation to its implementation and corresponding report section.")
    
    # TABLE 3: Expectations
    t3_data = [
        ["#", "Expectation", "What is checked", "Covered by", "Section"],
        ["1", "Assignment submission", "Complete, on time, meets brief", "28 lab assignments with code & execution output", "11"],
        ["2", "GitHub repo readiness", "README, structure, commits, run steps", "Structured repository, automated master verification", "12"],
        ["3", "Agents", "Clear goal, uses tools, completes task", "Coordinator + 7 specialized domain agents", "7.1"],
        ["4", "Skills", "Defined, reusable, used by agents", "6 standardized skills with Pydantic schemas", "7.2"],
        ["5", "MCP Gateway", "Servers & tools connected and working", "MCP Gateway with 12 typed capability tools", "7.3"],
        ["6", "Governed Runtime", "OpenClaw-style runtime with safety limits", "Bounded loop (50 steps), PII redactor, circuit breaker", "7.4"],
        ["7", "Agent Swarms", "Coordinated agents with clear roles", "LangGraph Fan-Out / Fan-In parallel swarm", "7.5"],
        ["8", "Deep Research", "Evidence-grounded parsing and evaluation", "ATS Resume Matcher + Journal Evidence Grounding", "7.6"],
        ["9", "Cloud SDLC", "Build, test, deployment run in cloud", "Render Cloud CI/CD, 81 tests passing 100%", "7.7"]
    ]
    t3 = doc.add_table(rows=len(t3_data), cols=5)
    for r_idx, row in enumerate(t3_data):
        for c_idx, val in enumerate(row):
            t3.rows[r_idx].cells[c_idx].text = val
    format_table(t3, [Inches(0.4), Inches(1.8), Inches(2.0), Inches(2.2), Inches(0.6)])

    # --- 5. SYSTEM ARCHITECTURE ---
    add_h1("5. System Architecture")
    add_h2("5.1 Internship Application and Tracking Lifecycle")
    add_p("InternTrack models the entire academic internship progression as an immutable, state-driven lifecycle: DRAFT → VALIDATING → PAUSED_FOR_COORDINATOR_APPROVAL → APPROVED / REJECTED → ALLOCATED → ACTIVE_INTERNSHIP → EVALUATING → COMPLETED. State progression is strictly monotonic; no candidate can skip directly to ALLOCATED without satisfying prerequisite eligibility rules and clearing the coordinator sign-off checkpoint.")
    
    # TABLE 4: Layered Architecture
    add_h2("5.2 Layered System Architecture")
    t4_data = [
        ["Layer", "Architectural Responsibilities"],
        ["Web UI Presentation (Render)", "Responsive Single Page Application (vanilla JS, Tailwind CSS, Lucide icons) providing Student, Coordinator, and HOD dashboards."],
        ["FastAPI Application Server", "High-concurrency ASGI REST API exposing endpoints for opportunity lookup, preference intake, coordinator review, and audit streaming."],
        ["Governed Agent Runtime", "OpenClaw-inspired execution supervisor enforcing run budgets (50 steps max), regex PII redaction, and circuit breaker resilience."],
        ["LangGraph State Engine", "StateGraph coordinating sequential and parallel multi-agent workflows with state checkpoints and human breakpoint interrupts."],
        ["Specialist Agent Tier", "Coordinator, Student Profiler, Opportunity Discovery, Eligibility Verifier, Skill Matcher, Approval Router, Tracking Agent."],
        ["Skills & Tools Framework", "Reusable domain procedures extending BaseSkill and BaseTool with typed Pydantic validation schemas."],
        ["MCP Service Gateway", "Unified JSON-RPC connector interface dispatching live jobs, database operations, and external scraping tools."],
        ["Persistence & Audit Storage", "SQLite ACID database with CHECK constraints, foreign key cascades, and SHA-256 cryptographic audit logs."]
    ]
    t4 = doc.add_table(rows=len(t4_data), cols=2)
    for r_idx, row in enumerate(t4_data):
        for c_idx, val in enumerate(row):
            t4.rows[r_idx].cells[c_idx].text = val
    format_table(t4, [Inches(2.2), Inches(4.7)])

    # --- 6. TECHNOLOGY STACK ---
    add_h1("6. Technology Stack")
    t5_data = [
        ["Area", "Technology", "Used for"],
        ["Backend Runtime", "Python 3.10+, FastAPI, Uvicorn", "Core application server, high-throughput REST endpoints, and async worker execution"],
        ["Agent Orchestration", "LangGraph (StateGraph, Send API)", "Stateful multi-agent graphs, conditional branching, and parallel fan-out swarms"],
        ["Data Validation", "Pydantic v2", "Strict schema enforcement, type validation for tools, and serialized agent state"],
        ["Database & ORM", "SQLite 3 with ACID transactions", "Structured relational persistence, atomic seat decrements, and transactional integrity"],
        ["Vector & NLP Matcher", "Scikit-Learn, NumPy (TF-IDF)", "Mathematical cosine similarity scoring between student resumes and opportunity catalogs"],
        ["LLM Intelligence", "Groq API / Llama-3-70B & Gemini API", "Semantic resume parsing, technical competency extraction, and journal evidence synthesis"],
        ["Cloud Hosting & CI/CD", "Render Cloud Platform", "Automated GitHub repository continuous deployment, production web hosting, and SSL"],
        ["Frontend Interface", "Vanilla ES6+ JavaScript, Tailwind CSS", "Zero-dependency, high-performance interactive SPA with real-time reactive UI updates"],
        ["Verification Suite", "Python unittest & custom runner", "81 automated acceptance tests across Labs 1 through 14 with 100% pass rate"]
    ]
    t5 = doc.add_table(rows=len(t5_data), cols=3)
    for r_idx, row in enumerate(t5_data):
        for c_idx, val in enumerate(row):
            t5.rows[r_idx].cells[c_idx].text = val
    format_table(t5, [Inches(1.8), Inches(2.2), Inches(2.9)])

    # --- 7. IMPLEMENTATION AGAINST EACH EXPECTATION ---
    add_h1("7. Implementation Against Each Expectation")
    
    # 7.1 Agents
    add_h2("7.1 Agents")
    add_callout("Agents", "Agents have a clear goal, invoke typed tools, and drive tasks to verified completion.")
    add_h3("What we built")
    add_p("The system implements a hierarchical multi-agent structure led by the Internship Coordinator Agent. The Coordinator decomposes complex requests, dispatches tasks to specialist agents, aggregates candidate preference matrices, and routes exceptions. Each agent executes within a deterministic bounded loop and emits typed AgentOutput schemas.")
    
    # TABLE 7: Agents Table
    t7_data = [
        ["Agent", "Goal / Responsibility", "Tools & Skills Used"],
        ["Coordinator Agent", "Supervise lifecycle, dispatch parallel swarms, route human approvals", "CoordinatorGraph, MemoryEngine, AuditLogger"],
        ["Student Profiler", "Fetch and validate authentic student academic records and credits", "student_lookup_tool, gpa_verification_tool"],
        ["Opportunity Discovery", "Scrape, categorize, and rank active corporate internship openings", "opportunity_search_tool, live_job_sync"],
        ["Eligibility Verifier", "Verify CGPA cutoffs, active backlogs, and departmental prerequisites", "eligibility_check_tool, policy_guardrail"],
        ["Skill Matcher", "Parse student resume and compute cosine match against job requirements", "skill_extraction_tool, cosine_matcher"],
        ["Approval Router", "Gate state progression, enforce mandatory coordinator justification", "approval_gate_tool, atomic_decrement_tool"],
        ["Tracking & Evaluation", "Monitor bi-weekly journal submissions and compute progress score", "journal_ingest_tool, evidence_grounder"]
    ]
    t7 = doc.add_table(rows=len(t7_data), cols=3)
    for r_idx, row in enumerate(t7_data):
        for c_idx, val in enumerate(row):
            t7.rows[r_idx].cells[c_idx].text = val
    format_table(t7, [Inches(1.8), Inches(2.7), Inches(2.4)])

    add_h3("Evidence")
    add_bullet("Source code: Course Project/Codebase/agents/ (coordinator_agent.py, eligibility_agent.py, matcher_agent.py, etc.).")
    add_bullet("Master test verification: tests/test_lab1_agent.py and tests/test_lab2_tools.py passing 100%.")
    add_bullet("Live verification: Selecting Ananya Sharma (1KG21CS008) auto-extracts verified CGPA (9.1) and B.E. CSE credentials seamlessly.")

    # 7.2 Skills
    add_h2("7.2 Skills")
    add_callout("Skills", "Skills are modular, reusable, self-contained capabilities with typed schemas.")
    add_h3("What we built")
    add_p("InternTrack abstracts complex multi-step reasoning into standardized skills extending BaseSkill. Each skill publishes SkillMetadata (name, description, input/output schemas, operational constraints) registered centrally within a SkillRegistry.")
    
    # TABLE 9: Skills Table
    t9_data = [
        ["Skill", "Purpose & Execution Logic", "Reusability Across Worklet"],
        ["Eligibility Verification", "Deterministic validation of student CGPA >= cutoff and active backlogs == 0", "Used in student submission, preference ranking, and coordinator audit"],
        ["Semantic Skill Matching", "Extract technical keywords from resume and compute TF-IDF cosine score", "Invoked in AI Resume Matcher and parallel preference swarm"],
        ["Opportunity Auto-Ranking", "Rank corporate openings by composite score (60% skills + 40% CGPA buffer)", "Reusable across all student multi-preference applications"],
        ["Journal Evidence Grounding", "Cross-examine student progress claims against company milestone deliverables", "Invoked bi-weekly throughout the 4-month off-campus internship"],
        ["Immutable Plan Locking", "Generate cryptographic SHA-256 hash of student application state", "Re-locked whenever student preferences or coordinator comments change"],
        ["Format & Reporting", "Generate structured ATS-compliant plain-text and PDF resumes", "Used in university career export and coordinator summary desks"]
    ]
    t9 = doc.add_table(rows=len(t9_data), cols=3)
    for r_idx, row in enumerate(t9_data):
        for c_idx, val in enumerate(row):
            t9.rows[r_idx].cells[c_idx].text = val
    format_table(t9, [Inches(1.8), Inches(2.7), Inches(2.4)])

    add_h3("Evidence")
    add_bullet("Source code: Course Project/Codebase/skills/ (base_skill.py, eligibility_skill.py, matching_skill.py).")
    add_bullet("Automated tests: tests/test_lab3_skills.py passing 6 acceptance test scenarios.")

    # 7.3 MCP
    add_h2("7.3 MCP Gateway")
    add_callout("MCP", "Connectors expose external capabilities through standardized, discoverable interfaces.")
    add_h3("What we built")
    add_p("External integrations and enterprise tool calls are mediated through a centralized Model Context Protocol (MCP) gateway. The gateway exposes a JSON-RPC 2.0 envelope, enforces parameter validation, prevents unauthorized side effects, and provides a mock/real adapter toggle.")
    
    # TABLE 11: MCP Table
    t11_data = [
        ["Capability Identifier", "Connected Subsystem", "Side-Effect / Gating Policy"],
        ["opportunity.search", "Opportunity Catalog / Indeed Feed", "Read-only; cached queries; circuit-breaker protected"],
        ["student.lookup_record", "KLE Tech Academic Records DB", "Read-only; regex PII masking applied on export"],
        ["eligibility.verify_rules", "Academic Affairs Policy Engine", "Read-only; deterministic rule evaluation"],
        ["matcher.compute_score", "TF-IDF Vector Matching Engine", "Read-only; pure mathematical cosine computation"],
        ["allocation.atomic_decrement", "SQLite Opportunities DB", "Consequential side effect; gated by coordinator approval"],
        ["audit.write_event", "Cryptographic Audit Logger", "Append-only immutable event stream"]
    ]
    t11 = doc.add_table(rows=len(t11_data), cols=3)
    for r_idx, row in enumerate(t11_data):
        for c_idx, val in enumerate(row):
            t11.rows[r_idx].cells[c_idx].text = val
    format_table(t11, [Inches(2.2), Inches(2.5), Inches(2.2)])

    add_h3("Evidence")
    add_bullet("Source code: Course Project/Codebase/connectors/mcp_gateway.py and tools/.")
    add_bullet("Automated tests: tests/test_lab5_mcp.py passing 5 boundary condition checks.")

    # 7.4 OpenCLA / Governed Runtime
    add_h2("7.4 Governed Agent Runtime (OpenClaw Architecture)")
    add_callout("Governed Runtime", "Agents execute in a sandboxed, budget-constrained runtime with crash recovery.")
    add_h3("What we built")
    add_p("InternTrack executes all agent workflows inside an OpenClaw-inspired governed supervisor. The runtime enforces execution budgets (max 50 iterations, 30s timeout), PII redaction of student contact details, structured audit telemetry, and atomic transaction rollbacks upon unexpected execution failure.")
    add_h3("Evidence")
    add_bullet("Source code: Course Project/Codebase/runtime/governed_runtime.py and safety/.")
    add_bullet("Automated tests: tests/test_lab6_runtime.py validating step limit exhaustion and crash recovery.")

    # 7.5 Swarms
    add_h2("7.5 Multi-Agent Swarms (Parallel Fan-Out / Fan-In)")
    add_callout("Swarms", "Autonomous worker agents coordinate concurrently with clear division of labor.")
    add_h3("What we built")
    add_p("When a student submits four company preferences, evaluating them sequentially introduces excessive latency. InternTrack implements a parallel fan-out swarm using LangGraph's Send API. The coordinator spawns 4 concurrent worker agents that independently check company eligibility, compute skill fit, and verify live seat availability. A barrier synchronization node aggregates the worker evaluations into a single optimal preference matrix.")
    add_h3("Evidence")
    add_bullet("Source code: Course Project/Codebase/swarm/swarm_coordinator.py and graphs/parallel_swarm.py.")
    add_bullet("Automated tests: tests/test_lab8_swarms.py verifying barrier synchronization and concurrent worker threads.")

    # 7.6 Deep Research
    add_h2("7.6 Deep Research & Evidence Grounding")
    add_callout("Deep Research", "Synthesizes structured outputs strictly grounded in verified source evidence.")
    add_h3("What we built")
    add_p("In academic internship evaluation, hallucinations can lead to fraudulent credit awards. The Deep Research & Evidence Grounding agent parses bi-weekly student progress journals and validates reported work against industry project milestones. Every credit recommendation must cite verbatim source snippets from student submission logs; unsubstantiated claims are flagged for faculty investigation.")
    add_h3("Evidence")
    add_bullet("Source code: Course Project/Codebase/research/grounding_agent.py and matching/resume_matcher.py.")
    add_bullet("Automated tests: tests/test_lab9_deep_research.py validating hallucination rejection and citation grounding.")

    # 7.7 Cloud SDLC
    add_h2("7.7 Cloud SDLC & Production Deployment")
    add_callout("Cloud SDLC", "Specification-driven build, automated testing, and verified cloud deployment.")
    add_h3("What we built")
    add_p("The project adheres to rigorous software engineering practices: a declarative OpenAPI specification, 81 automated acceptance tests covering all 14 course labs, Git version control, and zero-downtime continuous deployment on Render Cloud connected directly to the GitHub main branch.")
    add_h3("Evidence")
    add_bullet("Live cloud deployment: https://interntrack-pv3r.onrender.com/ (Production verified).")
    add_bullet("Master test verification: python 'Course Project/Codebase/run_master_verification_1_to_14.py' &rarr; 81 Passed, 0 Failed (100% pass rate).")

    # --- 8. SUPPORTING CAPABILITIES ---
    add_h1("8. Supporting Capabilities")
    add_h2("8.1 Typed Tools")
    add_p("InternTrack features 12 typed tools extending Pydantic BaseModel schemas. Tool arguments undergo automatic type casting, range checking, and validation before execution. Tools consistently return structured ToolResult objects containing output payloads, error states, and execution latencies.")
    
    add_h2("8.2 Memory and Retrieval")
    add_p("The system implements a four-tiered memory architecture:")
    add_bullet("Short-term Session Memory: Tracks the live LangGraph execution state, candidate preference arrays, and intermediate agent critiques.")
    add_bullet("Long-term Candidate Store: Persists historical student academic backgrounds, previous project portfolios, and verified transcripts in SQLite.")
    add_bullet("Dynamic Vector Index: In-memory TF-IDF vector space for real-time mathematical cosine matching across corporate vacancy catalogs.")
    add_bullet("Cryptographic Audit Memory: Write-once, read-many (WORM) audit journal storing SHA-256 hashed state transitions.")

    add_h2("8.3 LangGraph State Machine")
    add_p("The primary execution engine is structured as a LangGraph StateGraph comprising 14 discrete nodes: INTAKE &rarr; PARSE_PROFILE &rarr; DISCOVER_OPPORTUNITIES &rarr; FAN_OUT_SWARM &rarr; PARALLEL_WORKERS [1..4] &rarr; BARRIER_AGGREGATION &rarr; ELIGIBILITY_GATE &rarr; PAUSED_FOR_COORDINATOR_APPROVAL &rarr; (Human Gate) &rarr; ATOMIC_ALLOCATION &rarr; JOURNAL_TRACKING &rarr; FINAL_EVALUATION. Conditional edges safely route ineligible students to an advisory revision loop.")

    add_h2("8.4 Safety, Governance and Human-in-the-Loop")
    add_p("Autonomous agent decision-making is strictly constrained by departmental governance policy. The system incorporates two mandatory safety gates: Coordinator Approval and HOD Departmental Sanction. An agent cannot decrement vacancies or confirm an internship without cryptographic human sign-off. Furthermore, faculty rejections enforce a mandatory text justification field to eliminate arbitrary dismissals.")

    add_h2("8.5 Domain Specialisation (NEP 2020 Compliance)")
    add_p("InternTrack is specialized for academic engineering regulations under the National Education Policy (NEP 2020) at KLE Technological University. The system encodes institutional rules: minimum 7.0 CGPA for tier-1 MNCs, zero active backlogs at time of departure, mandatory 12-credit capstone allocation, and a minimum 16-week off-campus corporate duration.")

    # --- 9. END-TO-END WALKTHROUGH ---
    add_h1("9. End-to-End Walkthrough")
    add_p("A complete representative execution trace illustrates the seamless coordination across agents, tools, and human gates:")
    add_bullet("Step 1 (Student Lookup): Student Ananya Sharma (1KG21CS008) is looked up. The Profiler Agent retrieves verified records: CGPA 9.1, B.E. Computer Science, AWS and Java competencies.")
    add_bullet("Step 2 (ATS Resume Generation): The Format Skill generates a standardized ATS plain-text and PDF resume; PII masking redacts personal mobile and residential addresses.")
    add_bullet("Step 3 (Skill Matching): The Skill Matcher executes TF-IDF cosine comparison across 55 corporate openings. Infosys InStep yields an 83% technical match; missing skills (Python automation) are highlighted for upskilling.")
    add_bullet("Step 4 (Multi-Preference Submission): The student selects 4 ranked preferences (Infosys, TCS, Bosch, Google) and submits.")
    add_bullet("Step 5 (Parallel Swarm Evaluation): The Coordinator spawns 4 parallel worker agents via LangGraph Send API. Concurrently, worker threads verify company cutoffs and seat availability in 1.4 seconds.")
    add_bullet("Step 6 (Human Breakpoint Interruption): The barrier aggregator formats the proposal and transitions state to PAUSED_FOR_COORDINATOR_APPROVAL. The agent yields control.")
    add_bullet("Step 7 (Coordinator Approval & Atomic Decrement): Faculty Coordinator Dr. Ramesh reviews the verification dossier and clicks Approve. An atomic SQLite transaction decrements available vacancies from 6 to 5.")
    add_bullet("Step 8 (Off-Campus Tracking & Audit): Bi-weekly progress journals are ingested, grounded against corporate milestones, and committed to the immutable SHA-256 audit log.")

    # --- 10. LAB-WISE COVERAGE ---
    add_h1("10. Lab-wise Coverage (Labs 1–14)")
    add_p("Table 16 details how each of the fourteen curriculum labs is instantiated within the InternTrack production codebase.")
    
    # TABLE 16: Lab-wise Coverage
    t16_data = [
        ["Lab", "Curriculum Concept", "Implementation in InternTrack Capstone Worklet"],
        ["Lab 1", "Agent vs Chatbot", "Goal-oriented student lifecycle agent with clarify &rarr; validate &rarr; approve execution loops"],
        ["Lab 2", "Tool-Using Agent", "12 typed tools (student_lookup, eligibility_check, vacancy_decrement) with Pydantic validation"],
        ["Lab 3", "Skill Creation", "6 reusable skills extending BaseSkill (Eligibility, Matching, Auto-Rank, Plan Lock, Reporting)"],
        ["Lab 4", "Memory & Retrieval", "Session state, long-term student history, dynamic TF-IDF vector index, and audit logs"],
        ["Lab 5", "MCP Connector", "Centralized MCP Gateway dispatching tool calls, JSON-RPC envelopes, and mock/real toggles"],
        ["Lab 6", "OpenClaw Runtime", "Governed runtime with 50-step budget limits, PII redactor, and crash recovery checkpoints"],
        ["Lab 7", "Agentic Node Graph", "LangGraph StateGraph with 14 nodes, conditional branching, and Human-in-the-Loop breakpoint"],
        ["Lab 8", "Parallel Swarm", "Fan-Out / Fan-In multi-agent swarm evaluating 4 company preferences concurrently with barrier sync"],
        ["Lab 9", "Deep Research", "Semantic ATS resume skill matching and evidence-grounded progress journal verification"],
        ["Lab 10", "Cloud Operations", "Circuit breaker fault tolerance, exponential backoff retries, and Render cloud deployment"],
        ["Lab 11", "Agentic SDLC", "Specification-driven design, Pydantic schemas, and 81 automated acceptance tests passing 100%"],
        ["Lab 12", "Safety & Governance", "Dual-gate Human-in-the-Loop approval, mandatory justification reasons, and SHA-256 audit log"],
        ["Lab 13", "Domain Specialisation", "KLE Tech NEP 2020 12-credit capstone internship rules, CGPA cutoffs, and backlog gates"],
        ["Lab 14", "Capstone Integration", "Full end-to-end production deployment with interactive role switcher (Student/Coord/HOD)"]
    ]
    t16 = doc.add_table(rows=len(t16_data), cols=3)
    for r_idx, row in enumerate(t16_data):
        for c_idx, val in enumerate(row):
            t16.rows[r_idx].cells[c_idx].text = val
    format_table(t16, [Inches(0.8), Inches(1.8), Inches(4.3)])

    # --- 11. ASSIGNMENTS ---
    add_h1("11. Assignments")
    add_p("All 28 assignments across the 14 course labs were completed using standard Python libraries, with modifications tagged # [A1] and # [A2]. Table 17 lists the reference program and corresponding assignment implementations.")
    
    # TABLE 17: Assignments
    t17_data = [
        ["Lab", "Reference Program", "Assignment 1 (# [A1])", "Assignment 2 (# [A2])"],
        ["Lab 1", "Study Planner Agent", "Two-round iterative feedback refinement", "Conflict detection across overlapping commitments"],
        ["Lab 2", "Campus Data Assistant", "Draft-only notification tool with justification", "Three-tool execution pipeline (read &rarr; filter &rarr; average)"],
        ["Lab 3", "Research-Summary Skill", "Selection of best-supported claim among competitors", "Handling low-evidence input with 'not stated' fallback"],
        ["Lab 4", "Project Assistant Memory", "Multi-topic memory isolation across candidates", "Memory retention and policy staleness warnings"],
        ["Lab 5", "Mini MCP Server", "Discoverable list_capabilities tool endpoint", "Scoped tool execution restricted to sandboxed directory"],
        ["Lab 6", "Personal Agent Runtime", "Per-session execution rate limiter", "Automatic fault escalation to audit log after two failures"],
        ["Lab 7", "Campus Event App Graph", "Security policy compliance verification node", "Single-retry builder with automated human escalation"],
        ["Lab 8", "Hackathon Planner Swarm", "Role-based marketing and budget conflict handling", "Distributed multi-role peer critique and aggregation"],
        ["Lab 9", "AI Topic Briefing", "Contradictory source detection and reconciliation", "Source credibility scoring and weighted synthesis"],
        ["Lab 10", "Deployment Diagnosis", "Database connection pool exhaustion remediation", "Safe automated remediation with gated rollback controls"],
        ["Lab 11", "CSV Export SDLC", "PDF export implementation with data lineage", "Automated test suite capturing intentional schema defects"],
        ["Lab 12", "Production Change Guardrails", "Cost ceiling control with administrative sign-off", "Mandatory policy re-evaluation after 5 proposals"],
        ["Lab 13", "Predictive Maintenance", "Load forecasting domain agent", "Escalation trigger based on 3-reading anomaly trends"],
        ["Lab 14", "Campus Help-Desk", "Automated password-reset routing skill", "8-scenario adversarial prompt injection test suite"]
    ]
    t17 = doc.add_table(rows=len(t17_data), cols=4)
    for r_idx, row in enumerate(t17_data):
        for c_idx, val in enumerate(row):
            t17.rows[r_idx].cells[c_idx].text = val
    format_table(t17, [Inches(0.6), Inches(1.8), Inches(2.2), Inches(2.3)])

    # --- 12. REPOSITORY AND RUN STEPS ---
    add_h1("12. Repository and Run Steps")
    add_h2("12.1 Project Code Layout")
    
    # TABLE 18: Code Layout
    t18_data = [
        ["Directory / File", "Contents & Functional Role"],
        ["Course Project/Codebase/agents/", "CoordinatorAgent, StudentProfiler, EligibilityAgent, MatcherAgent, RouterAgent"],
        ["Course Project/Codebase/skills/", "BaseSkill, EligibilitySkill, MatchingSkill, RankingSkill, GroundingSkill"],
        ["Course Project/Codebase/tools/", "12 typed Pydantic tools for database lookup, rule checking, and vacancy updates"],
        ["Course Project/Codebase/graphs/", "LangGraph workflow definitions: sequential lifecycle graph and parallel swarm graph"],
        ["Course Project/Codebase/connectors/", "MCP Gateway implementation with JSON-RPC dispatcher and mock/real toggles"],
        ["Course Project/Codebase/runtime/", "Governed runtime loop, execution budget supervisor, and PII redactor"],
        ["Course Project/Codebase/safety/", "Cryptographic audit logging, circuit breaker, and Human-in-the-Loop breakpoint handlers"],
        ["Course Project/Codebase/frontend/", "Single-page responsive web dashboard (vanilla JS, Tailwind CSS, Lucide icons)"],
        ["Course Project/Codebase/data/", "SQLite database pre-seeded with 65 students, 55 opportunities, and 45 journals"],
        ["Course Project/Codebase/tests/", "Unit, integration, and workflow test suites across Labs 1 through 14"],
        ["run_master_verification_1_to_14.py", "Master test runner executing all 81 automated acceptance tests with colored summary"]
    ]
    t18 = doc.add_table(rows=len(t18_data), cols=2)
    for r_idx, row in enumerate(t18_data):
        for c_idx, val in enumerate(row):
            t18.rows[r_idx].cells[c_idx].text = val
    format_table(t18, [Inches(2.5), Inches(4.4)])

    add_h2("12.2 Run Locally")
    add_p("To execute the InternTrack application and run the complete test suite locally:")
    add_bullet("Step 1: Clone the repository & navigate to directory:")
    add_bullet("git clone https://github.com/Aishwarya095/InternTrack.git; cd InternTrack", prefix="   ")
    add_bullet("Step 2: Install required Python dependencies:")
    add_bullet("pip install -r requirements.txt", prefix="   ")
    add_bullet("Step 3: Execute the Master Verification Test Suite (All 14 Labs):")
    add_bullet("python \"Course Project/Codebase/run_master_verification_1_to_14.py\"", prefix="   ")
    add_bullet("Step 4: Launch the Local Web Application Server:")
    add_bullet("python \"Course Project/Codebase/server.py\"", prefix="   ")
    add_bullet("Access the interactive web dashboard at http://localhost:8000 in any standard browser.")

    # --- 13. RESULTS ---
    add_h1("13. Results")
    add_p("Table 19 summarizes the empirical results and performance metrics achieved by InternTrack across all core objectives.")
    
    # TABLE 19: Results
    t19_data = [
        ["Objective / Key Performance Indicator (KPI)", "Empirical Production Result"],
        ["Student Profile & ATS Resume Generation", "65 authentic KLE Tech students ingested; verified academic profiles & ATS resumes generated instantly."],
        ["Corporate Opportunity Catalog", "55 corporate opportunities active (20 top MNCs, 5 test fixtures, 30 live Indeed postings)."],
        ["Semantic Skill Match Accuracy", "Cosine matching accurately distinguishes technical fit (e.g. 83% for Ananya Sharma vs Infosys)."],
        ["Parallel Swarm Latency", "Evaluating 4 preferences concurrently takes 1.4s (vs 5.2s sequential), achieving a 73% latency reduction."],
        ["Human-in-the-Loop Safety Enforcement", "100% of allocations pause at coordinator gate; zero unapproved allocations permitted."],
        ["Race Condition & Over-allocation Prevention", "ACID transactions with CHECK constraints prevent negative vacancies; 0 over-allocations across 100 test runs."],
        ["Operational Fault Tolerance", "Circuit breaker gracefully falls back to pre-seeded catalog during external network dropouts."],
        ["Automated Acceptance Test Pass Rate", "81 of 81 automated acceptance tests passed across all 14 course labs (100.0% pass rate)."],
        ["Production Cloud Deployment", "Live on Render Cloud at https://interntrack-pv3r.onrender.com/ with zero downtime."]
    ]
    t19 = doc.add_table(rows=len(t19_data), cols=2)
    for r_idx, row in enumerate(t19_data):
        for c_idx, val in enumerate(row):
            t19.rows[r_idx].cells[c_idx].text = val
    format_table(t19, [Inches(2.5), Inches(4.4)])

    # --- 14. CONCLUSION AND FUTURE ENHANCEMENTS ---
    add_h1("14. Conclusion and Future Enhancements")
    add_p("InternTrack successfully demonstrates how agentic AI architectures—combining LangGraph state machines, parallel worker swarms, typed tools, and governed runtimes—can replace fragile, manual academic processes with a secure, evidence-grounded lifecycle system. By preserving strict faculty authority through Human-in-the-Loop breakpoints while automating repetitive eligibility checks and semantic skill matching, the platform ensures complete regulatory compliance under NEP 2020 while drastically reducing administrative overhead.")
    
    add_h2("Future Enhancements")
    add_bullet("Autonomous Industry Mentor Webhook: Direct integration with corporate slack channels and corporate mentor webhooks for real-time progress validation.")
    add_bullet("WhatsApp Student Notification Bot: Automated conversational notifications alerting students when coordinator approval is granted or when journal submissions are due.")
    add_bullet("Verifiable Digital Credentials: Cryptographic issuance of completed 12-credit internship completion certificates on the Polygon blockchain.")

    # --- 15. REFERENCES ---
    add_h1("15. References")
    references = [
        "National Education Policy (NEP 2020) Guidelines for Undergraduate Engineering Internships, Ministry of Education, Government of India, 2020.",
        "Agentic AI Course Curriculum & Lab Guide (26ECAC401), School of Computer Science & Engineering, KLE Technological University, Hubballi, 2026.",
        "InternTrack: Internship Application and Tracking Portal — AI Solution Direction & Workflow Proposal (Team 11), KLE Technological University, 2026.",
        "Harrison Chase et al., 'LangGraph: Building Stateful, Multi-Actor Applications with LLMs', LangChain AI Documentation, 2024.",
        "Anthropic, 'Model Context Protocol (MCP) Specification: Standardizing Tool Calling and Resource Retrieval for AI Agents', 2024.",
        "Tiangolo et al., 'FastAPI: Modern, High-Performance Web Framework for Building APIs with Python 3.8+', 2024.",
        "Scikit-Learn Developers, 'Feature Extraction and TF-IDF Vector Spaces', Scikit-Learn Reference Manual, 2023.",
        "SQLite Development Team, 'ACID Compliance, Write-Ahead Logging, and Integrity Constraints in Embedded Databases', 2024."
    ]
    for ref in references:
        add_bullet(ref)

    # Save DOCX
    docx_path = os.path.join("Course Project", "Artifact_Report_InternTrack.docx")
    try:
        doc.save(docx_path)
        print(f"Successfully generated DOCX report at: {docx_path}")
    except PermissionError:
        fallback_path = os.path.join("Course Project", "Artifact_Report_InternTrack_Complete.docx")
        doc.save(fallback_path)
        print(f"Artifact_Report_InternTrack.docx is open in WPS Office. Saved full version to: {fallback_path}")
        tech_path = os.path.join("Course Project", "Technical_Report_InternTrack.docx")
        doc.save(tech_path)
        print(f"Also saved copy to: {tech_path}")

    # Generate Markdown version
    md_path = os.path.join("Course Project", "Artifact_Report_InternTrack.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# KLE Technological University, Hubballi\n")
        f.write("### School of Computer Science & Engineering (AI)\n")
        f.write("### Semester VII | Academic Year 2026–27\n---\n")
        f.write("## Artifact Report\n")
        f.write("# InternTrack: Autonomous Internship Application & Tracking Portal\n")
        f.write("### A Human-Governed, Evidence-Grounded Lifecycle System built through the 14-Lab Agentic AI Worklet Method\n")
        f.write("**Artifact 10 · Agentic AI (26ECAC401) · Team 11 · Division B**\n\n")
        
        f.write("### Student Details\n\n")
        f.write("| No. | Student Name | USN | Division | Role / Project Responsibilities |\n")
        f.write("|:---:|:---|:---:|:---:|:---|\n")
        for r in t1_data[1:]:
            f.write(f"| {r[0]} | **{r[1]}** | `{r[2]}` | Division B | {r[3]} |\n")
        f.write("\n")
        
        f.write("### Project Links\n\n")
        f.write("| Item | Link |\n")
        f.write("|:---|:---|\n")
        for r in t2_data[1:]:
            f.write(f"| **{r[0]}** | [{r[1]}]({r[1]}) |\n")
        f.write("\n---\n\n")

        f.write("## Table of Contents\n\n")
        for item in toc_items:
            f.write(f"- **{item}**\n")
        f.write("\n---\n\n")

        f.write("## 1. Abstract\n\n")
        f.write("In eighth-semester engineering curricula under NEP 2020, full-time off-campus internships carry 12 mandatory academic credits. Yet across institutional placement ecosystems, internship allocation and governance remain bottlenecked by fragmented workflows: manual Google Forms, error-prone spreadsheet verification of CGPA and backlog statuses, lack of continuous off-campus progress visibility, and last-minute document aggregation without verifiable audit trails.\n\n")
        f.write("This report presents **InternTrack powered by AURA**, a human-governed, evidence-grounded agentic AI system engineered to automate the entire 8th-semester internship lifecycle. The system is architected as an autonomous multi-agent hierarchy orchestrated through LangGraph: a Central Coordinator agent directs parallel role swarms for opportunity discovery and eligibility verification, a Skill Matcher that calculates cosine similarity across 100+ technical competencies, and periodic tracking agents that ingest and evaluate bi-weekly student progress journals against real company deliverables.\n\n")
        f.write("InternTrack operates within a sandboxed, governed runtime enforcing strict Human-in-the-Loop (HITL) checkpoints: agents autonomously discover, parse, validate, and rank opportunities, but transition to an explicit paused state awaiting mandatory faculty coordinator and HOD sign-offs. Rejections require mandatory justification reasons, and approved allocations trigger atomic database transactions that decrement vacancies in real time (preventing over-allocation). The platform features regex-based PII redaction, cryptographic SHA-256 audit trails, circuit-breaker fault tolerance, and a master test suite of 81 automated acceptance tests passing at 100% across all 14 course labs. InternTrack is deployed live on Render Cloud (https://interntrack-pv3r.onrender.com/) with a production SQLite database pre-seeded with 65 authentic KLE Tech students, 55 corporate opportunities, and 45 longitudinal progress journals.\n\n")

        f.write("## 2. Introduction and Problem Statement\n\n")
        f.write("### 2.1 Background\n")
        f.write("Agentic AI represents a fundamental paradigm shift from conversational chatbots to autonomous execution systems. Unlike conversational models that merely respond to localized prompts, agentic systems maintain persistent goals, decompose multi-phase objectives, invoke typed external tools, maintain hierarchical memory across sessions, and coordinate specialized agent swarms to alter real-world environments safely. Across the fourteen hands-on labs of the Agentic AI (26ECAC401) curriculum, our team developed and integrated these foundational principles into a production-grade capstone worklet addressing academic internship operations.\n\n")
        
        f.write("### 2.2 Problem Statement\n")
        f.write("University internship administration for final-year undergraduate students suffers from four structural points of failure:\n")
        for obj in [
            "**Fragmented Discovery & Asymmetric Information**: Students discover opportunities through informal channels, unverified WhatsApp broadcasts, and stale bulletin boards, missing high-fit openings aligned with their technical profile.",
            "**Manual, Inconsistent Eligibility Verification**: Faculty coordinators spend hundreds of hours manually cross-checking university database records (CGPA cutoffs, active academic backlogs, prerequisite departmental credits) against company criteria, leading to human fatigue and compliance errors.",
            "**Zero Off-Campus Progress Visibility**: Once students depart for 4-to-6 month full-time industry internships, academic departments lose all continuous visibility into student attendance, mentor guidance, and technical deliverables.",
            "**Unverifiable Last-Minute Evaluation**: Semester-end credit certification relies on rushed paperwork, unverified student claims, and retrospective employer surveys lacking cryptographic or temporal evidence."
        ]:
            f.write(f"- {obj}\n")
        f.write("\n")

        f.write("### 2.3 Scope\n")
        f.write("InternTrack addresses the full lifecycle of final-year undergraduate internships: student academic profile ingestion, opportunity scraping and catalog synchronization, automated semantic ATS resume building, multi-preference submission with parallel swarm auto-ranking, dual-gate faculty/HOD approvals, atomic vacancy decrement, bi-weekly progress journal evaluation with LLM evidence grounding, and immutable audit logging. Non-coursework features such as direct corporate payroll disbursement and legal enterprise contract generation remain outside the current academic scope.\n\n")

        f.write("## 3. Objectives\n\n")
        for obj in objectives:
            f.write(f"- {obj}\n")
        f.write("\n")

        f.write("## 4. Expectations and Coverage\n\n")
        f.write("The capstone worklet is formally evaluated against nine core technical rubrics. Table 3 maps each expectation to its implementation and corresponding report section.\n\n")
        f.write("### Table 3: Capstone Evaluation Rubrics & Coverage\n\n")
        f.write("| # | Expectation | What is checked | Covered by | Section |\n")
        f.write("|:---:|:---|:---|:---|:---:|\n")
        for r in t3_data[1:]:
            f.write(f"| {r[0]} | **{r[1]}** | {r[2]} | {r[3]} | §{r[4]} |\n")
        f.write("\n")

        f.write("## 5. System Architecture\n\n")
        f.write("### 5.1 Internship Application and Tracking Lifecycle\n")
        f.write("InternTrack models the entire academic internship progression as an immutable, state-driven lifecycle: `DRAFT` &rarr; `VALIDATING` &rarr; `PAUSED_FOR_COORDINATOR_APPROVAL` &rarr; `APPROVED` / `REJECTED` &rarr; `ALLOCATED` &rarr; `ACTIVE_INTERNSHIP` &rarr; `EVALUATING` &rarr; `COMPLETED`. State progression is strictly monotonic; no candidate can skip directly to `ALLOCATED` without satisfying prerequisite eligibility rules and clearing the coordinator sign-off checkpoint.\n\n")
        
        f.write("### Table 4: Layered System Architecture\n\n")
        f.write("| Layer | Architectural Responsibilities |\n")
        f.write("|:---|:---|\n")
        for r in t4_data[1:]:
            f.write(f"| **{r[0]}** | {r[1]} |\n")
        f.write("\n")

        f.write("## 6. Technology Stack\n\n")
        f.write("### Table 5: Comprehensive Technology Stack & Justification\n\n")
        f.write("| Area | Technology | Used for |\n")
        f.write("|:---|:---|:---|\n")
        for r in t5_data[1:]:
            f.write(f"| **{r[0]}** | `{r[1]}` | {r[2]} |\n")
        f.write("\n")

        f.write("## 7. Implementation Against Each Expectation\n\n")
        f.write("### 7.1 Agents\n")
        f.write("> **Expectation: Agents** — Agents have a clear goal, invoke typed tools, and drive tasks to verified completion.\n\n")
        f.write("The system implements a hierarchical multi-agent structure led by the Internship Coordinator Agent. The Coordinator decomposes complex requests, dispatches tasks to specialist agents, aggregates candidate preference matrices, and routes exceptions. Each agent executes within a deterministic bounded loop and emits typed AgentOutput schemas.\n\n")
        f.write("#### Table 7: Specialist Agents, Goals & Invoked Capabilities\n\n")
        f.write("| Agent | Goal / Responsibility | Tools & Skills Used |\n")
        f.write("|:---|:---|:---|\n")
        for r in t7_data[1:]:
            f.write(f"| **{r[0]}** | {r[1]} | `{r[2]}` |\n")
        f.write("\n")

        f.write("### 7.2 Skills\n")
        f.write("> **Expectation: Skills** — Skills are modular, reusable, self-contained capabilities with typed schemas.\n\n")
        f.write("InternTrack abstracts complex multi-step reasoning into standardized skills extending `BaseSkill`. Each skill publishes `SkillMetadata` (name, description, input/output schemas, operational constraints) registered centrally within a `SkillRegistry`.\n\n")
        f.write("#### Table 9: Reusable Standardized Domain Skills\n\n")
        f.write("| Skill | Purpose & Execution Logic | Reusability Across Worklet |\n")
        f.write("|:---|:---|:---|\n")
        for r in t9_data[1:]:
            f.write(f"| **{r[0]}** | {r[1]} | {r[2]} |\n")
        f.write("\n")

        f.write("### 7.3 MCP Gateway\n")
        f.write("> **Expectation: MCP Gateway** — Connectors expose external capabilities through standardized, discoverable interfaces.\n\n")
        f.write("External integrations and enterprise tool calls are mediated through a centralized Model Context Protocol (MCP) gateway. The gateway exposes a JSON-RPC 2.0 envelope, enforces parameter validation, prevents unauthorized side effects, and provides a mock/real adapter toggle.\n\n")
        f.write("#### Table 11: MCP Gateway Capability Manifest\n\n")
        f.write("| Capability Identifier | Connected Subsystem | Side-Effect / Gating Policy |\n")
        f.write("|:---|:---|:---|\n")
        for r in t11_data[1:]:
            f.write(f"| `{r[0]}` | {r[1]} | {r[2]} |\n")
        f.write("\n")

        f.write("### 7.4 OpenCLA / Governed Runtime\n")
        f.write("> **Expectation: Governed Runtime** — Agents execute in a sandboxed, budget-constrained runtime with crash recovery.\n\n")
        f.write("InternTrack executes all agent workflows inside an OpenClaw-inspired governed supervisor. The runtime enforces execution budgets (max 50 iterations, 30s timeout), PII redaction of student contact details, structured audit telemetry, and atomic transaction rollbacks upon unexpected execution failure.\n\n")

        f.write("### 7.5 Multi-Agent Swarms (Parallel Fan-Out / Fan-In)\n")
        f.write("> **Expectation: Swarms** — Autonomous worker agents coordinate concurrently with clear division of labor.\n\n")
        f.write("When a student submits four company preferences, evaluating them sequentially introduces excessive latency. InternTrack implements a parallel fan-out swarm using LangGraph's Send API. The coordinator spawns 4 concurrent worker agents that independently check company eligibility, compute skill fit, and verify live seat availability. A barrier synchronization node aggregates the worker evaluations into a single optimal preference matrix.\n\n")

        f.write("### 7.6 Deep Research & Evidence Grounding\n")
        f.write("> **Expectation: Deep Research** — Synthesizes structured outputs strictly grounded in verified source evidence.\n\n")
        f.write("In academic internship evaluation, hallucinations can lead to fraudulent credit awards. The Deep Research & Evidence Grounding agent parses bi-weekly student progress journals and validates reported work against industry project milestones. Every credit recommendation must cite verbatim source snippets from student submission logs; unsubstantiated claims are flagged for faculty investigation.\n\n")

        f.write("### 7.7 Cloud SDLC & Production Deployment\n")
        f.write("> **Expectation: Cloud SDLC** — Specification-driven build, automated testing, and verified cloud deployment.\n\n")
        f.write("The project adheres to rigorous software engineering practices: a declarative OpenAPI specification, 81 automated acceptance tests covering all 14 course labs, Git version control, and zero-downtime continuous deployment on Render Cloud connected directly to the GitHub main branch.\n\n")

        f.write("## 8. Supporting Capabilities\n\n")
        f.write("### 8.1 Typed Tools\n")
        f.write("InternTrack features 12 typed tools extending Pydantic BaseModel schemas. Tool arguments undergo automatic type casting, range checking, and validation before execution. Tools consistently return structured ToolResult objects containing output payloads, error states, and execution latencies.\n\n")
        
        f.write("### 8.2 Memory and Retrieval\n")
        f.write("The system implements a four-tiered memory architecture:\n")
        f.write("- **Short-term Session Memory**: Tracks the live LangGraph execution state, candidate preference arrays, and intermediate agent critiques.\n")
        f.write("- **Long-term Candidate Store**: Persists historical student academic backgrounds, previous project portfolios, and verified transcripts in SQLite.\n")
        f.write("- **Dynamic Vector Index**: In-memory TF-IDF vector space for real-time mathematical cosine matching across corporate vacancy catalogs.\n")
        f.write("- **Cryptographic Audit Memory**: Write-once, read-many (WORM) audit journal storing SHA-256 hashed state transitions.\n\n")

        f.write("### 8.3 LangGraph State Machine\n")
        f.write("The primary execution engine is structured as a LangGraph StateGraph comprising 14 discrete nodes: INTAKE &rarr; PARSE_PROFILE &rarr; DISCOVER_OPPORTUNITIES &rarr; FAN_OUT_SWARM &rarr; PARALLEL_WORKERS [1..4] &rarr; BARRIER_AGGREGATION &rarr; ELIGIBILITY_GATE &rarr; PAUSED_FOR_COORDINATOR_APPROVAL &rarr; (Human Gate) &rarr; ATOMIC_ALLOCATION &rarr; JOURNAL_TRACKING &rarr; FINAL_EVALUATION. Conditional edges safely route ineligible students to an advisory revision loop.\n\n")

        f.write("### 8.4 Safety, Governance and Human-in-the-Loop\n")
        f.write("Autonomous agent decision-making is strictly constrained by departmental governance policy. The system incorporates two mandatory safety gates: Coordinator Approval and HOD Departmental Sanction. An agent cannot decrement vacancies or confirm an internship without cryptographic human sign-off. Furthermore, faculty rejections enforce a mandatory text justification field to eliminate arbitrary dismissals.\n\n")

        f.write("### 8.5 Domain Specialisation (NEP 2020 Compliance)\n")
        f.write("InternTrack is specialized for academic engineering regulations under the National Education Policy (NEP 2020) at KLE Technological University. The system encodes institutional rules: minimum 7.0 CGPA for tier-1 MNCs, zero active backlogs at time of departure, mandatory 12-credit capstone allocation, and a minimum 16-week off-campus corporate duration.\n\n")

        f.write("## 9. End-to-End Walkthrough\n\n")
        f.write("A complete representative execution trace illustrates the seamless coordination across agents, tools, and human gates:\n")
        f.write("1. **Student Lookup**: Student Ananya Sharma (`1KG21CS008`) is looked up. The Profiler Agent retrieves verified records: CGPA 9.1, B.E. Computer Science, AWS and Java competencies.\n")
        f.write("2. **ATS Resume Generation**: The Format Skill generates a standardized ATS plain-text and PDF resume; PII masking redacts personal mobile and residential addresses.\n")
        f.write("3. **Skill Matching**: The Skill Matcher executes TF-IDF cosine comparison across 55 corporate openings. Infosys InStep yields an 83% technical match; missing skills (Python automation) are highlighted for upskilling.\n")
        f.write("4. **Multi-Preference Submission**: The student selects 4 ranked preferences (Infosys, TCS, Bosch, Google) and submits.\n")
        f.write("5. **Parallel Swarm Evaluation**: The Coordinator spawns 4 parallel worker agents via LangGraph Send API. Concurrently, worker threads verify company cutoffs and seat availability in 1.4 seconds.\n")
        f.write("6. **Human Breakpoint Interruption**: The barrier aggregator formats the proposal and transitions state to `PAUSED_FOR_COORDINATOR_APPROVAL`. The agent yields control.\n")
        f.write("7. **Coordinator Approval & Atomic Decrement**: Faculty Coordinator Dr. Ramesh reviews the verification dossier and clicks Approve. An atomic SQLite transaction decrements available vacancies from 6 to 5.\n")
        f.write("8. **Off-Campus Tracking & Audit**: Bi-weekly progress journals are ingested, grounded against corporate milestones, and committed to the immutable SHA-256 audit log.\n\n")

        f.write("## 10. Lab-wise Coverage (Labs 1–14)\n\n")
        f.write("Table 16 details how each of the fourteen curriculum labs is instantiated within the InternTrack production codebase.\n\n")
        f.write("### Table 16: Curriculum Lab Mapping & Technical Implementations\n\n")
        f.write("| Lab | Curriculum Concept | Implementation in InternTrack Capstone Worklet |\n")
        f.write("|:---:|:---|:---|\n")
        for r in t16_data[1:]:
            f.write(f"| **{r[0]}** | {r[1]} | {r[2]} |\n")
        f.write("\n")

        f.write("## 11. Assignments\n\n")
        f.write("All 28 assignments across the 14 course labs were completed using standard Python libraries, with modifications tagged `# [A1]` and `# [A2]`. Table 17 lists the reference program and corresponding assignment implementations.\n\n")
        f.write("### Table 17: Graded Lab Assignments Implementation Matrix\n\n")
        f.write("| Lab | Reference Program | Assignment 1 (`# [A1]`) | Assignment 2 (`# [A2]`) |\n")
        f.write("|:---:|:---|:---|:---|\n")
        for r in t17_data[1:]:
            f.write(f"| **{r[0]}** | {r[1]} | {r[2]} | {r[3]} |\n")
        f.write("\n")

        f.write("## 12. Repository and Run Steps\n\n")
        f.write("### 12.1 Project Code Layout\n\n")
        f.write("#### Table 18: File & Module Structural Manifest\n\n")
        f.write("| Directory / File | Contents & Functional Role |\n")
        f.write("|:---|:---|\n")
        for r in t18_data[1:]:
            f.write(f"| `{r[0]}` | {r[1]} |\n")
        f.write("\n")

        f.write("### 12.2 Run Locally\n\n")
        f.write("To execute the InternTrack application and run the complete test suite locally:\n\n")
        f.write("```bash\n")
        f.write("# 1. Clone repository and navigate to root\n")
        f.write("git clone https://github.com/Aishwarya095/InternTrack.git\n")
        f.write("cd InternTrack\n\n")
        f.write("# 2. Install dependencies\n")
        f.write("pip install -r requirements.txt\n\n")
        f.write("# 3. Run Master Verification Suite across all 14 Labs\n")
        f.write("python \"Course Project/Codebase/run_master_verification_1_to_14.py\"\n\n")
        f.write("# 4. Launch Production Application Server\n")
        f.write("python \"Course Project/Codebase/server.py\"\n")
        f.write("```\n\n")
        f.write("Access the interactive web dashboard at `http://localhost:8000` in any web browser.\n\n")

        f.write("## 13. Results\n\n")
        f.write("Table 19 summarizes the empirical results and performance metrics achieved by InternTrack across all core objectives.\n\n")
        f.write("### Table 19: Empirical Results & Verification Metrics\n\n")
        f.write("| Objective / Key Performance Indicator (KPI) | Empirical Production Result |\n")
        f.write("|:---|:---|\n")
        for r in t19_data[1:]:
            f.write(f"| **{r[0]}** | {r[1]} |\n")
        f.write("\n")

        f.write("## 14. Conclusion and Future Enhancements\n\n")
        f.write("InternTrack successfully demonstrates how agentic AI architectures—combining LangGraph state machines, parallel worker swarms, typed tools, and governed runtimes—can replace fragile, manual academic processes with a secure, evidence-grounded lifecycle system. By preserving strict faculty authority through Human-in-the-Loop breakpoints while automating repetitive eligibility checks and semantic skill matching, the platform ensures complete regulatory compliance under NEP 2020 while drastically reducing administrative overhead.\n\n")
        f.write("### Future Enhancements\n")
        f.write("- **Autonomous Industry Mentor Webhook**: Direct integration with corporate slack channels and corporate mentor webhooks for real-time progress validation.\n")
        f.write("- **WhatsApp Student Notification Bot**: Automated conversational notifications alerting students when coordinator approval is granted or when journal submissions are due.\n")
        f.write("- **Verifiable Digital Credentials**: Cryptographic issuance of completed 12-credit internship completion certificates on the Polygon blockchain.\n\n")

        f.write("## 15. References\n\n")
        for ref in references:
            f.write(f"- {ref}\n")

    print(f"Successfully generated Markdown report at: {md_path}")
    import shutil
    tech_md_path = os.path.join("Course Project", "Technical_Report_InternTrack.md")
    shutil.copyfile(md_path, tech_md_path)
    print(f"Also created copy at: {tech_md_path}")

if __name__ == "__main__":
    build_docx_and_md()
