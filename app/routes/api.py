import datetime
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Appointment, MedicalProfile, Medication
from app.services.ai import scan_emergency_red_flags
from app.services.clinical_kb import (
    get_medication_card,
    lookup_disease,
    match_brands_to_catalog,
    build_consultation_briefing,
)


api_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")


@api_bp.route("/clinical/medication-card", methods=["GET", "POST"])
def api_medication_card():
    """
    Return structured medication card for a disease.
    Includes: generic drug, Indian brands, dosage, meal timing, max dose,
    prescription type, precautions, home care, lab tests, emergency flags,
    and pharmacy catalog matches.

    GET  /api/v1/clinical/medication-card?disease=Migraine+with+Aura
    POST /api/v1/clinical/medication-card  {"disease": "Type 2 Diabetes Mellitus"}
    """
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        disease_name = (data.get("disease") or "").strip()
    else:
        disease_name = (request.args.get("disease") or "").strip()

    if not disease_name:
        return jsonify({"status": "error", "message": "disease parameter is required"}), 400

    card = get_medication_card(disease_name)
    if not card:
        return jsonify({
            "status": "not_found",
            "message": f"No clinical data found for: {disease_name}",
            "data": None
        }), 404

    return jsonify({"status": "success", "data": card}), 200


@api_bp.route("/clinical/lookup", methods=["GET"])
def api_disease_lookup():
    """
    Return full clinical profile for a disease from the knowledge base.
    GET /api/v1/clinical/lookup?disease=Acute+Viral+Fever
    """
    disease_name = (request.args.get("disease") or "").strip()
    if not disease_name:
        return jsonify({"status": "error", "message": "disease parameter is required"}), 400

    profile = lookup_disease(disease_name)
    if not profile:
        return jsonify({"status": "not_found", "data": None}), 404

    # Return a safe subset (exclude huge symptom text for bandwidth)
    safe_profile = {
        "name": profile.get("name", disease_name),
        "hindi_names": profile.get("hindi_names", ""),
        "specialty_category": profile.get("specialty_category", ""),
        "typical_duration": profile.get("typical_duration", ""),
        "symptoms_list": profile.get("symptoms_list", [])[:8],
        "clarifying_questions": profile.get("clarifying_questions", []),
        "generic_drug": profile.get("generic_drug", ""),
        "indian_brands": profile.get("indian_brands", []),
        "strength_mg": profile.get("strength_mg", ""),
        "dosage_frequency": profile.get("dosage_frequency", ""),
        "meal_timing": profile.get("meal_timing", ""),
        "duration_days": profile.get("duration_days", ""),
        "prescription_type": profile.get("prescription_type", ""),
        "max_safe_limit_24h": profile.get("max_safe_limit_24h", ""),
        "supportive_medicines": profile.get("supportive_medicines", ""),
        "investigations": profile.get("investigations", [])[:6],
        "precautions": profile.get("precautions", ""),
        "home_care_advice": profile.get("home_care_advice", []),
        "emergency_flags": profile.get("emergency_flags", []),
    }
    return jsonify({"status": "success", "data": safe_profile}), 200




@api_bp.route("/health", methods=["GET"])
def api_health():
    from app import get_system_status

    status = get_system_status()
    return jsonify({
        "status": "success",
        "data": status
    }), 200 if status["database"]["healthy"] else 503


@api_bp.route("/triage/scan", methods=["POST"])
def api_triage_scan():
    data = request.get_json(silent=True) or {}
    symptoms = (data.get("symptoms") or request.form.get("symptoms") or "").strip()
    if not symptoms:
        return jsonify({"status": "error", "message": "Symptoms text is required."}), 400

    scan_result = scan_emergency_red_flags(symptoms)
    return jsonify({
        "status": "success",
        "data": scan_result
    }), 200


@api_bp.route("/appointments", methods=["GET"])
@login_required
def api_get_appointments():
    appointments = (
        Appointment.query
        .filter_by(user_id=current_user.id)
        .order_by(Appointment.date.asc(), Appointment.time.asc())
        .all()
    )
    return jsonify({
        "status": "success",
        "count": len(appointments),
        "data": [
            {
                "id": a.id,
                "date": a.date.isoformat(),
                "time": a.time,
                "doctor": a.doctor,
                "notes": a.notes or "",
                "created_at": a.created_at.isoformat() if a.created_at else None,
                "is_upcoming": a.date >= datetime.date.today(),
            }
            for a in appointments
        ]
    }), 200


@api_bp.route("/appointments", methods=["POST"])
@login_required
def api_create_appointment():
    data = request.get_json(silent=True) or request.form
    date_str = (data.get("date") or "").strip()
    time = (data.get("time") or "").strip()
    doctor = (data.get("doctor") or "").strip()
    notes = (data.get("notes") or "").strip()

    if not doctor or len(doctor) > 100:
        return jsonify({"status": "error", "message": "Doctor name must be 1 to 100 characters."}), 400

    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid date format. Expected YYYY-MM-DD."}), 400

    if date_obj < datetime.date.today():
        return jsonify({"status": "error", "message": "Appointment date cannot be in the past."}), 400

    appointment = Appointment(
        date=date_obj,
        time=time,
        doctor=doctor,
        notes=notes,
        user_id=current_user.id
    )
    db.session.add(appointment)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Appointment scheduled successfully.",
        "data": {
            "id": appointment.id,
            "date": appointment.date.isoformat(),
            "time": appointment.time,
            "doctor": appointment.doctor,
            "notes": appointment.notes,
        }
    }), 201


@api_bp.route("/appointments/<int:appointment_id>", methods=["DELETE"])
@login_required
def api_delete_appointment(appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id, user_id=current_user.id).first()
    if not appointment:
        return jsonify({"status": "error", "message": "Appointment not found."}), 404

    db.session.delete(appointment)
    db.session.commit()
    return jsonify({
        "status": "success",
        "message": "Appointment cancelled successfully."
    }), 200


@api_bp.route("/profile", methods=["GET"])
@login_required
def api_get_profile():
    profile = MedicalProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        return jsonify({
            "status": "success",
            "data": {
                "blood_group": "",
                "allergies": "",
                "chronic_conditions": "",
                "emergency_contact_name": "",
                "emergency_contact_phone": "",
            }
        }), 200

    return jsonify({
        "status": "success",
        "data": profile.to_dict()
    }), 200


@api_bp.route("/profile", methods=["POST", "PUT"])
@login_required
def api_upsert_profile():
    data = request.get_json(silent=True) or request.form
    profile = MedicalProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = MedicalProfile(user_id=current_user.id)
        db.session.add(profile)

    if "blood_group" in data:
        profile.blood_group = (data.get("blood_group") or "").strip()[:10]
    if "allergies" in data:
        profile.allergies = (data.get("allergies") or "").strip()
    if "chronic_conditions" in data:
        profile.chronic_conditions = (data.get("chronic_conditions") or "").strip()
    if "emergency_contact_name" in data:
        profile.emergency_contact_name = (data.get("emergency_contact_name") or "").strip()[:100]
    if "emergency_contact_phone" in data:
        profile.emergency_contact_phone = (data.get("emergency_contact_phone") or "").strip()[:50]

    db.session.commit()
    return jsonify({
        "status": "success",
        "message": "Medical profile saved successfully.",
        "data": profile.to_dict()
    }), 200


@api_bp.route("/medications", methods=["GET"])
@login_required
def api_get_medications():
    medications = (
        Medication.query
        .filter_by(user_id=current_user.id)
        .order_by(Medication.created_at.desc())
        .all()
    )
    return jsonify({
        "status": "success",
        "count": len(medications),
        "data": [m.to_dict() for m in medications]
    }), 200


@api_bp.route("/medications", methods=["POST"])
@login_required
def api_add_medication():
    data = request.get_json(silent=True) or request.form
    name = (data.get("name") or "").strip()
    if not name or len(name) > 120:
        return jsonify({"status": "error", "message": "Medication name is required (up to 120 characters)."}), 400

    medication = Medication(
        user_id=current_user.id,
        name=name,
        dosage=(data.get("dosage") or "").strip()[:60],
        frequency=(data.get("frequency") or "").strip()[:60],
        instructions=(data.get("instructions") or "").strip(),
        is_active=bool(data.get("is_active", True)),
    )
    db.session.add(medication)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Medication added successfully.",
        "data": medication.to_dict()
    }), 201


@api_bp.route("/medications/<int:medication_id>", methods=["DELETE"])
@login_required
def api_delete_medication(medication_id):
    medication = Medication.query.filter_by(id=medication_id, user_id=current_user.id).first()
    if not medication:
        return jsonify({"status": "error", "message": "Medication not found."}), 404

    db.session.delete(medication)
    db.session.commit()
    return jsonify({
        "status": "success",
        "message": "Medication removed successfully."
    }), 200


@api_bp.route("/locations/suggest", methods=["GET"])
def api_location_suggest():
    """Return fast autocomplete suggestions for Indian cities, districts, towns, and villages."""
    query = (request.args.get("q") or "").strip()
    from app.services.india_geo import suggest_locations
    return jsonify({
        "status": "success",
        "query": query,
        "suggestions": suggest_locations(query)
    }), 200

