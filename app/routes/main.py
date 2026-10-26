import json
import datetime
import re

from flask import Blueprint, Response, current_app, flash, jsonify, redirect, render_template, request, send_file, session, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from app.extensions import db
from app.models import Appointment, Consultation, MedicalProfile, Medication
from app.services.ai import (
    analysis_summary,
    ask_gemini,
    generate_followup_questions,
    match_disease,
    normalize_analysis_payload,
    parse_ai_analysis,
    scan_emergency_red_flags,
    validate_symptoms,
)
from app.services.hospital import build_hospital_map
from app.services.pdf import render_consultation_pdf_bytes
from app.services import pharmacy_catalog


main_bp = Blueprint("main", __name__)

DOCTOR_DEPARTMENTS = [
    {
        "id": "physician",
        "name": "General Physician",
        "tagline": "Fever, cold, routine checkup & general wellness",
        "icon": "stethoscope",
        "badge": "5 Specialists",
        "about_title": "What is a General Physician?",
        "about_desc": "General Physicians are primary care medical doctors who diagnose and treat acute everyday ailments (such as viral fevers, seasonal infections, respiratory issues) and oversee long-term wellness like diabetes and blood pressure.",
        "symptoms": ["Viral Fever, Cold & Flu", "Fatigue, Weakness & Chills", "Stomach Infection & Vomiting", "Routine Executive Health Checkup"],
        "when_to_see": "Consult first when you have early or undiagnosed symptoms, need prescription refills, or want a full physical examination.",
        "doctors": [
            {
                "id": "dr-ananya",
                "name": "Dr. Ananya Mehta, MD",
                "specialty": "Senior General Physician",
                "department": "General Physician",
                "experience": "14+ yrs exp",
                "rating": "4.9",
                "reviews": "1,420",
                "image": "images/doctor_ananya.jpg",
                "availability": "Slots Open Today",
                "badge": "Clinical Lead",
                "fee": "₹600",
                "default_notes": "General clinical checkup, review symptoms, discuss lab results."
            },
            {
                "id": "dr-rajesh",
                "name": "Dr. Rajesh Sharma, MD",
                "specialty": "Senior Consultant Physician",
                "department": "General Physician",
                "experience": "20+ yrs exp",
                "rating": "4.9",
                "reviews": "2,100",
                "image": "images/doctor_rajesh.jpg",
                "availability": "Slots Open Tomorrow",
                "badge": "Chief of Medicine",
                "fee": "₹650",
                "default_notes": "Routine health checkup, physical examination, medication review."
            },
            {
                "id": "dr-suresh",
                "name": "Dr. Suresh Kulkarni, MBBS, MD",
                "specialty": "Consultant Family Physician",
                "department": "General Physician",
                "experience": "12+ yrs exp",
                "rating": "4.8",
                "reviews": "940",
                "image": "images/doctor_arvind.jpg",
                "availability": "Available Today",
                "badge": "Family Medicine",
                "fee": "₹550",
                "default_notes": "Fever, infection treatment, seasonal illness and vitals checkup."
            },
            {
                "id": "dr-arvind-physician",
                "name": "Dr. Arvind Swamy, MD",
                "specialty": "Internal Medicine Specialist",
                "department": "General Physician",
                "experience": "16+ yrs exp",
                "rating": "4.9",
                "reviews": "1,180",
                "image": "images/doctor_arvind.jpg",
                "availability": "Slots Open Today",
                "badge": "Internal Medicine",
                "fee": "₹700",
                "default_notes": "Metabolic disorder review, chronic hypertension checkup, blood panel follow-up."
            },
            {
                "id": "dr-sneha-physician",
                "name": "Dr. Sneha Iyer, MBBS, DNB",
                "specialty": "General Physician & Wellness",
                "department": "General Physician",
                "experience": "8+ yrs exp",
                "rating": "4.8",
                "reviews": "620",
                "image": "images/doctor_sneha.jpg",
                "availability": "Available Today",
                "badge": "Preventive Care",
                "fee": "₹500",
                "default_notes": "Acute seasonal illness, allergy cough, general dietary and vitals review."
            }
        ]
    },
    {
        "id": "cardiologist",
        "name": "Cardiologist",
        "tagline": "Blood pressure, ECG, chest pain & heart health",
        "icon": "heart",
        "badge": "3 Specialists",
        "about_title": "What is a Cardiologist?",
        "about_desc": "Cardiologists are specialized physicians who prevent, diagnose, and treat disorders of the cardiovascular system, including high blood pressure, cholesterol blocks, palpitations, and heart disease.",
        "symptoms": ["Chest Heaviness or Discomfort", "High Blood Pressure (Hypertension)", "Palpitations & Irregular Pulse", "Shortness of Breath on Exertion"],
        "when_to_see": "Consult when experiencing unusual chest pressure, chronic hypertension, abnormal ECG findings, or high cardiovascular risk.",
        "doctors": [
            {
                "id": "dr-alok-cardio",
                "name": "Dr. Alok Sharma, DM",
                "specialty": "Chief Interventional Cardiologist",
                "department": "Cardiologist",
                "experience": "18+ yrs exp",
                "rating": "4.9",
                "reviews": "1,350",
                "image": "images/doctor_alistair.jpg",
                "availability": "Available Tomorrow",
                "badge": "Heart Specialist",
                "fee": "₹900",
                "default_notes": "Cardiovascular consultation, blood pressure review, ECG evaluation."
            },
            {
                "id": "dr-sanjay-cardio",
                "name": "Dr. Sanjay Bhatt, MD, DM",
                "specialty": "Senior Consultant Cardiologist",
                "department": "Cardiologist",
                "experience": "16+ yrs exp",
                "rating": "4.9",
                "reviews": "880",
                "image": "images/doctor_arvind.jpg",
                "availability": "Available Today",
                "badge": "Cardiac Care",
                "fee": "₹850",
                "default_notes": "Chest discomfort review, lipid profile check, hypertension monitoring."
            },
            {
                "id": "dr-ritu-cardio",
                "name": "Dr. Ritu Kapoor, DNB",
                "specialty": "Consultant Clinical Cardiologist",
                "department": "Cardiologist",
                "experience": "10+ yrs exp",
                "rating": "4.8",
                "reviews": "720",
                "image": "images/doctor_sneha.jpg",
                "availability": "Slots Open Tomorrow",
                "badge": "Preventive Care",
                "fee": "₹800",
                "default_notes": "Heart health screening, stress assessment, routine cardiac checkup."
            }
        ]
    },
    {
        "id": "dermatologist",
        "name": "Dermatologist",
        "tagline": "Skin allergies, acne, rashes & cosmetic care",
        "icon": "sparkles",
        "badge": "4 Specialists",
        "about_title": "What is a Dermatologist?",
        "about_desc": "Dermatologists are clinical specialists in diseases of the skin, hair, and nails. They treat conditions ranging from stubborn acne, fungal infections, eczema, to hair loss and aesthetic dermatology.",
        "symptoms": ["Stubborn Acne & Face Breakouts", "Severe Hair Loss & Dandruff", "Skin Rashes, Itching & Allergy", "Fungal Patches & Eczema"],
        "when_to_see": "Consult if over-the-counter creams don't resolve rashes, for chronic acne flares, or sudden hair thinning.",
        "doctors": [
            {
                "id": "dr-priya",
                "name": "Dr. Priya Nair, MD",
                "specialty": "Consultant Dermatologist",
                "department": "Dermatologist",
                "experience": "11+ yrs exp",
                "rating": "4.8",
                "reviews": "1,150",
                "image": "images/doctor_priya.jpg",
                "availability": "Slots Open Today",
                "badge": "Skin & Allergy",
                "fee": "₹700",
                "default_notes": "Skin rash evaluation, allergic irritation review, acne treatment."
            },
            {
                "id": "dr-sneha-derma",
                "name": "Dr. Sneha Iyer, DVD, MD",
                "specialty": "Consultant Cosmetologist & Derm",
                "department": "Dermatologist",
                "experience": "9+ yrs exp",
                "rating": "4.9",
                "reviews": "860",
                "image": "images/doctor_sneha.jpg",
                "availability": "Slots Open Tomorrow",
                "badge": "Aesthetic Skin",
                "fee": "₹750",
                "default_notes": "Acne scars, hair loss treatment, eczema, allergy patch consultation."
            },
            {
                "id": "dr-rohan-derma",
                "name": "Dr. Rohan Verma, MD",
                "specialty": "Consultant Dermatologist",
                "department": "Dermatologist",
                "experience": "8+ yrs exp",
                "rating": "4.8",
                "reviews": "640",
                "image": "images/doctor_rajesh.jpg",
                "availability": "Available Today",
                "badge": "Skin Specialist",
                "fee": "₹650",
                "default_notes": "Fungal infections, pigmentation, psoriasis, general skin checkup."
            },
            {
                "id": "dr-meera-derma",
                "name": "Dr. Meera Nambiar, MD",
                "specialty": "Senior Skin & Trichology Specialist",
                "department": "Dermatologist",
                "experience": "15+ yrs exp",
                "rating": "4.9",
                "reviews": "1,290",
                "image": "images/doctor_ananya.jpg",
                "availability": "Slots Open Today",
                "badge": "Trichology Lead",
                "fee": "₹800",
                "default_notes": "Hair loss evaluation, scalp therapy, chronic dermatitis management."
            }
        ]
    },
    {
        "id": "pediatrician",
        "name": "Pediatrician",
        "tagline": "Child wellness, growth, immunizations & newborn care",
        "icon": "smile",
        "badge": "3 Specialists",
        "about_title": "What is a Pediatrician?",
        "about_desc": "Pediatricians specialize in the physical, behavioral, and emotional health of babies, children, and teenagers. They manage developmental milestones, immunizations, and childhood infections.",
        "symptoms": ["High Fever & Cough in Children", "Vaccination Schedule & Milestones", "Newborn Feeding & Colic Issues", "Childhood Allergies & Asthma"],
        "when_to_see": "Consult for routine pediatric immunization charts, sudden high fever in infants, or growth and nutritional concerns.",
        "doctors": [
            {
                "id": "dr-pooja-ped",
                "name": "Dr. Pooja Singhal, MD",
                "specialty": "Senior Pediatrician & Neonatologist",
                "department": "Pediatrician",
                "experience": "13+ yrs exp",
                "rating": "4.9",
                "reviews": "1,280",
                "image": "images/doctor_ananya.jpg",
                "availability": "Slots Open Today",
                "badge": "Child Specialist",
                "fee": "₹600",
                "default_notes": "Childhood fever, vaccinations, growth & dietary wellness."
            },
            {
                "id": "dr-amit-ped",
                "name": "Dr. Amit Joshi, DCH, DNB",
                "specialty": "Consultant Pediatrician",
                "department": "Pediatrician",
                "experience": "15+ yrs exp",
                "rating": "4.9",
                "reviews": "990",
                "image": "images/doctor_arvind.jpg",
                "availability": "Available Tomorrow",
                "badge": "Pediatric Care",
                "fee": "₹650",
                "default_notes": "Pediatric allergies, viral fever, newborn development checkup."
            },
            {
                "id": "dr-meenakshi-ped",
                "name": "Dr. Meenakshi Sundaram, MD",
                "specialty": "Associate Consultant Child Health",
                "department": "Pediatrician",
                "experience": "10+ yrs exp",
                "rating": "4.8",
                "reviews": "810",
                "image": "images/doctor_sneha.jpg",
                "availability": "Slots Open Today",
                "badge": "Immunization Lead",
                "fee": "₹600",
                "default_notes": "Infant care, vaccine review, childhood nutritional guidance."
            }
        ]
    },
    {
        "id": "orthopedic",
        "name": "Orthopedic",
        "tagline": "Joints, spine, fractures, arthritis & sports injuries",
        "icon": "shield",
        "badge": "4 Specialists",
        "about_title": "What is an Orthopedic Specialist?",
        "about_desc": "Orthopedic surgeons diagnose and treat disorders of the bones, joints, ligaments, tendons, and spine. They help restore mobility, manage arthritis, heal fractures, and treat sports injuries.",
        "symptoms": ["Knee, Hip or Shoulder Joint Pain", "Lower Back Pain & Sciatica", "Fractures, Sprains & Sports Injuries", "Stiffness & Walking Discomfort"],
        "when_to_see": "Consult when joint pain restricts your everyday movement, following a physical fall/sprain, or for long-standing arthritis.",
        "doctors": [
            {
                "id": "dr-vikram-ortho",
                "name": "Dr. Vikram Malhotra, MS",
                "specialty": "Senior Orthopedic & Joint Surgeon",
                "department": "Orthopedic",
                "experience": "19+ yrs exp",
                "rating": "4.9",
                "reviews": "1,520",
                "image": "images/doctor_marcus.jpg",
                "availability": "Available Today",
                "badge": "Joint Specialist",
                "fee": "₹850",
                "default_notes": "Knee & hip pain, arthritis consultation, joint stiffness check."
            },
            {
                "id": "dr-harish-ortho",
                "name": "Dr. Harish Chandra, D.Ortho, MS",
                "specialty": "Consultant Spine & Trauma Specialist",
                "department": "Orthopedic",
                "experience": "16+ yrs exp",
                "rating": "4.8",
                "reviews": "940",
                "image": "images/doctor_rajesh.jpg",
                "availability": "Slots Open Tomorrow",
                "badge": "Spine & Sports",
                "fee": "₹800",
                "default_notes": "Lower back pain, sciatica, sports injury rehabilitation review."
            },
            {
                "id": "dr-manoj-ortho",
                "name": "Dr. Manoj Deshmukh, MS, M.Ch",
                "specialty": "Orthopedic Consultant",
                "department": "Orthopedic",
                "experience": "12+ yrs exp",
                "rating": "4.8",
                "reviews": "760",
                "image": "images/doctor_arvind.jpg",
                "availability": "Available Today",
                "badge": "Bone & Fracture",
                "fee": "₹750",
                "default_notes": "Fracture healing follow-up, tendonitis, shoulder joint assessment."
            },
            {
                "id": "dr-pradeep-ortho",
                "name": "Dr. Pradeep Verma, MS",
                "specialty": "Joint Replacement Specialist",
                "department": "Orthopedic",
                "experience": "14+ yrs exp",
                "rating": "4.9",
                "reviews": "1,110",
                "image": "images/doctor_alistair.jpg",
                "availability": "Slots Open Tomorrow",
                "badge": "Arthritis Care",
                "fee": "₹850",
                "default_notes": "Osteoarthritis assessment, knee mobility evaluation, joint injections."
            }
        ]
    },
    {
        "id": "gynecologist",
        "name": "Gynecologist",
        "tagline": "Women's wellness, pregnancy care & hormonal health",
        "icon": "user-check",
        "badge": "3 Specialists",
        "about_title": "What is a Gynecologist?",
        "about_desc": "Gynecologists and Obstetricians provide comprehensive medical care for female reproductive health, pregnancy trimesters, hormonal disorders (PCOS/PCOD), and preventive wellness.",
        "symptoms": ["PCOS / PCOD Hormonal Imbalances", "Irregular or Painful Periods", "Pregnancy Routine Checkup", "Pelvic Pain & Preconception Advice"],
        "when_to_see": "Consult for irregular menstrual cycles, pregnancy planning, reproductive wellness screening, or pelvic pain.",
        "doctors": [
            {
                "id": "dr-sunita-gyn",
                "name": "Dr. Sunita Agarwal, MD, DGO",
                "specialty": "Senior Obstetrician & Gynecologist",
                "department": "Gynecologist",
                "experience": "21+ yrs exp",
                "rating": "4.9",
                "reviews": "2,300",
                "image": "images/doctor_ananya.jpg",
                "availability": "Slots Open Today",
                "badge": "Women's Care Lead",
                "fee": "₹750",
                "default_notes": "Antenatal checkup, menstrual irregularity, PCOS/PCOD guidance."
            },
            {
                "id": "dr-kavita-gyn",
                "name": "Dr. Kavita Reddy, MS",
                "specialty": "Consultant Laparoscopic Gynecologist",
                "department": "Gynecologist",
                "experience": "14+ yrs exp",
                "rating": "4.9",
                "reviews": "1,140",
                "image": "images/doctor_sneha.jpg",
                "availability": "Available Tomorrow",
                "badge": "Fertility & Care",
                "fee": "₹700",
                "default_notes": "Hormonal imbalances, pelvic pain, fertility and preconception check."
            },
            {
                "id": "dr-shalini-gyn",
                "name": "Dr. Shalini Saxena, DNB",
                "specialty": "Consultant Gynecologist",
                "department": "Gynecologist",
                "experience": "11+ yrs exp",
                "rating": "4.8",
                "reviews": "890",
                "image": "images/doctor_priya.jpg",
                "availability": "Slots Open Today",
                "badge": "Well Woman Care",
                "fee": "₹650",
                "default_notes": "Routine pelvic examination, post-partum recovery checkup."
            }
        ]
    },
    {
        "id": "neurologist",
        "name": "Neurologist",
        "tagline": "Migraine, brain, nerve disorders & spine health",
        "icon": "activity",
        "badge": "2 Specialists",
        "about_title": "What is a Neurologist?",
        "about_desc": "Neurologists are medical specialists who manage disorders of the brain, spinal cord, and peripheral nervous system, diagnosing headaches, neurological nerve pains, and seizures.",
        "symptoms": ["Chronic Migraines & Headaches", "Nerve Numbness & Tingling Hands/Feet", "Tremors & Loss of Balance", "Memory Lapses & Dizziness"],
        "when_to_see": "Consult for persistent severe headaches, shooting nerve sensations, sudden loss of coordination, or seizure symptoms.",
        "doctors": [
            {
                "id": "dr-alok-neuro",
                "name": "Dr. Alok Gupta, DM",
                "specialty": "Chief Neurologist",
                "department": "Neurologist",
                "experience": "20+ yrs exp",
                "rating": "4.9",
                "reviews": "1,450",
                "image": "images/doctor_alistair.jpg",
                "availability": "Available Tomorrow",
                "badge": "Neuro Specialist",
                "fee": "₹950",
                "default_notes": "Migraine evaluation, epilepsy management, neuropathy review."
            },
            {
                "id": "dr-deepa-neuro",
                "name": "Dr. Deepa Nambiar, MD, DM",
                "specialty": "Consultant Neurologist",
                "department": "Neurologist",
                "experience": "14+ yrs exp",
                "rating": "4.9",
                "reviews": "910",
                "image": "images/doctor_sneha.jpg",
                "availability": "Available Today",
                "badge": "Brain Care",
                "fee": "₹900",
                "default_notes": "Memory complaints, persistent headaches, nerve numbness."
            }
        ]
    },
    {
        "id": "pulmonologist",
        "name": "Pulmonologist",
        "tagline": "Asthma, breathing issues, chronic cough & lungs",
        "icon": "wind",
        "badge": "2 Specialists",
        "about_title": "What is a Pulmonologist?",
        "about_desc": "Pulmonologists specialize in respiratory care, diagnosing illnesses of the lungs and bronchial tubes, including persistent bronchitis, asthma attacks, pneumonia, and sleep apnea.",
        "symptoms": ["Chronic Cough Lasting > 2 Weeks", "Wheezing & Difficulty Breathing", "Chest Congestion & Pollution Allergies", "Snoring & Sleep Apnea"],
        "when_to_see": "Consult when you feel breathlessness during light activity, have an unexplained long-term cough, or recurring chest congestion.",
        "doctors": [
            {
                "id": "dr-vivek-pulmo",
                "name": "Dr. Vivek Mehra, MD",
                "specialty": "Chief Pulmonologist & Sleep Specialist",
                "department": "Pulmonologist",
                "experience": "17+ yrs exp",
                "rating": "4.9",
                "reviews": "1,180",
                "image": "images/doctor_marcus.jpg",
                "availability": "Slots Open Today",
                "badge": "Chest & Lungs",
                "fee": "₹800",
                "default_notes": "Asthma review, chronic cough follow-up, breathing assessment."
            },
            {
                "id": "dr-aarti-pulmo",
                "name": "Dr. Aarti Mishra, DTCD, MD",
                "specialty": "Senior Consultant Chest Physician",
                "department": "Pulmonologist",
                "experience": "13+ yrs exp",
                "rating": "4.8",
                "reviews": "850",
                "image": "images/doctor_priya.jpg",
                "availability": "Available Tomorrow",
                "badge": "Respiratory Care",
                "fee": "₹750",
                "default_notes": "Persistent bronchitis, chest congestion, lung function check."
            }
        ]
    }
]

# Flattened list for backwards compatibility
AVAILABLE_DOCTORS = [doc for dept in DOCTOR_DEPARTMENTS for doc in dept["doctors"]]





def build_analysis_prompt(patient_name, symptoms, followup_responses=None, medical_profile=None):
    prompt = [
        f"Patient: {patient_name}.",
        f"Symptoms: {symptoms}.",
    ]
    if medical_profile:
        allergies = medical_profile.get("allergies")
        chronic = medical_profile.get("chronic_conditions")
        if allergies:
            prompt.append(f"Patient Known Drug Allergies (CRITICAL: DO NOT prescribe these or related classes): {allergies}.")
        if chronic:
            prompt.append(f"Patient Known Chronic Medical Conditions: {chronic}.")

    if followup_responses:
        prompt.append(f"Follow-up responses: {followup_responses}.")
    prompt.append(
        "You are an expert clinical physician AI. Analyze the patient presentation and the follow-up responses carefully. "
        "Pay special attention to follow-up responses to disambiguate the true root cause. "
        "Return valid JSON only with no markdown fences or comments. "
        "Use these keys exactly: presenting_complaint, differential_diagnoses, investigations, "
        "treatment, medications, precautions, and disclaimer. "
        "Keep the response concise and dashboard-friendly. "
        "Use one short sentence for presenting_complaint and disclaimer. "
        "For differential_diagnoses, investigations, treatment, medications, and precautions, "
        "prefer arrays of 2 to 5 concise bullet items with each item under 28 words. "
        "Ensure medications are safe, avoiding any known patient drug allergies or contraindications."
    )
    return " ".join(prompt)


def save_consultation(user_id, symptoms, followup_responses, analysis):
    normalized = normalize_analysis_payload(analysis)
    if not normalized.get("red_flag_alert"):
        scan = scan_emergency_red_flags(symptoms)
        if scan.get("is_emergency"):
            normalized["red_flag_alert"] = scan

    consultation = Consultation(
        user_id=user_id,
        symptoms=symptoms,
        followup_responses=json.dumps(followup_responses) if followup_responses else None,
        diagnosis=json.dumps(normalized)
    )
    db.session.add(consultation)
    db.session.commit()
    return consultation


def consultation_card_context(limit=4):
    consultations = (
        Consultation.query
        .filter_by(user_id=current_user.id)
        .order_by(Consultation.timestamp.desc())
        .limit(limit)
        .all()
    )
    items = []
    for consultation in consultations:
        analysis = normalize_analysis_payload(json.loads(consultation.diagnosis))
        items.append({
            "id": consultation.id,
            "timestamp": consultation.timestamp,
            "symptoms": consultation.symptoms,
            "summary": analysis_summary(analysis.get("differential_diagnoses"))
        })
    return items


@main_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("landing.html")


@main_bp.route("/health")
def health():
    from app import get_system_status

    status = get_system_status()
    return jsonify(status), 200 if status["database"]["healthy"] else 503


@main_bp.route("/robots.txt")
def robots():
    site_url = current_app.config.get("SITE_URL") or request.url_root.rstrip("/")
    content = "\n".join([
        "User-agent: *",
        "Allow: /",
        "Allow: /hospital_locator",
        "Allow: /hospital-locator",
        "Allow: /medications",
        "Disallow: /dashboard",
        "Disallow: /history",
        "Disallow: /appointment",
        "Disallow: /reminders",
        "Disallow: /settings",
        "Disallow: /api/",
        f"Sitemap: {site_url}/sitemap.xml",
    ])
    return Response(content, mimetype="text/plain")


@main_bp.route("/sitemap.xml")
def sitemap():
    today = datetime.date.today().isoformat()
    items = [
        {"loc": url_for("main.home", _external=True), "priority": "1.0", "changefreq": "daily", "lastmod": today},
        {"loc": url_for("main.hospital_locator", _external=True), "priority": "0.9", "changefreq": "weekly", "lastmod": today},
        {"loc": url_for("main.medications", _external=True), "priority": "0.9", "changefreq": "weekly", "lastmod": today},
        {"loc": url_for("auth.login", _external=True), "priority": "0.5", "changefreq": "monthly", "lastmod": today},
        {"loc": url_for("auth.register", _external=True), "priority": "0.6", "changefreq": "monthly", "lastmod": today},
    ]
    xml = render_template("sitemap.xml", items=items, urls=[it["loc"] for it in items])
    return Response(xml, mimetype="application/xml")


@main_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        symptoms = (request.form.get("symptoms") or "").strip()
        validation_error = validate_symptoms(symptoms)
        if validation_error:
            return jsonify({"success": False, "error": validation_error}), 400

        session["symptoms"] = symptoms
        user_gender = getattr(current_user.medical_profile, "gender", None) if getattr(current_user, "medical_profile", None) else None
        try:
            matched_disease = match_disease(symptoms, gender=user_gender)
        except TypeError:
            matched_disease = match_disease(symptoms)
        session["matched_disease"] = matched_disease

        if matched_disease:
            return jsonify({"redirect": url_for("main.followup")})

        try:
            med_prof = current_user.medical_profile.to_dict() if current_user.medical_profile else None
            analysis = parse_ai_analysis(
                ask_gemini(build_analysis_prompt(current_user.display_name, symptoms, None, med_prof), current_app.config)
            )
            save_consultation(current_user.id, symptoms, None, analysis)
            html = render_template("consultations/result_partial.html", analysis=analysis)
            return jsonify({"success": True, "html": html})
        except Exception as exc:
            current_app.logger.error("Dashboard analysis failed: %s", exc)
            return jsonify({"success": False, "error": str(exc)}), 502

    consultation_count = Consultation.query.filter_by(user_id=current_user.id).count()
    appointment_count = Appointment.query.filter_by(user_id=current_user.id).count()
    active_days = (
        db.session.query(func.count(func.distinct(func.date(Consultation.timestamp))))
        .filter(Consultation.user_id == current_user.id)
        .scalar()
    ) or 0
    next_appointment = (
        Appointment.query
        .filter(
            Appointment.user_id == current_user.id,
            Appointment.date >= datetime.date.today()
        )
        .order_by(Appointment.date.asc(), Appointment.time.asc())
        .first()
    )
    latest_consultation = (
        Consultation.query
        .filter_by(user_id=current_user.id)
        .order_by(Consultation.timestamp.desc())
        .first()
    )
    activity_score = min(
        20
        + (consultation_count * 15)
        + (appointment_count * 12)
        + (10 if latest_consultation else 0)
        + (8 if next_appointment else 0),
        100,
    )

    workspace_highlights = [
        {
            "title": "Saved consultations",
            "value": (
                f"{consultation_count} record{'s' if consultation_count != 1 else ''} saved"
                if consultation_count else
                "Your consultation history will appear here"
            ),
            "tone": "success" if consultation_count else "neutral",
        },
        {
            "title": "Appointments",
            "value": (
                f"Next visit on {next_appointment.date.strftime('%d %b %Y')}"
                if next_appointment else
                "Add your next doctor visit anytime"
            ),
            "tone": "success" if next_appointment else "neutral",
        },
        {
            "title": "Reports",
            "value": "PDF downloads are ready for saved consultations",
            "tone": "success",
        },
    ]

    return render_template(
        "consultations/dashboard.html",
        consultation_count=consultation_count,
        appointment_count=appointment_count,
        active_days=active_days,
        recent_consultations=consultation_card_context(),
        next_appointment=next_appointment,
        latest_consultation=latest_consultation,
        workspace_highlights=workspace_highlights,
        activity_score=activity_score,
    )


@main_bp.route("/followup", methods=["GET", "POST"])
@login_required
def followup():
    symptoms = session.get("symptoms")
    matched_disease = session.get("matched_disease")

    if not symptoms:
        flash("Start from the consultation dashboard first.", "warning")
        return redirect(url_for("main.dashboard"))

    questions = generate_followup_questions(symptoms, matched_disease)

    if request.method == "POST":
        answers = []
        for index, question in enumerate(questions):
            answer = (request.form.get(f"response{index}") or "").strip()
            answers.append({"question": question, "answer": answer})

        additional_notes = (request.form.get("additional_notes") or "").strip()
        if additional_notes:
            answers.append({
                "question": "Additional Patient Observations & Notes",
                "answer": additional_notes
            })

        try:
            med_prof = current_user.medical_profile.to_dict() if current_user.medical_profile else None
            analysis = parse_ai_analysis(
                ask_gemini(build_analysis_prompt(current_user.display_name, symptoms, answers, med_prof), current_app.config)
            )
            save_consultation(current_user.id, symptoms, answers, analysis)
            return render_template("consultations/result_page.html", analysis=analysis)
        except Exception as exc:
            current_app.logger.error("Follow-up analysis failed: %s", exc)
            flash(str(exc), "danger")
            return redirect(url_for("main.followup"))

    return render_template(
        "consultations/followup.html",
        disease_name="your symptoms",
        questions=questions
    )


@main_bp.route("/history")
@login_required
def history():
    consultations = (
        Consultation.query
        .filter_by(user_id=current_user.id)
        .order_by(Consultation.timestamp.desc())
        .all()
    )

    date_totals = {}
    history_items = []
    for consultation in consultations:
        analysis = normalize_analysis_payload(json.loads(consultation.diagnosis))
        day = consultation.timestamp.strftime("%Y-%m-%d")
        date_totals[day] = date_totals.get(day, 0) + 1
        history_items.append({
            "id": consultation.id,
            "timestamp": consultation.timestamp,
            "symptoms": consultation.symptoms,
            "analysis": analysis,
            "summary": analysis_summary(analysis.get("differential_diagnoses"))
        })

    chart_labels = sorted(date_totals.keys())
    chart_data = [date_totals[label] for label in chart_labels]
    total_consultations = len(history_items)
    most_recent = history_items[0]["timestamp"] if history_items else None
    most_active_day = max(date_totals, key=date_totals.get) if date_totals else None

    return render_template(
        "consultations/history.html",
        consultations=history_items,
        chart_labels=chart_labels,
        chart_data=chart_data,
        total_consultations=total_consultations,
        most_recent=most_recent,
        most_active_day=most_active_day,
    )


@main_bp.route("/delete_consultation/<int:consultation_id>", methods=["POST"])
@login_required
def delete_consultation(consultation_id):
    consultation = Consultation.query.filter_by(id=consultation_id, user_id=current_user.id).first_or_404()
    db.session.delete(consultation)
    db.session.commit()
    flash("Consultation record deleted successfully.", "success")
    return redirect(url_for("main.history"))


@main_bp.route("/download_pdf/<int:consultation_id>")
@login_required
def download_pdf(consultation_id):
    consultation = Consultation.query.filter_by(id=consultation_id, user_id=current_user.id).first_or_404()
    try:
        pdf_buffer = render_consultation_pdf_bytes(consultation, current_user.display_name)
        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"consultation_report_{consultation.timestamp.strftime('%Y%m%d')}.pdf"
        )
    except Exception as exc:
        flash(str(exc), "warning")
        return redirect(url_for("main.history"))


@main_bp.route("/hospital_locator")
@main_bp.route("/hospital-locator")
def hospital_locator():
    location_input = (request.args.get("location") or request.args.get("city") or "").strip()
    category = (request.args.get("category") or "all").strip().lower()
    q = (request.args.get("q") or "").strip()
    sort = (request.args.get("sort") or "relevance").strip().lower()

    # Intelligent Query Separation:
    # If user typed "Hospitals in Sitapur" or "Eye clinic in Varanasi" or "Dentist near Alwar"
    match = re.search(r'\b(?:in|near|at|around)\s+([a-zA-Z\s]{2,40})$', q, re.IGNORECASE)
    if match and not location_input:
        location_input = match.group(1).strip()
        q = q[:match.start()].strip()
    elif not location_input and q:
        from app.services.india_geo import INDIAN_LOCATIONS_DB
        if q.lower() in INDIAN_LOCATIONS_DB:
            location_input = q
            q = ""

    if not location_input:
        location_input = "Jaipur"

    try:
        locator_result = build_hospital_map(location_input, category_filter=category, search_query=q, sort_by=sort)
        map_html = locator_result["map_html"]
        hospital_cards = locator_result["hospitals"]
        total_count = locator_result.get("total_count", len(hospital_cards))
        filtered_count = locator_result.get("filtered_count", len(hospital_cards))
        city = locator_result.get("city_name", location_input.title())
        city_display = locator_result.get("resolved_location", f"{city}")
    except Exception as exc:
        current_app.logger.error("Hospital locator failed: %s", exc)
        flash("Could not load hospital map right now.", "danger")
        return redirect(url_for("main.dashboard"))

    return render_template(
        "hospital/index.html",
        city=city,
        location=location_input,
        city_display=city_display,
        category=category,
        q=q,
        sort=sort,
        map_html=map_html,
        hospital_cards=hospital_cards,
        total_count=total_count,
        filtered_count=filtered_count,
    )


@main_bp.route("/appointment", methods=["GET", "POST"])
@login_required
def appointment():
    appointments = (
        Appointment.query
        .filter_by(user_id=current_user.id)
        .order_by(Appointment.date.asc(), Appointment.time.asc())
        .all()
    )

    if request.method == "POST":
        date_str = request.form.get("date")
        time = (request.form.get("time") or "").strip()
        doctor = (request.form.get("doctor") or "").strip()
        notes = (request.form.get("notes") or "").strip()

        if not doctor or len(doctor) > 100:
            flash("Enter a valid doctor name under 100 characters.", "warning")
            return redirect(url_for("main.appointment"))

        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Use the date format YYYY-MM-DD.", "danger")
            return redirect(url_for("main.appointment"))

        if date_obj < datetime.date.today():
            flash("Appointment date cannot be in the past.", "warning")
            return redirect(url_for("main.appointment"))

        new_appointment = Appointment(
            date=date_obj,
            time=time,
            doctor=doctor,
            notes=notes,
            user_id=current_user.id
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash("Appointment scheduled successfully.", "success")
        return redirect(url_for("main.appointment"))

    upcoming_count = len([appointment for appointment in appointments if appointment.date >= datetime.date.today()])
    next_appointment = next(
        (appointment for appointment in appointments if appointment.date >= datetime.date.today()),
        None,
    )
    return render_template(
        "appointments/index.html",
        appointments=appointments,
        today_iso=datetime.date.today().isoformat(),
        upcoming_count=upcoming_count,
        next_appointment=next_appointment,
        available_doctors=AVAILABLE_DOCTORS,
        doctor_departments=DOCTOR_DEPARTMENTS,
    )


@main_bp.route("/delete_appointment/<int:appointment_id>", methods=["POST"])
@login_required
def delete_appointment(appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id, user_id=current_user.id).first_or_404()
    db.session.delete(appointment)
    db.session.commit()
    flash("Appointment cancelled successfully.", "success")
    return redirect(url_for("main.appointment"))


@main_bp.route("/appointment/<int:appointment_id>/calendar.ics")
@main_bp.route("/appointments/<int:appointment_id>/calendar.ics")
@login_required
def download_appointment_ics(appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id, user_id=current_user.id).first_or_404()

    start_dt = datetime.datetime.combine(appointment.date, datetime.time(9, 0))
    time_str = (appointment.time or "").strip()
    try:
        if ":" in time_str:
            parts = time_str.split(":")
            hour = int(parts[0])
            minute = int(parts[1][:2])
            start_dt = datetime.datetime.combine(appointment.date, datetime.time(hour, minute))
    except Exception:
        pass

    end_dt = start_dt + datetime.timedelta(hours=1)
    dtstamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dtstart = start_dt.strftime("%Y%m%dT%H%M%S")
    dtend = end_dt.strftime("%Y%m%dT%H%M%S")

    clean_notes = (appointment.notes or "Scheduled clinical consultation").replace("\n", " ").replace("\r", "")
    clean_doctor = (appointment.doctor or "Consultant").replace("\n", " ").replace("\r", "")

    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Care Cliniq//Medical Appointment Calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "BEGIN:VEVENT",
        f"UID:carecliniq-appt-{appointment.id}@{request.host}",
        f"DTSTAMP:{dtstamp}",
        f"DTSTART:{dtstart}",
        f"DTEND:{dtend}",
        f"SUMMARY:Medical Visit: {clean_doctor}",
        f"DESCRIPTION:{clean_notes} (Patient: {current_user.display_name})",
        "LOCATION:Clinical Practice / Hospital",
        "STATUS:CONFIRMED",
        "END:VEVENT",
        "END:VCALENDAR",
    ]
    ics_body = "\r\n".join(ics_lines) + "\r\n"

    return Response(
        ics_body,
        mimetype="text/calendar",
        headers={
            "Content-Disposition": f'attachment; filename="appointment_{appointment.date.strftime("%Y%m%d")}_{appointment.id}.ics"',
            "Content-Type": "text/calendar; charset=utf-8",
        },
    )


@main_bp.route("/medications", methods=["GET", "POST"])
def medications():
    if request.method == "POST":
        if not current_user.is_authenticated:
            flash("Please sign in to save medications to your personal schedule.", "info")
            return redirect(url_for("auth.login", next=url_for("main.medications")))

        name = (request.form.get("name") or "").strip()
        dosage = (request.form.get("dosage") or "").strip()
        frequency = (request.form.get("frequency") or "").strip()
        instructions = (request.form.get("instructions") or "").strip()

        if not name or len(name) > 120:
            flash("Medication name is required and must be under 120 characters.", "warning")
            return redirect(url_for("main.medications"))

        med = Medication(
            user_id=current_user.id,
            name=name,
            dosage=dosage[:60],
            frequency=frequency[:60],
            instructions=instructions,
            is_active=True,
        )
        db.session.add(med)
        db.session.commit()
        flash(f"Medication '{name}' added to your schedule.", "success")
        return redirect(url_for("main.medications"))

    if current_user.is_authenticated:
        user_medications = (
            Medication.query
            .filter_by(user_id=current_user.id)
            .order_by(Medication.is_active.desc(), Medication.created_at.desc())
            .all()
        )
    else:
        user_medications = []

    # Catalog & search parameters
    category = request.args.get("category", "all")
    search_q = request.args.get("q", "").strip()
    rx_filter = request.args.get("rx", "all")
    sort_by = request.args.get("sort", "popularity")

    catalog_products = pharmacy_catalog.get_all_products(
        category=category,
        search=search_q,
        rx_filter=rx_filter if rx_filter in ["otc", "rx"] else None,
        sort_by=sort_by
    )
    categories = pharmacy_catalog.get_categories()
    category_stats = pharmacy_catalog.get_category_stats()

    return render_template(
        "medications/index.html",
        medications=user_medications,
        catalog_products=catalog_products,
        categories=categories,
        category_stats=category_stats,
        selected_category=category,
        search_query=search_q,
        rx_filter=rx_filter,
        sort_by=sort_by,
        total_count=len(catalog_products)
    )


@main_bp.route("/medications/admin", methods=["GET", "POST"])
@login_required
def pharmacy_admin():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        salt = (request.form.get("salt") or "").strip()
        category_id = (request.form.get("category_id") or "pain-fever").strip()
        dosage_form = (request.form.get("dosage_form") or "Tablet").strip()
        pack_size = (request.form.get("pack_size") or "10 tablets").strip()
        mrp = float(request.form.get("mrp") or 100)
        price = float(request.form.get("price") or mrp)
        manufacturer = (request.form.get("manufacturer") or "Care Cliniq").strip()
        indications = (request.form.get("indications") or "").strip()
        is_rx_required = bool(request.form.get("is_rx_required"))
        is_bestseller = bool(request.form.get("is_bestseller"))
        stock = int(request.form.get("stock") or 100)

        if not name or not salt:
            flash("Product name and composition/salt are required.", "warning")
            return redirect(url_for("main.pharmacy_admin"))

        pharmacy_catalog.add_product({
            "name": name,
            "salt": salt,
            "category_id": category_id,
            "dosage_form": dosage_form,
            "pack_size": pack_size,
            "mrp": mrp,
            "price": price,
            "manufacturer": manufacturer,
            "indications": indications,
            "is_rx_required": is_rx_required,
            "is_bestseller": is_bestseller,
            "stock": stock
        })
        flash(f"Successfully added '{name}' to the pharmacy catalog.", "success")
        return redirect(url_for("main.pharmacy_admin"))

    category_filter = request.args.get("category", "all")
    search_q = request.args.get("q", "").strip()

    products = pharmacy_catalog.get_all_products(category=category_filter, search=search_q)
    categories = pharmacy_catalog.get_categories()
    category_stats = pharmacy_catalog.get_category_stats()

    return render_template(
        "medications/admin.html",
        products=products,
        categories=categories,
        category_stats=category_stats,
        selected_category=category_filter,
        search_query=search_q,
        total_products=len(products)
    )


@main_bp.route("/medications/admin/edit/<int:product_id>", methods=["POST"])
@login_required
def pharmacy_admin_edit(product_id):
    name = (request.form.get("name") or "").strip()
    salt = (request.form.get("salt") or "").strip()
    category_id = (request.form.get("category_id") or "pain-fever").strip()
    dosage_form = (request.form.get("dosage_form") or "Tablet").strip()
    pack_size = (request.form.get("pack_size") or "10 tablets").strip()
    mrp = float(request.form.get("mrp") or 100)
    price = float(request.form.get("price") or mrp)
    manufacturer = (request.form.get("manufacturer") or "Care Cliniq").strip()
    indications = (request.form.get("indications") or "").strip()
    is_rx_required = bool(request.form.get("is_rx_required"))
    is_bestseller = bool(request.form.get("is_bestseller"))
    stock = int(request.form.get("stock") or 100)

    updated = pharmacy_catalog.update_product(product_id, {
        "name": name,
        "salt": salt,
        "category_id": category_id,
        "dosage_form": dosage_form,
        "pack_size": pack_size,
        "mrp": mrp,
        "price": price,
        "manufacturer": manufacturer,
        "indications": indications,
        "is_rx_required": is_rx_required,
        "is_bestseller": is_bestseller,
        "stock": stock
    })
    if updated:
        flash(f"Updated product '{name}' successfully.", "success")
    else:
        flash("Product not found.", "danger")
    return redirect(url_for("main.pharmacy_admin"))


@main_bp.route("/medications/admin/delete/<int:product_id>", methods=["POST"])
@login_required
def pharmacy_admin_delete(product_id):
    success = pharmacy_catalog.delete_product(product_id)
    if success:
        flash("Product removed from catalog.", "success")
    else:
        flash("Product not found.", "warning")
    return redirect(url_for("main.pharmacy_admin"))


@main_bp.route("/api/medications/search")
def api_medications_search():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "all")
    rx_filter = request.args.get("rx")
    sort_by = request.args.get("sort")

    results = pharmacy_catalog.get_all_products(
        category=category,
        search=q,
        rx_filter=rx_filter,
        sort_by=sort_by
    )
    return jsonify({
        "query": q,
        "category": category,
        "total": len(results),
        "products": results
    })


@main_bp.route("/medications/<int:medication_id>/delete", methods=["POST"])
@login_required
def delete_medication(medication_id):
    med = Medication.query.filter_by(id=medication_id, user_id=current_user.id).first_or_404()
    db.session.delete(med)
    db.session.commit()
    flash("Medication removed from your record.", "success")
    return redirect(url_for("main.medications"))


@main_bp.route("/reminders")
@login_required
def reminders():
    upcoming_appointments = (
        Appointment.query
        .filter(
            Appointment.user_id == current_user.id,
            Appointment.date >= datetime.date.today()
        )
        .order_by(Appointment.date.asc(), Appointment.time.asc())
        .all()
    )
    active_medications = (
        Medication.query
        .filter_by(user_id=current_user.id, is_active=True)
        .order_by(Medication.created_at.desc())
        .all()
    )
    return render_template(
        "reminders/index.html",
        appointments=upcoming_appointments,
        medications=active_medications,
    )


@main_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    profile = MedicalProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = MedicalProfile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()

    if request.method == "POST":
        profile.blood_group = (request.form.get("blood_group") or "").strip()[:10]
        profile.allergies = (request.form.get("allergies") or "").strip()
        profile.chronic_conditions = (request.form.get("chronic_conditions") or "").strip()
        profile.emergency_contact_name = (request.form.get("emergency_contact_name") or "").strip()[:100]
        profile.emergency_contact_phone = (request.form.get("emergency_contact_phone") or "").strip()[:50]
        db.session.commit()
        flash("Medical profile updated successfully.", "success")
        return redirect(url_for("main.settings"))

    return render_template("settings/index.html", profile=profile)

