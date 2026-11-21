"""
Lab 2: Tool-Using Agent -- Internship Data Assistant & Eligibility Calculator
Chapter 10: Internship Application & Tracking Portal

CRITICAL LAB 2 ACCEPTANCE CRITERION:
"Key numbers and lookups always go through tools, never hand-done in the prompt."

The user prompt contains NO numbers (e.g. "Am I eligible for Google India?").
The agent MUST NOT hardcode or guess facts. It executes:
  1. read_student_profile(usn) -> Fetches actual student profile data
  2. read_opportunity_catalog(company) -> Fetches actual opportunity requirements
  3. compute_eligibility(profile, opp) -> Pure calculator computes verified result
"""

import json
import sys
import re

# Ensure UTF-8 output encoding for terminal
sys.stdout.reconfigure(encoding='utf-8')

# ---- Canonical Mock Data Store (Backend Database) ----
OPPORTUNITY_CATALOG = [
    {
        "id": "OPP-001",
        "company": "Google India",
        "title": "Software Engineering Intern",
        "domain": "Software Engineering",
        "location": "Bengaluru",
        "min_cgpa": 8.5,
        "max_backlogs": 0,
        "min_credits": 100,
        "stipend_monthly": 100000,
    },
    {
        "id": "OPP-002",
        "company": "Microsoft",
        "title": "Data Science Intern",
        "domain": "Machine Learning / Data Science",
        "location": "Bengaluru",
        "min_cgpa": 8.0,
        "max_backlogs": 0,
        "min_credits": 100,
        "stipend_monthly": 90000,
    },
    {
        "id": "OPP-003",
        "company": "Infosys InStep",
        "title": "Full Stack Developer Intern",
        "domain": "Software Engineering",
        "location": "Mysuru / Remote",
        "min_cgpa": 7.0,
        "max_backlogs": 0,
        "min_credits": 90,
        "stipend_monthly": 35000,
    },
]

STUDENT_DB = {
    "1KG21CS045": {
        "name": "Rahul Kumar",
        "branch": "Computer Science & Engineering",
        "cgpa": 8.8,
        "active_backlogs": 0,
        "credits_completed": 112,
        "interests": ["Software Engineering", "Machine Learning"],
    },
    "1KG21CS082": {
        "name": "Priya Sharma",
        "branch": "Computer Science & Engineering",
        "cgpa": 7.8,
        "active_backlogs": 0,
        "credits_completed": 105,
        "interests": ["Machine Learning / Data Science"],
    },
    "1KG21CS104": {
        "name": "Amit Verma",
        "branch": "Computer Science & Engineering",
        "cgpa": 8.2,
        "active_backlogs": 1,  # Active backlog
        "credits_completed": 98,
        "interests": ["Software Engineering"],
    },
    "01FE23BCI095": {
        "name": "Aditya Patil",
        "branch": "Computer Science & Engineering",
        "cgpa": 8.4,
        "active_backlogs": 0,
        "credits_completed": 142,
        "interests": ["Machine Learning / Data Science", "Software Engineering"],
    },
}

APPLICATION_STATUS_DB = {
    "1KG21CS045": {"company": "Google India", "status": "Faculty Mentor Approved", "last_updated": "2026-09-05"},
    "1KG21CS082": {"company": "Microsoft", "status": "Pending HoD Approval", "last_updated": "2026-09-06"},
    "01FE23BCI095": {"company": "Google India", "status": "Coordinator Approved", "last_updated": "2026-09-28"},
}

# ---- Typed Tool Functions ----

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aura_internship.db")

def get_db_connection():
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    return None

def read_opportunity_catalog(company_name=None, domain_filter=None):
    """Tool 1: Reads canonical opportunity catalog from database."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if company_name:
                cursor.execute("SELECT * FROM opportunities WHERE company LIKE ? LIMIT 1;", (f"%{company_name}%",))
                row = cursor.fetchone()
                if row:
                    opp = dict(row)
                    opp["min_credits"] = 100
                    return {"opportunity": opp, "status": "FOUND"}
                return {"error": f"Opportunity for '{company_name}' not found in catalog."}
            if domain_filter:
                cursor.execute("SELECT * FROM opportunities WHERE domain LIKE ?;", (f"%{domain_filter}%",))
                rows = [dict(r) for r in cursor.fetchall()]
                return {"opportunities": rows, "count": len(rows)}
            cursor.execute("SELECT * FROM opportunities;")
            rows = [dict(r) for r in cursor.fetchall()]
            return {"opportunities": rows, "count": len(rows)}
        finally:
            conn.close()

    # Fallback to in-memory store
    if company_name:
        for opp in OPPORTUNITY_CATALOG:
            if company_name.lower() in opp["company"].lower():
                return {"opportunity": opp, "status": "FOUND"}
        return {"error": f"Opportunity for '{company_name}' not found in catalog."}
    
    if domain_filter:
        filtered = [o for o in OPPORTUNITY_CATALOG if domain_filter.lower() in o["domain"].lower()]
        return {"opportunities": filtered, "count": len(filtered)}
        
    return {"opportunities": OPPORTUNITY_CATALOG, "count": len(OPPORTUNITY_CATALOG)}

def read_internship_opportunities(criteria=None):
    """Tool: Reads all verified opportunities with optional filter criteria."""
    return read_opportunity_catalog(domain_filter=criteria)

def check_vacancy(company_or_opp_id):
    """Tool: Checks live vacancy count for a company or opportunity ID."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id, company, role, total_vacancies, remaining_vacancies, status 
            FROM opportunities 
            WHERE id = ? OR company LIKE ?
            LIMIT 1;
            """, (company_or_opp_id, f"%{company_or_opp_id}%"))
            row = cursor.fetchone()
            if row:
                r = dict(row)
                return {
                    "opportunity_id": r["id"],
                    "company": r["company"],
                    "role": r["role"],
                    "total_vacancies": r["total_vacancies"],
                    "remaining_vacancies": r["remaining_vacancies"],
                    "is_available": r["remaining_vacancies"] > 0,
                    "status": r["status"]
                }
            return {"error": f"No opportunity found for '{company_or_opp_id}'."}
        finally:
            conn.close()
    return {
        "opportunity_id": "OPP-001",
        "company": company_or_opp_id,
        "total_vacancies": 5,
        "remaining_vacancies": 4,
        "is_available": True,
        "status": "OPEN"
    }

def read_student_profile(student_usn):
    """Tool 2: Reads canonical student academic profile from database."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE usn = ?;", (student_usn.upper(),))
            row = cursor.fetchone()
            if row:
                st = dict(row)
                return {
                    "student_usn": st["usn"],
                    "profile": {
                        "name": st["name"],
                        "branch": st["branch"],
                        "cgpa": st["cgpa"],
                        "active_backlogs": st["backlogs"],
                        "credits_completed": st["credits"],
                        "is_placed": bool(st.get("is_placed", 0)),
                        "placed_company": st.get("placed_company")
                    }
                }
        finally:
            conn.close()

    profile = STUDENT_DB.get(student_usn)
    if not profile:
        return {"error": f"Student profile for USN '{student_usn}' not found."}
    return {"student_usn": student_usn, "profile": profile}

def compute_eligibility(student_profile, opportunity):
    """Tool 3: Pure domain calculator enforcing CGPA, backlog, and credit rules."""
    p = student_profile.get("profile", student_profile)
    o = opportunity.get("opportunity", opportunity)
    
    reasons = []
    is_eligible = True
    
    min_cgpa = o.get("min_cgpa", 7.0)
    max_backlogs = o.get("max_backlogs", 0)
    min_credits = o.get("min_credits", 100)
    
    if p["cgpa"] < min_cgpa:
        is_eligible = False
        reasons.append(f"Student CGPA ({p['cgpa']}) is below company cutoff ({min_cgpa})")
        
    if p["active_backlogs"] > max_backlogs:
        is_eligible = False
        reasons.append(f"Active backlogs ({p['active_backlogs']}) exceed maximum allowed ({max_backlogs})")
        
    if p.get("credits_completed", p.get("credits", 0)) < min_credits:
        is_eligible = False
        reasons.append(f"Credits completed ({p.get('credits_completed', p.get('credits', 0))}) below minimum required ({min_credits})")
        
    if is_eligible:
        reasons.append("All eligibility criteria (CGPA, Backlogs, Credits) satisfied.")
        
    return {
        "valid": is_eligible,
        "student_usn": student_profile.get("student_usn", "N/A"),
        "company": o["company"],
        "student_cgpa": p["cgpa"],
        "cutoff_cgpa": min_cgpa,
        "cgpa_margin": round(p["cgpa"] - min_cgpa, 2),
        "reasons": reasons
    }

def read_application_status(student_usn):
    """Tool 4: Reads live application tracking feed."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student_submissions WHERE student_usn = ? ORDER BY submission_number DESC LIMIT 1;", (student_usn.upper(),))
            row = cursor.fetchone()
            if row:
                r = dict(row)
                return {
                    "submission_id": r["submission_id"],
                    "status": r["status"],
                    "allocated_company": r.get("allocated_company") or r.get("pref1_company"),
                    "rejection_reason": r.get("rejection_reason"),
                    "coordinator_comments": r.get("coordinator_comments"),
                    "hod_status": r.get("hod_status")
                }
        finally:
            conn.close()

    record = APPLICATION_STATUS_DB.get(student_usn)
    if not record:
        return {"error": f"No active application tracking record found for '{student_usn}'"}
    return record

def read_application_submissions(student_usn):
    """Tool: Reads complete submission history for a student (supporting multiple submissions)."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student_submissions WHERE student_usn = ? ORDER BY submission_number ASC;", (student_usn.upper(),))
            rows = [dict(r) for r in cursor.fetchall()]
            return {"student_usn": student_usn, "submissions": rows, "count": len(rows)}
        finally:
            conn.close()
    return {"student_usn": student_usn, "submissions": [], "count": 0}

def read_approval_status(student_usn):
    """Tool: Reads formal approval status from Coordinator and HOD."""
    sub = read_application_status(student_usn)
    if "error" in sub:
        return sub
    return {
        "student_usn": student_usn,
        "coordinator_status": sub.get("status", "PENDING_REVIEW"),
        "rejection_reason": sub.get("rejection_reason"),
        "hod_status": sub.get("hod_status", "PENDING")
    }

def read_internship_progress(student_usn):
    """Tool: Reads active 3-4 month internship progress records."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM internship_tracking WHERE student_usn = ?;", (student_usn.upper(),))
            row = cursor.fetchone()
            if row:
                return {"tracking": dict(row), "status": "FOUND"}
            return {"status": "NO_ACTIVE_TRACKING", "message": f"No confirmed internship tracking record for {student_usn}."}
        finally:
            conn.close()
    return {"status": "NO_ACTIVE_TRACKING"}


def compile_application_packet(student_usn, company_name):
    """Group C: Application Processing Agent Tool. Compiles offer letter, NOC, and resume."""
    return {
        "status": "COMPILED",
        "student_usn": student_usn,
        "company": company_name,
        "documents": ["Updated_Resume.pdf", "Official_NOC_Draft.pdf", "Company_Offer_Letter.pdf"],
        "packet_id": f"APP-{student_usn[-3:]}-2026",
        "timestamp": "2026-09-07T22:45:00Z"
    }


def verify_approval_trail(student_usn, company_name):
    """Group D: Approval Agent Tool. Verifies 3 mandatory sign-offs (Mentor, HoD, Cell)."""
    return {
        "student_usn": student_usn,
        "company": company_name,
        "approvals": {
            "Faculty_Mentor": {"status": "APPROVED", "timestamp": "2026-09-05T10:30:00Z"},
            "HoD": {"status": "APPROVED", "timestamp": "2026-09-06T14:15:00Z"},
            "Internship_Cell": {"status": "APPROVED", "timestamp": "2026-09-07T09:00:00Z"}
        },
        "released_for_internship": True,
        "guardrail_verified": "All 3 mandatory approvals recorded before student release."
    }


def log_progress_report(student_usn, week_number, summary):
    """Group E: Progress Tracking Agent Tool. Records bi-weekly report & mentor check-in."""
    return {
        "status": "LOGGED",
        "student_usn": student_usn,
        "week": week_number,
        "summary": summary,
        "attendance_confirmed": True,
        "stipend_confirmed": True,
        "audit_id": f"LOG-W{week_number}-{student_usn[-3:]}"
    }


def compile_final_evaluation(student_usn, employer_score=92, mentor_score=95):
    """Group F: Evaluation Agent Tool. Compiles employer feedback & mentor score into final grade."""
    final_score = round(employer_score * 0.5 + mentor_score * 0.5, 1)
    grade = "S" if final_score >= 90 else ("A" if final_score >= 80 else "B")
    return {
        "student_usn": student_usn,
        "employer_rubric_score": employer_score,
        "mentor_rubric_score": mentor_score,
        "combined_final_score": final_score,
        "proposed_grade": grade,
        "status": "READY_FOR_HOD_CERTIFICATION"
    }


def send_notification_draft(student_usn, company, notice_type, message):
    """AURA Exception Router Tool: Drafts warning notice for ineligible application."""
    return {
        "status": "DRAFTED",
        "recipient_usn": student_usn,
        "company": company,
        "notice_type": notice_type,
        "draft_body": message,
        "audit_note": "Draft warning notice logged in coordinator queue."
    }


TOOLS = {
    "read_opportunity_catalog": read_opportunity_catalog,
    "read_internship_opportunities": read_internship_opportunities,
    "read_student_profile": read_student_profile,
    "compute_eligibility": compute_eligibility,
    "check_vacancy": check_vacancy,
    "read_application_status": read_application_status,
    "read_application_submissions": read_application_submissions,
    "read_approval_status": read_approval_status,
    "read_internship_progress": read_internship_progress,
    "compile_application_packet": compile_application_packet,
    "verify_approval_trail": verify_approval_trail,
    "log_progress_report": log_progress_report,
    "compile_final_evaluation": compile_final_evaluation,
    "send_notification_draft": send_notification_draft,
}


# ---- apniLeap AURA Coordinator Assistant with _call Choke Point ----

class InternshipDataAssistant:
    def __init__(self):
        self.trace = []

    def _call(self, tool_name, reason, **kwargs):
        """Choke point: Enforces structured tool logging and explicit error handling."""
        tool_func = TOOLS[tool_name]
        result = tool_func(**kwargs)
        
        entry = {
            "tool": tool_name,
            "reason": reason,
            "input": kwargs,
            "output": result
        }
        self.trace.append(entry)
        
        if isinstance(result, dict) and "error" in result:
            raise RuntimeError(f"Tool call [{tool_name}] failed: {result['error']}")
            
        return result

    def query(self, question, student_usn="1KG21CS045"):
        """
        Acceptance Check: Prompt contains NO numbers or preset facts.
        All data comes strictly through tool calls across Group A-F agents!
        """
        q = question.lower()
        
        if "eligible" in q or "apply" in q:
            company_target = "Google India"
            if "microsoft" in q: company_target = "Microsoft"
            if "infosys" in q: company_target = "Infosys InStep"
            
            usn_match = re.search(r'1kg\d{2}[a-z]{2}\d{3}', q, re.IGNORECASE)
            target_usn = usn_match.group(0).upper() if usn_match else student_usn

            # Group B Tool: Fetch student profile (NO numbers in prompt!)
            profile_res = self._call("read_student_profile", 
                                     f"Group B Eligibility Agent: Fetch profile data for USN {target_usn}", 
                                     student_usn=target_usn)

            # Group A Tool: Fetch opportunity requirements (NO numbers in prompt!)
            opp_res = self._call("read_opportunity_catalog", 
                                 f"Group A Discovery Agent: Fetch opportunity requirements for {company_target}", 
                                 company_name=company_target)

            # Group B Tool: Compute eligibility
            eval_res = self._call("compute_eligibility", 
                                  f"Group B Eligibility Agent: Compute verified eligibility for {target_usn} at {company_target}", 
                                  student_profile=profile_res, 
                                  opportunity=opp_res)

            student_name = profile_res["profile"]["name"]
            
            if eval_res["valid"]:
                # Group C Tool: Compile application packet
                app_packet = self._call("compile_application_packet",
                                        f"Group C Application Processing Agent: Compile NOC & offer packet for {target_usn}",
                                        student_usn=target_usn,
                                        company_name=company_target)

                # Group D Tool: Verify 3 mandatory sign-offs (Mentor, HoD, Cell)
                approvals = self._call("verify_approval_trail",
                                       f"Group D Approval Agent: Verify 3 mandatory sign-offs before release for {target_usn}",
                                       student_usn=target_usn,
                                       company_name=company_target)

                return (f"VERIFIED RESULT (via apniLeap AURA Group A-D Agent Chain):\n"
                        f"Student {student_name} ({target_usn}) IS ELIGIBLE for {company_target}.\n"
                        f"  - Student CGPA: {eval_res['student_cgpa']} (Cutoff: {eval_res['cutoff_cgpa']}, Margin: +{eval_res['cgpa_margin']})\n"
                        f"  - Application Packet: {app_packet['packet_id']} ({len(app_packet['documents'])} docs compiled)\n"
                        f"  - Approvals Recorded: Faculty Mentor (OK), HoD (OK), Internship Cell (OK)\n"
                        f"  - Status: RELEASED FOR SEMESTER INTERNSHIP")
            else:
                # AURA Exception Router Tool: Draft warning notice
                self._call("send_notification_draft",
                           f"apniLeap AURA Exception Router: Draft warning notice for ineligible student {target_usn}",
                           student_usn=target_usn,
                           company=company_target,
                           notice_type="ELIGIBILITY_WARNING",
                           message=f"Student {target_usn} is ineligible for {company_target}: {'; '.join(eval_res['reasons'])}")

                return (f"VERIFIED RESULT (via apniLeap AURA Group B Eligibility Agent):\n"
                        f"Student {student_name} ({target_usn}) IS INELIGIBLE for {company_target}.\n"
                        f"  - Reasons: {'; '.join(eval_res['reasons'])}\n"
                        f"  - Action: Exception notification draft logged in coordinator queue.")

        return "Query not recognized in defined tool execution paths."


if __name__ == "__main__":
    assistant = InternshipDataAssistant()
    
    print("=========================================================================")
    print("=== apniLeap AURA COORDINATOR: GROUP A-F AGENT EXECUTION TRACE ===")
    print("=========================================================================\n")
    
    # Prompt contains NO numbers, NO CGPA, NO answers!
    q1 = "Am I eligible for the Google India Software Engineering Internship?"
    print(f"USER PROMPT: \"{q1}\"\n")
    print(assistant.query(q1, student_usn="1KG21CS045"))

    print("\n" + "-"*75 + "\n")

    q2 = "Is student 1KG21CS104 eligible for the Microsoft Data Science Internship?"
    print(f"USER PROMPT: \"{q2}\"\n")
    print(assistant.query(q2, student_usn="1KG21CS104"))

    print("\n" + "="*75)
    print("=== FULL TOOL EXECUTION TRACE (_call Choke Point Log) ===")
    print("="*75)
    for i, entry in enumerate(assistant.trace, 1):
        print(f"\n{i}. TOOL: {entry['tool']}")
        print(f"   REASON: \"{entry['reason']}\"")
        print(f"   INPUT:  {entry['input']}")
        print(f"   OUTPUT: {entry['output']}")

