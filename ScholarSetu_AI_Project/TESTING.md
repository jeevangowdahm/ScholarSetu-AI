# Test Suite & Verification Matrix — ScholarSetu AI (v2.0.0)

| ID | Module / Test Case | Input / Action | Expected Result | Status |
|---|---|---|---|---|
| **T01** | System Health | `GET /health` | HTTP 200, `{"status": "ok", "version": "2.0.0"}` | ✅ PASS |
| **T02** | Platform Stats | `GET /api/stats` | Returns total_schemes: 16, total_ministries: 8, max_aid | ✅ PASS |
| **T03** | Scheme Repository | `GET /api/schemes` | Returns 16 authentic seeded government schemes | ✅ PASS |
| **T04** | Scheme Details | `GET /api/schemes/2` | Returns full AICTE Pragati metadata & document list | ✅ PASS |
| **T05** | Category Filtering | `GET /api/schemes?category=Technical Education` | Returns AICTE Pragati, Saksham, Swanath, CSIS | ✅ PASS |
| **T06** | Full Text Search | Search query `Karnataka` | Filters to Karnataka State Post-Matric Scholarship (SSP) | ✅ PASS |
| **T07** | Step 1 Form Navigation | Fill Gender & Age, click `Continue` | Steps to Step 2 with completed checkmark on Step 1 | ✅ PASS |
| **T08** | Step 2 Form Navigation | Fill Level, Stream, Marks, click `Continue` | Steps to Step 3 with completed checkmark on Step 2 | ✅ PASS |
| **T09** | Valid Profile Screening | Female, UG, Engg, 85%, OBC, ₹2.4L income | Returns 5 Directly Eligible matches, ₹2,40,000 aid | ✅ PASS |
| **T10** | Male Gender Exclusion | Male student vs AICTE Pragati / Begum Hazrat | AICTE Pragati marked "Not matched" with female-only note | ✅ PASS |
| **T11** | Income Limit Rejection | Income ₹10,00,000 vs Post-Matric SC/ST (₹2.5L) | Marked "Not matched" with "Income exceeds ceiling" | ✅ PASS |
| **T12** | Marks Threshold Check | Marks 45% vs PM-USP Central Sector (80% cut-off) | Marked "Not matched" with "Marks fall below 80%" | ✅ PASS |
| **T13** | Domicile Check | State Karnataka vs Ishan Uday (North Eastern States) | Marked "Not matched" with "Restricted to 8 NER states" | ✅ PASS |
| **T14** | Special Status Matching | Check "Differently Abled (PwD >= 40%)" | AICTE Saksham becomes 100% Direct Match | ✅ PASS |
| **T15** | Scheme Comparison | Select AICTE Pragati + PM-USP + Karnataka SSP | Renders side-by-side comparison matrix with 10 rows | ✅ PASS |
| **T16** | Document Readiness | Tick Aadhaar + Income + Marksheet + Bonafide | Calculates score (70%) with actionable DigiLocker advice | ✅ PASS |
| **T17** | Shortlist Persistence | Click "☆ Save" on Scheme 1 | Persists in SQLite `saved` table; Shortlist count = 1 | ✅ PASS |
| **T18** | Shortlist Removal | Click "✕ Remove" on saved scheme | Deletes entry from SQLite `saved`; count updates | ✅ PASS |
| **T19** | Printable Application Kit | Click "🖨️ Print Application Checklist" | Prepares print view with checkboxes for submission | ✅ PASS |
| **T20** | Accessibility Controls | Toggle High Contrast & Font Resizer | Styles switch instantly; preference saved in localStorage | ✅ PASS |
| **T21** | Global Quick Search | Press `Ctrl + K` or click search trigger | Opens search modal; instant keyboard navigation | ✅ PASS |
| **T22** | Data Safety & Concurrency | SQLite WAL Mode + Busy Timeout 5s | Non-blocking concurrent queries; zero database locked errors | ✅ PASS |
| **T23** | High-Throughput Caching | In-Memory `_SCHEMES_CACHE` | Sub-millisecond evaluation latency (< 0.5ms) | ✅ PASS |
| **T24** | Automated Snapshot Backup | Trigger `POST /api/backup` | Atomic snapshot saved to `scholarsetu_backup.db` | ✅ PASS |
| **T25** | AI Assistant Chatbot (Saarthi) | `POST /api/chat` with Natural Language Query | Returns grounded scheme matches with official portal links | ✅ PASS |
| **T26** | Enterprise SAST Security Audit | Semgrep 290 Security & Secret Rules | 0 Vulnerabilities, 0 Leaked Secrets, Enforced HTTP Security Headers | ✅ PASS |
| **T27** | Secure Dual-Portal Authentication | Student & Nodal Officer Sign-In via `/api/auth/login` | PBKDF2 Hashing, Brute-Force Lockout (5 attempts), Immutable Audit Logging | ✅ PASS |
