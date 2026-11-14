/**
 * INTERNTRACK — AI Resume & CV Builder Frontend Controller
 * Provides interactive resume authoring, real-time preview, ATS-friendly plain-text export,
 * and direct 1-click bridge to the Resume & Skills Matcher.
 */

const RESUME_BUILDER_SAMPLES = {
  aiml: {
    fullName: "ANANYA S.",
    usn: "1KG21CS045",
    email: "ananya.s@kletech.ac.in",
    phone: "+91 98765 43210",
    location: "Bangalore / Hubballi, Karnataka",
    linkedin: "linkedin.com/in/ananya-s",
    github: "github.com/ananya-s",
    role: "AI / Machine Learning Engineer Intern",
    summary: "Final-year Computer Science undergraduate specializing in Artificial Intelligence and Multi-Agent Systems. Experienced in developing deterministic LangGraph pipelines, RAG engines, and deep learning architectures with high accuracy and audit compliance.",
    college: "KLE Technological University, Hubballi",
    degree: "B.E. Computer Science & Engineering (AI)",
    semester: "8th Semester",
    cgpa: "8.65 / 10",
    languages: "Python, C++, Java, SQL, TypeScript",
    frameworks: "PyTorch, TensorFlow, LangGraph, Scikit-learn, Pandas, NumPy, FastAPI",
    cloudTools: "Docker, Git, Linux, AWS (EC2, S3), GitHub Actions, Vector Databases",
    databases: "SQLite, PostgreSQL, MongoDB, Redis",
    proj1Title: "AURA Multi-Agent Healthcare RAG & Decision Engine",
    proj1Tech: "LangGraph, Python, PyTorch, FAISS",
    proj1Bullets: "• Architected multi-agent graph with bounded retry loops, achieving 94% retrieval accuracy.\n• Implemented cryptographic audit logging and role-based access for HIPAA compliance.\n• Reduced query hallucination rates to 0% with cross-encoder verification.",
    proj2Title: "Real-Time Object Detection & Tracking Pipeline",
    proj2Tech: "PyTorch, OpenCV, Docker, AWS",
    proj2Bullets: "• Built low-latency object recognition pipeline processing 45 FPS on edge hardware.\n• Containerized application with Docker and established automated CI/CD pipeline on AWS.",
    certifications: "• AWS Certified Cloud Practitioner (Score: 890/1000)\n• Deep Learning Specialization (DeepLearning.AI / Coursera)\n• Winner, University Smart Campus Innovation Hackathon 2025"
  },
  fullstack: {
    fullName: "ROHIT VERMA",
    usn: "1FE23BCS042",
    email: "rohit.verma@kletech.ac.in",
    phone: "+91 98123 45678",
    location: "Bengaluru, Karnataka",
    linkedin: "linkedin.com/in/rohit-verma",
    github: "github.com/rohit-v",
    role: "Full-Stack Web Developer Intern",
    summary: "Proactive 8th-semester engineering student with strong skills in React, Node.js, and cloud backends. Passionate about designing responsive frontends and microservices architectures.",
    college: "KLE Technological University, Hubballi",
    degree: "B.E. Computer Science & Engineering",
    semester: "8th Semester",
    cgpa: "8.20 / 10",
    languages: "JavaScript, TypeScript, Python, Java, SQL, HTML5, CSS3",
    frameworks: "React, Next.js, Node.js, Express, TailwindCSS, Redux",
    cloudTools: "Git, Docker, AWS, Postman, Linux, Vercel",
    databases: "PostgreSQL, MongoDB, SQLite, Redis",
    proj1Title: "Autonomous Internship Tracking & Vacancy Portal",
    proj1Tech: "React, Node.js, SQLite, REST APIs",
    proj1Bullets: "• Built full-stack student management portal handling 500+ active candidates.\n• Integrated real-time vacancy counters and role-based authentication with JWT.",
    proj2Title: "Distributed Cloud Task Manager",
    proj2Tech: "Next.js, TypeScript, PostgreSQL, Docker",
    proj2Bullets: "• Developed responsive collaboration workspace with WebSocket live updates.\n• Achieved sub-100ms API response times with Redis caching.",
    certifications: "• Meta Front-End Developer Professional Certificate\n• MongoDB Certified Associate Developer"
  },
  cloud: {
    fullName: "PRIYA KULKARNI",
    usn: "1FE23BCS088",
    email: "priya.k@kletech.ac.in",
    phone: "+91 97654 32109",
    location: "Hubballi / Bengaluru",
    linkedin: "linkedin.com/in/priya-kulkarni",
    github: "github.com/priyak",
    role: "Cloud Infrastructure & DevOps Intern",
    summary: "DevOps and cloud enthusiast with practical experience in Kubernetes, Terraform, and CI/CD automation across AWS and Azure environments.",
    college: "KLE Technological University, Hubballi",
    degree: "B.E. Information Science & Engineering",
    semester: "8th Semester",
    cgpa: "8.40 / 10",
    languages: "Python, Go, Bash, SQL",
    frameworks: "FastAPI, Flask, PyTest",
    cloudTools: "AWS, Azure, Docker, Kubernetes, Terraform, Prometheus, Grafana, GitHub Actions",
    databases: "PostgreSQL, Redis, MySQL",
    proj1Title: "Automated Multi-Cloud Infrastructure as Code",
    proj1Tech: "Terraform, AWS, Kubernetes, Helm",
    proj1Bullets: "• Automated high-availability multi-region cluster deployment with Terraform.\n• Configured monitoring dashboards in Grafana with automated alert rules.",
    proj2Title: "GitOps Continuous Deployment Pipeline",
    proj2Tech: "ArgoCD, GitHub Actions, Docker",
    proj2Bullets: "• Established zero-downtime deployment pipelines reducing release cycles by 60%.\n• Implemented automated vulnerability scanning using Trivy.",
    certifications: "• HashiCorp Certified: Terraform Associate\n• AWS Certified Solutions Architect — Associate"
  }
};

function getResumeBuilderFormData() {
  const getVal = (id, fallback = "") => {
    const el = document.getElementById(id);
    return el ? el.value.trim() : fallback;
  };

  return {
    fullName: getVal("rbFullName", "ANANYA S."),
    usn: getVal("rbUSN", "1KG21CS045"),
    email: getVal("rbEmail", "ananya.s@kletech.ac.in"),
    phone: getVal("rbPhone", "+91 98765 43210"),
    location: getVal("rbLocation", "Bangalore / Hubballi"),
    linkedin: getVal("rbLinkedIn", "linkedin.com/in/ananya-s"),
    github: getVal("rbGitHub", "github.com/ananya-s"),
    role: getVal("rbRole", "AI / Machine Learning Engineer Intern"),
    summary: getVal("rbSummary", "Computer Science undergraduate with expertise in AI, ML, and scalable web services."),
    college: getVal("rbCollege", "KLE Technological University"),
    degree: getVal("rbDegree", "B.E. Computer Science & Engineering"),
    semester: getVal("rbSemester", "8th Semester"),
    cgpa: getVal("rbCGPA", "8.65 / 10"),
    languages: getVal("rbLanguages", "Python, C++, Java, SQL"),
    frameworks: getVal("rbFrameworks", "PyTorch, LangGraph, React, FastAPI"),
    cloudTools: getVal("rbCloudTools", "Docker, Git, AWS, Linux"),
    databases: getVal("rbDatabases", "PostgreSQL, SQLite, MongoDB"),
    proj1Title: getVal("rbProj1Title", "Multi-Agent Autonomous RAG Engine"),
    proj1Tech: getVal("rbProj1Tech", "LangGraph, Python, Vector DB"),
    proj1Bullets: getVal("rbProj1Bullets", "• Built deterministic graph workflow with 94% retrieval accuracy."),
    proj2Title: getVal("rbProj2Title", "Real-Time Placement & Vacancy Portal"),
    proj2Tech: getVal("rbProj2Tech", "FastAPI, React, SQLite"),
    proj2Bullets: getVal("rbProj2Bullets", "• Engineered full-stack tracking with atomic vacancy decrements."),
    certifications: getVal("rbCertifications", "• AWS Certified Cloud Practitioner\n• Deep Learning Specialization")
  };
}

function updateResumeBuilderPreview() {
  const data = getResumeBuilderFormData();
  const preview = document.getElementById("resumePreviewSheet");
  if (!preview) return;

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
    data.usn ? `<strong>USN:</strong> ${escapeHtml(data.usn)}` : "",
    data.email ? `<a href="mailto:${escapeHtml(data.email)}" style="color:#0284c7; text-decoration:none;">${escapeHtml(data.email)}</a>` : "",
    data.phone ? escapeHtml(data.phone) : "",
    data.location ? escapeHtml(data.location) : "",
    data.linkedin ? `<span style="color:#0284c7;">${escapeHtml(data.linkedin)}</span>` : "",
    data.github ? `<span style="color:#0284c7;">${escapeHtml(data.github)}</span>` : ""
  ].filter(Boolean).join(" &nbsp;|&nbsp; ");

  preview.innerHTML = `
    <div style="border-bottom:2px solid #0f172a; padding-bottom:6px; margin-bottom:10px;">
      <h2 style="margin:0; font-size:1.4rem; color:#0f172a; letter-spacing:0.5px;">${escapeHtml(data.fullName.toUpperCase())}</h2>
      ${data.role ? `<div style="font-size:0.88rem; font-weight:600; color:#2563eb; margin-top:2px;">${escapeHtml(data.role)}</div>` : ""}
      <div style="font-size:0.75rem; color:#475569; margin-top:4px;">${contactItems}</div>
    </div>

    ${data.summary ? `
    <div style="margin-bottom:10px;">
      <div class="resume-sheet-section-title">PROFESSIONAL SUMMARY</div>
      <p style="margin:4px 0 0 0; font-size:0.8rem; color:#334155; line-height:1.4;">${escapeHtml(data.summary)}</p>
    </div>` : ""}

    <div style="margin-bottom:10px;">
      <div class="resume-sheet-section-title">EDUCATION</div>
      <div style="display:flex; justify-content:space-between; align-items:baseline; margin-top:3px;">
        <strong style="color:#0f172a; font-size:0.82rem;">${escapeHtml(data.college)}</strong>
        <span style="font-size:0.75rem; color:#64748b;">${escapeHtml(data.semester)}</span>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:0.78rem; color:#334155;">
        <span>${escapeHtml(data.degree)}</span>
        <strong style="color:#059669;">CGPA: ${escapeHtml(data.cgpa)}</strong>
      </div>
    </div>

    <div style="margin-bottom:10px;">
      <div class="resume-sheet-section-title">TECHNICAL SKILLS</div>
      <div style="font-size:0.78rem; color:#334155; line-height:1.45; margin-top:4px;">
        ${data.languages ? `<div><strong>Languages:</strong> ${escapeHtml(data.languages)}</div>` : ""}
        ${data.frameworks ? `<div><strong>Frameworks & Libraries:</strong> ${escapeHtml(data.frameworks)}</div>` : ""}
        ${data.cloudTools ? `<div><strong>Cloud & DevOps:</strong> ${escapeHtml(data.cloudTools)}</div>` : ""}
        ${data.databases ? `<div><strong>Databases:</strong> ${escapeHtml(data.databases)}</div>` : ""}
      </div>
    </div>

    ${(data.proj1Title || data.proj2Title) ? `
    <div style="margin-bottom:10px;">
      <div class="resume-sheet-section-title">ACADEMIC & TECHNICAL PROJECTS</div>
      
      ${data.proj1Title ? `
      <div style="margin-top:5px; margin-bottom:8px;">
        <div style="display:flex; justify-content:space-between; font-size:0.82rem;">
          <strong style="color:#0f172a;">${escapeHtml(data.proj1Title)}</strong>
          ${data.proj1Tech ? `<span style="font-size:0.74rem; color:#4338ca; font-weight:600;">[${escapeHtml(data.proj1Tech)}]</span>` : ""}
        </div>
        <ul style="margin:2px 0 0 1.1rem; padding:0; font-size:0.77rem; color:#334155;">
          ${formatBullets(data.proj1Bullets)}
        </ul>
      </div>` : ""}

      ${data.proj2Title ? `
      <div style="margin-top:5px;">
        <div style="display:flex; justify-content:space-between; font-size:0.82rem;">
          <strong style="color:#0f172a;">${escapeHtml(data.proj2Title)}</strong>
          ${data.proj2Tech ? `<span style="font-size:0.74rem; color:#4338ca; font-weight:600;">[${escapeHtml(data.proj2Tech)}]</span>` : ""}
        </div>
        <ul style="margin:2px 0 0 1.1rem; padding:0; font-size:0.77rem; color:#334155;">
          ${formatBullets(data.proj2Bullets)}
        </ul>
      </div>` : ""}
    </div>` : ""}

    ${data.certifications ? `
    <div style="margin-bottom:6px;">
      <div class="resume-sheet-section-title">CERTIFICATIONS & HONORS</div>
      <ul style="margin:3px 0 0 1.1rem; padding:0; font-size:0.77rem; color:#334155;">
        ${formatBullets(data.certifications)}
      </ul>
    </div>` : ""}
  `;
}

function loadSampleResumeBuilder(profileType) {
  const sample = RESUME_BUILDER_SAMPLES[profileType] || RESUME_BUILDER_SAMPLES.aiml;
  const setVal = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.value = val;
  };

  setVal("rbFullName", sample.fullName);
  setVal("rbUSN", sample.usn);
  setVal("rbEmail", sample.email);
  setVal("rbPhone", sample.phone);
  setVal("rbLocation", sample.location);
  setVal("rbLinkedIn", sample.linkedin);
  setVal("rbGitHub", sample.github);
  setVal("rbRole", sample.role);
  setVal("rbSummary", sample.summary);
  setVal("rbCollege", sample.college);
  setVal("rbDegree", sample.degree);
  setVal("rbSemester", sample.semester);
  setVal("rbCGPA", sample.cgpa);
  setVal("rbLanguages", sample.languages);
  setVal("rbFrameworks", sample.frameworks);
  setVal("rbCloudTools", sample.cloudTools);
  setVal("rbDatabases", sample.databases);
  setVal("rbProj1Title", sample.proj1Title);
  setVal("rbProj1Tech", sample.proj1Tech);
  setVal("rbProj1Bullets", sample.proj1Bullets);
  setVal("rbProj2Title", sample.proj2Title);
  setVal("rbProj2Tech", sample.proj2Tech);
  setVal("rbProj2Bullets", sample.proj2Bullets);
  setVal("rbCertifications", sample.certifications);

  updateResumeBuilderPreview();

  const statusEl = document.getElementById("rbStatusMessage");
  if (statusEl) {
    statusEl.innerHTML = `<span style="color:#10b981;"><i class="fa-solid fa-check"></i> Loaded sample <strong>${profileType.toUpperCase()}</strong> profile!</span>`;
    setTimeout(() => { if (statusEl) statusEl.innerHTML = ""; }, 3500);
  }
}

function generateResumePlainText() {
  const d = getResumeBuilderFormData();
  return `${d.fullName.toUpperCase()} (USN: ${d.usn})
${d.degree} | ${d.college}
${d.semester} | CGPA: ${d.cgpa} | ${d.location}
Contact: ${d.email} | ${d.phone} | ${d.linkedin} | ${d.github}

TARGET ROLE: ${d.role}

PROFESSIONAL SUMMARY:
${d.summary}

TECHNICAL SKILLS:
- Languages: ${d.languages}
- Frameworks & Libraries: ${d.frameworks}
- Cloud, DevOps & Tools: ${d.cloudTools}
- Databases: ${d.databases}

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
  navigator.clipboard.writeText(text).then(() => {
    const statusEl = document.getElementById("rbStatusMessage");
    if (statusEl) {
      statusEl.innerHTML = `<span style="color:#10b981;"><i class="fa-solid fa-clipboard-check"></i> Formatted plain-text resume copied to clipboard!</span>`;
      setTimeout(() => { if (statusEl) statusEl.innerHTML = ""; }, 3500);
    }
  }).catch(() => {
    alert("Copied successfully!");
  });
}

function printResumeSheet() {
  window.print();
}

function transferResumeToSkillsMatcher() {
  const text = generateResumePlainText();
  
  // 1. Switch to Resume Matcher view
  if (typeof switchView === "function") {
    switchView("resume-matcher");
  }

  // 2. Populate the Resume Matcher textarea
  const textarea = document.getElementById("resumeTextInput");
  if (textarea) {
    textarea.value = text;
  }

  // 3. Show confirmation badge
  const statusEl = document.getElementById("resumeInputStatus");
  if (statusEl) {
    statusEl.innerHTML = `
      <div style="background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.4); border-radius:4px; padding:0.4rem 0.75rem; margin-top:0.4rem; color:#34d399;">
        <i class="fa-solid fa-circle-check"></i> <strong>Resume imported from Builder successfully!</strong> Click <strong>'Auto-Calculate Skill Match'</strong> below to analyze opportunities.
      </div>
    `;
  }

  // 4. Scroll smoothly to the calculate button
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
  // Initial render with default values
  setTimeout(updateResumeBuilderPreview, 300);
});
