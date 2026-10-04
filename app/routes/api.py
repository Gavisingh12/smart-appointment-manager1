import datetime
from flask import Blueprint, current_app, jsonify, request
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Appointment, MedicalProfile, Medication
from app.services.ai import scan_emergency_red_flags


api_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")


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
