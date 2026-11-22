/**
 * INTERNTRACK — AI Resume & CV Builder Controller
 * Features:
 * - Live type-to-search database lookup from SQLite (/api/students/all)
 * - 3-Step Guided Wizard (Academic Identity -> Skills & Projects -> Review & Match)
 * - Interactive Clickable Skill Chips (100+ Skill Taxonomy)
 * - Real-Time ATS White-Paper Preview Sheet matching university standards
 * - 1-Click Bridge to Resume / Skills Auto-Matcher
 * - Export to Print/PDF and Plain Text Copy
 */

let rbSelectedSkills = new Set();
let rbSearchDebounceTimer = null;
let rbInitialized = false;

document.addEventListener("DOMContentLoaded", () => {
  const inputsToWatch = [
    "rbFullName", "rbHeadline", "rbUsn", "rbBranch", "rbSemester", "rbCollege", "rbCgpa",
    "rbBacklogs", "rbCredits", "rbEmail", "rbPhone", "rbLinkedin", "rbGithub",
    "rbSummary", "rbProj1Title", "rbProj1Tech", "rbProj1Desc",
    "rbProj2Title", "rbProj2Tech", "rbProj2Desc", "rbProj3Title", "rbProj3Tech", "rbProj3Desc",
    "rbExpCompany", "rbExpRole", "rbExpDuration", "rbExpDesc", "rbAchievements"
  ];

  inputsToWatch.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("input", updateResumeBuilderPreview);
    }
  });
});

async function initResumeBuilder() {
  if (rbInitialized && document.getElementById("rbFullName") && document.getElementById("rbFullName").value) {
    return;
  }
  rbInitialized = true;
  // Default to Ananya Sharma (1KG21CS008) to match the standard verified demo preview
  await fetchStudentByUSN("1KG21CS008");
  rbGoToStep(3);
}

// ---------------------------------------------------------------------
// 1. Live Type-to-Search Database Lookup
// ---------------------------------------------------------------------

function handleStudentSearchInput(event) {
  const query = event.target.value.trim();
  const dropdown = document.getElementById("rbSearchResultsDropdown");
  if (!dropdown) return;

  if (rbSearchDebounceTimer) clearTimeout(rbSearchDebounceTimer);

  if (query.length < 2) {
    dropdown.style.display = "none";
    dropdown.innerHTML = "";
    return;
  }

  rbSearchDebounceTimer = setTimeout(async () => {
    try {
      const res = await fetch(`/api/students/all?search=${encodeURIComponent(query)}`);
      if (!res.ok) throw new Error("Search failed");
      const students = await res.json();

      if (!students || students.length === 0) {
        dropdown.innerHTML = `<div class="rb-search-item" style="color:var(--text-muted); cursor:default;">No university records found matching "${query}"</div>`;
        dropdown.style.display = "block";
        return;
      }

      dropdown.innerHTML = students.slice(0, 8).map(s => `
        <div class="rb-search-item" onclick="selectStudentSearchResult('${encodeURIComponent(JSON.stringify(s))}')">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="color:#f8fafc;">${s.name}</strong>
            <span class="badge" style="font-size:0.7rem; background:rgba(56,189,248,0.15); color:#38bdf8;">${s.usn}</span>
          </div>
          <div style="font-size:0.75rem; color:#94a3b8; display:flex; gap:0.75rem; margin-top:2px;">
            <span><i class="fa-solid fa-graduation-cap"></i> ${s.branch} (Sem ${s.semester})</span>
            <span><i class="fa-solid fa-star" style="color:#f59e0b;"></i> CGPA: ${s.cgpa}</span>
            <span><i class="fa-solid fa-briefcase"></i> ${s.placement_status === 'PLACED_COMPANY' ? (s.placed_company || 'Placed') : 'Eligible'}</span>
          </div>
        </div>
      `).join("");
      dropdown.style.display = "block";
    } catch (err) {
      console.error("Student search error:", err);
      dropdown.style.display = "none";
    }
  }, 250);
}

function handleStudentSearchKeydown(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    executeStudentFetchFromSearch();
  }
}

function selectStudentSearchResult(encodedJson) {
  try {
    const student = JSON.parse(decodeURIComponent(encodedJson));
    populateStudentData(student);
    const dropdown = document.getElementById("rbSearchResultsDropdown");
    if (dropdown) dropdown.style.display = "none";
    const input = document.getElementById("rbSearchStudentInput");
    if (input) input.value = `${student.name} (${student.usn})`;
    rbGoToStep(3);
  } catch (err) {
    console.error("Error selecting student:", err);
  }
}

async function executeStudentFetchFromSearch() {
  const input = document.getElementById("rbSearchStudentInput");
  if (!input) return;
  const val = input.value.trim();
  if (!val) return;

  try {
    const res = await fetch(`/api/students/all?search=${encodeURIComponent(val)}`);
    if (!res.ok) throw new Error("Search failed");
    const students = await res.json();
    if (students && students.length > 0) {
      populateStudentData(students[0]);
      input.value = `${students[0].name} (${students[0].usn})`;
      const dropdown = document.getElementById("rbSearchResultsDropdown");
      if (dropdown) dropdown.style.display = "none";
      rbGoToStep(3);
    } else {
      alert(`No student record found matching "${val}".`);
    }
  } catch (err) {
    console.error("Fetch error:", err);
    alert("Could not connect to university records database.");
  }
}

async function fetchStudentByUSN(usn) {
  try {
    const res = await fetch(`/api/students/all?search=${encodeURIComponent(usn)}`);
    if (res.ok) {
      const list = await res.json();
      if (list && list.length > 0) {
        populateStudentData(list[0]);
        const input = document.getElementById("rbSearchStudentInput");
        if (input) input.value = `${list[0].name} (${list[0].usn})`;
      }
    }
  } catch (err) {
    console.warn("Could not auto-fetch USN data:", err);
  }
}

function populateStudentData(s) {
  setVal("rbFullName", s.name);
  setVal("rbHeadline", "Software Engineering & AI Intern");
  setVal("rbUsn", s.usn);
  setVal("rbBranch", s.branch ? `${s.branch} (Computer Science & Engineering)` : "Computer Science & Engineering");
  setVal("rbSemester", s.semester || 8);
  setVal("rbCollege", "KLE Technological University, Hubballi");
  setVal("rbCgpa", s.cgpa || "9.1");
  setVal("rbBacklogs", s.backlogs !== undefined ? s.backlogs : "0");
  setVal("rbCredits", s.credits || "118");
  setVal("rbEmail", s.email || `${s.usn.toLowerCase()}@kletech.ac.in`);
  setVal("rbPhone", s.phone || "+91 9876543211");

  if (!getVal("rbLinkedin")) setVal("rbLinkedin", `https://linkedin.com/in/${s.name.toLowerCase().replace(/[^a-z0-9]/g, '-')}`);
  if (!getVal("rbGithub")) setVal("rbGithub", `https://github.com/${s.name.split(' ')[0].toLowerCase()}${s.usn.slice(-3)}`);

  setVal("rbSummary", "Final-year Computer Science & Engineering undergraduate at KLE Tech with solid foundations in algorithms, software systems, and data-driven problem solving.");

  // Populate skills
  rbSelectedSkills.clear();
  document.querySelectorAll(".rb-skill-chip").forEach(c => c.classList.remove("selected"));

  let skillsArr = [];
  if (Array.isArray(s.skills)) {
    skillsArr = s.skills;
  } else if (typeof s.skills === "string") {
    try {
      skillsArr = JSON.parse(s.skills);
    } catch {
      skillsArr = s.skills.split(",").map(x => x.trim());
    }
  }

  if (skillsArr.length === 0) {
    skillsArr = ["Java", "Spring Boot", "AWS", "Microservices", "Docker", "Python", "SQL"];
  }

  skillsArr.forEach(sk => {
    rbSelectedSkills.add(sk.trim());
    const chip = document.querySelector(`.rb-skill-chip[data-skill="${sk.trim().toLowerCase()}"]`);
    if (chip) chip.classList.add("selected");
  });

  // Default projects
  setVal("rbProj1Title", "InternTrack — Autonomous University Regulatory Assistant (AURA)");
  setVal("rbProj1Tech", "Python, LangGraph, SQLite3, FastAPI");
  setVal("rbProj1Desc", "• Engineered a 14-lab autonomous agent platform to govern university internship discovery, approvals, and 12-credit evaluations.\n• Built multi-agent swarms with fan-out/fan-in parallel search and human-in-the-loop coordinator approval gates.\n• Achieved 100% pass rate across 81 automated tests with immutable SHA-256 cryptographic audit logs.");

  setVal("rbProj2Title", "Self-Correcting RAG System for Hallucination Detection");
  setVal("rbProj2Tech", "Python, LLaMA, FAISS, BM25");
  setVal("rbProj2Desc", "• Implemented a hybrid dense/sparse retrieval pipeline with cross-encoder re-ranking and NLI verification.\n• Mitigated factual hallucinations, achieving 64% accuracy and 0.6975 F1 score on the RAGTruth benchmark.");

  setVal("rbAchievements", "• IEEE Publication: Zero-Shot Traffic Classification for Unseen Applications Using CNN and Word2Vec (IEEE I3CTCON 2026).\n• Smart India Hackathon: Shortlisted for AI-based crop disease diagnosis platform.\n• AWS Certified: AWS Cloud Practitioner Essentials (Amazon Web Services).");

  updateResumeBuilderPreview();
}

function setVal(id, v) {
  const el = document.getElementById(id);
  if (el && v !== undefined && v !== null) el.value = v;
}

function getVal(id) {
  const el = document.getElementById(id);
  return el ? el.value.trim() : "";
}

// ---------------------------------------------------------------------
// 2. Wizard Navigation (Steps 1, 2, 3)
// ---------------------------------------------------------------------

function rbGoToStep(step) {
  for (let i = 1; i <= 3; i++) {
    const card = document.getElementById(`rbStepCard${i}`);
    const btn = document.getElementById(`rbStepBtn${i}`);
    if (card) card.style.display = i === step ? "block" : "none";
    if (btn) {
      if (i === step) btn.classList.add("active");
      else btn.classList.remove("active");
    }
  }
}

// ---------------------------------------------------------------------
// 3. Interactive Skill Chips & Custom Tags
// ---------------------------------------------------------------------

function toggleSkillTag(skillName, chipEl) {
  if (rbSelectedSkills.has(skillName)) {
    rbSelectedSkills.delete(skillName);
    if (chipEl) chipEl.classList.remove("selected");
  } else {
    rbSelectedSkills.add(skillName);
    if (chipEl) chipEl.classList.add("selected");
  }
  updateResumeBuilderPreview();
}

function addCustomSkillTag() {
  const input = document.getElementById("rbCustomSkillInput");
  if (!input) return;
  const val = input.value.trim();
  if (!val) return;

  const parts = val.split(",").map(p => p.trim()).filter(Boolean);
  parts.forEach(skill => {
    rbSelectedSkills.add(skill);
    const container = document.getElementById("rbCustomSkillsContainer");
    if (container) {
      const chip = document.createElement("span");
      chip.className = "rb-skill-chip selected";
      chip.innerHTML = `${skill} <i class="fa-solid fa-xmark" style="font-size:0.7rem; margin-left:4px;" onclick="removeCustomSkillTag('${skill}', this.parentElement)"></i>`;
      container.appendChild(chip);
    }
  });

  input.value = "";
  updateResumeBuilderPreview();
}

function removeCustomSkillTag(skill, el) {
  rbSelectedSkills.delete(skill);
  if (el) el.remove();
  updateResumeBuilderPreview();
}

// ---------------------------------------------------------------------
// 4. Live ATS-Standard Paper Preview Sheet Rendering
// ---------------------------------------------------------------------

function updateResumeBuilderPreview() {
  const preview = document.getElementById("resumePreviewSheet");
  if (!preview) return;

  const name = getVal("rbFullName") || "ANANYA SHARMA";
  const headline = getVal("rbHeadline") || "Software Engineering & AI Intern";
  const usn = getVal("rbUsn") || "1KG21CS008";
  const branch = "B.E. Computer Science & Engineering";
  const college = "KLE Technological University, Hubballi";
  const cgpa = getVal("rbCgpa") || "9.1";
  const email = getVal("rbEmail") || "ananya.s@kletech.ac.in";
  const phone = getVal("rbPhone") || "+91 9876543211";
  const summary = getVal("rbSummary") || "Final-year Computer Science & Engineering undergraduate at KLE Tech with solid foundations in algorithms, software systems, and data-driven problem solving.";

  const proj1Title = getVal("rbProj1Title");
  const proj1Tech = getVal("rbProj1Tech");
  const proj1Desc = getVal("rbProj1Desc");

  const proj2Title = getVal("rbProj2Title");
  const proj2Tech = getVal("rbProj2Tech");
  const proj2Desc = getVal("rbProj2Desc");

  const achievements = getVal("rbAchievements");
  const skillsList = Array.from(rbSelectedSkills);

  // Group skills into clean categories if possible
  const langSkills = skillsList.filter(s => ["python", "java", "c++", "c", "javascript", "typescript", "sql", "html5", "css3"].includes(s.toLowerCase()));
  const fwSkills = skillsList.filter(s => ["spring boot", "fastapi", "react", "react.js", "node.js", "pytorch", "tensorflow", "scikit-learn", "langgraph", "faiss", "llama"].includes(s.toLowerCase()));
  const toolSkills = skillsList.filter(s => !langSkills.includes(s) && !fwSkills.includes(s));

  // Build Exact ATS White Sheet HTML matching the reference screenshot
  let html = `
    <div style="font-family:'Segoe UI', Calibri, -apple-system, BlinkMacSystemFont, Arial, sans-serif; line-height:1.4; color:#0f172a;">
      
      <!-- ATS Header: Left-Aligned -->
      <div style="border-bottom:2px solid #0f172a; padding-bottom:6px; margin-bottom:10px;">
        <h1 style="margin:0; font-size:1.55rem; font-weight:800; letter-spacing:0.5px; text-transform:uppercase; color:#0f172a; line-height:1.2;">
          ${name}
        </h1>
        <div style="font-size:0.92rem; font-weight:700; color:#0284c7; margin-top:2px; margin-bottom:3px;">
          ${headline}
        </div>
        <div style="font-size:0.78rem; color:#475569; font-weight:500;">
          <strong>USN:</strong> ${usn} &nbsp;|&nbsp; 
          <a href="mailto:${email}" style="color:#0284c7; text-decoration:none;">${email}</a> &nbsp;|&nbsp; 
          ${phone}
        </div>
      </div>

      <!-- Professional Summary -->
      <div style="margin-bottom:10px;">
        <div style="font-weight:800; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.5px; color:#0f172a; border-bottom:1px solid #0f172a; padding-bottom:1px; margin-bottom:4px;">
          PROFESSIONAL SUMMARY
        </div>
        <div style="font-size:0.8rem; color:#1e293b; text-align:justify; line-height:1.45;">
          ${summary}
        </div>
      </div>

      <!-- Academic Background -->
      <div style="margin-bottom:10px;">
        <div style="font-weight:800; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.5px; color:#0f172a; border-bottom:1px solid #0f172a; padding-bottom:1px; margin-bottom:4px;">
          ACADEMIC BACKGROUND
        </div>
        <div style="display:flex; justify-content:space-between; align-items:baseline;">
          <strong style="font-size:0.82rem; color:#0f172a;">${college}</strong>
          <span style="font-size:0.76rem; color:#64748b;">8th Semester</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:baseline; font-size:0.8rem; color:#334155;">
          <span>${branch}</span>
          <span style="font-weight:700; color:#059669;">Verified CGPA: ${cgpa} / 10</span>
        </div>
      </div>

      <!-- Technical Competencies -->
      <div style="margin-bottom:10px;">
        <div style="font-weight:800; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.5px; color:#0f172a; border-bottom:1px solid #0f172a; padding-bottom:1px; margin-bottom:4px;">
          TECHNICAL COMPETENCIES
        </div>
        <div style="font-size:0.79rem; color:#1e293b; line-height:1.5;">
          ${langSkills.length > 0 ? `<div><strong>Languages:</strong> ${langSkills.join(", ")}</div>` : ''}
          ${fwSkills.length > 0 ? `<div><strong>Frameworks & AI:</strong> ${fwSkills.join(", ")}</div>` : ''}
          ${toolSkills.length > 0 ? `<div><strong>Cloud & Tools:</strong> ${toolSkills.join(", ")}</div>` : ''}
          ${(langSkills.length === 0 && fwSkills.length === 0 && toolSkills.length === 0) ? `<div>${skillsList.join(" • ")}</div>` : ''}
        </div>
      </div>

      <!-- Featured Projects -->
      ${(proj1Title || proj2Title) ? `
      <div style="margin-bottom:10px;">
        <div style="font-weight:800; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.5px; color:#0f172a; border-bottom:1px solid #0f172a; padding-bottom:1px; margin-bottom:5px;">
          FEATURED PROJECTS
        </div>

        ${proj1Title ? `
        <div style="margin-bottom:6px;">
          <div style="display:flex; justify-content:space-between; font-size:0.81rem;">
            <strong style="color:#0f172a;">${proj1Title}</strong>
            ${proj1Tech ? `<span style="font-size:0.75rem; font-style:italic; color:#475569;">${proj1Tech}</span>` : ''}
          </div>
          ${proj1Desc ? `
          <ul style="margin:2px 0 0 16px; padding:0; font-size:0.78rem; color:#334155; line-height:1.4;">
            ${proj1Desc.split('\n').filter(Boolean).map(line => `<li>${line.replace(/^[•\-\*]\s*/, '')}</li>`).join('')}
          </ul>` : ''}
        </div>
        ` : ''}

        ${proj2Title ? `
        <div style="margin-bottom:6px;">
          <div style="display:flex; justify-content:space-between; font-size:0.81rem;">
            <strong style="color:#0f172a;">${proj2Title}</strong>
            ${proj2Tech ? `<span style="font-size:0.75rem; font-style:italic; color:#475569;">${proj2Tech}</span>` : ''}
          </div>
          ${proj2Desc ? `
          <ul style="margin:2px 0 0 16px; padding:0; font-size:0.78rem; color:#334155; line-height:1.4;">
            ${proj2Desc.split('\n').filter(Boolean).map(line => `<li>${line.replace(/^[•\-\*]\s*/, '')}</li>`).join('')}
          </ul>` : ''}
        </div>
        ` : ''}

      </div>
      ` : ''}

      <!-- Achievements -->
      ${achievements ? `
      <div style="margin-bottom:6px;">
        <div style="font-weight:800; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.5px; color:#0f172a; border-bottom:1px solid #0f172a; padding-bottom:1px; margin-bottom:4px;">
          KEY ACHIEVEMENTS & CERTIFICATIONS
        </div>
        <ul style="margin:2px 0 0 16px; padding:0; font-size:0.78rem; color:#334155; line-height:1.4;">
          ${achievements.split('\n').filter(Boolean).map(line => `<li>${line.replace(/^[•\-\*]\s*/, '')}</li>`).join('')}
        </ul>
      </div>
      ` : ''}

    </div>
  `;

  preview.innerHTML = html;
}

// ---------------------------------------------------------------------
// 5. Reset, Copy Plain Text & Print PDF
// ---------------------------------------------------------------------

function resetResumeBuilder() {
  if (confirm("Reset the resume builder and clear all fields?")) {
    document.querySelectorAll("#view-resume-builder input, #view-resume-builder textarea").forEach(el => el.value = "");
    rbSelectedSkills.clear();
    document.querySelectorAll(".rb-skill-chip").forEach(c => c.classList.remove("selected"));
    const container = document.getElementById("rbCustomSkillsContainer");
    if (container) container.innerHTML = "";
    updateResumeBuilderPreview();
    rbGoToStep(1);
  }
}

function generateResumePlainText() {
  const name = getVal("rbFullName") || "STUDENT NAME";
  const usn = getVal("rbUsn") || "";
  const branch = getVal("rbBranch") || "CSE";
  const college = getVal("rbCollege") || "KLE Technological University";
  const cgpa = getVal("rbCgpa") || "9.1";
  const email = getVal("rbEmail") || "";
  const phone = getVal("rbPhone") || "";
  const linkedin = getVal("rbLinkedin") || "";
  const github = getVal("rbGithub") || "";
  const summary = getVal("rbSummary") || "";
  const skillsList = Array.from(rbSelectedSkills);

  const lines = [
    name.toUpperCase(),
    `${email} | ${phone} | ${usn}`,
    `${linkedin} | ${github}`,
    "----------------------------------------------------------------",
    "PROFESSIONAL SUMMARY:",
    summary,
    "",
    "ACADEMIC BACKGROUND:",
    `${college} (2023 - 2027)`,
    `Bachelor of Engineering in ${branch} | Verified CGPA: ${cgpa}/10.0`,
    "",
    "TECHNICAL COMPETENCIES:",
    skillsList.join(", "),
    "",
    "FEATURED PROJECTS:",
    getVal("rbProj1Title") ? `${getVal("rbProj1Title")} (${getVal("rbProj1Tech")})\n${getVal("rbProj1Desc")}\n` : "",
    getVal("rbProj2Title") ? `${getVal("rbProj2Title")} (${getVal("rbProj2Tech")})\n${getVal("rbProj2Desc")}\n` : "",
    getVal("rbAchievements") ? `KEY ACHIEVEMENTS & CERTIFICATIONS:\n${getVal("rbAchievements")}` : ""
  ];

  return lines.filter(l => l !== undefined && l !== null).join("\n");
}

function copyResumePlainText() {
  const text = generateResumePlainText();
  navigator.clipboard.writeText(text).then(() => {
    alert("✅ ATS-Formatted Resume copied to clipboard as clean plain text!");
  }).catch(err => {
    console.error("Copy failed:", err);
    alert("Could not copy automatically. You can copy from the preview.");
  });
}

function printResumeSheet() {
  const content = document.getElementById("resumePreviewSheet");
  if (!content) return;

  const printWindow = window.open("", "_blank");
  printWindow.document.write(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>${getVal("rbFullName") || "Resume"} - InternTrack CV</title>
        <style>
          @page { margin: 12mm; size: A4; }
          body { font-family: 'Segoe UI', Calibri, Arial, sans-serif; margin: 0; padding: 0; color: #0f172a; background: #fff; }
          a { color: #0f172a; text-decoration: none; }
          ul { margin-top: 3px; }
          li { margin-bottom: 2px; }
        </style>
      </head>
      <body>
        ${content.innerHTML}
        <script>
          window.onload = function() { window.print(); window.close(); };
        </script>
      </body>
    </html>
  `);
  printWindow.document.close();
}

function transferResumeToSkillsMatcher() {
  const text = generateResumePlainText();
  if (!text || text.length < 30) {
    alert("Please enter your academic details and skills first!");
    return;
  }

  if (typeof switchView === "function") {
    switchView("resume-matcher");
  }

  const pasteInput = document.getElementById("resumeTextInput") || document.getElementById("resumePasteInput");
  if (pasteInput) {
    pasteInput.value = text;
  }

  const usn = getVal("rbUsn");
  if (usn) {
    if (typeof currentUSN !== "undefined") currentUSN = usn;
    const formUsnInput = document.getElementById("formStudentUSNInput");
    if (formUsnInput) formUsnInput.value = usn;
  }

  setTimeout(() => {
    if (typeof runResumeMatch === "function") {
      runResumeMatch();
    } else if (typeof window.runResumeMatch === "function") {
      window.runResumeMatch();
    }
  }, 250);
}
window.transferResumeToSkillsMatcher = transferResumeToSkillsMatcher;
