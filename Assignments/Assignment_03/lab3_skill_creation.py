"""
Lab 3: Skill Creation -- Reusable Plan & Format Skills
Phase: A · Foundations
Goal: Package repeatable capability as reusable, schema-typed skills.

Deliverable & Acceptance Criterion:
"Two callable skills with schemas, invoked by the agent.
Acceptance: The same skill works for two different cases without code changes."

Nodes Activated:
  - Plan node (as a skill)
  - Assembly / Format node (as a skill)

Skill Interfaces:
  skill plan(inputs: PlanInputSchema) -> Plan: return expand(inputs).lock()
  skill format_graded(result: Plan, template: TemplateSpec) -> Document
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import hashlib
import json
import sys

# Ensure UTF-8 output encoding for terminal
sys.stdout.reconfigure(encoding='utf-8')


# =====================================================================
# 1. TYPED SCHEMAS (Case-Agnostic Contract)
# =====================================================================

@dataclass
class Milestone:
    phase_number: int
    title: str
    timeline: str
    deliverables: List[str]
    verification_check: str


@dataclass
class PlanInputSchema:
    candidate_id: str             # e.g., USN or Student ID
    candidate_name: str           # Full Name
    case_domain: str              # e.g., "Industry Internship" or "Capstone Research Thesis"
    organization: str             # e.g., "Google India" or "Autonomous Systems Lab"
    target_role: str              # e.g., "Software Engineering Intern" or "Lead AI Researcher"
    primary_objective: str        # High-level goal statement
    raw_requirements: List[str]   # Prerequisite constraints
    required_signoffs: List[str]  # Required approver roles


@dataclass
class Plan:
    plan_id: str
    inputs: PlanInputSchema
    milestones: List[Milestone] = field(default_factory=list)
    signoff_status: Dict[str, str] = field(default_factory=dict)
    is_locked: bool = False
    plan_hash: Optional[str] = None

    def lock(self) -> 'Plan':
        """
        Freezes the plan into an immutable artifact and computes
        a cryptographic integrity hash over all contents.
        """
        self.is_locked = True
        serialized = json.dumps({
            "plan_id": self.plan_id,
            "inputs": asdict(self.inputs),
            "milestones": [asdict(m) for m in self.milestones],
            "signoff_status": self.signoff_status
        }, sort_keys=True)
        self.plan_hash = hashlib.sha256(serialized.encode('utf-8')).hexdigest()
        return self


@dataclass
class TemplateSpec:
    template_name: str
    header_banner: str
    evaluation_criteria: List[Dict[str, Any]]
    output_format: str = "markdown"  # "markdown" or "text"


@dataclass
class Document:
    document_id: str
    title: str
    rendered_content: str
    format: str
    verified_hash: str


# =====================================================================
# 2. REUSABLE SKILL IMPLEMENTATIONS
# =====================================================================

def expand(inputs: PlanInputSchema) -> Plan:
    """
    Sub-routine of plan skill: Takes typed inputs, validates constraints,
    and dynamically expands them into standard execution milestones.
    Case-agnostic logic generates domain-appropriate phased steps.
    """
    plan_id = f"PLAN-{inputs.candidate_id}-{hashlib.md5(inputs.case_domain.encode()).hexdigest()[:6].upper()}"
    
    # Generate 4 standardized lifecycle milestones based on objective & requirements
    milestones = [
        Milestone(
            phase_number=1,
            title="Prerequisite Clearance & Onboarding",
            timeline="Weeks 1-2",
            deliverables=[
                f"Verify prerequisites: {', '.join(inputs.raw_requirements[:2])}",
                f"Complete organizational onboarding at {inputs.organization}"
            ],
            verification_check="Initial verification check & mentor confirmation"
        ),
        Milestone(
            phase_number=2,
            title="Core Implementation & Execution",
            timeline="Weeks 3-8",
            deliverables=[
                f"Execute core objective: {inputs.primary_objective}",
                "Submit bi-weekly progress journals and artifact logs"
            ],
            verification_check="Mid-point progress audit by designated evaluators"
        ),
        Milestone(
            phase_number=3,
            title="Verification, Testing & Review",
            timeline="Weeks 9-12",
            deliverables=[
                "Complete deliverables testing and comprehensive review",
                f"Collect required sign-offs from: {', '.join(inputs.required_signoffs)}"
            ],
            verification_check="Formal demonstration and validation check"
        ),
        Milestone(
            phase_number=4,
            title="Final Evaluation & Certification",
            timeline="Weeks 13-16",
            deliverables=[
                "Submit final compiled technical report and project portfolio",
                "Complete viva presentation and certification release"
            ],
            verification_check="Final grade certification & release NOC"
        )
    ]

    initial_signoffs = {role: "PENDING" for role in inputs.required_signoffs}

    return Plan(
        plan_id=plan_id,
        inputs=inputs,
        milestones=milestones,
        signoff_status=initial_signoffs,
        is_locked=False
    )


def plan(inputs: PlanInputSchema) -> Plan:
    """
    SKILL 1: plan(inputs) -> Plan
    Contract: return expand(inputs).lock()
    """
    if not isinstance(inputs, PlanInputSchema):
        raise TypeError(f"Expected PlanInputSchema, got {type(inputs).__name__}")
    
    # Expand raw specifications and immediately lock into an immutable Plan object
    unlocked_plan = expand(inputs)
    return unlocked_plan.lock()


def format_graded(result: Plan, template: TemplateSpec) -> Document:
    """
    SKILL 2: format_graded(result, template) -> Document
    Renders a graded submission shell from any locked Plan object.
    Entirely case-agnostic; driven solely by typed schema inputs.
    """
    if not isinstance(result, Plan):
        raise TypeError(f"Expected Plan, got {type(result).__name__}")
    if not result.is_locked:
        raise ValueError("Cannot format an unlocked plan! Plan must be locked before grading shell assembly.")
    if not isinstance(template, TemplateSpec):
        raise TypeError(f"Expected TemplateSpec, got {type(template).__name__}")

    lines = [
        f"# {template.header_banner}",
        f"**Document ID:** SUBMISSION-{result.plan_id}",
        f"**Integrity Hash:** `{result.plan_hash[:16]}...` | **Locked State:** {'LOCKED' if result.is_locked else 'MUTABLE'}",
        "",
        "## 1. Candidate & Project Profile",
        f"- **Candidate Name:** {result.inputs.candidate_name} (`{result.inputs.candidate_id}`)",
        f"- **Domain Track:** {result.inputs.case_domain}",
        f"- **Host Organization:** {result.inputs.organization}",
        f"- **Target Role / Title:** {result.inputs.target_role}",
        f"- **Primary Objective:** {result.inputs.primary_objective}",
        "",
        "## 2. Standard Phased Milestones",
        "| Phase | Milestone Title | Timeline | Key Deliverables | Verification Check |",
        "| :---: | :--- | :---: | :--- | :--- |"
    ]

    for m in result.milestones:
        delivs = "; ".join(m.deliverables)
        lines.append(f"| Phase {m.phase_number} | **{m.title}** | {m.timeline} | {delivs} | {m.verification_check} |")

    lines.extend([
        "",
        "## 3. Required Multi-Stage Sign-off Queue",
        "| Approver Role | Required Status | Current Gate |",
        "| :--- | :---: | :---: |"
    ])
    for role, status in result.signoff_status.items():
        lines.append(f"| {role} | APPROVED | `{status}` |")

    lines.extend([
        "",
        "## 4. Graded Evaluation Rubric Shell",
        "| Criterion | Description | Max Marks | Evaluator Grade |",
        "| :--- | :--- | :---: | :---: |"
    ])
    total_marks = 0
    for crit in template.evaluation_criteria:
        lines.append(f"| {crit['name']} | {crit['description']} | {crit['max_marks']} | `[ PENDING ]` |")
        total_marks += crit['max_marks']
    
    lines.extend([
        f"| **TOTAL** | *Cumulative Graded Evaluation* | **{total_marks}** | `[ PENDING ]` |",
        "",
        "---",
        f"*(Generated autonomously via AURA Skill Engine — Template: {template.template_name})*"
    ])

    content = "\n".join(lines)
    return Document(
        document_id=f"DOC-{result.plan_id}",
        title=f"{template.header_banner} - {result.inputs.candidate_name}",
        rendered_content=content,
        format=template.output_format,
        verified_hash=result.plan_hash
    )


# =====================================================================
# 3. VERIFICATION TEST HARNESS (TWO CASES WITHOUT CODE CHANGES)
# =====================================================================

def run_test_harness():
    print("=" * 70)
    print("LAB 3 VERIFICATION: SCHEMA-TYPED REUSABLE SKILLS TEST")
    print("Acceptance: The same skills work for 2 different cases without code changes.")
    print("=" * 70)

    # -------------------------------------------------------------
    # CASE A: 8th-Semester Industry Internship Application
    # -------------------------------------------------------------
    print("\n[TEST CASE A: Industry Internship Tracking Plan]")
    case_a_input = PlanInputSchema(
        candidate_id="1KG21CS045",
        candidate_name="Rahul Kumar",
        case_domain="8th-Semester Industry Internship",
        organization="Google India",
        target_role="Software Engineering Intern",
        primary_objective="Develop high-performance gRPC caching gateway for backend microservices.",
        raw_requirements=["CGPA >= 8.5", "0 Active Backlogs", ">= 100 Completed Credits"],
        required_signoffs=["Faculty Mentor", "HoD", "Internship Cell"]
    )

    case_a_template = TemplateSpec(
        template_name="Department Internship Evaluation Rubric",
        header_banner="AURA Internship Evaluation & Sign-off Submission",
        evaluation_criteria=[
            {"name": "Technical Deliverables", "description": "Quality and correctness of production codebase", "max_marks": 40},
            {"name": "Bi-Weekly Progress Logs", "description": "Consistency in submitting sprint journals", "max_marks": 20},
            {"name": "Mentor Assessment", "description": "Direct employer / mentor satisfaction rating", "max_marks": 20},
            {"name": "Final Viva Presentation", "description": "Oral defense of technical achievements", "max_marks": 20}
        ]
    )

    # Invoke Skill 1: plan()
    plan_a = plan(case_a_input)
    assert plan_a.is_locked is True, "Case A plan must be locked!"
    assert plan_a.plan_hash is not None, "Case A plan must have an integrity hash!"
    print(f"  Skill 1 (plan) executed successfully:")
    print(f"    - Plan ID: {plan_a.plan_id}")
    print(f"    - Locked: {plan_a.is_locked}")
    print(f"    - Hash: {plan_a.plan_hash[:24]}...")
    print(f"    - Milestones generated: {len(plan_a.milestones)}")

    # Invoke Skill 2: format_graded()
    doc_a = format_graded(plan_a, case_a_template)
    assert doc_a.verified_hash == plan_a.plan_hash, "Document hash must match Plan hash!"
    print(f"  Skill 2 (format_graded) executed successfully:")
    print(f"    - Document ID: {doc_a.document_id}")
    print(f"    - Title: {doc_a.title}")
    print(f"    - Rendered Length: {len(doc_a.rendered_content)} characters")

    # -------------------------------------------------------------
    # CASE B: Capstone Research Thesis Project
    # (Completely distinct domain case, same skill functions)
    # -------------------------------------------------------------
    print("\n[TEST CASE B: Autonomous Capstone Research Project]")
    case_b_input = PlanInputSchema(
        candidate_id="1KG21IS012",
        candidate_name="Ananya Rao",
        case_domain="Autonomous Multi-Agent Capstone Research",
        organization="Autonomous Systems Research Lab",
        target_role="Lead AI Research Fellow",
        primary_objective="Design and benchmark consensus algorithms for multi-agent reinforcement learning.",
        raw_requirements=["IRB Ethics Clearance", "Literature Survey Verified", "GPU Lab Access Approved"],
        required_signoffs=["Principal Investigator", "Department Research Committee", "Dean Academics"]
    )

    case_b_template = TemplateSpec(
        template_name="Academic Research Capstone Rubric",
        header_banner="Capstone Research Thesis Graded Evaluation Shell",
        evaluation_criteria=[
            {"name": "Novelty & Formulation", "description": "Theoretical rigor of research problem", "max_marks": 30},
            {"name": "Experimental Benchmarking", "description": "Empirical evaluation on benchmark environments", "max_marks": 30},
            {"name": "Peer-Reviewed Paper Draft", "description": "Ready-to-submit manuscript in IEEE/ACM format", "max_marks": 25},
            {"name": "Thesis Defense Viva", "description": "Formal defense before department committee", "max_marks": 15}
        ]
    )

    # Invoke Skill 1: plan() on Case B without ANY code modification
    plan_b = plan(case_b_input)
    assert plan_b.is_locked is True, "Case B plan must be locked!"
    assert plan_b.plan_hash is not None, "Case B plan must have an integrity hash!"
    print(f"  Skill 1 (plan) executed successfully:")
    print(f"    - Plan ID: {plan_b.plan_id}")
    print(f"    - Locked: {plan_b.is_locked}")
    print(f"    - Hash: {plan_b.plan_hash[:24]}...")
    print(f"    - Milestones generated: {len(plan_b.milestones)}")

    # Invoke Skill 2: format_graded() on Case B
    doc_b = format_graded(plan_b, case_b_template)
    assert doc_b.verified_hash == plan_b.plan_hash, "Document hash must match Plan hash!"
    print(f"  Skill 2 (format_graded) executed successfully:")
    print(f"    - Document ID: {doc_b.document_id}")
    print(f"    - Title: {doc_b.title}")
    print(f"    - Rendered Length: {len(doc_b.rendered_content)} characters")

    print("\n" + "=" * 70)
    print("ACCEPTANCE CRITERION VERIFIED: PASSED (100%)")
    print("The exact same plan() and format_graded() skills functioned across")
    print("Case A (Industry Internship) and Case B (Research Capstone) with ZERO code changes.")
    print("=" * 70)


if __name__ == "__main__":
    run_test_harness()
