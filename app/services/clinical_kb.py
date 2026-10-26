"""
app/services/clinical_kb.py
============================
Clinical Knowledge Base Service
Provides fast lookups into the enriched disease_knowledge.json:
- Disease lookup by name (exact + 4-level fuzzy, prefers enriched entries)
- Medication card retrieval (generic drug, Indian brands, dose, timing, precautions)
- Pharmacy catalog matching (link recommended brands to cart-able products)
- Structured consultation briefing builder (professional English output)
"""

from __future__ import annotations

import json
import logging
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

ML_DIR = Path(__file__).resolve().parent.parent / "ml"
KNOWLEDGE_PATH = ML_DIR / "disease_knowledge.json"

# Pharmacy catalog for cross-linking brands to purchasable products
CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "pharmacy_catalog.json"


# ─── Data Loaders ─────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def _load_knowledge() -> dict[str, dict]:
    try:
        with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        logger.error("Failed to load clinical knowledge base: %s", exc)
        return {}


@lru_cache(maxsize=1)
def _load_catalog() -> list[dict]:
    try:
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("products", [])
    except Exception as exc:
        logger.error("Failed to load pharmacy catalog: %s", exc)
        return []


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


# ─── Disease Lookup (4-level smart fuzzy) ─────────────────────────────────────

def lookup_disease(disease_name: str) -> dict[str, Any] | None:
    """
    Return the full knowledge base profile for a disease.
    4-level fallback — always prefers the entry that has a medication_card:
      1. Exact key match with medication_card
      2. Case-insensitive exact match with medication_card
      3. Token-based fuzzy match across enriched entries (e.g. Pneumonia -> Community-Acquired Pneumonia)
      4. Return any unenriched match rather than nothing
    """
    kb = _load_knowledge()
    if not kb or not disease_name:
        return None

    target = _norm(disease_name)
    unenriched = None

    # Level 1 & 2: Exact / case-insensitive match (always prioritized)
    exact_match = None
    for key, profile in kb.items():
        key_norm = _norm(key)
        if key == disease_name or key_norm == target:
            if profile.get("medication_card") and profile["medication_card"].get("generic_drug"):
                return profile
            if exact_match is None:
                exact_match = profile

    if exact_match is not None:
        return exact_match

    # Level 3: Token-based fuzzy search across enriched KB entries (only if no exact match)
    tokens = set(t for t in target.split() if len(t) > 3)
    if tokens:
        best_score = 0
        best_entry = None
        for key, profile in kb.items():
            if not (profile.get("medication_card") and profile["medication_card"].get("generic_drug")):
                continue
            key_norm = _norm(key)
            key_tokens = set(t for t in key_norm.split() if len(t) > 3)
            # Prevent respiratory vs urinary mismatches
            if "respiratory" in tokens and "urinary" in key_tokens:
                continue
            if "urinary" in tokens and "respiratory" in key_tokens:
                continue
            overlap = len(tokens.intersection(key_tokens))
            if overlap > best_score:
                best_score = overlap
                best_entry = profile

        if best_entry and best_score >= max(1, len(tokens) // 2):
            return best_entry

    return None


def get_medication_card(disease_name: str) -> dict[str, Any] | None:
    """
    Return the structured medication card for a disease, ready for UI display.
    """
    profile = lookup_disease(disease_name)
    if not profile:
        return None

    if profile.get("medication_card") and profile["medication_card"].get("generic_drug"):
        card = dict(profile["medication_card"])
        card["pharmacy_matches"] = match_brands_to_catalog(
            card.get("indian_brands", []),
            card.get("generic_drug", "")
        )
        return card

    # Fallback: build card from flat profile fields
    return {
        "disease": profile.get("name", disease_name),
        "generic_drug": profile.get("generic_drug", ""),
        "indian_brands": profile.get("indian_brands", []),
        "strength_mg": profile.get("strength_mg", ""),
        "dosage_frequency": profile.get("dosage_frequency", ""),
        "meal_timing": profile.get("meal_timing", ""),
        "duration_days": profile.get("duration_days", ""),
        "supportive_medicines": _to_list(profile.get("supportive_medicines", "")),
        "max_safe_limit_24h": profile.get("max_safe_limit_24h", ""),
        "prescription_type": profile.get("prescription_type", "Rx"),
        "precautions": profile.get("precautions", ""),
        "home_care": profile.get("home_care_advice", []),
        "lab_tests": profile.get("investigations", []),
        "emergency_red_flags": profile.get("emergency_flags", []),
        "clarifying_questions": profile.get("clarifying_questions", []),
        "pharmacy_matches": match_brands_to_catalog(
            profile.get("indian_brands", []),
            profile.get("generic_drug", "")
        ),
    }


def _to_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return value
    if isinstance(value, str) and value.strip():
        return [p.strip() for p in re.split(r";\s*", value) if p.strip()]
    return []


# ─── Pharmacy Catalog Matching ────────────────────────────────────────────────

def match_brands_to_catalog(brand_names: list[str], generic_drug: str) -> list[dict]:
    """
    Cross-link recommended Indian brand names (from KB) to purchasable products
    in the pharmacy catalog.  Returns a list of matching product dicts.
    """
    products = _load_catalog()
    if not products:
        return []

    matched = []
    seen_ids = set()

    brand_norms = [_norm(b) for b in (brand_names or []) if b]
    generic_norm = _norm(generic_drug)

    for product in products:
        prod_name_norm = _norm(product.get("name", ""))
        prod_salt_norm = _norm(product.get("salt", ""))

        hit = False
        for bn in brand_norms:
            if bn and (bn in prod_name_norm or prod_name_norm in bn):
                hit = True
                break

        if not hit and generic_norm and len(generic_norm) > 3:
            primary_generic = generic_norm.split()[0]
            if len(primary_generic) > 4 and primary_generic in prod_salt_norm:
                hit = True

        if hit and product["id"] not in seen_ids:
            seen_ids.add(product["id"])
            matched.append({
                "id": product["id"],
                "name": product["name"],
                "salt": product.get("salt", ""),
                "price": product.get("price"),
                "mrp": product.get("mrp"),
                "discount_percent": product.get("discount_percent"),
                "is_rx_required": product.get("is_rx_required", True),
                "is_bestseller": product.get("is_bestseller", False),
                "category_id": product.get("category_id", ""),
                "stock": product.get("stock", 0),
            })

    return matched[:5]


# ─── Consultation Briefing Builder ────────────────────────────────────────────

def build_consultation_briefing(
    disease_name: str,
    symptoms_text: str = "",
    followup_answers: list[dict] | None = None,
) -> dict[str, Any]:
    """
    Build a complete, structured consultation briefing dict for a given disease.
    Uses the enriched KB to always populate medication details.
    All text is in professional English.
    """
    profile = lookup_disease(disease_name)
    med_card = get_medication_card(disease_name)

    if not profile and not med_card:
        return {}

    p = profile or {}
    mc = med_card or {}

    # Use KB canonical name (not ML model's generic label)
    canonical_name = p.get("name") or mc.get("disease") or disease_name

    # Build presenting complaint
    followup_context = ""
    if followup_answers:
        answered = [a.get("answer", "") for a in followup_answers if a.get("answer")]
        if answered:
            followup_context = "; ".join(answered)

    presenting_complaint = symptoms_text or p.get("symptoms", "Clinical symptoms as reported by patient.")
    if followup_context:
        presenting_complaint = f"{presenting_complaint} — Follow-up context: {followup_context}"

    # Differential diagnoses
    differentials = p.get("differential_diagnoses", [])
    differentials_str = "; ".join(differentials[:4]) if differentials else canonical_name

    # Investigations
    investigations = mc.get("lab_tests") or p.get("investigations", [])
    if not investigations:
        investigations = ["Clinical evaluation and vital signs", "Focused diagnostic workup"]
    investigations_str = "; ".join(investigations[:5])

    # Treatment = KB treatment + home care
    kb_treatment = p.get("treatment", "")
    home_care = mc.get("home_care") or p.get("home_care_advice", [])
    treatment_parts = []
    if kb_treatment and not kb_treatment.startswith("Standard clinical management for"):
        treatment_parts.append(kb_treatment)
    else:
        treatment_parts.append(f"Structured clinical management for {canonical_name}")
    if home_care:
        treatment_parts.append("Self-care: " + "; ".join(str(h) for h in home_care[:3]))
    treatment_str = ". ".join(treatment_parts)

    # Medications
    medications_str = _format_medication_output(mc, canonical_name, p)

    # Precautions
    precautions = mc.get("precautions") or p.get("precautions", "")
    if not precautions:
        precautions = (
            f"Follow prescribed dosage strictly for {canonical_name}. "
            "Do not self-medicate without a doctor's advice. "
            "Seek immediate care if symptoms worsen."
        )

    # Emergency flags
    emergency_flags = mc.get("emergency_red_flags") or p.get("emergency_flags", [])

    return {
        "presenting_complaint": presenting_complaint,
        "differential_diagnoses": differentials_str,
        "investigations": investigations_str,
        "treatment": treatment_str,
        "medications": medications_str,
        "precautions": precautions,
        "emergency_flags": emergency_flags,
        "medication_card": mc,
        "matched_disease_name": canonical_name,
        "hindi_names": p.get("hindi_names", ""),
        "specialty_category": p.get("specialty_category", ""),
        "typical_duration": p.get("typical_duration", ""),
        "clarifying_questions": mc.get("clarifying_questions", p.get("clarifying_questions", [])),
        "disclaimer": (
            "This analysis was generated in standard guidance mode by Care Cliniq using a structured clinical knowledge base "
            "of 1000+ medical conditions. It is for guidance only and does not replace in-person medical diagnosis. "
            "Always consult a qualified doctor before starting or changing any medication."
        ),
    }


def _format_medication_output(mc: dict, disease_name: str, profile: dict | None = None) -> str:
    """
    Format medication details into a complete, always-populated clinical string.
    Falls back to profile.medications if medication_card is missing/empty.
    """
    if not mc or not mc.get("generic_drug"):
        # Fallback to raw profile medications list
        if profile and profile.get("medications"):
            meds = profile["medications"]
            meds_str = "; ".join(meds[:4]) if isinstance(meds, list) else str(meds)
            return f"Medications: {meds_str}. Note: Consult a doctor before starting treatment."
        return f"Physician-directed pharmacotherapy required for {disease_name}. Consult a qualified doctor."

    parts = []

    generic = mc.get("generic_drug", "")
    brands = mc.get("indian_brands", [])
    strength = mc.get("strength_mg", "")
    freq = mc.get("dosage_frequency", "")
    timing = mc.get("meal_timing", "")
    duration = mc.get("duration_days", "")
    max_dose = mc.get("max_safe_limit_24h", "")
    rx_type = mc.get("prescription_type", "")
    supportive = mc.get("supportive_medicines", [])

    # Primary medicine line
    if generic:
        line = f"Primary medication: {generic}"
        if strength:
            line += f" — {strength}"
        parts.append(line)

    # Dosage details
    dosage_parts = []
    if freq:
        dosage_parts.append(freq)
    if timing:
        dosage_parts.append(timing)
    if duration:
        dosage_parts.append(f"for {duration}")
    if dosage_parts:
        parts.append("Dosage: " + " | ".join(dosage_parts))

    # Indian brands
    if brands:
        parts.append(f"Available Indian brands: {', '.join(brands[:4])}")

    # Safe limit
    if max_dose:
        parts.append(f"Maximum safe dose: Do not exceed {max_dose} per 24 hours")

    # Rx / OTC status
    if rx_type:
        if rx_type.upper() == "OTC":
            label = "Available OTC — no prescription needed"
        else:
            label = f"Prescription required ({rx_type}) — consult a registered doctor"
        parts.append(label)

    # Supportive medicines
    if supportive:
        supp_list = supportive if isinstance(supportive, list) else [supportive]
        valid_supp = [s for s in supp_list if s and str(s).strip()]
        if valid_supp:
            parts.append(f"Supportive therapy: {'; '.join(str(s) for s in valid_supp[:3])}")

    return ". ".join(parts) if parts else f"Physician-directed pharmacotherapy for {disease_name}. Consult a doctor."
