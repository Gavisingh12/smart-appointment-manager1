import datetime
import re

from flask_login import UserMixin

from app.extensions import db


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email_verified = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utc_now)
    consultations = db.relationship("Consultation", backref="user", lazy=True, cascade="all, delete-orphan")
    appointments = db.relationship("Appointment", backref="user", lazy=True, cascade="all, delete-orphan")
    medical_profile = db.relationship("MedicalProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    medications = db.relationship("Medication", backref="user", lazy=True, cascade="all, delete-orphan")

    @property
    def display_name(self):
        name = (self.username or "").strip()
        email_name = (self.email.split("@", 1)[0] or "").strip()

        if name and name.casefold() != email_name.casefold():
            return name

        cleaned = re.sub(r"\d+$", "", email_name)
        cleaned = re.sub(r"[._-]+", " ", cleaned)
        cleaned = " ".join(cleaned.split()).strip()
        if not cleaned:
            return "Member"
        return " ".join(part.capitalize() for part in cleaned.split())

    @property
    def greeting_name(self):
        parts = self.display_name.split()
        return parts[0] if parts else "there"

    def set_password(self, password):
        from werkzeug.security import generate_password_hash

        self.password = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash

        return check_password_hash(self.password, password)


class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symptoms = db.Column(db.Text, nullable=False)
    followup_responses = db.Column(db.Text)
    diagnosis = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=utc_now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(10), nullable=False)
    doctor = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utc_now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class MedicalProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    blood_group = db.Column(db.String(10))
    allergies = db.Column(db.Text)
    chronic_conditions = db.Column(db.Text)
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    def to_dict(self):
        return {
            "blood_group": self.blood_group or "",
            "allergies": self.allergies or "",
            "chronic_conditions": self.chronic_conditions or "",
            "emergency_contact_name": self.emergency_contact_name or "",
            "emergency_contact_phone": self.emergency_contact_phone or "",
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    dosage = db.Column(db.String(60))
    frequency = db.Column(db.String(60))
    instructions = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "dosage": self.dosage or "",
            "frequency": self.frequency or "",
            "instructions": self.instructions or "",
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class EmailOtp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    code = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(80), nullable=True)
    purpose = db.Column(db.String(20), default="login")
    created_at = db.Column(db.DateTime, default=utc_now)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)

    def is_valid(self):
        return not self.is_used and utc_now() <= self.expires_at and self.attempts < 5
