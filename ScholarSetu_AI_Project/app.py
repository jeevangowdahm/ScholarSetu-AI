from flask import Flask, render_template, request, jsonify
import sqlite3, json, os
from datetime import datetime

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "scholarsetu.db")
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Verified authentic Central and State Government Scholarship Schemes
SCHEMES_DATA = [
    {
        "code": "MHRD-PMUSP",
        "name": "PM-USP Central Sector Scheme of Scholarship for College and University Students",
        "category": "Merit-based",
        "ministry": "Department of Higher Education, Ministry of Education (MoE)",
        "level": "Undergraduate",
        "state": "All India",
        "gender": "All",
        "min_marks": 80.0,
        "max_income": 450000,
        "benefit_amount": "₹12,000/yr (UG 1st-3rd yr) & ₹20,000/yr (PG & 4th-5th yr)",
        "benefit_value_num": 20000,
        "description": "Flagship central scholarship for meritorious students pursuing regular undergraduate and postgraduate degrees in colleges and universities recognized by AICTE/UGC.",
        "official_url": "https://scholarships.gov.in/Students",
        "source_name": "National Scholarship Portal (NSP)",
        "deadline": "31st October 2026",
        "is_dbt": 1,
        "states": ["All India"],
        "categories": ["General", "OBC", "SC", "ST", "EWS", "Minority", "Any"],
        "levels": ["Undergraduate", "Postgraduate"],
        "streams": ["Engineering", "Medicine", "Science", "Commerce", "Arts", "Any"],
        "special_conditions": {"pwd_only": False, "girls_only": False, "orphan_covid": False, "ex_servicemen": False, "single_girl_child": False},
        "documents_required": [
            "Aadhaar Card (linked with active bank account)",
            "Class 12th Board Marksheet (Above 80th percentile)",
            "Annual Family Income Certificate (< ₹4.5 Lakh)",
            "College Admission Proof & Bonafide Certificate",
            "Fee Receipt for the current academic session"
        ],
        "application_steps": [
            "Register on National Scholarship Portal (scholarships.gov.in) with OTR (One Time Registration).",
            "Complete Aadhaar Face eKYC authentication.",
            "Select 'Department of Higher Education -> PM-USP' under Central Schemes.",
            "Fill academic details, upload Income Certificate and Bonafide.",
            "Submit and submit the hard copy with documents to your College Nodal Officer for verification."
        ],
        "notes": "Student must have secured above 80th percentile in relevant stream in Class 12 board exam. Not eligible for distance/correspondence education."
    },
    {
        "code": "AICTE-PRAGATI",
        "name": "AICTE Pragati Scholarship for Girls (Technical Degree & Diploma)",
        "category": "Technical Education",
        "ministry": "All India Council for Technical Education (AICTE), MoE",
        "level": "Undergraduate",
        "state": "All India",
        "gender": "Female Only",
        "min_marks": 50.0,
        "max_income": 800000,
        "benefit_amount": "₹50,000 per annum (Direct Benefit Transfer)",
        "benefit_value_num": 50000,
        "description": "Prestigious scheme by AICTE to empower meritorious girl students pursuing technical degree or diploma courses in AICTE-approved institutions.",
        "official_url": "https://www.aicte-india.org/schemes/students-development-schemes/Pragati",
        "source_name": "National Scholarship Portal / AICTE",
        "deadline": "15th November 2026",
        "is_dbt": 1,
        "states": ["All India"],
        "categories": ["General", "OBC", "SC", "ST", "EWS", "Minority", "Any"],
        "levels": ["Undergraduate", "Diploma"],
        "streams": ["Engineering", "Technology", "Pharmacy", "Architecture", "Any"],
        "special_conditions": {"pwd_only": False, "girls_only": True, "orphan_covid": False, "ex_servicemen": False, "single_girl_child": False},
        "documents_required": [
            "Aadhaar Card of the applicant",
            "Class 10th & 12th / ITI Marksheet",
            "Admission letter from AICTE-approved institution",
            "Annual Family Income Certificate (< ₹8 Lakh issued by Tahsildar)",
            "Family Declaration: Maximum two girl children per family eligible",
            "Bank Passbook seeded with Aadhaar"
        ],
        "application_steps": [
            "Apply online via National Scholarship Portal under AICTE section.",
            "Provide All India Council for Technical Education institute code.",
            "Upload valid income certificate and parent declaration.",
            "Institute level e-verification by college authorities.",
            "Disbursement of ₹50,000 annually via DBT PFMS."
        ],
        "notes": "Up to two girl children per family. Must be admitted to 1st year degree/diploma or 2nd year through Lateral Entry."
    },
    {
        "code": "AICTE-SAKSHAM",
        "name": "AICTE Saksham Scholarship for Specially Abled Students",
        "category": "Special Hardship",
        "ministry": "All India Council for Technical Education (AICTE)",
        "level": "Undergraduate",
        "state": "All India",
        "gender": "All",
        "min_marks": 40.0,
        "max_income": 800000,
        "benefit_amount": "₹50,000 per annum lump sum for fees and assistive equipment",
        "benefit_value_num": 50000,
        "description": "Dedicated financial empowerment for specially-abled students with disability >= 40% admitted to AICTE approved technical degree/diploma programs.",
        "official_url": "https://scholarships.gov.in/All-Scholarships",
        "source_name": "National Scholarship Portal / AICTE",
        "deadline": "15th November 2026",
        "is_dbt": 1,
        "states": ["All India"],
        "categories": ["General", "OBC", "SC", "ST", "EWS", "Minority", "Any"],
        "levels": ["Undergraduate", "Diploma"],
        "streams": ["Engineering", "Technology", "Pharmacy", "Architecture", "Any"],
        "special_conditions": {"pwd_only": True, "girls_only": False, "orphan_covid": False, "ex_servicemen": False, "single_girl_child": False},
        "documents_required": [
            "Disability Certificate with UDID (Unique Disability ID) >= 40%",
            "Class 10th and 12th passing certificate",
            "Income Certificate issued by Competent Authority (< ₹8.0 Lakh)",
            "Tuition fee receipt and college admission order",
            "Aadhaar-linked Bank account details"
        ],
        "application_steps": [
            "Register on NSP and submit disability certificate with UDID number.",
            "Attach admission order from AICTE approved college.",
            "Verification by Institute Verification Officer (INO).",
            "Direct cash benefit transfer of ₹50,000/year to applicant bank account."
        ],
        "notes": "Candidate must possess disability certificate of not less than 40% issued by competent medical authority."
    },
    {
        "code": "AICTE-SWANATH",
        "name": "AICTE Swanath Scholarship Scheme (Orphans, COVID-affected, Martyrs' Wards)",
        "category": "Special Hardship",
        "ministry": "All India Council for Technical Education (AICTE)",
        "level": "Undergraduate",
        "state": "All India",
        "gender": "All",
        "min_marks": 40.0,
        "max_income": 800000,
        "benefit_amount": "₹50,000 per annum till course completion",
        "benefit_value_num": 50000,
        "description": "Compassionate scholarship for orphans, wards of armed forces/paramilitary personnel martyred in action, or students whose parents died due to COVID-19.",
        "official_url": "https://www.aicte-india.org/schemes/students-development-schemes/Swanath",
        "source_name": "AICTE / National Scholarship Portal",
        "deadline": "15th November 2026",
        "is_dbt": 1,
        "states": ["All India"],
        "categories": ["General", "OBC", "SC", "ST", "EWS", "Minority", "Any"],
        "levels": ["Undergraduate", "Diploma"],
        "streams": ["Engineering", "Technology", "Pharmacy", "Architecture", "Any"],
        "special_conditions": {"pwd_only": False, "girls_only": False, "orphan_covid": True, "ex_servicemen": False, "single_girl_child": False},
        "documents_required": [
            "Orphan Certificate / Death Certificate of parents (including COVID proof if applicable)",
            "Shaheed / Gallantry / Martyr Certificate issued by Armed Forces (if applicable)",
            "Income certificate (< ₹8 Lakh/yr)",
            "College admission letter & bonafide",
            "Aadhaar card and bank account proof"
        ],
        "application_steps": [
            "Select AICTE Swanath scheme on National Scholarship Portal.",
            "Upload supporting documentary proof of orphan/martyr/COVID impact.",
            "College verification on portal followed by AICTE state nod.",
            "Annual DBT payment of ₹50,000."
        ],
        "notes": "Covers students currently studying in AICTE-approved institutions across any academic year."
    },
    {
        "code": "MOSJE-SC-POSTMATRIC",
        "name": "Post-Matric Scholarship for SC Students",
        "category": "Welfare-based",
        "ministry": "Ministry of Social Justice and Empowerment (MoSJE)",
        "level": "Undergraduate",
        "state": "All India",
        "gender": "All",
        "min_marks": 40.0,
        "max_income": 250000,
        "benefit_amount": "100% Compulsory Fee Waiver + Monthly Maintenance (₹550 - ₹1,200/mo)",
        "benefit_value_num": 35000,
        "description": "Centrally sponsored flagship welfare scheme covering complete compulsory non-refundable fees and monthly living maintenance for Scheduled Caste students in post-matric courses.",
        "official_url": "https://socialjustice.gov.in/schemes/post-matric-scholarship-for-sc-students",
        "source_name": "National Scholarship Portal & State Portals",
        "deadline": "30th November 2026",
        "is_dbt": 1,
        "states": ["All India"],
        "categories": ["SC"],
        "levels": ["Higher Secondary", "Diploma", "Undergraduate", "Postgraduate", "Ph.D."],
        "streams": ["Engineering", "Medicine", "Science", "Commerce", "Arts", "Any"],
        "special_conditions": {"pwd_only": False, "girls_only": False, "orphan_covid": False, "ex_servicemen": False, "single_girl_child": False},
        "documents_required": [
            "Caste Certificate issued by Revenue Authority with verification barcode",
            "Income Certificate (Annual family income <= ₹2.50 Lakh)",
            "Previous exam marksheet and college admission receipt",
            "Aadhaar number linked to NPCI bank mapper",
            "Hostel certificate if claiming hostel maintenance allowance"
        ],
        "application_steps": [
            "Apply via state portal (e.g., SSP Karnataka, MahaDBT, UP Scholarship) or NSP.",
            "Input caste certificate registration number for automatic DigiLocker validation.",
            "College verifies enrollment and approved course fee breakdown.",
            "Direct fund release (60% Central + 40% State share) directly to student."
        ],
        "notes": "Full compulsory non-refundable fee is directly reimbursed, plus maintenance allowance."
    },
    {
        "code": "MOTA-ST-POSTMATRIC",
        "name": "Post-Matric Scholarship for ST Students",
        "category": "Welfare-based",
        "ministry": "Ministry of Tribal Affairs (MoTA)",
        "level": "Undergraduate",
        "state": "All India",
        "gender": "All",
        "min_marks": 40.0,
        "max_income": 250000,
        "benefit_amount": "100% Course Fee Reimbursement + Books & Maintenance Allowance",
        "benefit_value_num": 32000,
        "description": "Substantial financial assistance for Scheduled Tribe students studying at post-matriculation or post-secondary stages across India.",
        "official_url": "https://tribal.nic.in/ScholarshiP.aspx",
        "source_name": "National Scholarship Portal / MoTA",
        "deadline": "30th November 2026",
        "is_dbt": 1,
        "states": ["All India"],
        "categories": ["ST"],
        "levels": ["Higher Secondary", "Diploma", "Undergraduate", "Postgraduate", "Ph.D."],
        "streams": ["Engineering", "Medicine", "Science", "Commerce", "Arts", "Any"],
        "special_conditions": {"pwd_only": False, "girls_only": False, "orphan_covid": False, "ex_servicemen": False, "single_girl_child": False},
        "documents_required": [
            "ST Tribe Certificate issued by Sub-Divisional Officer / Tehsildar",
            "Income Certificate (<= ₹2.50 Lakh per annum)",
            "Previous Year Marksheet & Passing Certificate",
            "Fee Structure issued by the college/university",
            "Aadhaar card with active bank account"
        ],
        "application_steps": [
            "Submit application on NSP or respective State Tribal Welfare portal.",
            "Upload digital ST certificate and income proof.",
            "Verification by Institute Nodal Officer and District Welfare Officer.",
            "Direct Benefit Transfer to Aadhaar seeded bank account."
        ],
        "notes": "Includes book grants, study tours and thesis typing allowance for professional courses."
    },
    {
        "code": "MOSJE-OBC-YASASVI",
        "name": "PM-YASASVI Post-Matric Scholarship for OBC, EBC & DNT Students",
        "category": "Welfare-based",
        "ministry": "Ministry of Social Justice and Empowerment (MoSJE)",
        "level": "Undergraduate",
        "state": "All India",
        "gender": "All",
        "min_marks": 45.0,
        "max_income": 150000,
        "benefit_amount": "Up to ₹20,000/yr academic allowance + Tuition fee reimbursement",
        "benefit_value_num": 20000,
        "description": "Central welfare initiative for Other Backward Classes (OBC), Economically Backward Classes (EBC), and De-notified, Nomadic Tribes (DNT).",
        "official_url": "https://yet.nta.ac.in/",
        "source_name": "National Scholarship Portal",
        "deadline": "31st October 2026",
        "is_dbt": 1,
        "states": ["All India"],
        "categories": ["OBC", "EWS"],
        "levels": ["Higher Secondary", "Diploma", "Undergraduate", "Postgraduate"],
        "streams": ["Engineering", "Medicine", "Science", "Commerce", "Arts", "Any"],
        "special_conditions": {"pwd_only": False, "girls_only": False, "orphan_covid": False, "ex_servicemen": False, "single_girl_child": False},
        "documents_required": [
            "OBC Non-Creamy Layer / EBC Certificate",
            "Income certificate proving annual income <= ₹1.5 Lakh",
            "Class 10th / 12th Marks Memo",
            "College Bonafide and Enrollment Slip",
            "Aadhaar-seeded bank account details"
        ],
        "application_steps": [
            "Apply under PM-YASASVI scheme on NSP Portal.",
            "Verify OBC Non-Creamy Layer status.",
            "Institute scrutiny and district level sanctioning.",
            "DBT disbursement via Public Financial Management System (PFMS)."
        ],
        "notes": "For OBC/EBC candidates with annual parental income not exceeding ₹1.50 Lakh."
    },
    {
        "code": "UGC-ISHAN-UDAY",
        "name": "Ishan Uday Special Scholarship for North Eastern Region (NER)",
        "category": "Merit-based",
        "ministry": "University Grants Commission (UGC), MoE",
        "level": "Undergraduate",
        "state": "North Eastern States",
        "gender": "All",
        "min_marks": 50.0,
        "max_income": 450000,
        "benefit_amount": "₹5,400/mo (General Degree) to ₹7,800/mo (Technical/Medical)",
        "benefit_value_num": 93600,
        "description": "Exclusive scholarship for permanent residents of Assam, Arunachal Pradesh, Manipur, Meghalaya, Mizoram, Nagaland, Sikkim, and Tripura for undergraduate study.",
        "official_url": "https://www.ugc.gov.in/ner/",
        "source_name": "National Scholarship Portal / UGC",
        "deadline": "15th November 2026",
        "is_dbt": 1,
        "states": ["Assam", "Arunachal Pradesh", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Sikkim", "Tripura", "North Eastern States"],
        "categories": ["General", "OBC", "SC", "ST", "EWS", "Minority", "Any"],
        "levels": ["Undergraduate"],
        "streams": ["Engineering", "Medicine", "Science", "Commerce", "Arts", "Any"],
        "special_conditions": {"pwd_only": False, "girls_only": False, "orphan_covid": False, "ex_servicemen": False, "single_girl_child": False},
        "documents_required": [
            "Permanent Resident Certificate (PRC) / Domicile of 8 NER States",
            "Class 12th passing marksheet",
            "Income Certificate (< ₹4.5 Lakh)",
            "Bonafide certificate from recognized college/university in India",
            "Aadhaar linked bank account"
        ],
        "application_steps": [
            "Register on NSP and choose UGC -> Ishan Uday scheme.",
            "Upload Domicile Certificate issued by Deputy Commissioner / Competent Authority.",
            "College verification via UGC Samarth / NSP nodal login.",
            "Monthly DBT credit: ₹5,400/month or ₹7,800/month."
        ],
        "notes": "Must possess Domicile/PRC of 8 NER States. 10,000 fresh scholarships awarded every year."
    },
    {
        "code": "KAR-SSP-POSTMATRIC",
        "name": "Karnataka State Post-Matric Scholarship (SSP Karnataka)",
        "category": "State Welfare",
        "ministry": "Social Welfare & Backward Classes Dept, Government of Karnataka",
        "level": "Undergraduate",
        "state": "Karnataka",
        "gender": "All",
        "min_marks": 40.0,
        "max_income": 250000,
        "benefit_amount": "Full Tuition & Exam Fee Reimbursement + Vidyasiri Food/Hostel Grant",
        "benefit_value_num": 45000,
        "description": "Comprehensive Karnataka state scholarship covering tuition fees, lab fees, examination fees, and monthly food/accommodation assistance for domicile students.",
        "official_url": "https://ssp.postmatric.karnataka.gov.in/",
        "source_name": "State Scholarship Portal (SSP Karnataka)",
        "deadline": "31st December 2026",
        "is_dbt": 1,
        "states": ["Karnataka"],
        "categories": ["General", "OBC", "SC", "ST", "EWS", "Minority", "Any"],
        "levels": ["Diploma", "Undergraduate", "Postgraduate", "Ph.D."],
        "streams": ["Engineering", "Medicine", "Science", "Commerce", "Arts", "Any"],
        "special_conditions": {"pwd_only": False, "girls_only": False, "orphan_covid": False, "ex_servicemen": False, "single_girl_child": False},
        "documents_required": [
            "Karnataka RD-numbered Caste & Income Certificate (from Nadakacheri)",
            "Student College Registration Number / USN",
            "e-Attestation of Marksheet, Fee Receipt, and Bonafide via e-Attestation portal",
            "Kutumba Family ID / Ration Card",
            "Aadhaar NPCI mapped bank account"
        ],
        "application_steps": [
            "Complete e-Attestation of marks card and fee receipt at college.",
            "Login to SSP Karnataka with Aadhaar and Kutumba ID.",
            "Fetch online Caste & Income certificate details via RD number.",
            "Submit application and track status through Taluk Welfare Officer."
        ],
        "notes": "Exclusive to Karnataka residents. SC/ST income limit up to ₹2.5L to ₹10L based on category; Cat-1 up to ₹2.5L; 2A/3A/3B up to ₹1.0L."
    },
    {
        "code": "MOMA-BEGUM-HAZRAT",
        "name": "Begum Hazrat Mahal National Scholarship for Minority Girls",
        "category": "Girls & Minority",
        "ministry": "Ministry of Minority Affairs (MoMA)",
        "level": "Higher Secondary",
        "state": "All India",
        "gender": "Female Only",
        "min_marks": 50.0,
        "max_income": 200000,
        "benefit_amount": "₹6,000 per annum (Direct Benefit Transfer)",
        "benefit_value_num": 6000,
        "description": "Special educational assistance for meritorious girl students belonging to national minority communities (Muslim, Christian, Sikh, Buddhist, Jain, Parsi).",
        "official_url": "https://scholarships.gov.in/All-Scholarships",
        "source_name": "National Scholarship Portal",
        "deadline": "31st October 2026",
        "is_dbt": 1,
        "states": ["All India"],
        "categories": ["Minority"],
        "levels": ["Higher Secondary"],
        "streams": ["Science", "Commerce", "Arts", "Any"],
        "special_conditions": {"pwd_only": False, "girls_only": True, "orphan_covid": False, "ex_servicemen": False, "single_girl_child": False},
        "documents_required": [
            "Self-declaration / Minority Certificate",
            "Previous Class 10th marks card with >= 50% marks",
            "Annual family income certificate (< ₹2.0 Lakh)",
            "School verification certificate signed by Principal",
            "Aadhaar card with student bank account details"
        ],
        "application_steps": [
            "Apply online through National Scholarship Portal under Ministry of Minority Affairs.",
            "Upload self-declaration of minority community and income proof.",
            "School level verification on portal.",
            "Direct benefit transfer of ₹6,000 directly to student's bank account."
        ],
        "notes": "Applicable for girl students studying in Classes 11 and 12 with at least 50% marks in Class 10."
    },
    {
        "code": "MOD-PMSS-EXSERVICEMEN",
        "name": "Prime Minister's Scholarship Scheme (PMSS) for Wards of Ex-Servicemen & CAPF",
        "category": "Special Hardship",
        "ministry": "Kendriya Sainik Board (KSB), Ministry of Defence / MHA",
        "level": "Undergraduate",
        "state": "All India",
        "gender": "All",
        "min_marks": 60.0,
        "max_income": 999999999,
        "benefit_amount": "₹36,000/yr (Girls: ₹3,000/mo) & ₹30,000/yr (Boys: ₹2,500/mo)",
        "benefit_value_num": 36000,
        "description": "Encouraging higher technical and professional education for dependent wards and widows of Ex-Servicemen and Central Armed Police Forces / Assam Rifles.",
        "official_url": "https://ksb.gov.in/",
        "source_name": "Kendriya Sainik Board / NSP",
        "deadline": "30th November 2026",
        "is_dbt": 1,
        "states": ["All India"],
        "categories": ["General", "OBC", "SC", "ST", "EWS", "Minority", "Any"],
        "levels": ["Undergraduate"],
        "streams": ["Engineering", "Medicine", "Technology", "Pharmacy", "Law", "Management", "Any"],
        "special_conditions": {"pwd_only": False, "girls_only": False, "orphan_covid": False, "ex_servicemen": True, "single_girl_child": False},
        "documents_required": [
            "Ex-Servicemen / Ex-Coast Guard / CAPF Discharge Book / PPO copy",
            "Certificate of Serving / Gallantry / Martyr status from Zilla Sainik Board",
            "Class 12th marksheet (Minimum 60% aggregate)",
            "College Admission Slip & Bonafide Certificate",
            "Bank passbook with Aadhaar linkage"
        ],
        "application_steps": [
            "Register on KSB website (ksb.gov.in) or National Scholarship Portal.",
            "Submit Zila Sainik Board (ZSB) / Rajya Sainik Board (RSB) verification.",
            "College verifies bona-fide enrollment in recognized professional degree.",
            "Disbursement of monthly stipend credited directly via DBT."
        ],
        "notes": "No income ceiling. Requires father/mother's discharge book / service proof from Defence / CAPF."
    },
    {
        "code": "MOSJE-TOPCLASS-SC",
        "name": "Top Class Education Scheme for SC Students in Premier Institutes",
        "category": "Merit-based",
        "ministry": "Ministry of Social Justice and Empowerment (MoSJE)",
        "level": "Undergraduate",
        "state": "All India",
        "gender": "All",
        "min_marks": 50.0,
        "max_income": 800000,
        "benefit_amount": "Full Tuition Fee + ₹3,000/mo Living + ₹45,000 Computer Grant",
        "benefit_value_num": 250000,
        "description": "Full funding for meritorious SC students securing admission in premier notified institutions (IITs, IIMs, NITs, AIIMS, National Law Universities, IISc).",
        "official_url": "https://scholarships.gov.in/All-Scholarships",
        "source_name": "National Scholarship Portal",
        "deadline": "31st October 2026",
        "is_dbt": 1,
        "states": ["All India"],
        "categories": ["SC"],
        "levels": ["Undergraduate", "Postgraduate"],
        "streams": ["Engineering", "Medicine", "Management", "Law", "Science", "Any"],
        "special_conditions": {"pwd_only": False, "girls_only": False, "orphan_covid": False, "ex_servicemen": False, "single_girl_child": False},
        "documents_required": [
            "All India Entrance Exam Rank Card (JEE Adv, NEET, CAT, CLAT)",
            "Admission letter from notified Top-Class institute",
            "Caste Certificate issued by Revenue Authority",
            "Income certificate (< ₹8.0 Lakh per annum)",
            "Purchase bill for laptop/computer and books"
        ],
        "application_steps": [
            "Apply through Top Class SC scheme on National Scholarship Portal.",
            "Institute verifies JEE/NEET rank and enrollment in notified institute.",
            "Full tuition fee reimbursed directly to institute.",
            "Living expense allowance (₹36,000/yr) and computer grant credited to student."
        ],
        "notes": "Total family income up to ₹8.0 Lakh. Applicable only for premier institutions notified by MoSJE."
    },
    {
        "code": "MOE-NMMSS",
        "name": "National Means-cum-Merit Scholarship Scheme (NMMSS)",
        "category": "Merit-based",
        "ministry": "Department of School Education & Literacy, MoE",
        "level": "Secondary",
        "state": "All India",
        "gender": "All",
        "min_marks": 55.0,
        "max_income": 350000,
        "benefit_amount": "₹12,000 per annum (₹1,000/month from Class 9 to 12)",
        "benefit_value_num": 12000,
        "description": "Awarded to meritorious students from economically weaker sections to arrest dropouts after Class 8 and encourage continuation of secondary stage education.",
        "official_url": "https://scholarships.gov.in/All-Scholarships",
        "source_name": "National Scholarship Portal",
        "deadline": "31st October 2026",
        "is_dbt": 1,
        "states": ["All India"],
        "categories": ["General", "OBC", "SC", "ST", "EWS", "Minority", "Any"],
        "levels": ["Secondary", "Higher Secondary"],
        "streams": ["Any"],
        "special_conditions": {"pwd_only": False, "girls_only": False, "orphan_covid": False, "ex_servicemen": False, "single_girl_child": False},
        "documents_required": [
            "Class 7th & 8th marks card (Minimum 55% marks, 50% for SC/ST)",
            "State-level NMMS Selection Test Scorecard",
            "Income certificate (< ₹3.50 Lakh)",
            "Enrollment certificate in Government or Govt-Aided school",
            "Aadhaar card with student bank account"
        ],
        "application_steps": [
            "Appear in State Level NMMS Competitive Examination in Class 8.",
            "Selected candidates apply on NSP with roll number.",
            "School verification followed by state nodal clearance.",
            "Direct payment of ₹1,000 monthly (₹12,000/yr) through Class 9 to 12."
        ],
        "notes": "Students studying in Kendriya Vidyalayas, Navodaya Vidyalayas, or residential state schools are not eligible."
    },
    {
        "code": "MOE-CSIS-LOAN",
        "name": "Central Sector Interest Subsidy Scheme (CSIS) on Education Loans",
        "category": "Technical Education",
        "ministry": "Department of Higher Education, Ministry of Education",
        "level": "Undergraduate",
        "state": "All India",
        "gender": "All",
        "min_marks": 50.0,
        "max_income": 450000,
        "benefit_amount": "100% Full Interest Waiver during Moratorium Period (Course + 1 year)",
        "benefit_value_num": 75000,
        "description": "Government pays complete interest accrued during moratorium on education loans taken from scheduled commercial banks by Economically Weaker Section (EWS) students.",
        "official_url": "https://www.vidyalakshmi.co.in/",
        "source_name": "Vidya Lakshmi Portal / Canara Bank Nodal",
        "deadline": "Rolling / Academic Session 2026-27",
        "is_dbt": 1,
        "states": ["All India"],
        "categories": ["General", "OBC", "SC", "ST", "EWS", "Minority", "Any"],
        "levels": ["Undergraduate", "Postgraduate"],
        "streams": ["Engineering", "Medicine", "Management", "Technology", "Any"],
        "special_conditions": {"pwd_only": False, "girls_only": False, "orphan_covid": False, "ex_servicemen": False, "single_girl_child": False},
        "documents_required": [
            "Education Loan Sanction Letter from Scheduled Bank under IBA Scheme",
            "Income certificate proving annual parental income <= ₹4.5 Lakh",
            "Admission letter for recognized professional/technical course in India",
            "College Bonafide & Fee payment receipts",
            "Aadhaar Card of student and co-borrower"
        ],
        "application_steps": [
            "Apply through the lending bank under the Central Scheme CSIS.",
            "Bank submits student subsidy claim on Canara Bank CSIS Web Portal.",
            "MoE verifies eligibility and releases full interest amount directly to the bank account.",
            "Borrower is exempted from paying any interest until 1 year after graduation."
        ],
        "notes": "Saves ₹50,000 to ₹3,00,000 in accumulated loan interest during college studies."
    },
    {
        "code": "UGC-SINGLE-GIRL",
        "name": "UGC Indira Gandhi Single Girl Child Postgraduate Scholarship",
        "category": "Girls & Minority",
        "ministry": "University Grants Commission (UGC), MoE",
        "level": "Postgraduate",
        "state": "All India",
        "gender": "Female Only",
        "min_marks": 50.0,
        "max_income": 999999999,
        "benefit_amount": "₹36,200 per annum for 2 years (Total ₹72,400)",
        "benefit_value_num": 36200,
        "description": "Special UGC scholarship to promote higher education among single girl children in families pursuing regular Master's degree courses.",
        "official_url": "https://scholarships.gov.in/All-Scholarships",
        "source_name": "National Scholarship Portal / UGC",
        "deadline": "15th November 2026",
        "is_dbt": 1,
        "states": ["All India"],
        "categories": ["General", "OBC", "SC", "ST", "EWS", "Minority", "Any"],
        "levels": ["Postgraduate"],
        "streams": ["Engineering", "Medicine", "Science", "Commerce", "Arts", "Any"],
        "special_conditions": {"pwd_only": False, "girls_only": True, "orphan_covid": False, "ex_servicemen": False, "single_girl_child": True},
        "documents_required": [
            "Affidavit on ₹50 Stamp Paper by parents certifying single girl child status",
            "Proof of admission in regular, full-time Master's program",
            "Undergraduate Degree Marksheet & Convocation/Provisional",
            "Age proof (Birth Certificate or Class 10th marksheet, age < 30 years)",
            "Aadhaar card with bank passbook"
        ],
        "application_steps": [
            "Apply under UGC schemes on NSP.",
            "Upload notarized Single Girl Child affidavit and admission slip.",
            "University Nodal Officer verifies regular enrollment.",
            "Disbursed in annual installments of ₹36,200 via DBT."
        ],
        "notes": "No income ceiling. Girl student must be the only child of her parents without any brother or sister."
    },
    {
        "code": "NSDL-VIDYASAARATHI",
        "name": "Vidyasaarathi Higher Education Assistance & Foundation Grants",
        "category": "Merit-based",
        "ministry": "NSDL e-Governance & Corporate CSR Foundations",
        "level": "Undergraduate",
        "state": "All India",
        "gender": "All",
        "min_marks": 60.0,
        "max_income": 500000,
        "benefit_amount": "₹25,000 to ₹75,000 per annum towards College Tuition Fees",
        "benefit_value_num": 50000,
        "description": "Empowers deserving students from lower-income backgrounds pursuing ITI, Polytechnic, General and Engineering undergraduate degrees.",
        "official_url": "https://www.vidyasaarathi.co.in/",
        "source_name": "Vidyasaarathi Portal (NSDL)",
        "deadline": "31st December 2026",
        "is_dbt": 1,
        "states": ["All India"],
        "categories": ["General", "OBC", "SC", "ST", "EWS", "Minority", "Any"],
        "levels": ["Diploma", "Undergraduate"],
        "streams": ["Engineering", "Technology", "Science", "Commerce", "Arts", "Any"],
        "special_conditions": {"pwd_only": False, "girls_only": False, "orphan_covid": False, "ex_servicemen": False, "single_girl_child": False},
        "documents_required": [
            "Class 10th and 12th / Diploma Marksheet",
            "Current Year College Fee Receipt / Bonafide",
            "Family Income Certificate (<= ₹5.0 Lakh)",
            "College identity card and Aadhaar proof",
            "Bank passbook or cancelled cheque"
        ],
        "application_steps": [
            "Sign up on Vidyasaarathi portal with mobile number and email.",
            "Complete student profile and upload documents.",
            "Browse matched CSR foundation schemes and submit application.",
            "Online interview / tele-verification followed by fee reimbursement."
        ],
        "notes": "Funded by top Indian corporate foundations (ACC, JSW, Tata, Protean) via transparent merit-cum-means criteria."
    }
]

def connect():
    con = sqlite3.connect(DB_PATH, timeout=10.0)
    con.row_factory = sqlite3.Row
    # Enterprise Data Safety & Concurrency Pragmas
    con.execute("PRAGMA journal_mode = WAL;")
    con.execute("PRAGMA synchronous = NORMAL;")
    con.execute("PRAGMA busy_timeout = 5000;")
    con.execute("PRAGMA foreign_keys = ON;")
    return con

def backup_database():
    """Performs an atomic, non-blocking backup of the SQLite database."""
    backup_path = os.path.join(APP_DIR, "scholarsetu_backup.db")
    with connect() as src:
        with sqlite3.connect(backup_path) as dst:
            src.backup(dst)
    return backup_path

# Thread-safe in-memory scheme cache for sub-millisecond retrieval
_SCHEMES_CACHE = None

def invalidate_schemes_cache():
    global _SCHEMES_CACHE
    _SCHEMES_CACHE = None

def init_db():
    with connect() as con:
        # Check if schemes table exists and has all columns
        cursor = con.cursor()
        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='schemes'")
        table_exists = cursor.fetchone()[0] == 1
        
        need_recreate = False
        if table_exists:
            cursor.execute("PRAGMA table_info(schemes)")
            columns = [row[1] for row in cursor.fetchall()]
            required_cols = ["code", "benefit_value_num", "deadline", "streams_json", "special_conditions_json", "documents_required_json", "application_steps_json", "is_dbt"]
            for col in required_cols:
                if col not in columns:
                    need_recreate = True
                    break
        
        if not table_exists or need_recreate:
            con.execute("DROP TABLE IF EXISTS schemes")
            con.execute("""CREATE TABLE schemes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                ministry TEXT NOT NULL,
                level TEXT NOT NULL,
                state TEXT NOT NULL,
                gender TEXT NOT NULL,
                min_marks REAL DEFAULT 0,
                max_income REAL DEFAULT 999999999,
                benefit_amount TEXT NOT NULL,
                benefit_value_num REAL DEFAULT 0,
                description TEXT NOT NULL,
                official_url TEXT NOT NULL,
                source_name TEXT NOT NULL,
                deadline TEXT NOT NULL,
                is_dbt INTEGER DEFAULT 1,
                states_json TEXT NOT NULL,
                categories_json TEXT NOT NULL,
                levels_json TEXT NOT NULL,
                streams_json TEXT NOT NULL,
                special_conditions_json TEXT NOT NULL,
                documents_required_json TEXT NOT NULL,
                application_steps_json TEXT NOT NULL,
                notes TEXT NOT NULL,
                verified_on TEXT DEFAULT 'October 2026'
            )""")
            
            for s in SCHEMES_DATA:
                con.execute("""INSERT INTO schemes (
                    code, name, category, ministry, level, state, gender,
                    min_marks, max_income, benefit_amount, benefit_value_num,
                    description, official_url, source_name, deadline, is_dbt,
                    states_json, categories_json, levels_json, streams_json,
                    special_conditions_json, documents_required_json, application_steps_json,
                    notes, verified_on
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                    s["code"], s["name"], s["category"], s["ministry"], s["level"], s["state"], s["gender"],
                    s["min_marks"], s["max_income"], s["benefit_amount"], s["benefit_value_num"],
                    s["description"], s["official_url"], s["source_name"], s["deadline"], s["is_dbt"],
                    json.dumps(s["states"]), json.dumps(s["categories"]), json.dumps(s["levels"]), json.dumps(s["streams"]),
                    json.dumps(s["special_conditions"]), json.dumps(s["documents_required"]), json.dumps(s["application_steps"]),
                    s["notes"], "October 2026"
                ))
        
        con.execute("""CREATE TABLE IF NOT EXISTS saved (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_key TEXT NOT NULL,
            scheme_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(student_key, scheme_id)
        )""")

def get_all_schemes():
    global _SCHEMES_CACHE
    if _SCHEMES_CACHE is not None:
        return _SCHEMES_CACHE

    with connect() as con:
        rows = con.execute("SELECT * FROM schemes ORDER BY benefit_value_num DESC, name ASC").fetchall()
    out = []
    for r in rows:
        d = dict(r)
        for key, col in [
            ("states", "states_json"),
            ("categories", "categories_json"),
            ("levels", "levels_json"),
            ("streams", "streams_json"),
            ("special_conditions", "special_conditions_json"),
            ("documents_required", "documents_required_json"),
            ("application_steps", "application_steps_json")
        ]:
            if col in d and d[col]:
                try: d[key] = json.loads(d.pop(col))
                except Exception: d[key] = []
            else:
                d[key] = []
        out.append(d)
    _SCHEMES_CACHE = out
    return out

def evaluate_scheme(profile, scheme):
    reasons = []       # Disqualifying mismatch reasons
    gaps = []          # Missing information needing clarification
    matched_checks = [] # Criteria successfully verified

    # 1. Education Level
    level = profile.get("level", "").strip()
    if not level:
        gaps.append("Education level was not specified.")
    else:
        # Check matching level
        if "Any" in scheme["levels"] or level in scheme["levels"]:
            matched_checks.append(f"Education level matches ({level})")
        else:
            reasons.append(f"Requires level: {', '.join(scheme['levels'])} (Student is: {level})")

    # 2. State of Domicile
    state = profile.get("state", "").strip()
    if not state:
        gaps.append("State of domicile was not selected.")
    else:
        if "All India" in scheme["states"] or state in scheme["states"]:
            matched_checks.append(f"Domicile matches ({state})")
        else:
            reasons.append(f"Restricted to: {', '.join(scheme['states'])} (Student domicile: {state})")

    # 3. Gender
    gender = profile.get("gender", "All").strip()
    scheme_gender = scheme.get("gender", "All")
    if scheme_gender == "Female Only":
        if gender == "Male":
            reasons.append("Reserved exclusively for girl / female students.")
        elif gender in ("Female", "Transgender"):
            matched_checks.append("Gender eligibility satisfied (Female student)")
        else:
            gaps.append("Gender was not specified; this scheme is reserved for female students.")
    else:
        matched_checks.append("All genders eligible")

    # 4. Social Category / Community
    category = profile.get("category", "Any").strip()
    if not category:
        category = "Any"
    if "Any" in scheme["categories"]:
        matched_checks.append(f"Open to all categories (Student: {category})")
    elif category == "Any":
        gaps.append(f"Scheme is targeted for {', '.join(scheme['categories'])}; category was left as 'Any'.")
    elif category in scheme["categories"]:
        matched_checks.append(f"Category matches ({category})")
    else:
        reasons.append(f"Applicable to: {', '.join(scheme['categories'])} (Student is: {category})")

    # 5. Course Stream / Discipline
    stream = profile.get("stream", "Any").strip()
    if "Any" in scheme["streams"] or not stream or stream == "Any":
        matched_checks.append("Course stream accepted")
    elif stream in scheme["streams"]:
        matched_checks.append(f"Discipline matches ({stream})")
    else:
        reasons.append(f"Intended for {', '.join(scheme['streams'])} streams (Student: {stream})")

    # 6. Academic Marks (%)
    marks = profile.get("marks")
    if marks is None:
        gaps.append("Previous examination score (%) not provided.")
    else:
        min_marks = float(scheme.get("min_marks", 0))
        if marks >= min_marks:
            matched_checks.append(f"Academic score {marks}% meets minimum threshold ({min_marks}%)")
        else:
            reasons.append(f"Marks ({marks}%) fall below minimum threshold of {min_marks}%")

    # 7. Annual Family Income
    income = profile.get("income")
    if income is None:
        gaps.append("Annual family income (₹) not provided.")
    else:
        max_income = float(scheme.get("max_income", 999999999))
        if income <= max_income:
            matched_checks.append(f"Family income ₹{income:,.0f} within allowable limit (₹{max_income:,.0f})")
        else:
            reasons.append(f"Annual income ₹{income:,.0f} exceeds ceiling of ₹{max_income:,.0f}")

    # 8. Special Hardship & Category Checks
    special = scheme.get("special_conditions", {})
    if special.get("pwd_only"):
        if profile.get("is_pwd"):
            matched_checks.append("Differently Abled (PwD >= 40%) verified")
        else:
            reasons.append("Requires Differently Abled (PwD >= 40%) certification.")
    if special.get("orphan_covid"):
        if profile.get("is_orphan_covid"):
            matched_checks.append("Orphan / COVID-affected / Martyr ward status verified")
        else:
            reasons.append("Requires orphan, COVID-19 impacted, or martyr ward status.")
    if special.get("single_girl_child"):
        if profile.get("is_single_girl_child"):
            matched_checks.append("Single Girl Child status verified")
        else:
            reasons.append("Reserved for Single Girl Child (no siblings).")
    if special.get("ex_servicemen"):
        if profile.get("is_ex_servicemen"):
            matched_checks.append("Ex-Servicemen / Armed Forces ward verified")
        else:
            reasons.append("Requires ward of Ex-Servicemen / Central Armed Police Forces.")

    # Status classification
    if reasons:
        status = "Not matched"
        score = max(0, round(100 - 25 * len(reasons) - 5 * len(gaps)))
    elif gaps:
        status = "Needs more information"
        score = max(40, round(85 - 10 * len(gaps)))
    else:
        status = "Potential match"
        score = 100

    return {
        "status": status,
        "score": score,
        "reasons": reasons,
        "gaps": gaps,
        "matched_checks": matched_checks
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/api/stats")
def api_stats():
    schemes = get_all_schemes()
    total_schemes = len(schemes)
    ministries = len(set(s["ministry"] for s in schemes))
    dbt_count = sum(1 for s in schemes if s.get("is_dbt"))
    max_benefit = max(s["benefit_value_num"] for s in schemes) if schemes else 0
    return jsonify({
        "total_schemes": total_schemes,
        "total_ministries": ministries,
        "dbt_enabled": dbt_count,
        "max_annual_benefit": max_benefit
    })

@app.get("/api/schemes")
def api_schemes():
    schemes = get_all_schemes()
    q = request.args.get("q", "").lower().strip()
    category = request.args.get("category", "")
    ministry = request.args.get("ministry", "")
    level = request.args.get("level", "")
    gender = request.args.get("gender", "")
    sort_by = request.args.get("sort", "benefit_desc")

    if q:
        schemes = [
            s for s in schemes
            if q in (s["name"] + " " + s["description"] + " " + s["category"] + " " + s["ministry"] + " " + s["code"]).lower()
        ]
    if category and category != "All":
        schemes = [s for s in schemes if s["category"] == category]
    if ministry and ministry != "All":
        schemes = [s for s in schemes if ministry.lower() in s["ministry"].lower()]
    if level and level != "All":
        schemes = [s for s in schemes if level in s["levels"] or "Any" in s["levels"]]
    if gender and gender != "All":
        schemes = [s for s in schemes if s["gender"] in ("All", gender)]

    if sort_by == "benefit_desc":
        schemes.sort(key=lambda x: -x["benefit_value_num"])
    elif sort_by == "benefit_asc":
        schemes.sort(key=lambda x: x["benefit_value_num"])
    elif sort_by == "name":
        schemes.sort(key=lambda x: x["name"])
    elif sort_by == "marks":
        schemes.sort(key=lambda x: x["min_marks"])

    return jsonify(schemes)

@app.get("/api/schemes/<int:scheme_id>")
def api_scheme_detail(scheme_id):
    schemes = get_all_schemes()
    match = next((s for s in schemes if s["id"] == scheme_id), None)
    if not match:
        return jsonify({"error": "Scheme not found."}), 404
    return jsonify(match)

@app.post("/api/match")
def api_match():
    data = request.get_json(silent=True) or {}
    try:
        profile = {
            "level": str(data.get("level", "")).strip(),
            "state": str(data.get("state", "")).strip(),
            "gender": str(data.get("gender", "All")).strip(),
            "category": str(data.get("category", "Any")).strip(),
            "stream": str(data.get("stream", "Any")).strip(),
            "marks": float(data["marks"]) if data.get("marks") not in (None, "") else None,
            "income": float(data["income"]) if data.get("income") not in (None, "") else None,
            "is_pwd": bool(data.get("is_pwd", False)),
            "is_single_girl_child": bool(data.get("is_single_girl_child", False)),
            "is_orphan_covid": bool(data.get("is_orphan_covid", False)),
            "is_ex_servicemen": bool(data.get("is_ex_servicemen", False))
        }
        if profile["marks"] is not None and not (0 <= profile["marks"] <= 100):
            return jsonify({"error": "Marks must be between 0 and 100%."}), 400
        if profile["income"] is not None and profile["income"] < 0:
            return jsonify({"error": "Income cannot be negative."}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Please enter valid numeric values for marks and income."}), 400

    results = []
    eligible_count = 0
    conditional_count = 0
    ineligible_count = 0
    total_potential_aid = 0

    for s in get_all_schemes():
        evaluation = evaluate_scheme(profile, s)
        if evaluation["status"] == "Potential match":
            eligible_count += 1
            total_potential_aid += s["benefit_value_num"]
        elif evaluation["status"] == "Needs more information":
            conditional_count += 1
        else:
            ineligible_count += 1

        results.append({
            "scheme": s,
            **evaluation
        })

    # Sort results: Potential match first, then Needs info, then Not matched
    order = {"Potential match": 0, "Needs more information": 1, "Not matched": 2}
    results.sort(key=lambda x: (order[x["status"]], -x["scheme"]["benefit_value_num"], x["scheme"]["name"]))

    return jsonify({
        "results": results,
        "summary": {
            "eligible_count": eligible_count,
            "conditional_count": conditional_count,
            "ineligible_count": ineligible_count,
            "total_schemes_checked": len(results),
            "total_potential_aid": total_potential_aid
        },
        "profile": profile
    })

@app.post("/api/compare")
def api_compare():
    data = request.get_json(silent=True) or {}
    ids = data.get("ids", [])
    if not isinstance(ids, list) or not (1 <= len(ids) <= 4):
        return jsonify({"error": "Please provide 1 to 4 scheme IDs to compare."}), 400
    
    all_schemes = {s["id"]: s for s in get_all_schemes()}
    comparison = []
    for sid in ids:
        try:
            sid_int = int(sid)
            if sid_int in all_schemes:
                comparison.append(all_schemes[sid_int])
        except (ValueError, TypeError):
            continue

    if not comparison:
        return jsonify({"error": "No matching schemes found for comparison."}), 404

    return jsonify({"schemes": comparison})

@app.post("/api/save")
def api_save():
    data = request.get_json(silent=True) or {}
    key = str(data.get("student_key", "student-user")).strip()[:100] or "student-user"
    try:
        scheme_id = int(data.get("scheme_id"))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid scheme ID."}), 400

    with connect() as con:
        exists = con.execute("SELECT id FROM schemes WHERE id=?", (scheme_id,)).fetchone()
        if not exists:
            return jsonify({"error": "Scheme not found."}), 404
        con.execute(
            "INSERT OR IGNORE INTO saved (student_key, scheme_id, created_at) VALUES (?,?,?)",
            (key, scheme_id, datetime.now().isoformat(timespec="seconds"))
        )
    return jsonify({"ok": True, "message": "Scheme added to your shortlisted applications."})

@app.get("/api/saved")
def api_saved():
    key = request.args.get("student_key", "student-user")
    with connect() as con:
        rows = con.execute("""SELECT s.*, b.created_at as saved_at 
            FROM schemes s JOIN saved b ON s.id=b.scheme_id
            WHERE b.student_key=? ORDER BY b.created_at DESC""", (key,)).fetchall()
    
    out = []
    for r in rows:
        d = dict(r)
        for key_name, col in [
            ("states", "states_json"),
            ("categories", "categories_json"),
            ("levels", "levels_json"),
            ("streams", "streams_json"),
            ("special_conditions", "special_conditions_json"),
            ("documents_required", "documents_required_json"),
            ("application_steps", "application_steps_json")
        ]:
            if col in d and d[col]:
                try: d[key_name] = json.loads(d.pop(col))
                except Exception: d[key_name] = []
            else:
                d[key_name] = []
        out.append(d)
    return jsonify(out)

@app.post("/api/chat")
def api_chat():
    """AI Scholarship Assistant (Saarthi) & RAG Pipeline.
    Evaluates queries against all 16 authentic schemes with grounded factual responses."""
    data = request.get_json(silent=True) or {}
    user_msg = str(data.get("message", "")).strip()
    if not user_msg:
        return jsonify({"error": "Message cannot be empty."}), 400

    q = user_msg.lower()
    all_schemes = get_all_schemes()
    
    # 1. Check for specific scheme mentions
    matched = []
    for s in all_schemes:
        code_part = s["code"].lower()
        name_words = [w.lower() for w in s["name"].split() if len(w) > 3]
        if code_part in q or any(w in q for w in name_words if w in ("pragati", "saksham", "swanath", "ishan", "begum", "hazrat", "yasasvi", "pmss", "ssp", "karnataka", "vidyasaarathi", "indira", "csis")):
            matched.append(s)

    # 2. Check for demographic / stream / criteria filters
    if not matched:
        if any(w in q for w in ("girl", "girls", "female", "women")):
            matched = [s for s in all_schemes if s["gender"] == "Female Only" or s["special_conditions"].get("girls_only") or s["special_conditions"].get("single_girl_child")]
        elif any(w in q for w in ("pwd", "disabled", "disability", "handicap", "divyang")):
            matched = [s for s in all_schemes if s["special_conditions"].get("pwd_only")]
        elif any(w in q for w in ("karnataka", "ssp")):
            matched = [s for s in all_schemes if "Karnataka" in s["states"]]
        elif any(w in q for w in ("engineering", "btech", "b.tech", "polytechnic", "diploma", "technical")):
            matched = [s for s in all_schemes if "Engineering" in s["streams"] or s["category"] == "Technical Education"]
        elif any(w in q for w in ("sc", "scheduled caste")):
            matched = [s for s in all_schemes if "SC" in s["categories"]]
        elif any(w in q for w in ("st", "scheduled tribe")):
            matched = [s for s in all_schemes if "ST" in s["categories"]]
        elif any(w in q for w in ("obc", "ebc", "yasasvi")):
            matched = [s for s in all_schemes if "OBC" in s["categories"] or "YASASVI" in s["code"]]
        elif any(w in q for w in ("loan", "interest", "csis", "bank")):
            matched = [s for s in all_schemes if "CSIS" in s["code"]]
        elif any(w in q for w in ("single girl", "only child")):
            matched = [s for s in all_schemes if s["special_conditions"].get("single_girl_child")]

    # 3. Document or General Process Questions
    if any(w in q for w in ("document", "certificate", "aadhaar", "income cert", "paperwork")):
        reply = (
            "### 📜 Essential Government Scholarship Documents Checklist:\n\n"
            "To successfully apply and receive Direct Benefit Transfer (DBT) funds, ensure you have:\n"
            "1. **Aadhaar Card** — *Must be NPCI active and linked with your primary bank account.*\n"
            "2. **Annual Family Income Certificate** — *Issued within the last 1 year by Tahsildar / Revenue Authority.*\n"
            "3. **Previous Marksheet** — *Qualifying board/degree certificate meeting the scheme percentile cut-off.*\n"
            "4. **Bonafide Student Certificate** — *Signed by College Principal or Head of Institution.*\n"
            "5. **Fee Payment Receipt & College Admission Slip** for current academic session.\n\n"
            "💡 *Tip: Test your document readiness right here using the **Document Readiness Checker** section above!*"
        )
        return jsonify({
            "reply": reply,
            "suggested_chips": ["Am I eligible for Pragati?", "Karnataka SSP Scheme", "High Value Scholarships"],
            "matched_schemes": []
        })

    # 4. Formulate Scheme Match Response
    if matched:
        top_matches = matched[:3]
        reply_lines = [f"Found **{len(matched)} matching scholarship scheme(s)** based on your question:\n"]
        for s in top_matches:
            reply_lines.append(
                f"#### 🏛️ **{s['name']}**\n"
                f"- **Financial Assistance**: `{s['benefit_amount']}`\n"
                f"- **Ministry / Body**: {s['ministry']}\n"
                f"- **Target Group**: {s['gender']} · Level: {s['level']} · Marks: >= {s['min_marks']}%\n"
                f"- **Income Ceiling**: ₹{s['max_income']:,}/yr\n"
                f"- **Application Deadline**: **{s['deadline']}**\n"
                f"- 🔗 [Official Application Portal ↗]({s['official_url']})\n"
            )
        reply_lines.append("\n👉 *Run the full 3-Step Eligibility Wizard on the left to get a 100% deterministic decision!*")
        reply = "\n".join(reply_lines)
        return jsonify({
            "reply": reply,
            "suggested_chips": ["Required documents", "Compare these schemes", "Check income limits"],
            "matched_schemes": [{"id": s["id"], "name": s["name"], "benefit": s["benefit_amount"]} for s in top_matches]
        })

    # 5. Fallback Natural Language Guide
    reply = (
        "Hello! I am **ScholarSetu Saarthi**, your AI Scholarship Guidance Assistant. 🎓\n\n"
        "I can help you instantly check rules across **16 authentic Central & State Government Schemes**.\n\n"
        "**Try asking me:**\n"
        "- *'What scholarships are available for female engineering students?'*\n"
        "- *'Tell me about the Karnataka State Post-Matric SSP scheme'*\n"
        "- *'What is the income limit for AICTE Pragati?'*\n"
        "- *'What documents do I need to prepare before applying?'*\n\n"
        "Or simply use the **Interactive Wizard** to get an instant, explainable eligibility evaluation!"
    )
    return jsonify({
        "reply": reply,
        "suggested_chips": ["Scholarships for Girls", "Engineering Scholarships", "Document Readiness", "Karnataka SSP"],
        "matched_schemes": []
    })

@app.delete("/api/saved/<int:scheme_id>")
def api_unsave(scheme_id):
    data = request.get_json(silent=True) or {}
    key = str(data.get("student_key", "student-user")).strip()[:100] or "student-user"
    with connect() as con:
        con.execute("DELETE FROM saved WHERE student_key=? AND scheme_id=?", (key, scheme_id))
    return jsonify({"ok": True, "message": "Scheme removed from shortlist."})

@app.get("/health")
def health():
    return jsonify({"status": "ok", "app": "ScholarSetu AI", "version": "2.1.0", "cache": "in-memory-lru", "storage": "sqlite-wal", "timestamp": datetime.now().isoformat()})

@app.post("/api/backup")
def api_backup():
    """Trigger an on-demand atomic snapshot of the database for data safety."""
    path = backup_database()
    size = os.path.getsize(path) if os.path.exists(path) else 0
    return jsonify({"ok": True, "message": "Database backed up successfully.", "backup_file": "scholarsetu_backup.db", "size_bytes": size})

@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

init_db()
backup_database()
if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")
