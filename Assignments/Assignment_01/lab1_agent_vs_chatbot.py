"""
Lab 1: Agent vs Chatbot -- Internship Application & Tracking Planner Agent
Chapter 10: Internship Application & Tracking Portal

Implements the complete Goal -> Plan -> Act -> Observe -> Revise loop for the
8th-semester internship discovery, eligibility, approvals, and tracking process.

No external API needed: uses a structured goal predicate and rule-based planner loop
demonstrating Concept 1 (Goal-driven Agent Loop) and Phase A Foundations.
"""

import json

# ---- Simulated User Answers & Feedback ----
SIMULATED_ANSWERS = {
    "student_name": "Rahul Kumar",
    "student_usn": "1KG21CS045",
    "branch": "Computer Science & Engineering",
    "cgpa": 8.8,
    "active_backlogs": 0,
    "credits_completed": 112,
    "domain_interest": "Machine Learning / Data Science",
    "preferred_location": "Bengaluru (Hybrid)",
}

SIMULATED_FEEDBACK = "Add a specific milestone for mentor sign-off before mid-semester evaluation on Week 8."


class InternshipPlannerAgent:
    def __init__(self, existing_policy=None):
        # Goal modeled as data -- a checkable predicate, not prose.
        self.goal = {
            "student_name": None,
            "student_usn": None,
            "branch": None,
            "cgpa": None,
            "active_backlogs": None,
            "credits_completed": None,
            "domain_interest": None,
            "preferred_location": None,
            "plan_generated": False,
        }
        self.existing_policy = existing_policy or {
            "min_cgpa": 7.0,
            "max_backlogs": 0,
            "min_credits": 100,
            "mandatory_approvals": ["Faculty Mentor", "HoD", "Internship Cell"]
        }
        self.plan = None
        self.log = []

    # ---- Goal check predicate ---------------------------------------
    def satisfied(self):
        return self.goal["plan_generated"] is True

    # ---- Planner: decide the next step ------------------------------
    def next_step(self):
        for field in ("student_name", "student_usn", "branch", "cgpa", "active_backlogs", "credits_completed", "domain_interest", "preferred_location"):
            if self.goal[field] is None:
                return ("ask", field)
        return ("generate_plan", None)

    # ---- Tool: read existing policy / prerequisites ------------------
    def read_internship_policy(self):
        result = self.existing_policy
        if "error" in result:
            raise RuntimeError(f"tool error: {result['error']}")
        return result

    # ---- Core Agent Loop ---------------------------------------------
    def run(self, simulated_user_inputs):
        print("=== LAB 1: STARTING AGENT LOOP ===")
        iteration = 0
        while not self.satisfied():
            iteration += 1
            step, arg = self.next_step()
            
            if step == "ask":
                # Agent asks clarifying questions until inputs are complete
                question_map = {
                    "student_name": "What is your Full Name?",
                    "student_usn": "What is your Student USN or ID?",
                    "branch": "What is your Branch / Department?",
                    "cgpa": "What is your current cumulative CGPA?",
                    "active_backlogs": "How many active backlogs do you have?",
                    "credits_completed": "How many completed semester credits do you have?",
                    "domain_interest": "What domain/tech stack are you seeking an internship in?",
                    "preferred_location": "What is your preferred work location (e.g. Bengaluru, Remote)?",
                }
                user_val = simulated_user_inputs.get(arg)
                self.goal[arg] = user_val
                
                log_entry = {
                    "iteration": iteration,
                    "plan_state": "Clarifying Inputs",
                    "action": f"Asked user: '{question_map[arg]}'",
                    "observation": f"Received input for {arg} = '{user_val}'",
                    "reason": f"Field '{arg}' was missing in goal predicate.",
                }
                self.log.append(log_entry)
                print(f"[Iter {iteration}] ASK: {question_map[arg]} -> Answered: {user_val}")

            elif step == "generate_plan":
                # Agent reads policy tool before generating plan
                policy = self.read_internship_policy()
                
                self.plan = {
                    "title": f"8th Semester Tracked Internship Plan for {self.goal['student_name']} ({self.goal['student_usn']})",
                    "branch": self.goal["branch"],
                    "student_academic_summary": {
                        "cgpa": self.goal["cgpa"],
                        "active_backlogs": self.goal["active_backlogs"],
                        "credits_completed": self.goal["credits_completed"]
                    },
                    "domain": self.goal["domain_interest"],
                    "location": self.goal["preferred_location"],
                    "policy_constraints": policy,
                    "phases": [
                        {
                            "phase": "Phase 1: Opportunity Match & Eligibility Verification",
                            "weeks": "Week 1",
                            "actions": [
                                f"Filter listings in '{self.goal['domain_interest']}' in '{self.goal['preferred_location']}'",
                                f"Verify student eligibility against Min CGPA ({policy['min_cgpa']} <= Actual {self.goal['cgpa']}), Backlogs ({policy['max_backlogs']} == Actual {self.goal['active_backlogs']}), Credits ({policy['min_credits']} <= Actual {self.goal['credits_completed']})"
                            ]
                        },
                        {
                            "phase": "Phase 2: Application Compilation & Approvals Routing",
                            "weeks": "Week 2",
                            "actions": [
                                "Compile resume, transcript, and company offer/JD packet",
                                f"Route digital approval queue to: {', '.join(policy['mandatory_approvals'])}"
                            ]
                        },
                        {
                            "phase": "Phase 3: Semester Progress Tracking",
                            "weeks": "Weeks 3-14",
                            "actions": [
                                "Bi-weekly student work report submission & attendance verification",
                                "Monthly mentor check-in & progress logging"
                            ]
                        },
                        {
                            "phase": "Phase 4: Final Evaluation & Grading",
                            "weeks": "Weeks 15-16",
                            "actions": [
                                "Employer evaluation summary & project report submission",
                                "Final rubric-based grade proposal for Faculty Coordinator sign-off"
                            ]
                        }
                    ]
                }
                self.goal["plan_generated"] = True
                
                log_entry = {
                    "iteration": iteration,
                    "plan_state": "Plan Generated",
                    "action": "Fetched policy via tool and compiled 4-phase internship outline.",
                    "observation": f"Created plan with {len(self.plan['phases'])} phases for {self.goal['student_name']}.",
                    "reason": "All required goal fields are satisfied.",
                }
                self.log.append(log_entry)
                print(f"[Iter {iteration}] PLAN GENERATED successfully.")

        return self.plan

    # ---- Revise on Feedback ------------------------------------------
    def revise(self, feedback):
        print(f"\n=== REVISING PLAN BASED ON USER FEEDBACK ===")
        print(f"Feedback received: '{feedback}'")
        
        # Mutates existing plan object directly without re-running loop from scratch
        if "Week 8" in feedback or "mid-semester" in feedback.lower():
            self.plan["phases"][2]["actions"].append(
                "Week 8 Milestone: Mandatory Faculty Mentor mid-semester review & progress sign-off"
            )
            self.plan["phases"][2]["actions"].sort()
        
        rev_entry = {
            "iteration": len(self.log) + 1,
            "plan_state": "Plan Revised",
            "action": "Updated Phase 3 actions with Week 8 mid-semester evaluation milestone.",
            "observation": "Plan updated directly without destroying context.",
            "reason": f"User requested specific feedback: {feedback}",
        }
        self.log.append(rev_entry)
        print("Plan revised successfully!")
        return self.plan


if __name__ == "__main__":
    agent = InternshipPlannerAgent()
    
    # 1. Run the clarify -> plan loop
    plan = agent.run(SIMULATED_ANSWERS)
    
    print("\n--- Initial Proposed Plan ---")
    print(json.dumps(plan, indent=2))
    
    # 2. Revise based on feedback
    revised_plan = agent.revise(SIMULATED_FEEDBACK)
    
    print("\n--- Final Revised Plan ---")
    print(json.dumps(revised_plan, indent=2))
    
    print("\n=== Agent Trace Log ===")
    for entry in agent.log:
        print(f"Iter {entry['iteration']} | State: {entry['plan_state']} | Action: {entry['action']} | Reason: {entry['reason']}")

