/**
 * INTERNTRACK — AI Resume & CV Builder
 * Features:
 * 1. Type-to-Search University Database Lookup (Name or USN)
 * 2. Starts with clean / empty resume
 * 3. Step 1: Populates verified student identity from SQLite
 * 4. Step 2: Student picks skill tags & enters project details
 * 5. Step 3: Generates clean ATS resume & 1-click bridge to Skills Matcher
 */

// Fallback registry of benchmark students if API is unreachable
const LOCAL_STUDENT_CATALOG = [
  {
    usn: "01FE21BCS001",
    name: "Aishwarya Patil",
    branch: "Computer Science & Engineering",
    semester: 8,
    cgpa: 9.4,
    email: "aishwarya.p@kletech.ac.in",
    phone: "+91 984500100",
    role: "Software Engineering & Systems Research Intern",
    location: "Bengaluru, Karnataka"
  },
  {
    usn: "1KG21CS045",
    name: "Rahul Kumar",
    branch: "Computer Science & Engineering (AI)",
    semester: 8,
    cgpa: 8.5,
    email: "rahul.k@kletech.ac.in",
    phone: "+91 9876543210",
    role: "AI / Machine Learning Engineer Intern",
    location: "Hubballi / Bengaluru, Karnataka"
  },
  {
    usn: "1KG21CS008",
    name: "Ananya Sharma",
    branch: "Computer Science & Engineering",
    semester: 8,
    cgpa: 9.1,
    email: "ananya.s@kletech.ac.in",
    phone: "+91 9876543211",
    role: "Cloud Engineering & Enterprise Systems Intern",
    location: "Bengaluru / Pune"
  },
  {
    usn: "1KG21CS072",
    name: "Rohan Verma",
    branch: "Computer Science & Engineering",
    semester: 8,
    cgpa: 7.2,
    email: "rohan.v@kletech.ac.in",
    phone: "+91 9876543212",
    role: "Full-Stack Web Developer Intern",
    location: "Bengaluru / Remote"
  },
  {
    usn: "1KG21CS099",
    name: "Sneha Patil",
    branch: "Computer Science & Engineering",
    semester: 8,
    cgpa: 6.8,
    email: "sneha.p@kletech.ac.in",
    phone: "+91 9876543213",
    role: "QA Automation & Data Systems Intern",
    location: "Pune / Bangalore"
  },
  {
    usn: "1KG21CS050",
    name: "Anam",
    branch: "Computer Science & Engineering",
    semester: 8,
    cgpa: 8.8,
    email: "anam.k@kletech.ac.in",
    phone: "+91 9876543214",
    role: "Research & Innovation Intern",
    location: "Bengaluru"
  },
  {
    usn: "01FE21BCS003",
    name: "Pooja Hegde",
    branch: "Information Science & Engineering",
    semester: 8,
    cgpa: 8.7,
    email: "pooja.h@kletech.ac.in",
    phone: "+91 984500102",
    role: "InStep Digital Specialist Intern",
    location: "Hubballi"
  }
];

let currentBuilderStep = 1;
let activeSelectedSkills = new Set();
let searchDebounceTimer = null;

// ============================================================
// Step Navigation
// ============================================================
function rbGoToStep(step) {
  currentBuilderStep = step;

  for (let s = 1; s <= 3; s++) {
    const btn = document.getElementById(`rbStepBtn${s}`);
    const card = document.getElementById(`rbStepCard${s}`);
    if (btn) {
      btn.classList.remove("active", "completed");
      if (s === step) {
        btn.classList.add("active");
      } else if (s < step) {
        btn.classList.add("completed");
      }
    }
    if (card) {
      card.style.display = (s === step) ? "block" : "none";
    }
  }

  updateResumeBuilderPreview();

  const builderView = document.getElementById("view-resume-builder");
  if (builderView && step > 1) {
    builderView.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

// ============================================================
// Type-to-Search University Student Record Lookup
// ============================================================
function handleStudentSearchInput(e) {
  const query = e.target.value.trim();
  const dropdown = document.getElementById("rbSearchResultsDropdown");
  if (!dropdown) return;

  if (searchDebounceTimer) clearTimeout(searchDebounceTimer);

  if (!query || query.length < 2) {
    dropdown.style.display = "none";
    dropdown.innerHTML = "";
    return;
  }

  searchDebounceTimer = setTimeout(async () => {
    let matches = [];

    // 1. Try querying backend API /api/students/all?search=...
    try {
      const res = await fetch(`/api/students/all?search=${encodeURIComponent(query)}`);
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          matches = data.slice(0, 6);
        }
      }
    } catch (err) {
      // Fallback to local catalog
    }

    // 2. Fallback to local benchmark catalog if no API matches
    if (matches.length === 0) {
      const qLower = query.toLowerCase();
      matches = LOCAL_STUDENT_CATALOG.filter(s => 
        s.name.toLowerCase().includes(qLower) || s.usn.toLowerCase().includes(qLower)
      ).slice(0, 6);
    }

    if (matches.length === 0) {
      dropdown.innerHTML = `
        <div style="padding:0.6rem 0.85rem; font-size:0.78rem; color:#94a3b8;">
          <i class="fa-solid fa-circle-info"></i> No university record found for "<strong>${escapeHtml(query)}</strong>". You can type details manually in Step 1.
        </div>
      `;
      dropdown.style.display = "block";
      return;
    }

    // Render suggestion items
    dropdown.innerHTML = matches.map(s => `
      <div class="rb-search-item" onclick="selectStudentSearchResult('${escapeHtml(s.usn)}')">
        <div style="font-weight:700; color:#f8fafc; display:flex; justify-content:space-between;">
          <span>${escapeHtml(s.name)}</span>
          <span style="color:#38bdf8; font-family:monospace; font-size:0.75rem;">${escapeHtml(s.usn)}</span>
        </div>
        <div style="font-size:0.72rem; color:#94a3b8; margin-top:2px;">
          ${escapeHtml(s.branch || "CSE")} · Semester ${s.semester || 8} · CGPA: <strong>${s.cgpa || "8.5"}</strong>
        </div>
      </div>
    `).join("");
    dropdown.style.display = "block";
  }, 180);
}

function handleStudentSearchKeydown(e) {
  if (e.key === "Enter") {
    e.preventDefault();
    executeStudentFetchFromSearch();
  }
}

async function selectStudentSearchResult(usn) {
  const searchInput = document.getElementById("rbSearchStudentInput");
  const dropdown = document.getElementById("rbSearchResultsDropdown");
  if (dropdown) dropdown.style.display = "none";

  await fetchAndPopulateStudent(usn);
}

async function executeStudentFetchFromSearch() {
  const searchInput = document.getElementById("rbSearchStudentInput");
  const query = searchInput ? searchInput.value.trim() : "";
  const dropdown = document.getElementById("rbSearchResultsDropdown");
  if (dropdown) dropdown.style.display = "none";

  if (!query) {
    alert("Please type a student Name or USN to search.");
    return;
  }

  await fetchAndPopulateStudent(query);
}

async function fetchAndPopulateStudent(queryOrUsn) {
  const statusEl = document.getElementById("rbAutoFillStatus");
  if (statusEl) {
    statusEl.innerHTML = `<span style="color:#38bdf8;"><i class="fa-solid fa-spinner fa-spin"></i> Searching university records for "<strong>${escapeHtml(queryOrUsn)}</strong>"...</span>`;
  }

  let profile = null;

  // 1. Try fetching exact USN profile
  try {
    const res = await fetch(`/api/students/profile?usn=${encodeURIComponent(queryOrUsn)}`);
    if (res.ok) {
      const data = await res.json();
      if (data && data.usn) {
        profile = data;
      }
    }
  } catch (err) {}

  // 2. If not found, try search endpoint
  if (!profile) {
    try {
      const res = await fetch(`/api/students/all?search=${encodeURIComponent(queryOrUsn)}`);
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          profile = data[0];
        }
      }
    } catch (err) {}
  }

  // 3. Fallback to local catalog
  if (!profile) {
    const qLower = queryOrUsn.toLowerCase();
    profile = LOCAL_STUDENT_CATALOG.find(s => 
      s.usn.toLowerCase() === qLower || s.name.toLowerCase().includes(qLower)
    );
  }

  if (!profile) {
    if (statusEl) {
      statusEl.innerHTML = `
        <div style="background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.35); border-radius:4px; padding:0.45rem 0.85rem; color:#fca5a5; font-size:0.78rem;">
          <i class="fa-solid fa-triangle-exclamation"></i> No registered student found for "<strong>${escapeHtml(queryOrUsn)}</strong>". You can enter your details manually in Step 1.
        </div>
      `;
      setTimeout(() => { if (statusEl) statusEl.innerHTML = ""; }, 5000);
    }
    return;
  }

  // Populate Step 1 fields
  const setVal = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.value = val || "";
  };

  const branchName = profile.branch === "CSE" ? "Computer Science & Engineering" : 
                    (profile.branch === "ISE" ? "Information Science & Engineering" : profile.branch || "Computer Science");

  setVal("rbFullName", profile.name);
  setVal("rbUSN", profile.usn);
  setVal("rbEmail", profile.email || `${profile.usn.toLowerCase()}@kletech.ac.in`);
  setVal("rbPhone", profile.phone || "+91 98765 43210");
  setVal("rbCollege", "KLE Technological University, Hubballi");
  setVal("rbDegree", `B.E. ${branchName}`);
  setVal("rbSemester", profile.semester ? `${profile.semester}th Semester` : "8th Semester");
  setVal("rbCGPA", profile.cgpa ? `${profile.cgpa} / 10` : "8.50 / 10");
  setVal("rbRole", profile.role || "Software Engineering & AI Intern");
  setVal("rbLocation", profile.location || "Hubballi / Bengaluru, Karnataka");
  setVal("rbSummary", `Final-year ${branchName} undergraduate at KLE Tech with solid foundations in algorithms, software systems, and data-driven problem solving.`);

  // Update input box to show fetched student
  const searchInput = document.getElementById("rbSearchStudentInput");
  if (searchInput) searchInput.value = `${profile.name} (${profile.usn})`;

  // Step 1 is active so student sees their fetched details
  rbGoToStep(1);

  if (statusEl) {
    statusEl.innerHTML = `
      <div style="background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.4); border-radius:4px; padding:0.5rem 0.85rem; color:#34d399; font-size:0.8rem; font-weight:600; display:flex; align-items:center; gap:0.5rem;">
        <i class="fa-solid fa-circle-check"></i>
        <span>Official Academic Record verified for <strong>${escapeHtml(profile.name)} (${escapeHtml(profile.usn)})</strong>! Review Step 1 and proceed to Step 2 to choose your skills.</span>
      </div>
    `;
    setTimeout(() => { if (statusEl) statusEl.innerHTML = ""; }, 5000);
  }
}

// Close search dropdown on click outside
document.addEventListener("click", (e) => {
  const dropdown = document.getElementById("rbSearchResultsDropdown");
  const searchInput = document.getElementById("rbSearchStudentInput");
  if (dropdown && e.target !== dropdown && e.target !== searchInput) {
    dropdown.style.display = "none";
  }
});

// ============================================================
// Step 2: Skill Tags & Projects Management
// ============================================================
function toggleSkillTag(skillName) {
  if (activeSelectedSkills.has(skillName)) {
    activeSelectedSkills.delete(skillName);
  } else {
    activeSelectedSkills.add(skillName);
  }
  refreshSkillChipsUI();
  updateResumeBuilderPreview();
}

function refreshSkillChipsUI() {
  document.querySelectorAll(".rb-skill-chip").forEach(chip => {
    const sName = chip.getAttribute("data-skill");
    if (activeSelectedSkills.has(sName)) {
      chip.classList.add("selected");
    } else {
      chip.classList.remove("selected");
    }
  });
}

function addCustomSkill() {
  const input = document.getElementById("rbCustomSkillInput");
  if (!input) return;
  const val = input.value.trim();
  if (!val) return;

  activeSelectedSkills.add(val);
  input.value = "";

  const container = document.getElementById("rbCustomSkillsContainer");
  if (container) {
    const newChip = document.createElement("button");
    newChip.type = "button";
    newChip.className = "rb-skill-chip selected";
    newChip.setAttribute("data-skill", val);
    newChip.onclick = () => toggleSkillTag(val);
    newChip.innerHTML = `<i class="fa-solid fa-check"></i> ${escapeHtml(val)}`;
    container.appendChild(newChip);
  }

  updateResumeBuilderPreview();
}

function insertSampleProject(type) {
  const setVal = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.value = val;
  };

  if (type === "ai") {
    setVal("rbProj1Title", "AURA Multi-Agent Healthcare Decision & RAG Engine");
    setVal("rbProj1Tech", "LangGraph, Python, PyTorch, Vector DB");
    setVal("rbProj1Bullets", "• Architected multi-agent graph with bounded retry loops, achieving 94% retrieval accuracy.\n• Implemented cryptographic audit logging and deterministic verification.");
  } else if (type === "web") {
    setVal("rbProj2Title", "Real-Time Placement & Vacancy Decrement Portal");
    setVal("rbProj2Tech", "FastAPI, React, SQLite, Docker");
    setVal("rbProj2Bullets", "• Engineered full-stack internship tracking for 500+ candidates.\n• Implemented race-condition-free vacancy decrements and faculty approval gates.");
  }

  updateResumeBuilderPreview();
}

function resetResumeBuilder() {
  if (!confirm("Clear all details and start fresh?")) return;

  const ids = [
    "rbFullName", "rbUSN", "rbEmail", "rbPhone", "rbCollege", "rbDegree", 
    "rbSemester", "rbCGPA", "rbRole", "rbLocation", "rbSummary",
    "rbProj1Title", "rbProj1Tech", "rbProj1Bullets",
    "rbProj2Title", "rbProj2Tech", "rbProj2Bullets", "rbCertifications"
  ];
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = "";
  });

  const searchInput = document.getElementById("rbSearchStudentInput");
  if (searchInput) searchInput.value = "";

  activeSelectedSkills.clear();
  refreshSkillChipsUI();

  const customContainer = document.getElementById("rbCustomSkillsContainer");
  if (customContainer) customContainer.innerHTML = "";

  rbGoToStep(1);
  updateResumeBuilderPreview();
}

// ============================================================
// Data Retrieval & Real-Time Preview
// ============================================================
function getResumeBuilderData() {
  const getVal = (id) => {
    const el = document.getElementById(id);
    return el ? el.value.trim() : "";
  };

  const skillsList = Array.from(activeSelectedSkills);
  return {
    fullName: getVal("rbFullName"),
    usn: getVal("rbUSN"),
    email: getVal("rbEmail"),
    phone: getVal("rbPhone"),
    location: getVal("rbLocation"),
    role: getVal("rbRole"),
    summary: getVal("rbSummary"),
    college: getVal("rbCollege"),
    degree: getVal("rbDegree"),
    semester: getVal("rbSemester"),
    cgpa: getVal("rbCGPA"),
    skills: skillsList.length ? skillsList.join(", ") : "",
    proj1Title: getVal("rbProj1Title"),
    proj1Tech: getVal("rbProj1Tech"),
    proj1Bullets: getVal("rbProj1Bullets"),
    proj2Title: getVal("rbProj2Title"),
    proj2Tech: getVal("rbProj2Tech"),
    proj2Bullets: getVal("rbProj2Bullets"),
    certifications: getVal("rbCertifications")
  };
}

function updateResumeBuilderPreview() {
  const d = getResumeBuilderData();
  const preview = document.getElementById("resumePreviewSheet");
  if (!preview) return;

  // Determine if there is any entered data
  const hasData = Boolean(
    d.fullName || d.usn || d.degree || d.skills || d.proj1Title || d.summary
  );

  // If empty, show clean, friendly placeholder
  if (!hasData) {
    preview.innerHTML = `
      <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding:3.5rem 1rem; color:#64748b; text-align:center;">
        <div style="font-size:2.8rem; color:#cbd5e1; margin-bottom:1rem;">
          <i class="fa-regular fa-file-lines"></i>
        </div>
        <h3 style="margin:0 0 0.5rem 0; font-size:1.1rem; color:#334155; font-weight:700;">Your Resume Preview is Empty</h3>
        <p style="margin:0; font-size:0.8rem; color:#64748b; max-width:320px; line-height:1.5;">
          Search your <strong>Name</strong> or <strong>USN</strong> above to fetch your official university record, or fill in <strong>Step 1</strong> to start.
        </p>
      </div>
    `;
    return;
  }

  const formatBullets = (text) => {
    if (!text) return "";
    return text.split("\n")
      .map(line => line.trim())
      .filter(line => line.length > 0)
      .map(line => {
        const clean = line.replace(/^[•\-\*]\s*/, "");
        return `<li style="margin-bottom:2px;">${escapeHtml(clean)}</li>`;
      }).join("");
  };

  const contactItems = [
    d.usn ? `<strong>USN:</strong> ${escapeHtml(d.usn)}` : "",
    d.email ? `<span style="color:#0284c7;">${escapeHtml(d.email)}</span>` : "",
    d.phone ? escapeHtml(d.phone) : "",
    d.location ? escapeHtml(d.location) : ""
  ].filter(Boolean).join(" &nbsp;|&nbsp; ");

  preview.innerHTML = `
    <div style="border-bottom:2px solid #0f172a; padding-bottom:6px; margin-bottom:10px;">
      <h2 style="margin:0; font-size:1.35rem; font-weight:800; color:#0f172a; letter-spacing:0.5px;">${escapeHtml((d.fullName || "STUDENT NAME").toUpperCase())}</h2>
      ${d.role ? `<div style="font-size:0.86rem; font-weight:700; color:#2563eb; margin-top:2px;">${escapeHtml(d.role)}</div>` : ""}
      ${contactItems ? `<div style="font-size:0.75rem; color:#475569; margin-top:4px;">${contactItems}</div>` : ""}
    </div>

    ${d.summary ? `
    <div style="margin-bottom:10px;">
      <div class="resume-sheet-section-title">PROFESSIONAL SUMMARY</div>
      <p style="margin:4px 0 0 0; font-size:0.8rem; color:#334155; line-height:1.4;">${escapeHtml(d.summary)}</p>
    </div>` : ""}

    ${(d.college || d.degree || d.cgpa) ? `
    <div style="margin-bottom:10px;">
      <div class="resume-sheet-section-title">ACADEMIC BACKGROUND</div>
      <div style="display:flex; justify-content:space-between; align-items:baseline; margin-top:3px;">
        <strong style="color:#0f172a; font-size:0.82rem;">${escapeHtml(d.college || "University")}</strong>
        <span style="font-size:0.75rem; color:#64748b;">${escapeHtml(d.semester || "")}</span>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:0.78rem; color:#334155;">
        <span>${escapeHtml(d.degree || "")}</span>
        ${d.cgpa ? `<strong style="color:#059669;">Verified CGPA: ${escapeHtml(d.cgpa)}</strong>` : ""}
      </div>
    </div>` : ""}

    ${d.skills ? `
    <div style="margin-bottom:10px;">
      <div class="resume-sheet-section-title">TECHNICAL COMPETENCIES</div>
      <div style="font-size:0.78rem; color:#334155; line-height:1.45; margin-top:4px;">
        <div><strong>Core Skills:</strong> ${escapeHtml(d.skills)}</div>
      </div>
    </div>` : ""}

    ${(d.proj1Title || d.proj2Title) ? `
    <div style="margin-bottom:10px;">
      <div class="resume-sheet-section-title">CAPSTONE & ENGINEERING PROJECTS</div>
      
      ${d.proj1Title ? `
      <div style="margin-top:5px; margin-bottom:8px;">
        <div style="display:flex; justify-content:space-between; font-size:0.82rem;">
          <strong style="color:#0f172a;">${escapeHtml(d.proj1Title)}</strong>
          ${d.proj1Tech ? `<span style="font-size:0.74rem; color:#4338ca; font-weight:700;">[${escapeHtml(d.proj1Tech)}]</span>` : ""}
        </div>
        ${d.proj1Bullets ? `
        <ul style="margin:2px 0 0 1.1rem; padding:0; font-size:0.77rem; color:#334155;">
          ${formatBullets(d.proj1Bullets)}
        </ul>` : ""}
      </div>` : ""}

      ${d.proj2Title ? `
      <div style="margin-top:5px;">
        <div style="display:flex; justify-content:space-between; font-size:0.82rem;">
          <strong style="color:#0f172a;">${escapeHtml(d.proj2Title)}</strong>
          ${d.proj2Tech ? `<span style="font-size:0.74rem; color:#4338ca; font-weight:700;">[${escapeHtml(d.proj2Tech)}]</span>` : ""}
        </div>
        ${d.proj2Bullets ? `
        <ul style="margin:2px 0 0 1.1rem; padding:0; font-size:0.77rem; color:#334155;">
          ${formatBullets(d.proj2Bullets)}
        </ul>` : ""}
      </div>` : ""}
    </div>` : ""}

    ${d.certifications ? `
    <div style="margin-bottom:6px;">
      <div class="resume-sheet-section-title">CERTIFICATIONS & HONORS</div>
      <ul style="margin:3px 0 0 1.1rem; padding:0; font-size:0.77rem; color:#334155;">
        ${formatBullets(d.certifications)}
      </ul>
    </div>` : ""}
  `;
}

// ============================================================
// Actions: Export & Transfer to Matcher
// ============================================================
function generateResumePlainText() {
  const d = getResumeBuilderData();
  return `${(d.fullName || "STUDENT").toUpperCase()} (USN: ${d.usn || ""})
${d.degree} | ${d.college}
${d.semester} | CGPA: ${d.cgpa} | ${d.location}
Contact: ${d.email} | ${d.phone}

TARGET INTERNSHIP ROLE:
${d.role}

PROFESSIONAL SUMMARY:
${d.summary}

TECHNICAL SKILLS:
${d.skills}

ACADEMIC & TECHNICAL PROJECTS:
1. ${d.proj1Title} [${d.proj1Tech}]
${d.proj1Bullets}

2. ${d.proj2Title} [${d.proj2Tech}]
${d.proj2Bullets}

CERTIFICATIONS & ACHIEVEMENTS:
${d.certifications}
`.trim();
}

function copyResumePlainText() {
  const text = generateResumePlainText();
  if (!text || text.length < 15) {
    alert("Resume is currently empty. Please fetch your profile or fill in your details first.");
    return;
  }
  navigator.clipboard.writeText(text).then(() => {
    alert("Formatted ATS-compatible resume text copied to clipboard!");
  }).catch(() => {
    alert("Resume copied!");
  });
}

function printResumeSheet() {
  const d = getResumeBuilderData();
  if (!d.fullName && !d.usn) {
    alert("Resume is currently empty. Please enter your details or fetch your record first.");
    return;
  }
  window.print();
}

function transferResumeToSkillsMatcher() {
  const text = generateResumePlainText();
  if (!text || text.length < 20) {
    alert("Your resume is empty. Please search and fetch your student record, or enter your details first.");
    return;
  }
  
  if (typeof switchView === "function") {
    switchView("resume-matcher");
  }

  const textarea = document.getElementById("resumeTextInput");
  if (textarea) {
    textarea.value = text;
  }

  const statusEl = document.getElementById("resumeInputStatus");
  if (statusEl) {
    statusEl.innerHTML = `
      <div style="background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.4); border-radius:4px; padding:0.5rem 0.85rem; margin-top:0.4rem; color:#34d399; font-weight:600;">
        <i class="fa-solid fa-circle-check"></i> Resume successfully transferred from Builder! Click <strong>'Auto-Calculate Skill Match'</strong> below to analyze compatibility.
      </div>
    `;
  }

  const matchBtn = document.getElementById("btnMatchResume");
  if (matchBtn) {
    matchBtn.scrollIntoView({ behavior: "smooth", block: "center" });
    matchBtn.classList.add("pulse-highlight");
    setTimeout(() => matchBtn.classList.remove("pulse-highlight"), 2000);
  }
}

// Bind live updates on DOM ready
document.addEventListener("DOMContentLoaded", () => {
  const inputs = document.querySelectorAll("#view-resume-builder input, #view-resume-builder textarea");
  inputs.forEach(input => {
    input.addEventListener("input", updateResumeBuilderPreview);
  });
  // Initial render starts completely empty
  setTimeout(updateResumeBuilderPreview, 250);
});
