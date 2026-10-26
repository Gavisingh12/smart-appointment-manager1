"""
build_clinical_kb.py
====================
Reads app/data/clinical_kb/clinical_master_dataset.csv (547 diseases, 20 columns)
and MERGES it into app/ml/disease_knowledge.json, enriching every entry with
the new clinical fields while preserving all existing data.

Run with:  python build_clinical_kb.py
"""

import csv
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSV_PATH = HERE / "app" / "data" / "clinical_kb" / "clinical_master_dataset.csv"
KB_PATH  = HERE / "app" / "ml" / "disease_knowledge.json"

# ── CSV column order (20 columns) ────────────────────────────────────────────
CSV_COLS = [
    "Disease_Name", "Common_Names_Hindi", "Specialty_Category",
    "Primary_Symptoms", "Secondary_Symptoms", "Typical_Duration",
    "Clarifying_Questions", "First_Line_Generic_Drug", "Popular_Indian_Brands",
    "Adult_Strength_Mg", "Dosage_Frequency", "Meal_Timing",
    "Duration_Days", "Supportive_Medicines", "Max_Safe_Limit_24h",
    "Prescription_Type", "Precautions_Contraindications",
    "Home_Care_Advice", "Lab_Investigations", "Emergency_Red_Flags",
]


def split_semi(text: str) -> list:
    """Split a semicolon-delimited field into a clean list."""
    if not text or not text.strip():
        return []
    return [p.strip() for p in re.split(r";\s*", text) if p.strip()]


def build_symptom_text(row: dict) -> str:
    """Combine primary + secondary symptoms into a searchable string."""
    parts = []
    if row["Primary_Symptoms"]:
        parts.append(row["Primary_Symptoms"])
    if row["Secondary_Symptoms"]:
        parts.append(row["Secondary_Symptoms"])
    return "; ".join(parts)


def _build_med_card(row: dict, name: str) -> dict:
    """Build a structured medication card dict for UI rendering."""
    return {
        "disease": name,
        "generic_drug": row["First_Line_Generic_Drug"].strip(),
        "indian_brands": split_semi(row["Popular_Indian_Brands"]),
        "strength_mg": row["Adult_Strength_Mg"].strip(),
        "dosage_frequency": row["Dosage_Frequency"].strip(),
        "meal_timing": row["Meal_Timing"].strip(),
        "duration_days": row["Duration_Days"].strip(),
        "supportive_medicines": split_semi(row["Supportive_Medicines"]),
        "max_safe_limit_24h": row["Max_Safe_Limit_24h"].strip(),
        "prescription_type": row["Prescription_Type"].strip(),
        "precautions": row["Precautions_Contraindications"].strip(),
        "home_care": split_semi(row["Home_Care_Advice"]),
        "lab_tests": split_semi(row["Lab_Investigations"]),
        "emergency_red_flags": split_semi(row["Emergency_Red_Flags"]),
        "clarifying_questions": split_semi(row["Clarifying_Questions"]),
    }


def csv_row_to_kb_entry(row: dict, existing_id, next_id: int) -> dict:
    """Convert a CSV row to the standard KB entry format, enriched with clinical fields."""
    name = row["Disease_Name"].strip()
    sym_text = build_symptom_text(row)
    sym_list = split_semi(row["Primary_Symptoms"]) + split_semi(row["Secondary_Symptoms"])

    emergency_flags = split_semi(row["Emergency_Red_Flags"])
    if not emergency_flags:
        emergency_flags = [
            f"Sudden severe exacerbation of {name} symptoms.",
            "Shortness of breath, severe chest pain, or neurological deficits.",
        ]

    entry = {
        "name": name,
        "id": existing_id if existing_id is not None else next_id,
        "hindi_names": row["Common_Names_Hindi"].strip(),
        "specialty_category": row["Specialty_Category"].strip(),
        "symptoms": sym_text,
        "symptoms_list": sym_list,
        "typical_duration": row["Typical_Duration"].strip(),
        "clarifying_questions": split_semi(row["Clarifying_Questions"]),
        "differential_diagnoses": [],
        "investigations": split_semi(row["Lab_Investigations"]),
        "treatment": (
            row["Home_Care_Advice"].strip()
            if row["Home_Care_Advice"].strip() else
            f"Standard clinical management for {name}."
        ),
        # ── Rich medication fields ─────────────────────────────────────────
        "medications": split_semi(row["First_Line_Generic_Drug"]) + split_semi(row["Supportive_Medicines"]),
        "generic_drug": row["First_Line_Generic_Drug"].strip(),
        "indian_brands": split_semi(row["Popular_Indian_Brands"]),
        "strength_mg": row["Adult_Strength_Mg"].strip(),
        "dosage_frequency": row["Dosage_Frequency"].strip(),
        "meal_timing": row["Meal_Timing"].strip(),
        "duration_days": row["Duration_Days"].strip(),
        "supportive_medicines": row["Supportive_Medicines"].strip(),
        "max_safe_limit_24h": row["Max_Safe_Limit_24h"].strip(),
        "prescription_type": row["Prescription_Type"].strip(),
        "medication_card": _build_med_card(row, name),
        "precautions": row["Precautions_Contraindications"].strip(),
        "home_care_advice": split_semi(row["Home_Care_Advice"]),
        "emergency_flags": emergency_flags,
    }
    return entry


def normalize_key(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip().lower())


def main():
    print(f"Loading existing KB from: {KB_PATH}")
    with open(KB_PATH, "r", encoding="utf-8") as f:
        knowledge = json.load(f)

    existing_by_norm = {normalize_key(k): k for k in knowledge.keys()}
    next_id = max((v.get("id", 0) for v in knowledge.values()), default=0) + 1

    print(f"Reading CSV from: {CSV_PATH}")
    rows_processed = 0
    new_entries = 0
    enriched_entries = 0

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["Disease_Name"].strip()
            norm = normalize_key(name)

            if norm in existing_by_norm:
                existing_key = existing_by_norm[norm]
                existing_entry = knowledge[existing_key]
                new_entry = csv_row_to_kb_entry(row, existing_entry.get("id"), next_id)

                # Preserve existing richer fields when they exist
                if existing_entry.get("differential_diagnoses"):
                    new_entry["differential_diagnoses"] = existing_entry["differential_diagnoses"]
                if existing_entry.get("symptoms") and len(existing_entry["symptoms"]) > len(new_entry["symptoms"]):
                    new_entry["symptoms"] = existing_entry["symptoms"]
                if existing_entry.get("symptoms_list") and len(existing_entry["symptoms_list"]) > len(new_entry["symptoms_list"]):
                    new_entry["symptoms_list"] = existing_entry["symptoms_list"]

                knowledge[existing_key] = new_entry
                enriched_entries += 1
            else:
                new_entry = csv_row_to_kb_entry(row, None, next_id)
                knowledge[name] = new_entry
                existing_by_norm[norm] = name
                next_id += 1
                new_entries += 1

            rows_processed += 1

    print(f"\nResults:")
    print(f"  CSV rows processed       : {rows_processed}")
    print(f"  Existing entries enriched: {enriched_entries}")
    print(f"  New entries added        : {new_entries}")
    print(f"  Total KB entries now     : {len(knowledge)}")

    with open(KB_PATH, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, ensure_ascii=False, indent=2)
    print(f"\nSaved enriched KB to: {KB_PATH}")


if __name__ == "__main__":
    main()
