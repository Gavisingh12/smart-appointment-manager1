"""
app/services/clinical_nlp.py
============================
Intelligent Clinical Natural Language Processing & Safety Triage Guardrail.

Bridges everyday patient language (English, Hindi, Hinglish, casual phrases)
with professional medical classification and clinical safety guidelines:
1. Normalizes colloquial words ("sir bhari", "pet dard", "bukhar", "loose motion")
   into standardized clinical terminology.
2. Extracts clinical metadata: symptom duration, severity, and cardinal system flags.
3. Applies clinical guardrails (e.g., Pneumonia cannot be primary without respiratory symptoms;
   Glaucoma cannot be primary for isolated tension headache).
4. Routes generic / primary-care presentations safely to common conditions
   (Acute Viral Fever, Tension Headache, Common Cold, Acute Gastroenteritis).
"""

from __future__ import annotations

import re
from typing import Any


# ─── Hinglish / Hindi / Casual Symptom Mappings ──────────────────────────────
COLLOQUIAL_SYMPTOM_MAP = [
    # Head & Neurological
    (r"\b(sir\s+bhari\s+bhari|sir\s+bhari|sar\s+bhari|head\s+feels?\s+heavy|heaviness\s+in\s+head|heavy\s+head)\b", "head heaviness", "tension headache"),
    (r"\b(sir\s+dard|sar\s+dard|sar\s+me\s+dard|sir\s+me\s+dard|matha\s+dard|headache|head\s+pain)\b", "headache", "tension headache"),
    (r"\b(chakkar|chakkar\s+aa\s+rahe|sar\s+ghumna|sar\s+chakrana|dizziness|giddiness|spinning\s+head)\b", "dizziness", "vertigo"),
    (r"\b(adha\s+sar\s+dard|one\s+sided\s+headache|migraine|migrain)\b", "throbbing unilateral headache", "migraine"),

    # Fever & Systemic
    (r"\b(bukhar|bukhaar|halka\s+bukhar|tez\s+bukhar|tap\s+chara|tap\s+hai|body\s+garam|fever|high\s+temperature|pyrexia)\b", "fever", "acute viral fever"),
    (r"\b(thand\s+lag\s+rahi|kapkapi|chills|shivering|rigors)\b", "chills", "fever with chills"),
    (r"\b(badan\s+dard|body\s+ache|bodyache|ang\s+ang\s+dard|body\s+pain|muscles?\s+pain|myalgia)\b", "generalized body ache", "myalgia"),
    (r"\b(kamzori|kamzori\s+lag\s+rahi|thakan|thakaan|fatigue|weakness|tiredness|body\s+tut\s+rahi|lethargy)\b", "fatigue and weakness", "malaise"),

    # Respiratory & ENT
    (r"\b(khansi|khasi|cough|coughing|sukhi\s+khansi|balgam|phlegm|sputum)\b", "cough", "cough"),
    (r"\b(sardi|jukham|zukham|zukaam|runny\s+nose|running\s+nose|naak\s+beh\s+rahi|chheenk|sneezing|cold\s+and\s+cough|cold)\b", "coryza and nasal congestion", "common cold"),
    (r"\b(gale\s+me\s+dard|gala\s+kharab|gale\s+me\s+kharash|sore\s+throat|throat\s+pain|throat\s+infection)\b", "sore throat", "pharyngitis"),
    (r"\b(saans\s+phool\s+rahi|saans\s+lene\s+me\s+takleef|shortness\s+of\s+breath|difficulty\s+breathing|breathlessness|dyspnea)\b", "shortness of breath", "acute respiratory distress"),
    (r"\b(sine\s+me\s+dard|chaati\s+me\s+dard|chest\s+pain|chest\s+tightness|chest\s+discomfort)\b", "chest pain", "angina or pleuritic chest pain"),

    # Gastrointestinal
    (r"\b(pet\s+dard|pet\s+me\s+dard|pet\s+kharab|pet\s+me\s+marod|stomach\s+ache|stomach\s+pain|abdominal\s+pain|belly\s+pain)\b", "abdominal pain", "gastritis"),
    (r"\b(loose\s+motion|dast|patle?\s+dast|diarrhea|watery\s+stools|dast\s+lag\s+rahe)\b", "loose stools and diarrhea", "acute gastroenteritis"),
    (r"\b(ulti|ultian|vomit|vomiting|kai\s+aana|puking)\b", "vomiting", "acute gastritis"),
    (r"\b(ji\s+machlana|mitli|nausea|feeling\s+to\s+vomit)\b", "nausea", "nausea"),
    (r"\b(acidity|jalan\s+sine\s+me|heartburn|gas\s+ban\s+rahi|bloating|pet\s+phoolna)\b", "dyspepsia and acid reflux", "gastritis"),
    (r"\b(kabz|kabji|constipation|pet\s+saaf\s+nahi)\b", "constipation", "constipation"),

    # Hair & Scalp (Trichology)
    (r"\b(hairfall|hair\s+fall|hair\s+loss|baal\s+jhad|baal\s+gir|baal\s+tut|baldness|alopecia|receding\s+hairline|hair\s+thinning|thinning\s+hair|patle\s+baal)\b", "hair fall and scalp shedding", "hair fall"),
    (r"\b(dandruff|rusi|flaky\s+scalp|itchy\s+scalp|scalp\s+itching)\b", "dandruff and scalp flaking", "dandruff"),

    # Skin & Allergy (Dermatology)
    (r"\b(khujli|itching|itchy|rash|rashes|lal\s+chakatte|skin\s+allergy|hives|daane|pimples?|acne|eczema|fungal|ringworm|daad)\b", "pruritus and skin eruption", "dermatitis"),

    # Musculoskeletal, Spine & Joint (Orthopedics)
    (r"\b(kamar\s+dard|back\s+pain|lower\s+back\s+pain|backache|spine\s+pain|slip\s+disc|sciatica)\b", "lower back pain", "lumbar spondylosis"),
    (r"\b(ghutne\s+me\s+dard|knee\s+pain|joint\s+pain|jodo\s+me\s+dard|joints\s+pain|arthritis|gathiya|stiff\s+joints|morning\s+stiffness)\b", "joint pain and stiffness", "osteoarthritis"),
    (r"\b(gardan\s+me\s+dard|neck\s+pain|cervical|shoulder\s+pain)\b", "neck pain", "cervical spondylosis"),

    # Oral & Dental (Dentistry)
    (r"\b(daant\s+dard|daant\s+me\s+dard|tooth\s+pain|toothache|teeth\s+pain|swollen\s+gums|masudo\s+me\s+dard|gum\s+bleeding|cavity|dant\s+kide)\b", "dental pain and odontalgia", "dental caries"),

    # Eye & Vision (Ophthalmology)
    (r"\b(aankh\s+laal|aankh\s+me\s+dard|eye\s+pain|eye\s+redness|red\s+eyes|blurred\s+vision|watery\s+eyes|aankh\s+aana|conjunctivitis)\b", "ocular pain and conjunctival redness", "conjunctivitis"),

    # Urinary & Renal (Urology)
    (r"\b(peshab\s+me\s+jalan|burning\s+urination|burning\s+urine|dysuria|peshab\s+bar\s+bar\s+aana|frequent\s+urination|urine\s+infection|blood\s+in\s+urine)\b", "dysuria and urinary irritation", "urinary tract infection"),
    (r"\b(pathri|kidney\s+stone|flank\s+pain|gurde\s+me\s+dard)\b", "renal colic and flank pain", "renal calculi"),

    # Endocrine & Metabolic (Diabetes / Thyroid)
    (r"\b(sugar\s+badh|high\s+sugar|diabetes|diabetic|excessive\s+thirst|pyaas\s+zyada|bar\s+bar\s+peshab)\b", "hyperglycemia and metabolic symptoms", "type 2 diabetes"),
    (r"\b(thyroid|weight\s+gain\s+sudden|weight\s+loss\s+sudden|sardi\s+zyada\s+lag)\b", "thyroid endocrine disturbance", "hypothyroidism"),

    # Mental Health & Sleep
    (r"\b(anxiety|ghabrahat|bechaini|panic|depression|udas|tension|insomnia|neend\s+nahi|stress)\b", "anxiety and sleep disruption", "generalized anxiety"),
]

# ─── Temporal & Duration Extraction ──────────────────────────────────────────
DURATION_PATTERNS = [
    (r"\b(\d+)\s*(?:saal|years?)\b", r"\1 years"),
    (r"\b(\d+)\s*(?:mahine|months?)\b", r"\1 months"),
    (r"\b(\d+)\s*(?:hafte|weeks?)\b", r"\1 weeks"),
    (r"\b(\d+)\s*(?:din|dino|days?)\b", r"\1 days"),
    (r"\b(\d+)\s*(?:ghante|hours?)\b", r"\1 hours"),
    (r"\b(?:aaj\s+se|today|since\s+morning|subah\s+se)\b", "since today"),
    (r"\b(?:kal\s+se|since\s+yesterday)\b", "since yesterday"),
    (r"\b(?:last\s+few\s+days|kuch\s+dino\s+se)\b", "for several days"),
    (r"\b(?:last\s+year|pichle\s+saal\s+se)\b", "for 1 year"),
]

# ─── Severity Cues ────────────────────────────────────────────────────────────
SEVERITY_CUES = [
    (r"\b(bahut\s+zyada|severe|unbearable|bahut\s+tez|extreme|critical|intense)\b", "Severe"),
    (r"\b(moderate|theek\s+thaak|medium|darmiyana)\b", "Moderate"),
    (r"\b(halka|halka\s+phulka|mild|occasional|slight|thoda|thoda\s+bahut)\b", "Mild"),
]


def check_symptom_presence(pattern: str, text: str) -> bool:
    """
    Returns True only if the symptom pattern is found AND is not negated
    by English ('no', 'not', 'without', 'denies') or Hindi/Hinglish ('nahi', 'nahi hai', 'koi nahi').
    """
    for match in re.finditer(pattern, text):
        start = match.start()
        end = match.end()
        # 1. Prefix negation check (e.g., "no fever", "without cough", "koi dard nahi")
        prefix = text[max(0, start - 35):start]
        if re.search(r"\b(no|not|without|denies|denied|rule\s+out|koi|na)\s*$", prefix):
            continue
        # 2. Suffix negation check (e.g., "fever nahi hai", "dard nahi ho raha", "cough absent")
        suffix = text[end:min(len(text), end + 35)]
        if re.search(r"^\s*[:\-\—\?]?\s*(nahi|nahi\s+hai|nahi\s+ho\s+raha|absent|denied|none|not\s+present)\b", suffix):
            continue
        return True
    return False


def normalize_symptoms(text: str) -> dict[str, Any]:
    """
    Parse free-text input (English/Hindi/Hinglish) into standardized clinical tokens,
    duration, severity, and cardinal system involvement with negation handling.
    """
    raw = (text or "").strip()
    lowered = f" {raw.lower()} "

    # 1. Detect duration
    detected_duration = ""
    for pattern, repl in DURATION_PATTERNS:
        match = re.search(pattern, lowered)
        if match:
            detected_duration = match.group(0).strip()
            break

    # 2. Detect severity
    detected_severity = "Standard"
    for pattern, label in SEVERITY_CUES:
        if re.search(pattern, lowered):
            detected_severity = label
            break

    # 3. Match colloquial terms with negation awareness
    extracted_symptoms = []
    clinical_keywords = []
    normalized_phrases = []

    for pattern, clinical_term, disease_hint in COLLOQUIAL_SYMPTOM_MAP:
        if check_symptom_presence(pattern, lowered):
            extracted_symptoms.append(clinical_term)
            clinical_keywords.append(disease_hint)
            normalized_phrases.append(clinical_term)

    # 4. Cardinal system flags (negation-aware)
    has_fever = check_symptom_presence(r"\b(fever|bukhar|tap|temperature|pyrexia|chills|garam)\b", lowered)
    has_cough = check_symptom_presence(r"\b(cough|khansi|phlegm|balgam|sputum)\b", lowered)
    has_breathless = check_symptom_presence(r"\b(shortness\s+of\s+breath|breathless|saans|dyspnea|gasping|suffocat)\b", lowered)
    has_chest_pain = check_symptom_presence(r"\b(chest\s+pain|chaati\s+me\s+dard|sine\s+me\s+dard|pleuritic)\b", lowered)
    has_headache = check_symptom_presence(r"\b(headache|sir\s+dard|sar\s+dard|matha|head\s+pain|sir\s+bhari|head\s+heavy)\b", lowered)
    has_gi = check_symptom_presence(r"\b(pet|stomach|loose\s+motion|dast|diarrhea|vomit|ulti|nausea|acidity|belly)\b", lowered)
    has_throat = check_symptom_presence(r"\b(gala|gale|throat|pharyngitis|swallow)\b", lowered)
    has_cold = check_symptom_presence(r"\b(sardi|jukham|zukham|runny\s+nose|sneezing|chheenk|congestion)\b", lowered)
    has_fatigue = check_symptom_presence(r"\b(kamzori|thakan|fatigue|weakness|tiredness|body\s+tut\s+rahi|lethargy)\b", lowered)
    has_dizziness = check_symptom_presence(r"\b(chakkar|dizziness|giddiness|sar\s+ghumna)\b", lowered)

    # Specialized specialty flags
    has_hair = check_symptom_presence(r"\b(hairfall|hair\s+fall|hair\s+loss|baal|bald|alopecia|scalp|dandruff)\b", lowered)
    has_skin = check_symptom_presence(r"\b(khujli|itching|rash|rashes|skin|eczema|pimples?|acne|fungal|ringworm|daad|hives)\b", lowered)
    has_ortho = check_symptom_presence(r"\b(back\s+pain|kamar|ghutne|knee|joint|jodo|arthritis|gathiya|spine|cervical|sciatica)\b", lowered)
    has_dental = check_symptom_presence(r"\b(daant|tooth|teeth|toothache|gum|masudo|cavity)\b", lowered)
    has_eye = check_symptom_presence(r"\b(aankh|eye|eyes|vision|conjunctivitis)\b", lowered)
    has_urinary = check_symptom_presence(r"\b(peshab|urine|urination|dysuria|pathri|kidney\s+stone)\b", lowered)
    has_diabetes = check_symptom_presence(r"\b(sugar|diabetes|diabetic|excessive\s+thirst|pyaas\s+zyada)\b", lowered)
    has_mental = check_symptom_presence(r"\b(anxiety|ghabrahat|depression|stress|insomnia|neend\s+nahi)\b", lowered)

    # Construct clean English clinical narrative for the model / triage
    symptom_summary_parts = list(dict.fromkeys(extracted_symptoms))
    if not symptom_summary_parts:
        # Fallback to alphanumeric cleaning of raw text
        cleaned_words = [w for w in re.split(r"[^\w]+", lowered) if len(w) > 2 and w not in {"the", "and", "from", "for", "with", "have", "been", "hai", "rha", "tha", "thi", "lag"}]
        normalized_english = " ".join(cleaned_words)
    else:
        normalized_english = ", ".join(symptom_summary_parts)
        if detected_duration:
            normalized_english += f" for {detected_duration}"

    return {
        "original_text": raw,
        "normalized_english": normalized_english,
        "extracted_symptoms": symptom_summary_parts,
        "duration": detected_duration,
        "severity": detected_severity,
        "clinical_hints": list(dict.fromkeys(clinical_keywords)),
        "cardinal_flags": {
            "has_fever": has_fever,
            "has_respiratory": (has_cough or has_breathless or has_chest_pain),
            "has_cough": has_cough,
            "has_breathless": has_breathless,
            "has_chest_pain": has_chest_pain,
            "has_headache": has_headache,
            "has_throat": has_throat,
            "has_cold": has_cold,
            "has_gi": has_gi,
            "has_fatigue": has_fatigue,
            "has_dizziness": has_dizziness,
            "has_hair": has_hair,
            "has_skin": has_skin,
            "has_ortho": has_ortho,
            "has_dental": has_dental,
            "has_eye": has_eye,
            "has_urinary": has_urinary,
            "has_diabetes": has_diabetes,
            "has_mental": has_mental,
        }
    }


def clinical_safety_triage(
    symptoms_text: str,
    ml_predicted_disease: str | None = None,
    ml_confidence: float = 0.0,
    top_predictions: list[dict] | None = None,
) -> dict[str, Any]:
    """
    Applies medical guidelines and safety rules to select the appropriate
    clinical primary diagnosis and differential diagnosis list:
    - Never assign Pneumonia without respiratory symptoms (cough, dyspnea, pleuritic pain).
    - Never assign Glaucoma / Intracranial hemorrhage for simple tension head heaviness.
    - Default isolated fever (< 5 days) to Acute Viral Fever.
    - Default head heaviness / headache to Tension Headache.
    - Default cold/cough to Upper Respiratory Tract Infection (Common Cold).
    - Default loose stools to Acute Gastroenteritis.
    - If ML model prediction has high confidence (>= 28%) and satisfies cardinal criteria, preserve it.
    """
    parsed = normalize_symptoms(symptoms_text)
    flags = parsed["cardinal_flags"]
    cleaned_lower = symptoms_text.lower()

    primary_disease = None
    differentials = []
    confidence = ml_confidence
    triage_reason = "Clinical guideline evaluation"

    # ── High-Precision ML / Clinical Engine Validation (>= 75% Confidence) ───
    # If our 2-stage hierarchical engine ranked a specific condition with high confidence,
    # we enforce safety guardrails (rejecting false pneumonia/glaucoma) and preserve the specific diagnosis.
    if ml_predicted_disease and ml_confidence >= 75.0:
        is_unsafe = False
        # Guardrail 1: Pneumonia requires respiratory/cough signs
        if "pneumonia" in ml_predicted_disease.lower() and not (flags["has_respiratory"] or flags["has_cough"] or flags["has_breathless"]):
            is_unsafe = True
        # Guardrail 2: Glaucoma / Intracranial bleed for simple tension headache
        if any(g in ml_predicted_disease.lower() for g in ["glaucoma", "intracranial", "subarachnoid"]) and not flags["has_eye"] and flags["has_headache"]:
            is_unsafe = True

        if not is_unsafe:
            primary_disease = ml_predicted_disease
            if top_predictions:
                differentials = [p["disease"] for p in top_predictions[:4]]
            else:
                differentials = [ml_predicted_disease]
            confidence = ml_confidence
            triage_reason = f"High-precision clinical engine match ({ml_confidence:.1f}%)"

            deduped_diffs = [primary_disease]
            for d in differentials:
                if d and d not in deduped_diffs:
                    deduped_diffs.append(d)

            return {
                "primary_disease": primary_disease,
                "confidence": round(float(confidence), 1),
                "differentials": deduped_diffs[:4],
                "normalized_context": parsed,
                "triage_reason": triage_reason,
            }

    # ── RULE 1: Isolated Fever (No Respiratory / Chest Signs) ────────────────
    # A patient presenting with "fever from last 2 days" or "halka bukhar"
    # MUST NOT be given Pneumonia or Tuberculosis without respiratory signs!
    if flags["has_fever"] and not flags["has_respiratory"]:
        if flags["has_throat"] or flags["has_cold"]:
            primary_disease = "Upper Respiratory Tract Infection (Common Cold)"
            differentials = [
                "Upper Respiratory Tract Infection (Common Cold)",
                "Acute Viral Fever",
                "Influenza",
                "Acute Pharyngitis"
            ]
            confidence = max(confidence, 88.0)
            triage_reason = "Fever with upper respiratory/ENT involvement"
        elif flags["has_gi"]:
            primary_disease = "Acute Gastroenteritis"
            differentials = [
                "Acute Gastroenteritis",
                "Acute Viral Fever",
                "Enteric Fever (Typhoid)",
                "Gastritis"
            ]
            confidence = max(confidence, 85.0)
            triage_reason = "Fever with gastrointestinal symptoms"
        else:
            primary_disease = "Acute Viral Fever"
            differentials = [
                "Acute Viral Fever",
                "Upper Respiratory Tract Infection (Common Cold)",
                "Influenza",
                "Enteric Fever (Typhoid)"
            ]
            confidence = max(confidence, 92.0)
            triage_reason = "Isolated acute fever presentation without localizing respiratory signs"

    # ── RULE 2: Head Heaviness / Tension Headache ("sir bhari bhari") ────────
    elif flags["has_headache"] and not flags["has_fever"] and not flags["has_gi"]:
        # "sir bhari bhari", "sar me dard", "tension headache"
        if "migraine" in cleaned_lower or "one side" in cleaned_lower or "adha sar" in cleaned_lower:
            primary_disease = "Migraine"
            differentials = ["Migraine", "Tension Headache", "Cluster Headache", "Cervicogenic Headache"]
            confidence = max(confidence, 86.0)
            triage_reason = "Unilateral / throbbing headache pattern"
        else:
            primary_disease = "Tension Headache"
            differentials = [
                "Tension Headache",
                "Migraine",
                "Sinusitis",
                "Eye Strain / Refractive Error"
            ]
            confidence = max(confidence, 90.0)
            triage_reason = "Non-specific head heaviness and tension presentation"

    # ── RULE 3: Cold, Cough, Runny Nose, Sore Throat ─────────────────────────
    elif (flags["has_cold"] or (flags["has_cough"] and not flags["has_breathless"] and not flags["has_chest_pain"])):
        # Common cold or acute bronchitis presentation
        if flags["has_throat"] and not flags["has_cough"]:
            primary_disease = "Upper Respiratory Tract Infection (Common Cold)"
            differentials = [
                "Upper Respiratory Tract Infection (Common Cold)",
                "Acute Pharyngitis",
                "Acute Tonsillitis",
                "Allergic Rhinitis"
            ]
            confidence = max(confidence, 88.0)
            triage_reason = "Pharyngeal and upper airway irritation"
        else:
            primary_disease = "Upper Respiratory Tract Infection (Common Cold)"
            differentials = [
                "Upper Respiratory Tract Infection (Common Cold)",
                "Acute Bronchitis",
                "Influenza",
                "Allergic Rhinitis"
            ]
            confidence = max(confidence, 89.0)
            triage_reason = "Upper respiratory tract symptoms without lower respiratory consolidation"

    # ── RULE 4: Gastrointestinal (Loose stools, Pet dard, Vomiting) ───────────
    elif flags["has_gi"] and not flags["has_respiratory"]:
        if "loose motion" in cleaned_lower or "dast" in cleaned_lower or "diarrhea" in cleaned_lower:
            primary_disease = "Acute Gastroenteritis"
            differentials = [
                "Acute Gastroenteritis",
                "Food Poisoning",
                "Irritable Bowel Syndrome",
                "Gastritis"
            ]
            confidence = max(confidence, 91.0)
            triage_reason = "Acute diarrhea and fluid stool presentation"
        else:
            primary_disease = "Gastritis"
            differentials = [
                "Gastritis",
                "Gastroesophageal Reflux Disease (GERD)",
                "Peptic Ulcer Disease",
                "Dyspepsia"
            ]
            confidence = max(confidence, 87.0)
            triage_reason = "Epigastric discomfort and dyspeptic presentation"

    # ── RULE 5: Vague Fatigue & Weakness Presentation (Disambiguation First) ───
    elif flags["has_fatigue"] and not flags["has_fever"] and not flags["has_respiratory"] and not flags["has_gi"]:
        # Check if follow-up disambiguation answers are present in context
        if re.search(r"\b(pale|skin\s+peeli|peeli|anemia|khoon\s+ki\s+kami|breathless\s+on\s+walk)\b", cleaned_lower):
            primary_disease = "Iron Deficiency Anemia"
            differentials = ["Iron Deficiency Anemia", "Vitamin B12 Deficiency", "Generalized Fatigue & Weakness Evaluation", "Thalassemia Minor"]
            confidence = 88.0
            triage_reason = "Fatigue with pale skin and exertional shortness of breath"
        elif re.search(r"\b(weight\s+gain|wajan\s+badha|cold\s+intoleran|sardi\s+zyada|thyroid)\b", cleaned_lower):
            primary_disease = "Hypothyroidism"
            differentials = ["Hypothyroidism", "Generalized Fatigue & Weakness Evaluation", "Metabolic Syndrome", "Depression"]
            confidence = 88.0
            triage_reason = "Fatigue with weight gain and cold intolerance"
        elif re.search(r"\b(sugar|thirst|pyaas|frequent\s+urinat|peshab\s+bar|diabetes)\b", cleaned_lower):
            primary_disease = "Type 2 Diabetes Mellitus"
            differentials = ["Type 2 Diabetes Mellitus", "Prediabetes", "Generalized Fatigue & Weakness Evaluation", "Chronic Kidney Disease"]
            confidence = 88.0
            triage_reason = "Fatigue with polydipsia and frequent urination"
        elif re.search(r"\b(viral|fever\s+ke\s+baad|after\s+fever|infection)\b", cleaned_lower):
            primary_disease = "Post-Viral Asthenia"
            differentials = ["Post-Viral Asthenia", "Generalized Fatigue & Weakness Evaluation", "Chronic Fatigue Syndrome", "Iron Deficiency Anemia"]
            confidence = 85.0
            triage_reason = "Post-infectious recuperation fatigue"
        else:
            primary_disease = "Generalized Fatigue & Weakness Evaluation"
            differentials = [
                "Generalized Fatigue & Weakness Evaluation",
                "Iron Deficiency Anemia",
                "Hypothyroidism",
                "Type 2 Diabetes Mellitus"
            ]
            confidence = 90.0
            triage_reason = "Vague non-specific fatigue; requires targeted clinical disambiguation workup"

    # ── RULE 6: Dizziness / Vertigo Presentation ─────────────────────────────
    elif flags["has_dizziness"] and not flags["has_chest_pain"]:
        primary_disease = "Dizziness & Vertigo Evaluation"
        differentials = [
            "Dizziness & Vertigo Evaluation",
            "Benign Paroxysmal Positional Vertigo (BPPV)",
            "Orthostatic Hypotension (Low BP on standing)",
            "Inner Ear Labyrinthitis"
        ]
        confidence = 88.0
        triage_reason = "Dizziness presentation requiring positional vs systemic disambiguation"

    # ── RULE 7: True Pneumonia Validation (Requires Respiratory Signs) ───────
    elif ml_predicted_disease and "pneumonia" in ml_predicted_disease.lower():
        if flags["has_respiratory"] or flags["has_cough"] or flags["has_breathless"]:
            primary_disease = ml_predicted_disease
            differentials = [ml_predicted_disease, "Acute Bronchitis", "Influenza", "COVID-19"]
            confidence = max(confidence, 65.0)
            triage_reason = "Respiratory symptoms present consistent with lower respiratory infection"
        else:
            primary_disease = "Acute Viral Fever"
            differentials = [
                "Acute Viral Fever",
                "Upper Respiratory Tract Infection (Common Cold)",
                "Influenza",
                "Enteric Fever (Typhoid)"
            ]
            confidence = 88.0
            triage_reason = "Rejected Pneumonia due to absence of cardinal respiratory signs"

    # ── RULE 8: Hair & Scalp Presentation (Trichology / Dermatology) ─────────
    elif flags["has_hair"]:
        primary_disease = "Telogen Effluvium (Hair Fall)"
        differentials = [
            "Telogen Effluvium (Hair Fall)",
            "Androgenetic Alopecia (Male)",
            "Female Pattern Hair Loss",
            "Alopecia Areata",
        ]
        confidence = 92.0
        triage_reason = "Hair shedding and scalp presentation"

    # ── RULE 9: Musculoskeletal, Back & Joint Presentation (Orthopedics) ─────
    elif flags["has_ortho"] and not flags["has_fever"]:
        if re.search(r"\b(back|kamar|spine|slip\s+disc|sciatica)\b", cleaned_lower):
            primary_disease = "Lumbar Spondylosis (Lower Back Pain)"
            differentials = [
                "Lumbar Spondylosis (Lower Back Pain)",
                "Sciatica / Lumbar Disc Herniation",
                "Acute Lumbago / Muscle Spasm",
                "Degenerative Disc Disease",
            ]
        elif re.search(r"\b(knee|ghutne|joint|arthritis|gathiya|stiffness)\b", cleaned_lower):
            primary_disease = "Osteoarthritis (Knee)"
            differentials = [
                "Osteoarthritis (Knee)",
                "Rheumatoid Arthritis",
                "Gouty Arthritis",
                "Prepatellar Bursitis",
            ]
        else:
            primary_disease = "Lumbar Spondylosis (Lower Back Pain)"
            differentials = ["Lumbar Spondylosis (Lower Back Pain)", "Osteoarthritis (Knee)", "Cervical Spondylosis"]
        confidence = 90.0
        triage_reason = "Musculoskeletal joint/spinal pain presentation"

    # ── RULE 10: Oral & Dental Presentation (Dentistry) ───────────────────────
    elif flags["has_dental"] and not flags["has_respiratory"]:
        primary_disease = "Dental Caries / Pulpitis"
        differentials = [
            "Dental Caries / Pulpitis",
            "Gingivitis / Periodontitis",
            "Periapical Abscess",
            "Aphthous Stomatitis (Mouth Ulcers)",
        ]
        confidence = 93.0
        triage_reason = "Dental and periodontal presentation"

    # ── RULE 11: Eye & Vision Presentation (Ophthalmology) ───────────────────
    elif flags["has_eye"] and not flags["has_chest_pain"]:
        primary_disease = "Acute Conjunctivitis"
        differentials = [
            "Acute Conjunctivitis",
            "Dry Eye Syndrome",
            "Allergic Conjunctivitis",
            "Refractive Error / Eye Strain",
        ]
        confidence = 91.0
        triage_reason = "Ophthalmic presentation"

    # ── RULE 12: Endocrine & Metabolic (Diabetes / Thyroid) ──────────────────
    elif flags["has_diabetes"]:
        primary_disease = "Type 2 Diabetes Mellitus"
        differentials = [
            "Type 2 Diabetes Mellitus",
            "Impaired Fasting Glucose",
            "Metabolic Syndrome",
            "Primary Hypothyroidism",
        ]
        confidence = 90.0
        triage_reason = "Metabolic hyperglycemia presentation"

    # ── RULE 13: Urinary & Renal Presentation (Urology / Nephrology) ─────────
    elif flags["has_urinary"] and not flags["has_hair"]:
        if re.search(r"\b(pathri|kidney\s+stone|flank|renal\s+colic)\b", cleaned_lower):
            primary_disease = "Renal Calculi (Kidney Stone)"
            differentials = ["Renal Calculi (Kidney Stone)", "Urinary Tract Infection", "Ureteric Colic", "Acute Cystitis"]
        else:
            primary_disease = "Urinary Tract Infection"
            differentials = ["Urinary Tract Infection", "Acute Cystitis", "Urethritis", "Renal Calculi (Kidney Stone)"]
        confidence = 92.0
        triage_reason = "Urinary tract irritation and dysuria presentation"

    # ── RULE 14: Skin & Allergy Presentation (Dermatology) ────────────────────
    elif flags["has_skin"] and not flags["has_fever"] and not flags["has_hair"]:
        if re.search(r"\b(pimple|acne)\b", cleaned_lower):
            primary_disease = "Acne Vulgaris"
            differentials = ["Acne Vulgaris", "Folliculitis", "Contact Dermatitis / Eczema", "Seborrheic Dermatitis"]
        elif re.search(r"\b(fungal|ringworm|daad)\b", cleaned_lower):
            primary_disease = "Tinea Corporis (Fungal Infection)"
            differentials = ["Tinea Corporis (Fungal Infection)", "Contact Dermatitis / Eczema", "Pityriasis Versicolor", "Urticaria"]
        else:
            primary_disease = "Contact Dermatitis / Eczema"
            differentials = ["Contact Dermatitis / Eczema", "Urticaria", "Atopic Dermatitis", "Tinea Corporis (Fungal Infection)"]
        confidence = 91.0
        triage_reason = "Dermatological eruption and pruritus presentation"

    # ── RULE 15: Mental Health & Sleep ───────────────────────────────────────
    elif flags["has_mental"] and not flags["has_chest_pain"] and not flags["has_fever"]:
        primary_disease = "Generalized Anxiety Disorder"
        differentials = [
            "Generalized Anxiety Disorder",
            "Primary Insomnia",
            "Panic Disorder",
            "Major Depressive Disorder",
        ]
        confidence = 88.0
        triage_reason = "Anxiety, tension, and sleep disturbance presentation"

    # ── RULE 16: High Confidence ML Prediction (> 28%) with Cardinal Support ──
    if not primary_disease:
        if ml_predicted_disease and ml_confidence >= 28.0:
            primary_disease = ml_predicted_disease
            if top_predictions:
                differentials = [p["disease"] for p in top_predictions[:4]]
            else:
                differentials = [ml_predicted_disease]
            triage_reason = f"High-confidence ML model prediction ({ml_confidence:.1f}%)"
        elif parsed["clinical_hints"]:
            hint = parsed["clinical_hints"][0]
            hint_map = {
                "tension headache": "Tension Headache",
                "acute viral fever": "Acute Viral Fever",
                "common cold": "Upper Respiratory Tract Infection (Common Cold)",
                "acute gastroenteritis": "Acute Gastroenteritis",
                "gastritis": "Gastritis",
                "migraine": "Migraine",
                "vertigo": "Dizziness & Vertigo Evaluation",
                "fatigue and weakness": "Generalized Fatigue & Weakness Evaluation",
                "hair fall": "Telogen Effluvium (Hair Fall)",
                "dandruff": "Telogen Effluvium (Hair Fall)",
                "dermatitis": "Contact Dermatitis / Eczema",
                "lumbar spondylosis": "Lumbar Spondylosis (Lower Back Pain)",
                "osteoarthritis": "Osteoarthritis (Knee)",
                "cervical spondylosis": "Cervical Spondylosis",
                "dental caries": "Dental Caries / Pulpitis",
                "conjunctivitis": "Acute Conjunctivitis",
                "urinary tract infection": "Urinary Tract Infection",
                "renal calculi": "Renal Calculi (Kidney Stone)",
                "type 2 diabetes": "Type 2 Diabetes Mellitus",
                "hypothyroidism": "Hypothyroidism",
                "generalized anxiety": "Generalized Anxiety Disorder",
            }
            primary_disease = hint_map.get(hint, ml_predicted_disease or "Clinical Health Evaluation")
            differentials = [primary_disease]
            confidence = max(confidence, 85.0)
            triage_reason = f"Derived from normalized clinical hint: {hint}"
        else:
            primary_disease = ml_predicted_disease or "Clinical Health Evaluation"
            confidence = max(confidence, 50.0)
            differentials = [primary_disease]
            triage_reason = "Standard baseline clinical evaluation"

    # Deduplicate differentials while keeping primary first
    deduped_diffs = [primary_disease]
    for d in differentials:
        if d and d not in deduped_diffs:
            deduped_diffs.append(d)

    return {
        "primary_disease": primary_disease,
        "confidence": round(float(confidence), 1),
        "differentials": deduped_diffs[:4],
        "normalized_context": parsed,
        "triage_reason": triage_reason,
    }
