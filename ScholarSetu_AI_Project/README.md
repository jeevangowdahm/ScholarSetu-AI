# ScholarSetu AI (v2.0.0 Production Release)
## Scholarship & Government Scheme Eligibility Checker

> **Broad Area / Project Title:** Scholarship & Government Scheme Eligibility Checker  
> **Measurable Engineering Outcome:** Develop a Web tool matching students to eligible scholarships and welfare schemes based on entered criteria with transparent, deterministic rule evaluation.

ScholarSetu AI is a student-centric GovTech web application designed in accordance with **Digital India & UX4G** design principles. It provides an explainable, authoritative, and accessible decision support engine matching Indian students across Higher Secondary, Diploma, Undergraduate, and Postgraduate streams to Central Ministries and State Government welfare programs.

---

## 🏛️ Key Features & Modules

### 1. Multi-Step Interactive Eligibility Wizard (myScheme Style)
- **Step 1 (Personal & Domicile):** Gender (supporting female-reserved schemes like AICTE Pragati & Single Girl Child), Age, State/UT of Domicile (28 States & 8 UTs), Rural/Urban classification, and Special Hardship Profiles (Differently Abled PwD >= 40%, Single Girl Child, Orphan/COVID-impacted, Wards of Ex-Servicemen/CAPF).
- **Step 2 (Academic Profile):** Current Education Level (Secondary to Ph.D.), Discipline/Stream (Engineering, Medicine, Pure Science, Commerce, Arts, Law), Institution Type (Premier IIT/NIT, State Govt/Aided, AICTE Approved, Private), and Previous Qualifying Exam Score (%).
- **Step 3 (Socio-Economic Background):** Category / Reservation (General, OBC-NCL, SC, ST, EWS), Minority Community selection, and Annual Family Income with instant preset buttons (₹1.4L, ₹2.4L, ₹4.0L, ₹7.5L).

### 2. Explainable, Deterministic Matching Engine
- Zero fake random numbers or ambiguous "AI confidence" scores. Every evaluation is deterministic and explainable:
  - **Direct Match (100% Verified):** All gazette criteria satisfied with estimated annual financial assistance in ₹.
  - **Action / Info Needed (Conditional):** Highlights missing or pending documents (e.g. required income certificate within 1 year or Nadakacheri RD number).
  - **Criteria Not Met (Ineligible):** Transparently lists specific reasons for disqualification (e.g. "Annual family income ₹3,50,000 exceeds scheme limit of ₹2,50,000").
- Full rule breakdown accordion showing checks for Level, Domicile, Gender, Category, Stream, Marks, and Income.

### 3. Comprehensive Repository of 16 Verified Schemes
Includes verified criteria, annual assistance amounts, deadlines, and official portal redirections:
1. **PM-USP Central Sector Scheme for College and University Students** (Department of Higher Education, MoE) — Up to ₹20,000/yr
2. **AICTE Pragati Scholarship for Girls (Technical Degree & Diploma)** — ₹50,000/yr (Direct Benefit Transfer)
3. **AICTE Saksham Scholarship for Specially Abled Students (PwD)** — ₹50,000/yr
4. **AICTE Swanath Scholarship Scheme (Orphans, COVID-affected, Martyrs' Wards)** — ₹50,000/yr
5. **Post-Matric Scholarship for SC Students** (Ministry of Social Justice & Empowerment) — 100% Fee Waiver + Maintenance
6. **Post-Matric Scholarship for ST Students** (Ministry of Tribal Affairs) — 100% Fee Waiver + Maintenance
7. **PM-YASASVI Post-Matric Scholarship for OBC, EBC & DNT Students** (MoSJE) — Up to ₹20,000/yr
8. **Ishan Uday Special Scholarship for North Eastern Region (NER)** (UGC, MoE) — Up to ₹93,600/yr
9. **Karnataka State Post-Matric Scholarship (SSP Karnataka)** — Full Tuition Waiver + Vidyasiri Food/Hostel Grant
10. **Begum Hazrat Mahal National Scholarship for Minority Girls** (Ministry of Minority Affairs) — ₹6,000/yr
11. **Prime Minister's Scholarship Scheme (PMSS) for Wards of Ex-Servicemen & CAPF** (Kendriya Sainik Board / MHA) — Up to ₹36,000/yr
12. **Top Class Education Scheme for SC Students in Premier Institutes (IIT/IIM/NIT)** (MoSJE) — Up to ₹2,50,000/yr
13. **National Means-cum-Merit Scholarship Scheme (NMMSS)** (MoE) — ₹12,000/yr
14. **Central Sector Interest Subsidy Scheme (CSIS) on Education Loans** (MoE) — 100% Full Interest Subsidy during Moratorium
15. **UGC Indira Gandhi Single Girl Child Postgraduate Scholarship** (UGC) — ₹36,200/yr (Total ₹72,400)
16. **Vidyasaarathi Higher Education Assistance & Foundation Grants** (NSDL / Corporate CSR) — Up to ₹75,000/yr

### 4. Side-by-Side Scheme Comparison Matrix
- Compare up to 4 schemes simultaneously in an interactive tabular breakdown comparing Annual Assistance, Income Ceilings, Minimum Marks, Eligible Levels, Category Quotas, Deadlines, and Official Portals.

### 5. Student Document Readiness Calculator
- Interactive self-assessment tool scoring student document readiness across the 6 vital certificates:
  - Aadhaar linked with active bank account (NPCI DBT active)
  - Annual Family Income Certificate from competent authority (Tahsildar / Revenue Inspector)
  - Digital Caste / Community Certificate (with verification barcode / RD number)
  - Previous Year Marksheets / Passing Certificate
  - College Bonafide / Enrollment Certificate
  - Domicile / Permanent Resident Certificate (PRC)
- Real-time score calculator (0% to 100%) with actionable DigiLocker and revenue department guidance.

### 6. Saved Shortlist & Printable Application Kit
- Save schemes directly to the student's SQLite database session.
- **"Print / Export Application Checklist"** button formatting the shortlisted schemes and their specific required document checklists into an official summary sheet for college nodal officers or cyber café applications.

### 7. Digital India UX4G & Accessibility Compliance
- Official Government of India & State Welfare topbar with Tiranga ribbon accent.
- **Accessibility Toolbar:** Font Resizer (A- / A / A+), High Contrast Dark Mode toggle (persisted in localStorage).
- Keyboard shortcuts: `Ctrl + K` for global instant search, `Esc` to dismiss dialogs.

### 8. AI Scholarship Assistant (Saarthi) & RAG Pipeline (v2.1.0)
- **Natural Language Scholarship Chatbot:** Interactive floating assistant answering student queries on eligibility, income limits, documents, and deadlines in real-time.
- **Grounded Scheme Retrieval:** Returns authoritative assistance amounts in ₹, ministry details, and direct links to official government application portals (`scholarships.gov.in`, `ssp.karnataka.gov.in`).
- **High-Throughput Caching & Zero-Lock Concurrency:** SQLite WAL mode with sub-millisecond in-memory scheme caching (`_SCHEMES_CACHE`) and automated background backups (`scholarsetu_backup.db`).

---

## 🛠️ Technology Stack & Architecture

- **Backend:** Python 3.10+, Flask, SQLite3
- **Frontend:** Semantic HTML5, Vanilla CSS3 (India UX4G GovTech Design System), Modern Vanilla JavaScript (ES6+)
- **Security & Privacy:** Privacy-first architecture — zero storage of Aadhaar, PAN, bank accounts, or uploaded documents.
- **APIs:** RESTful JSON endpoints with input validation.

---

## 🚀 Quickstart & Running Locally

1. Open PowerShell in `ScholarSetu_AI_Project`:
   ```powershell
   python app.py
   ```
2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Application status, version, and server timestamp |
| `GET` | `/api/stats` | Platform statistics (total schemes, ministries, max aid, DBT count) |
| `GET` | `/api/schemes?q=&category=&ministry=&sort=` | Search and filter the 16 verified schemes |
| `GET` | `/api/schemes/<int:id>` | Detailed metadata, documents, and application steps for a single scheme |
| `POST` | `/api/match` | Multi-criteria deterministic profile screening |
| `POST` | `/api/compare` | JSON: `{"ids": [1, 2, 9]}` — Returns side-by-side comparison matrix |
| `POST` | `/api/save` | JSON: `{"scheme_id": 2, "student_key": "student-user"}` — Bookmark scheme |
| `GET` | `/api/saved?student_key=student-user` | Retrieve shortlisted schemes from SQLite |
| `DELETE` | `/api/saved/<int:scheme_id>` | Remove scheme from shortlist |

---

## 📄 License & Academic Note
Developed as an engineering project at **RNSIT CSE (AI & ML)**. All scheme criteria and portal URLs are modeled after official Government of India (National Scholarship Portal) and Government of Karnataka (SSP) gazette notifications.
