import json
import logging
import os
import re
from collections import OrderedDict

from rapidfuzz import fuzz, process


ai_cache = OrderedDict()
logger = logging.getLogger(__name__)
gemini_api_key = None

EMERGENCY_RED_FLAGS = [
    (r"\b(crushing\s+chest\s+pain|chest\s+pain|radiating\s+to\s+(?:left\s+)?arm|heart\s+attack|cardiac\s+arrest)\b", "Severe chest discomfort or acute cardiac risk"),
    (r"\b(can'?t\s+breathe|severe\s+shortness\s+of\s+breath|gasping\s+for\s+air|suffocating|turning\s+blue|cyanosis)\b", "Acute respiratory distress"),
    (r"\b(facial\s+droop|slurred\s+speech|sudden\s+weakness\s+on\s+one\s+side|loss\s+of\s+consciousness|passed\s+out|unconscious)\b", "Acute neurological deficit or stroke warning"),
    (r"\b(coughing\s+(?:up\s+)?blood|vomiting\s+blood|uncontrollable\s+bleeding|severe\s+head\s+injury)\b", "Acute hemorrhage or traumatic injury"),
    (r"\b(throat\s+closing|swollen\s+throat|anaphylaxis|swollen\s+tongue)\b", "Suspected anaphylaxis or airway compromise"),
]

ANALYSIS_DEFAULTS = {
    "presenting_complaint": "No presenting complaint was generated.",
    "differential_diagnoses": "No differential diagnoses were generated.",
    "investigations": "No investigations were generated.",
    "treatment": "No treatment guidance was generated.",
    "medications": "No medication guidance was generated.",
    "precautions": "No precautions were generated.",
    "disclaimer": "This is an AI-generated analysis and should not replace professional medical advice.",
    "red_flag_alert": None,
    # Clinical KB enrichment fields (populated when KB match is found)
    "medication_card": None,
    "hindi_names": "",
    "specialty_category": "",
    "typical_duration": "",
    "emergency_flags": [],
}
ANALYSIS_LIST_KEYS = {
    "differential_diagnoses",
    "investigations",
    "treatment",
    "medications",
    "precautions",
}

DISEASE_QUESTIONS = {
    "fever": [
        "How high is your fever right now?",
        "Are you also having chills or strong body aches?",
        "Did the fever start suddenly or build up slowly?",
        "Do you have a cough, sore throat, or runny nose?",
        "Have you travelled recently or been around anyone sick?"
    ],
    "diabetes": [
        "Have you been feeling unusually thirsty?",
        "Are you urinating more often than usual?",
        "Have you noticed any unexplained weight changes?",
        "Do you often feel tired or low on energy?",
        "Do you have a family history of diabetes?"
    ],
    "migraine": [
        "Is the headache one-sided or all over the head?",
        "Are you sensitive to light or sound?",
        "Do you feel nauseated during the headache?",
        "How long does the headache usually last?"
    ],
    "depression": [
        "How long have you been feeling low or emotionally drained?",
        "Have you lost interest in things you usually enjoy?",
        "Has your sleep changed recently?",
        "Are you finding it difficult to focus or make decisions?"
    ],
    "heart disease": [
        "Are you feeling chest pain, pressure, or tightness?",
        "Do you get short of breath during normal activity?",
        "Do you have a history of high blood pressure?",
        "Is there a family history of heart disease?"
    ],
    "covid-19": [
        "Have you noticed fever, cough, or body aches?",
        "Have you lost taste or smell recently?",
        "Have you been in contact with anyone unwell?",
        "Are your symptoms improving, stable, or worsening?"
    ],
    "asthma": [
        "Do you wheeze or feel tightness in your chest?",
        "Do symptoms get worse with exercise or dust exposure?",
        "Are symptoms worse at night?",
        "Do you have an inhaler and has it helped?"
    ],
    "gastritis": [
        "Are you feeling burning pain or heaviness in the upper abdomen?",
        "Do symptoms get worse after eating spicy or oily food?",
        "Are you feeling bloated or nauseated?",
        "Have you taken painkillers regularly in the last few days?"
    ],
    "Generalized Fatigue & Weakness Evaluation": [
        "Kya thakan ke saath saans phoolti hai, chakkar aate hain, ya skin peeli/pale lagti hai? (Anemia check)",
        "Kya pichle kuch dino/mahino me wajan achanak badha ya ghata hai, ya sardi/garmi zyada lagti hai? (Thyroid check)",
        "Kya pyaas zyada lagti hai, bhookh zyada lagti hai aur peshab bar-bar aata hai? (Diabetes check)",
        "Kya neend theek se puri ho rahi hai aur pichle kuch dino me bohot zyada stress ya mental exhaustion raha hai?",
        "Kya halka bukhar, body ache, ya kisi viral infection ke baad se yeh kamzori shuru hui hai? (Post-viral check)"
    ],
    "fatigue": [
        "Kya thakan ke saath saans phoolti hai, chakkar aate hain, ya skin peeli/pale lagti hai? (Anemia check)",
        "Kya pichle kuch dino/mahino me wajan achanak badha ya ghata hai, ya sardi/garmi zyada lagti hai? (Thyroid check)",
        "Kya pyaas zyada lagti hai, bhookh zyada lagti hai aur peshab bar-bar aata hai? (Diabetes check)",
        "Kya neend theek se puri ho rahi hai aur pichle kuch dino me bohot zyada stress ya mental exhaustion raha hai?",
        "Kya halka bukhar, body ache, ya kisi viral infection ke baad se yeh kamzori shuru hui hai? (Post-viral check)"
    ],
    "Dizziness & Vertigo Evaluation": [
        "Kya sar ghumne ka ehsaas gardan ghumane ya let kar uthne par hota hai? (BPPV / Inner ear check)",
        "Kya achanak khade hone par aankhon ke aage andhera chha jata hai? (Low BP / Orthostatic check)",
        "Kya kaano me seeti jaisi aawaz (tinnitus) ya sunne me koi kami mehsus hoti hai?",
        "Kya paani kam peene se dehydration ya kamzori aur thakan lag rahi hai?",
        "Kya chest discomfort, ghabrahat ya irregular heartbeat mehsus hoti hai?"
    ],
    "dizziness": [
        "Kya sar ghumne ka ehsaas gardan ghumane ya let kar uthne par hota hai? (BPPV / Inner ear check)",
        "Kya achanak khade hone par aankhon ke aage andhera chha jata hai? (Low BP / Orthostatic check)",
        "Kya kaano me seeti jaisi aawaz (tinnitus) ya sunne me koi kami mehsus hoti hai?",
        "Kya paani kam peene se dehydration ya kamzori aur thakan lag rahi hai?",
        "Kya chest discomfort, ghabrahat ya irregular heartbeat mehsus hoti hai?"
    ]
}

DEFAULT_FOLLOWUP_QUESTIONS = [
    "How severe is this problem on a scale from 1 to 10?",
    "How long have you been dealing with these symptoms?",
    "Have you taken any medicine or home treatment yet?",
    "What symptom is worrying you the most right now?"
]


def configure_ai():
    """Store configuration without importing the heavy Gemini SDK at app boot."""
    global gemini_api_key
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key and api_key.strip().lower() not in {
        "",
        "your-gemini-api-key-here",
        "replace-with-your-gemini-key",
        "replace-me",
        "changeme",
        "demo-key",
    }:
        gemini_api_key = api_key


def get_gemini_client():
    """Load Gemini only when a user requests an AI analysis."""
    if not gemini_api_key:
        return None
    import google.generativeai as genai

    genai.configure(api_key=gemini_api_key)
    return genai


def scan_emergency_red_flags(symptoms_text):
    text = (symptoms_text or "").casefold()
    if not text.strip():
        return {
            "is_emergency": False,
            "severity": "STANDARD",
            "flags": [],
            "advisory": None,
        }

    detected = []
    for pattern, description in EMERGENCY_RED_FLAGS:
        for match in re.finditer(pattern, text):
            start = match.start()
            end = match.end()
            # 1. Prefix negation check (e.g., "no chest pain", "not feeling shortness of breath", "denies ...")
            prefix = text[max(0, start - 35):start]
            if re.search(r"\b(no|not|denies|denied|without|negative\s+for|rules?\s+out|never)\s*$", prefix):
                continue
            # 2. Suffix negation check (e.g., "shortness of breath: No", "chest pain - denied")
            suffix = text[end:min(len(text), end + 35)]
            if re.search(r"^\s*[:\-\—\?]?\s*(no|denied|none|absent|not\s+experienced|not\s+present)\b", suffix):
                continue
            detected.append(description)
            break

    if detected:
        return {
            "is_emergency": True,
            "severity": "CRITICAL",
            "flags": detected,
            "advisory": (
                "Urgent Medical Alert: Symptoms include clinical red-flag criteria. "
                "Do not wait for standard clinic hours. Call emergency services (999 / 911 / 112) "
                "or proceed to the nearest emergency department immediately."
            ),
        }
    return {
        "is_emergency": False,
        "severity": "STANDARD",
        "flags": [],
        "advisory": None,
    }


def normalize_analysis_payload(payload):
    result = {
        key: payload.get(key) or default
        for key, default in ANALYSIS_DEFAULTS.items()
    }
    # If medication_card is missing (e.g. from raw Gemini output), enrich from Clinical KB
    if not result.get("medication_card"):
        diffs = str(result.get("differential_diagnoses") or "").strip()
        if diffs:
            first_diff = re.split(r"[;,\n]", diffs)[0].strip()
            first_diff = re.sub(r"^\d+[\.\)]\s*", "", first_diff).strip()
            if first_diff:
                try:
                    from app.services.clinical_kb import get_medication_card, lookup_disease
                    card = get_medication_card(first_diff)
                    if card:
                        result["medication_card"] = card
                    prof = lookup_disease(first_diff)
                    if prof:
                        if not result.get("hindi_names") and prof.get("hindi_names"):
                            result["hindi_names"] = prof["hindi_names"]
                        if not result.get("typical_duration") and prof.get("typical_duration"):
                            result["typical_duration"] = prof["typical_duration"]
                        if not result.get("specialty_category") and prof.get("specialty_category"):
                            result["specialty_category"] = prof["specialty_category"]
                except Exception as exc:
                    logger.debug("Failed to enrich payload with clinical KB: %s", exc)

    # If red_flag_alert is not explicitly passed, scan the presenting complaint
    if not result.get("red_flag_alert"):
        complaint = result.get("presenting_complaint", "")
        scan = scan_emergency_red_flags(complaint)
        if scan["is_emergency"]:
            result["red_flag_alert"] = scan
    return result


def analysis_text(value):
    if isinstance(value, list):
        return ", ".join(filter(None, [analysis_text(item) for item in value]))
    if isinstance(value, dict):
        parts = [f"{key}: {analysis_text(item)}" for key, item in value.items() if item]
        return "; ".join(parts)
    text = str(value or "").replace("\r", "\n").replace("\\n", "\n").strip()
    text = text.strip("[]")
    text = re.sub(r"^[\"']+|[\"']+$", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def analysis_points(value, max_items=6):
    if isinstance(value, list):
        raw_chunks = [analysis_text(item) for item in value]
    elif isinstance(value, dict):
        raw_chunks = [f"{key}: {analysis_text(item)}" for key, item in value.items() if item]
    else:
        normalized = str(value or "").replace("\r", "\n").replace("\\n", "\n").strip()
        normalized = normalized.strip("[]")
        normalized = normalized.replace('", "', '"\n"').replace("', '", "'\n'")
        raw_chunks = re.split(r"\n+|;\s+|\s\|\s", normalized)

    points = []
    for chunk in raw_chunks:
        piece = analysis_text(chunk)
        piece = re.sub(r"^[\-\u2022\*\d\.\)\(]+\s*", "", piece)
        piece = piece.strip(" \"'")
        if not piece:
            continue
        if len(piece) > 180 and len(raw_chunks) == 1:
            for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z])", piece):
                sentence = analysis_text(sentence)
                if sentence:
                    points.append(sentence)
        else:
            points.append(piece)

    deduped = []
    seen = set()
    for point in points:
        key = point.casefold()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(point)

    return deduped[:max_items] or [analysis_text(value)]


def analysis_summary(value, max_items=2):
    points = analysis_points(value, max_items=max_items)
    return " ".join(points[:max_items]).strip()


def clean_json_response(raw_json):
    cleaned = (raw_json or "").strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines)
    cleaned = re.sub(r"//.*", "", cleaned)
    return cleaned.strip()


def parse_ai_analysis(ai_response):
    parsed_response = json.loads(clean_json_response(ai_response))
    if not isinstance(parsed_response, dict):
        raise ValueError("AI response was not a valid JSON object.")
    return normalize_analysis_payload(parsed_response)


def validate_symptoms(symptoms):
    normalized = (symptoms or "").strip()
    if len(normalized) < 10:
        return "Please describe your symptoms in a bit more detail."
    if len(normalized) > 1000:
        return "Symptoms are too long. Please keep the description under 1000 characters."
    return None


class ClinicalQuestion(str):
    """
    Subclass of str representing a clinical intake question with quick suggestion chips.
    100% backward-compatible with legacy code that expects plain strings.
    """
    def __new__(cls, question_text, chips=None):
        obj = super().__new__(cls, question_text)
        obj.question = str(question_text)
        obj.chips = list(chips or [])
        return obj

    def __getitem__(self, key):
        if key == "question":
            return str(self)
        if key == "chips":
            return self.chips
        return super().__getitem__(key)

    def get(self, key, default=None):
        if key == "question":
            return str(self)
        if key == "chips":
            return self.chips
        return default


def generate_followup_questions(symptoms, matched_disease=None):
    """
    Generate professional, unbiased clinical intake questions tailored by medical domain.
    In clinical medicine, history-taking is strictly tailored to the affected organ system
    without assuming or declaring a diagnosis prematurely.
    """
    symp_lower = (symptoms or "").lower()
    matched_lower = (matched_disease or "").lower()

    # Look up specialty category and knowledge base profile
    kb_specialty = ""
    try:
        from app.services.clinical_engine import get_knowledge
        kb = get_knowledge()
        kb_profile = kb.get(matched_disease, {}) if matched_disease else {}
        kb_specialty = str(kb_profile.get("specialty_category", "")).lower()
    except Exception:
        kb_profile = {}

    combined = f"{symp_lower} {matched_lower} {kb_specialty}"

    # ── 1. Hair & Scalp (Trichology / Dermatology) ───────────────────────────
    if any(k in combined for k in ["hair", "hairfall", "alopecia", "baal", "bald", "dandruff", "scalp", "telogen", "effluvium", "follicle", "tricholog"]):
        return [
            ClinicalQuestion(
                "How would you describe your hair loss pattern (diffuse thinning all over, round circular bald patches, or receding frontal hairline)?",
                ["Diffuse overall thinning", "Circular bald patches (Alopecia)", "Receding hairline / temples", "Excessive daily shedding"]
            ),
            ClinicalQuestion(
                "Do you have any scalp symptoms like dandruff, itching, burning, redness, or oily flakes?",
                ["Dandruff & flaky scalp", "Severe itching & redness", "Painful scalp bumps", "No scalp symptoms / clean"]
            ),
            ClinicalQuestion(
                "Have you had recent blood tests (Thyroid/TSH, Iron/Ferritin, Vitamin D/B12), or had severe illness/fever/stress 2-3 months prior?",
                ["Low Iron / Vitamin D", "Thyroid imbalance", "Started post-illness/stress", "Never had blood tests done"]
            ),
            ClinicalQuestion(
                "Have you applied or taken any hair treatments like Minoxidil topical serum, Biotin supplements, or medicated shampoo?",
                ["None taken yet", "Biotin / Multivitamins", "Minoxidil topical serum", "Medicated anti-dandruff shampoo"]
            ),
            ClinicalQuestion(
                "Is there a family history of early hair thinning or baldness, and has the shedding gotten progressively worse?",
                ["Family history present", "No family history", "Gradually worsening", "Stable / constant shedding"]
            )
        ]

    # ── 2. Oral & Dental (Dentistry) ─────────────────────────────────────────
    elif any(k in combined for k in ["tooth", "teeth", "daant", "dant", "gum", "gums", "masudo", "masooro", "cavity", "dental", "dentistry", "odontalgia", "ulcer", "chhale", "gingiv", "periodont", "pulpitis"]):
        return [
            ClinicalQuestion(
                "Which tooth or area is painful, and is the pain sharp, throbbing, or a continuous dull ache?",
                ["Sharp throbbing toothache", "Dull continuous ache", "Back molar tooth", "Front teeth / gums"]
            ),
            ClinicalQuestion(
                "Do you experience sharp sensitivity or pain when drinking cold water, hot tea, or eating sweet foods?",
                ["Extreme cold sensitivity", "Pain on hot food / drinks", "Pain when biting / chewing", "No temperature sensitivity"]
            ),
            ClinicalQuestion(
                "Is there visible gum swelling, bleeding when brushing, a visible cavity hole, or pus discharge?",
                ["Swollen bleeding gums", "Visible black cavity hole", "Mouth ulcer / sore spot", "No visible swelling"]
            ),
            ClinicalQuestion(
                "Have you taken any pain relievers, rinsed with warm salt water, or applied clove oil / dental gel?",
                ["Warm salt water rinses", "Clove oil / Dental gel", "Painkiller (Paracetamol/Ibuprofen)", "None tried yet"]
            ),
            ClinicalQuestion(
                "Does the toothache radiate to your ear, jaw, or head, especially when lying down at night?",
                ["Disturbing sleep at night", "Radiating to ear / jaw", "Only when chewing food", "Manageable during day"]
            )
        ]

    # ── 3. Skin, Rash & Allergy (Dermatology) ────────────────────────────────
    elif any(k in combined for k in ["skin", "rash", "khujli", "itch", "pimples", "pimple", "acne", "eczema", "hives", "urticaria", "ringworm", "fungal", "daad", "psoriasis", "dermatology", "dermatitis"]):
        return [
            ClinicalQuestion(
                "Where on your body is the rash or irritation located, and does it feel like intense itching, burning, or stinging?",
                ["Intense itching", "Burning sensation", "Face & neck only", "Arms, legs or body folds"]
            ),
            ClinicalQuestion(
                "What do the skin lesions look like (raised red bumps/hives, dry peeling flakes, fluid blisters, or circular rings)?",
                ["Raised red bumps / hives", "Dry peeling / scaly patches", "Circular ring-like patches", "Pustules / pimples"]
            ),
            ClinicalQuestion(
                "Did this begin after contact with a new soap, cosmetic, detergent, plant, pet, or medication?",
                ["After new cosmetic / soap", "Suspected food / drug allergy", "Worse in hot / humid weather", "No clear trigger identified"]
            ),
            ClinicalQuestion(
                "Have you applied any topical ointments (antifungal, calamine, moisturizer) or taken antihistamines (like Cetirizine)?",
                ["None applied yet", "Antihistamine (Cetirizine)", "Calamine lotion / Moisturizer", "Medicated antifungal cream"]
            ),
            ClinicalQuestion(
                "Is the rash spreading to new areas or staying confined to the original location?",
                ["Spreading to new areas", "Confined to same area", "Improving with moisturizers", "Intermittent / comes and goes"]
            )
        ]

    # ── 4. Musculoskeletal, Spine, Shoulder & Joint (Orthopedics) ────────────
    elif any(k in combined for k in ["kamar", "back", "spine", "knee", "ghutne", "joint", "joints", "jodo", "arthritis", "gathiya", "sciatica", "cervical", "neck", "shoulder", "kandha", "kandhe", "frozen", "arm", "capsulitis", "sprain", "spondylosis", "orthopedic", "ortho", "rheumatol", "bone", "musculoskeletal"]):
        return [
            ClinicalQuestion(
                "Where is the pain most intense, and does it radiate anywhere (such as down your leg, buttocks, or arm)?",
                ["Lower back only", "Radiating down leg / sciatica", "Knee joint / difficulty bending", "Neck & shoulder area"]
            ),
            ClinicalQuestion(
                "Is the pain worse in the morning upon waking, or does it worsen after prolonged sitting, walking, or lifting weights?",
                ["Morning stiffness (>30 mins)", "Worse after sitting / bending", "Worse when walking or stairs", "Continuous aching pain"]
            ),
            ClinicalQuestion(
                "Are you experiencing visible joint swelling, warmth, numbness, tingling, or weakness in your limbs?",
                ["Visible swelling & warmth", "Numbness / tingling sensation", "No swelling or numbness", "Joint cracking / clicking sounds"]
            ),
            ClinicalQuestion(
                "Have you used any pain-relief sprays/balms, hot/cold compress, physiotherapy, or pain relievers?",
                ["None taken yet", "Pain balm / Spray", "Hot / cold pack", "Paracetamol / Painkiller"]
            ),
            ClinicalQuestion(
                "How is this affecting your daily movement (walking, standing, climbing stairs, or working)?",
                ["Difficulty climbing stairs", "Unable to sit or stand long", "Mildly uncomfortable only", "Significantly limiting mobility"]
            )
        ]

    # ── 5. Eye & Vision (Ophthalmology) ───────────────────────────────────────
    elif any(k in combined for k in ["aankh", "eye", "vision", "conjunctivitis", "blurry", "redness"]):
        return [
            ClinicalQuestion(
                "Are both eyes affected or only one, and is there redness, itching, grittiness, or sharp pain?",
                ["Both eyes affected", "One eye only", "Redness & grittiness", "Itching & watery eyes"]
            ),
            ClinicalQuestion(
                "Is there any discharge (sticky yellow crusting, white mucus, or watery tears)?",
                ["Yellow sticky crust in morning", "Watery tears only", "Dry gritty feeling", "No discharge"]
            ),
            ClinicalQuestion(
                "Have you noticed any blurred vision, halos around lights, or extreme sensitivity to bright light?",
                ["Sensitive to light (photophobia)", "Mildly blurred vision", "Vision is completely clear", "Pain on moving eyes"]
            ),
            ClinicalQuestion(
                "Do you wear contact lenses, spend long hours in front of screens, or had recent dust exposure?",
                ["High screen time / digital strain", "Contact lens wearer", "Dust / allergen exposure", "No clear trigger"]
            ),
            ClinicalQuestion(
                "Have you used any lubricating eye drops or antibiotic drops yet?",
                ["Lubricating tears (CMC)", "Washed with clean water", "Antibiotic / Antiallergic drops", "None used yet"]
            )
        ]

    # ── 6. Endocrine & Diabetes (Endocrinology) ──────────────────────────────
    elif any(k in combined for k in ["sugar", "diabetes", "diabetic", "thirst", "pyaas", "thyroid"]):
        return [
            ClinicalQuestion(
                "Have you checked your blood sugar recently? What were your approximate fasting or post-meal readings?",
                ["Fasting > 140 mg/dL", "Post-meal > 200 mg/dL", "Borderline / Pre-diabetes", "Not checked recently"]
            ),
            ClinicalQuestion(
                "Are you experiencing excessive unquenchable thirst, dry mouth, or unusually increased hunger?",
                ["Excessive unquenchable thirst", "Dry mouth constantly", "Increased hunger / cravings", "No unusual thirst"]
            ),
            ClinicalQuestion(
                "Have you noticed frequent urination at night, unexplained weight changes, or cuts healing slowly?",
                ["Waking multiple times to urinate", "Unexplained weight loss", "Slow wound healing / cuts", "Extreme tiredness after meals"]
            ),
            ClinicalQuestion(
                "Are you currently taking any diabetes medications (like Metformin), thyroid medicine, or following a specific diet?",
                ["Taking Metformin / Tablets", "On Insulin therapy", "Diet & walking control only", "Not on any medication yet"]
            ),
            ClinicalQuestion(
                "Are you experiencing any numbness, burning, or tingling in your feet or fingers?",
                ["Tingling / numbness in feet", "Burning soles at night", "Occasional cramps", "No foot numbness"]
            )
        ]

    # ── 7. Urinary & Renal (Urology / Nephrology) ─────────────────────────────
    elif any(k in combined for k in ["peshab", "urine", "urination", "dysuria", "pathri", "kidney stone", "flank"]):
        return [
            ClinicalQuestion(
                "Is there a burning sensation or stinging pain during or immediately after passing urine?",
                ["Severe burning sensation", "Mild stinging at end", "Pain in lower pelvis", "No burning sensation"]
            ),
            ClinicalQuestion(
                "How frequently do you need to pass urine, and do you feel an urgent need even when very little urine comes out?",
                ["Every 30-60 minutes", "Urgent feeling with low output", "Waking up 3+ times at night", "Normal frequency"]
            ),
            ClinicalQuestion(
                "Have you noticed any pink, reddish, or cloudy color in the urine, or a strong unpleasant odor?",
                ["Cloudy with strong smell", "Dark concentrated yellow", "Pinkish or bloody tinge", "Clear normal color"]
            ),
            ClinicalQuestion(
                "Are you having fever with chills, or severe pain in your lower back / flank side?",
                ["High fever with chills / shivering", "Severe one-sided flank pain", "Lower abdomen cramping", "No fever or back pain"]
            ),
            ClinicalQuestion(
                "Have you taken any urinary alkalizer syrup, antibiotics, or increased your daily water intake?",
                ["Increased water / coconut water", "Urinary alkalizer syrup", "Antibiotics prescribed earlier", "None taken yet"]
            )
        ]

    # ── 8. Digestive, Acidity & Gut (Gastroenterology) ────────────────────────
    elif any(k in combined for k in ["acidity", "gas", "pet", "belly", "stomach", "loose motion", "dast", "diarrhea", "vomit", "nausea", "constipation", "kabz", "heartburn", "gerd", "reflux", "esophagitis", "gastritis", "ulcer", "indigestion", "bloating", "piles", "gastro"]):
        return [
            ClinicalQuestion(
                "Where is the abdominal discomfort located, and does it feel like burning, cramping, sharp pain, or fullness?",
                ["Burning in chest & food pipe (Acidity)", "Upper stomach heaviness / gas", "Lower abdomen cramps", "Navel area sharp pain"]
            ),
            ClinicalQuestion(
                "Does the discomfort happen on an empty stomach, or does it trigger after eating oily, spicy, or heavy foods?",
                ["After spicy / fried food", "On empty stomach in morning", "Immediately after any meal", "Constant regardless of food"]
            ),
            ClinicalQuestion(
                "Are you having nausea, vomiting, loose motions, or difficulty passing stool (constipation)?",
                ["Watery loose motions", "Nausea & sour burps", "Hard stools / constipation", "No vomiting or loose motions"]
            ),
            ClinicalQuestion(
                "Have you taken any antacids (Digene/Gelusil), acidity tablets (Pantoprazole/Omeprazole), ORS, or digestive remedies?",
                ["Antacid gel (Digene/Gelusil)", "Acidity tablet (Pantoprazole)", "ORS / electrolyte fluids", "None taken yet"]
            ),
            ClinicalQuestion(
                "Have you noticed any black-colored stools, blood in vomit/stool, or severe fever?",
                ["None of these red flags", "Stomach cramps with loose stool", "Mild fever present", "Extreme weakness & dehydration"]
            )
        ]

    # ── 9. Respiratory & Throat (Pulmonology / ENT) ───────────────────────────
    elif any(k in combined for k in ["cough", "khansi", "cold", "sore throat", "gala", "phlegm", "saans", "breathless", "wheez", "asthma", "chest congestion", "sinus", "ear", "kaan", "pulmono", "ent", "respiratory"]):
        return [
            ClinicalQuestion(
                "Is your cough dry and tickling, or is it producing thick mucus or phlegm?",
                ["Dry hacking cough", "Loose cough with yellow/green phlegm", "Clear white phlegm", "Throat scratchiness only"]
            ),
            ClinicalQuestion(
                "Are you feeling any chest heaviness, whistling sounds (wheezing), or difficulty catching your breath when lying down?",
                ["Whistling wheeze sound", "Difficulty breathing when lying flat", "Chest tightness only", "Breathing is comfortable"]
            ),
            ClinicalQuestion(
                "Are you also having a runny/blocked nose, sinus headache, sore throat, or loss of smell/taste?",
                ["Runny & blocked nose", "Severe pain swallowing (Sore throat)", "Sinus forehead pressure", "Loss of taste / smell"]
            ),
            ClinicalQuestion(
                "Have you tried steam inhalation, saline gargles, cough syrup, or an inhaler?",
                ["Warm saline gargles & steam", "Cough syrup / Lozenges", "Asthma inhaler (Asthalin/Budecort)", "None tried yet"]
            ),
            ClinicalQuestion(
                "Do symptoms get worse with dust, cold air, smoke, or during night and early morning?",
                ["Worse with dust / smoke allergy", "Worse at night & early morning", "Triggered by cold drinks/weather", "Constant throughout day"]
            )
        ]

    # ── 10. Headache & Neurological ──────────────────────────────────────────
    elif any(k in combined for k in ["headache", "sar dard", "sir dard", "sir bhari", "migraine", "dizzy", "chakkar", "spinning", "vertigo", "neurolog", "seizure", "numbness"]):
        return [
            ClinicalQuestion(
                "Where is the pain located? Is it on one side of the head, across the forehead, back of the neck, or like a tight band?",
                ["One side only (Throbbing/Pulsating)", "Tight band around forehead", "Back of head & neck", "All over the head"]
            ),
            ClinicalQuestion(
                "Do you feel sensitive to bright lights, loud noises, or experience nausea/vomiting during the headache?",
                ["Sensitive to light & sound", "Nausea feeling present", "No light sensitivity or nausea", "Visual flashing zig-zags (Aura)"]
            ),
            ClinicalQuestion(
                "If feeling dizzy or lightheaded, does the room spin when you turn your head, or do you feel faint upon standing up quickly?",
                ["Room spinning (Vertigo)", "Faint / dark vision on standing up", "Unsteady unbalance feeling", "No dizziness / headache only"]
            ),
            ClinicalQuestion(
                "Have you taken any pain reliever (like Paracetamol or Naproxen), rested in a dark room, or had enough hydration?",
                ["Rested in dark quiet room", "Paracetamol / Headache tablet", "Drank water & had meal", "None taken yet"]
            ),
            ClinicalQuestion(
                "Did this start after high screen time, lack of sleep, stress, or skipped meals?",
                ["Late night / lack of sleep", "High computer screen time", "Heavy stress & workload", "Skipped meal / dehydration"]
            )
        ]

    # ── 11. Mental Health & Sleep ────────────────────────────────────────────
    elif any(k in combined for k in ["anxiety", "ghabrahat", "depression", "panic", "insomnia", "neend", "stress", "psychiat"]):
        return [
            ClinicalQuestion(
                "Are you experiencing persistent worry, racing thoughts, restlessness, or sudden panic attacks with a racing heartbeat?",
                ["Racing thoughts & restlessness", "Sudden panic & fast heartbeat", "Feeling low & hopeless", "Constant muscle tension"]
            ),
            ClinicalQuestion(
                "How has your sleep pattern changed? Do you have trouble falling asleep, frequent night awakenings, or unrefreshing sleep?",
                ["Difficulty falling asleep", "Waking up at 3-4 AM repeatedly", "Sleeping excessively", "Restless broken sleep"]
            ),
            ClinicalQuestion(
                "Have you noticed a loss of interest in activities you usually enjoy, or difficulty focusing at work/studies?",
                ["Loss of interest in hobbies", "Difficulty concentrating", "Feeling emotionally drained", "Manageable focus"]
            ),
            ClinicalQuestion(
                "Have you practiced breathing exercises, meditation, reduced caffeine, or consulted a counselor before?",
                ["Deep breathing / walks", "Cut down tea / coffee", "Past counseling / therapy", "None tried yet"]
            ),
            ClinicalQuestion(
                "Is there a major life change, work pressure, personal stressor, or physical health issue triggering this?",
                ["Work & financial pressure", "Family / personal relationship stress", "Health anxiety / illness fear", "No clear external trigger"]
            )
        ]

    # ── 12. General / Acute Fever & Infections (Default Fallback) ────────────
    else:
        return [
            ClinicalQuestion(
                "When did you first notice these symptoms, and did they develop suddenly or gradually over several days?",
                ["Started today (< 24 hours ago)", "Ongoing for 2 to 3 days", "Present for roughly 1 week", "Persistent for 2 or more weeks"]
            ),
            ClinicalQuestion(
                "On a scale from 1 to 10, how severe is the discomfort, and is it affecting your eating, sleeping, or daily activities?",
                ["Mild discomfort (2/10)", "Moderate discomfort (5/10)", "Severe distress (8/10)", "Very severe / Critical (10/10)"]
            ),
            ClinicalQuestion(
                "Are you experiencing any accompanying symptoms such as fever, fatigue, body aches, or chills?",
                ["Fever & severe chills", "Generalized body ache & weakness", "Mild fatigue only", "No fever or body aches"]
            ),
            ClinicalQuestion(
                "Have you taken any home remedies, hydration fluids, or medicines, and did they bring relief?",
                ["None taken yet", "Hydration fluids & rest", "Over-the-counter medicine", "Prescription medication"]
            ),
            ClinicalQuestion(
                "Are your symptoms getting progressively worse, staying about the same, or beginning to improve?",
                ["Gradually worsening", "Staying about the same", "Beginning to improve", "Fluctuating / coming and going"]
            )
        ]

def match_disease(user_input, gender=None, age=None):
    cleaned = (user_input or "").strip()
    if not cleaned:
        return None

    # 1. Clinical safety triage (handles colloquial Hindi/Hinglish terms & safety guardrails)
    try:
        from app.ml import predict_disease
        from app.services.clinical_nlp import clinical_safety_triage

        pred = predict_disease(cleaned, gender=gender, age=age)
        ml_name = pred.get("primary_disease") if pred else None
        ml_conf = pred.get("confidence", 0.0) if pred else 0.0
        top_preds = pred.get("top_predictions", []) if pred else []

        triage = clinical_safety_triage(cleaned, ml_name, ml_conf, top_preds)
        if triage and triage.get("primary_disease"):
            return triage["primary_disease"]
    except Exception as exc:
        logger.debug("Triage match_disease fallback: %s", exc)

    # 2. Fallback to dictionary matching
    diseases = list(DISEASE_QUESTIONS.keys())
    if diseases:
        match = process.extractOne(cleaned, diseases, scorer=fuzz.WRatio)
        if match and match[1] >= 50:
            return match[0]

    return "Clinical Health Evaluation"


def cache_ai_output(prompt, output, app_config):
    ai_cache[prompt] = output
    ai_cache.move_to_end(prompt)
    if len(ai_cache) > app_config["AI_CACHE_LIMIT"]:
        ai_cache.popitem(last=False)
    return output


def extract_symptom_context(prompt):
    match = re.search(
        r"Symptoms:\s*(.*?)(?:\.\s*Follow-up responses:|\.\s*Provide a detailed medical analysis|$)",
        prompt or "",
        flags=re.IGNORECASE | re.DOTALL,
    )
    if match:
        return " ".join(match.group(1).split())
    return (prompt or "").strip()


def extract_followup_context(prompt):
    match = re.search(
        r"Follow-up responses:\s*(.*?)(?:\.\s*Return valid JSON|\.\s*Provide a detailed|$)",
        prompt or "",
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return ""
    raw = match.group(1).strip()
    try:
        import ast
        items = ast.literal_eval(raw)
        if isinstance(items, list):
            pairs = []
            for item in items:
                if isinstance(item, dict) and item.get("answer"):
                    ans = item["answer"].strip()
                    if ans:
                        pairs.append(ans)
            if pairs:
                return "Follow-up answers: " + "; ".join(pairs)
    except Exception:
        pass
    return raw


def build_local_demo_analysis(prompt):
    symptom_context = extract_symptom_context(prompt)
    followup_context = extract_followup_context(prompt)
    if followup_context:
        presenting_complaint = f"{symptom_context} — {followup_context}"
    else:
        presenting_complaint = symptom_context or "General clinical symptoms reported by patient."

    # 1. Primary: Intelligent Clinical Triage + Enriched Clinical Knowledge Base (1000+ conditions)
    try:
        from app.ml import predict_disease
        from app.services.clinical_kb import build_consultation_briefing
        from app.services.clinical_nlp import clinical_safety_triage

        pred = predict_disease(symptom_context)
        ml_name = pred.get("primary_disease") if pred else None
        ml_conf = pred.get("confidence", 0.0) if pred else 0.0
        top_preds = pred.get("top_predictions", []) if pred else []

        # Run clinical safety triage
        triage = clinical_safety_triage(symptom_context, ml_name, ml_conf, top_preds)
        primary_name = triage["primary_disease"]
        triage_differentials = triage.get("differentials", [primary_name])

        profile = (pred.get("profile") if pred and ml_name == primary_name else None) or {}

        # ── Use enriched clinical KB briefing ──────────────────────────
        followup_list = None
        if followup_context:
            followup_list = [{"question": "Follow-up", "answer": followup_context}]

        briefing = build_consultation_briefing(
            disease_name=primary_name,
            symptoms_text=presenting_complaint,
            followup_answers=followup_list,
        )

        if briefing:
            # Set high-accuracy differential diagnoses from triage
            briefing["differential_diagnoses"] = "; ".join(triage_differentials[:4])

            analysis = {
                "presenting_complaint": briefing.get("presenting_complaint", presenting_complaint),
                "differential_diagnoses": briefing.get("differential_diagnoses", primary_name),
                "investigations": briefing.get("investigations", ""),
                "treatment": briefing.get("treatment", ""),
                "medications": briefing.get("medications", ""),
                "precautions": briefing.get("precautions", ""),
                "medication_card": briefing.get("medication_card"),
                "hindi_names": briefing.get("hindi_names", ""),
                "specialty_category": briefing.get("specialty_category", ""),
                "typical_duration": briefing.get("typical_duration", ""),
                "emergency_flags": briefing.get("emergency_flags", []),
                "disclaimer": briefing.get("disclaimer", (
                    "This response was generated in standard guidance mode by Care Cliniq's clinical knowledge engine "
                    "(1000+ medical conditions). For guidance only — not a replacement for in-person diagnosis."
                )),
            }

            # Emergency Red Flag Screening: ONLY scan patient's actual reported symptoms and answers!
            combined_patient_text = f"{symptom_context} {followup_context}"
            red_flag = scan_emergency_red_flags(combined_patient_text)
            if red_flag.get("is_emergency"):
                analysis["red_flag_alert"] = red_flag
            else:
                analysis["red_flag_alert"] = None

            return json.dumps(analysis)

        # Fallback: use raw profile if briefing failed
        inv_raw = profile.get("investigations") or ["Comprehensive clinical evaluation", "CBC and metabolic panel"]
        investigations_str = "; ".join(inv_raw[:4]) if isinstance(inv_raw, list) else str(inv_raw)
        treatment = profile.get("treatment") or f"Standard clinical management for {primary_name}."
        meds_raw = profile.get("medications") or ["Physician-directed therapy based on diagnostic confirmation"]
        medications_str = "; ".join(meds_raw[:4]) if isinstance(meds_raw, list) else str(meds_raw)
        prec_raw = profile.get("precautions") or f"Follow prescribed guidance for {primary_name}."
        precautions_str = " ".join(prec_raw[:3]) if isinstance(prec_raw, list) else str(prec_raw)

        analysis = {
            "presenting_complaint": presenting_complaint,
            "differential_diagnoses": "; ".join(triage_differentials[:4]),
            "investigations": investigations_str,
            "treatment": treatment,
            "medications": medications_str,
            "precautions": precautions_str,
            "disclaimer": (
                f"This response was generated in standard guidance mode by Care Cliniq (1000+ conditions). "
                f"For educational support only — not a medical diagnosis."
            ),
        }
        combined_patient_text = f"{symptom_context} {followup_context}"
        red_flag = scan_emergency_red_flags(combined_patient_text)
        if red_flag.get("is_emergency"):
            analysis["red_flag_alert"] = red_flag
        return json.dumps(analysis)

    except Exception as exc:
        logger.warning("ML local analysis failed, falling back to heuristic rules: %s", exc)

    # 2. Secondary Heuristic Fallback
    lowered = symptom_context.lower()
    possible_conditions = []
    if any(keyword in lowered for keyword in ["headache", "migraine", "head ache"]):
        possible_conditions.extend(["Tension-type headache", "Migraine episode", "Dehydration or stress-related headache"])
    if any(keyword in lowered for keyword in ["fever", "cough", "sore throat", "cold", "body ache"]):
        possible_conditions.extend(["Viral upper respiratory infection", "Flu-like illness", "Inflammatory or infectious process"])
    if any(keyword in lowered for keyword in ["stomach", "abdominal", "vomit", "nausea", "gas", "acidity"]):
        possible_conditions.extend(["Gastritis or acid irritation", "Indigestion", "Mild gastrointestinal infection"])
    if any(keyword in lowered for keyword in ["chest pain", "breath", "shortness of breath", "palpitation"]):
        possible_conditions.extend(["Cardiorespiratory cause that needs prompt assessment", "Anxiety-related symptoms", "Musculoskeletal chest discomfort"])
    if any(keyword in lowered for keyword in ["fatigue", "weakness", "tired"]):
        possible_conditions.extend(["Viral syndrome", "Sleep deprivation or stress", "Nutritional or metabolic imbalance"])

    if not possible_conditions:
        possible_conditions = [
            "Viral illness",
            "Stress-related or lifestyle-triggered symptoms",
            "Condition requiring in-person clinical evaluation if symptoms persist",
        ]

    investigations = [
        "Basic vital signs review",
        "Focused physical examination",
        "Symptom-duration review",
    ]
    if "fever" in lowered:
        investigations.append("Temperature monitoring and CBC if symptoms continue")
    if any(keyword in lowered for keyword in ["headache", "migraine"]):
        investigations.append("Neurological assessment if symptoms are severe or recurrent")
    if any(keyword in lowered for keyword in ["stomach", "abdominal", "nausea", "vomit"]):
        investigations.append("Hydration review and abdominal examination")

    treatment = (
        "Use supportive care first: adequate hydration, rest, light meals if tolerated, and short-term symptom monitoring. "
        "If symptoms are worsening, persistent, or unusually severe, arrange an in-person medical review."
    )
    medications = (
        "Only consider common over-the-counter symptom relief if it is normally safe for you, such as acetaminophen/paracetamol for pain or fever. "
        "Avoid self-medicating if you have allergies, chronic conditions, pregnancy, or are unsure what is safe."
    )
    precautions = (
        "Seek urgent medical help for red flags such as chest pain, difficulty breathing, confusion, fainting, seizures, very high fever, "
        "sudden severe headache, dehydration, or worsening symptoms."
    )

    analysis = {
        "presenting_complaint": presenting_complaint,
        "differential_diagnoses": "; ".join(dict.fromkeys(possible_conditions)),
        "investigations": "; ".join(dict.fromkeys(investigations)),
        "treatment": treatment,
        "medications": medications,
        "precautions": precautions,
        "disclaimer": (
            "This response was generated in standard guidance mode. It is educational support only and not a medical diagnosis."
        ),
    }
    return json.dumps(analysis)


def ask_gemini(prompt, app_config):
    if prompt in ai_cache:
        ai_cache.move_to_end(prompt)
        return ai_cache[prompt]

    if not app_config.get("AI_ENABLED", False):
        return cache_ai_output(prompt, build_local_demo_analysis(prompt), app_config)

    try:
        genai = get_gemini_client()
        if not genai:
            return cache_ai_output(prompt, build_local_demo_analysis(prompt), app_config)
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        output = response.text if response.text else build_local_demo_analysis(prompt)
    except Exception as exc:
        logger.warning("Gemini request failed. Falling back to local demo analysis: %s", exc)
        output = build_local_demo_analysis(prompt)

    return cache_ai_output(prompt, output, app_config)
