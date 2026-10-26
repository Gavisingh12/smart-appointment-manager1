"""
scripts/enrich_vague_symptoms_kb.py
===================================
Enriches conditions related to vague symptom disambiguation:
- Generalized Fatigue & Weakness Evaluation
- Hypothyroidism
- Type 2 Diabetes Mellitus
- Dizziness & Vertigo Evaluation
- Benign Paroxysmal Positional Vertigo (BPPV)
"""

import json
from pathlib import Path

KNOWLEDGE_FILE = Path(__file__).resolve().parent.parent / "app" / "ml" / "disease_knowledge.json"

ENRICHMENTS = {
    "Generalized Fatigue & Weakness Evaluation": {
        "name": "Generalized Fatigue & Weakness Evaluation",
        "hindi_names": "शारीरिक कमजोरी और थकान मूल्यांकन (Kamzori Aur Thakan)",
        "specialty_category": "Internal Medicine & General Practice",
        "typical_duration": "Days to weeks until underlying cause is treated",
        "symptoms": "Generalized physical exhaustion, lethargy, low stamina, feeling drained, morning fatigue, unrefreshing sleep, mild brain fog",
        "symptoms_list": ["Generalized fatigue", "Low energy", "Exertional weakness", "Poor concentration", "Sleep unrefreshing"],
        "clarifying_questions": [
            "Kya thakan ke saath saans phoolti hai, chakkar aate hain, ya skin peeli/pale lagti hai? (Anemia check)",
            "Kya pichle kuch dino/mahino me wajan achanak badha ya ghata hai, ya sardi/garmi zyada lagti hai? (Thyroid check)",
            "Kya pyaas zyada lagti hai, bhookh zyada lagti hai aur peshab bar-bar aata hai? (Diabetes / Blood sugar check)",
            "Kya neend theek se puri ho rahi hai aur pichle kuch dino me bohot zyada stress ya mental exhaustion raha hai?",
            "Kya halka bukhar, body ache, ya kisi viral infection ke baad se yeh kamzori shuru hui hai? (Post-viral recovery check)"
        ],
        "differential_diagnoses": [
            "Iron Deficiency Anemia",
            "Hypothyroidism",
            "Type 2 Diabetes Mellitus",
            "Post-Viral Asthenia",
            "Vitamin D & B12 Deficiency"
        ],
        "investigations": [
            "Complete Blood Count (CBC) with Peripheral Smear",
            "Serum Ferritin & Iron studies",
            "Thyroid Profile (TSH, Free T3, Free T4)",
            "Fasting Blood Glucose & HbA1c",
            "Vitamin D3 & Vitamin B12 levels"
        ],
        "treatment": "Comprehensive diagnostic laboratory workup to identify underlying root cause, nutritional replenishment, proper sleep hygiene (7-8 hours), and hydration.",
        "medications": ["Multivitamin & Mineral supplement", "Oral hydration support", "Specific therapy based on lab confirmation"],
        "generic_drug": "Multivitamins with Minerals (Supportive pending lab results)",
        "indian_brands": ["Becadexamin", "Supradyn Daily", "Zincovit", "A to Z NS"],
        "strength_mg": "1 Capsule daily",
        "dosage_frequency": "OD (Once daily after lunch or breakfast)",
        "meal_timing": "After Food",
        "duration_days": "15 to 30 days pending lab investigations",
        "supportive_medicines": ["Hydration (2.5-3 Litres water)", "High protein balanced diet", "Consistent sleep schedule"],
        "max_safe_limit_24h": "1 multivitamin tablet per day",
        "prescription_type": "OTC",
        "precautions": "Do not ignore persistent fatigue lasting > 2 weeks without a clinical blood workup. Avoid excessive caffeine intake which worsens adrenal fatigue. Consult a doctor for targeted prescription if anemia or thyroid is suspected.",
        "home_care_advice": [
            "Maintain a regular sleep schedule: 7 to 8 hours nightly in a dark room",
            "Stay well hydrated with clean water, lemon water, and coconut water",
            "Include iron and protein rich foods (spinach, lentils, eggs, dates, almonds)",
            "Engage in light morning walking (15-20 mins) to stimulate circulation"
        ],
        "emergency_flags": [
            "Sudden severe shortness of breath or chest pain on minimal movement",
            "Sudden fainting, loss of consciousness, or blackouts",
            "Unexplained rapid weight loss or persistent high fever with night sweats",
            "Blood in stool or black tarry stools"
        ],
        "medication_card": {
            "disease": "Generalized Fatigue & Weakness Evaluation",
            "generic_drug": "Multivitamins with Minerals & Zinc",
            "indian_brands": ["Becadexamin", "Supradyn Daily", "Zincovit", "A to Z NS"],
            "strength_mg": "1 Capsule Daily",
            "dosage_frequency": "OD (Once daily after breakfast)",
            "meal_timing": "After Food",
            "duration_days": "15 to 30 days pending lab tests",
            "supportive_medicines": ["Adequate hydration (2.5 L water)", "Nutritious balanced diet"],
            "max_safe_limit_24h": "1 tablet per day",
            "prescription_type": "OTC",
            "precautions": "Complete diagnostic blood panel (CBC, TSH, HbA1c) recommended if fatigue persists > 2 weeks; do not rely solely on supplements.",
            "home_care": [
                "Ensure 7 to 8 hours restful sleep nightly",
                "Drink 2.5 to 3 liters water daily",
                "Eat balanced meals with leafy greens, pulses, and fruits",
                "Avoid excessive caffeine"
            ],
            "lab_tests": ["CBC", "TSH", "HbA1c / Fasting Glucose", "Vitamin D3 & B12"],
            "emergency_red_flags": [
                "Chest pain or breathlessness on mild exertion",
                "Fainting or severe dizziness",
                "Unexplained high fever or night sweats"
            ],
            "clarifying_questions": [
                "1. Saans phoolti hai ya skin peeli lagti hai?",
                "2. Wajan me koi achanak badlaav aaya hai?",
                "3. Pyaas ya peshab zyada aata hai?"
            ]
        }
    },

    "Hypothyroidism": {
        "name": "Hypothyroidism",
        "hindi_names": "हाइपोथायरायडिज्म / थायराइड की कमी (Thyroid Gland Underactive)",
        "specialty_category": "Endocrinology & General Medicine",
        "typical_duration": "Chronic / Long-term manageable",
        "symptoms": "Persistent fatigue, unexplained weight gain, cold intolerance, dry skin, constipation, puffy face, hair thinning, muscle weakness, mood changes",
        "symptoms_list": ["Fatigue", "Weight gain", "Cold intolerance", "Constipation", "Dry coarse skin", "Hair loss", "Bradycardia"],
        "clarifying_questions": [
            "Kya pichle kuch mahino me bina kisi vajah ke wajan badha hai?",
            "Kya doosro ke mukable zyada sardi/thand lagti hai?",
            "Skin dry rehti hai aur pet saaf na hone (constipation) ki dikkat hai?"
        ],
        "differential_diagnoses": ["Iron Deficiency Anemia", "Depression", "Chronic Fatigue Syndrome", "Metabolic Syndrome"],
        "investigations": ["Thyroid Stimulating Hormone (TSH)", "Free T4 (Thyroxine)", "Anti-TPO antibodies if Hashimoto suspected"],
        "treatment": "Hormone replacement therapy with Levothyroxine sodium taken strictly on an empty stomach in the morning, periodic TSH monitoring every 6-8 weeks.",
        "medications": ["Levothyroxine sodium 25 to 50 mcg OD empty stomach"],
        "generic_drug": "Levothyroxine Sodium",
        "indian_brands": ["Thyronorm", "Eltroxin", "Thyrox"],
        "strength_mg": "25 mcg or 50 mcg (adjusted by doctor as per TSH)",
        "dosage_frequency": "OD (Once daily, strictly 45 minutes before tea or breakfast)",
        "meal_timing": "Empty Stomach (Early Morning with plain water)",
        "duration_days": "Long term as prescribed; repeat TSH at 6 to 8 weeks",
        "supportive_medicines": ["Adequate dietary fiber", "Selenium and Zinc rich foods"],
        "max_safe_limit_24h": "Dose titrated strictly by physician according to serum TSH levels",
        "prescription_type": "Rx (Doctor prescription mandatory)",
        "precautions": "Take strictly with plain water 45-60 minutes before breakfast, tea, or milk. Do not take calcium or iron tablets within 4 hours of Levothyroxine as they block absorption. Regular TSH testing is required to prevent overdosage.",
        "home_care_advice": [
            "Take tablet early morning immediately on waking with full glass of water",
            "Wait at least 45 minutes before morning tea, coffee, milk, or breakfast",
            "Maintain moderate daily physical activity to boost metabolic rate",
            "Eat a high fiber diet to manage sluggish digestion"
        ],
        "emergency_flags": [
            "Severe chest pain, palpitations, or rapid irregular heart rate (signs of overreplacement)",
            "Extreme lethargy, low body temperature, and confusion (myxedema coma - rare)",
            "Severe breathing difficulty"
        ],
        "medication_card": {
            "disease": "Hypothyroidism",
            "generic_drug": "Levothyroxine Sodium",
            "indian_brands": ["Thyronorm", "Eltroxin", "Thyrox"],
            "strength_mg": "25 mcg or 50 mcg (Titrated to TSH)",
            "dosage_frequency": "OD (Once daily)",
            "meal_timing": "Empty Stomach (45 mins before morning tea/breakfast)",
            "duration_days": "Ongoing under medical supervision",
            "supportive_medicines": ["Balanced nutrition", "Regular aerobic exercise"],
            "max_safe_limit_24h": "As prescribed by physician",
            "prescription_type": "Rx",
            "precautions": "Take on empty stomach with water; avoid milk/tea/calcium for 45 mins; periodic TSH monitoring required.",
            "home_care": [
                "Take tablet first thing in the morning with water",
                "Wait 45 minutes before morning tea or food",
                "Exercise regularly to support metabolism",
                "Repeat TSH blood test every 2-3 months"
            ],
            "lab_tests": ["Serum TSH", "Free T4"],
            "emergency_red_flags": [
                "Chest pain or rapid pounding heart (palpitations)",
                "Extreme drowsiness or hypothermia"
            ],
            "clarifying_questions": [
                "1. Wajan achanak badha hai?",
                "2. Sardi zyada lagti hai?",
                "3. Skin dry aur constipation hai?"
            ]
        }
    },

    "Type 2 Diabetes Mellitus": {
        "name": "Type 2 Diabetes Mellitus",
        "hindi_names": "टाइप 2 मधुमेह (Sugar / Madhumeh)",
        "specialty_category": "Endocrinology & General Medicine",
        "typical_duration": "Chronic manageable metabolic condition",
        "symptoms": "Increased thirst (polydipsia), frequent urination especially at night (polyuria), increased hunger (polyphagia), unexplained fatigue, blurred vision, slow healing cuts",
        "symptoms_list": ["Frequent urination (night time)", "Excessive thirst", "Unexplained fatigue", "Blurred vision", "Slow healing sores"],
        "clarifying_questions": [
            "Kya raat me peshab ke liye baar-baar uthna padta hai?",
            "Kya gala baar-baar sookh raha hai aur pyaas bohot lagti hai?",
            "Kya chot ya zakhm dheere theek hote hain ya aankhon ke aage dhundhla dikhta hai?"
        ],
        "differential_diagnoses": ["Prediabetes / Impaired Fasting Glucose", "Diabetes Insipidus", "Chronic Kidney Disease", "Cushing Syndrome"],
        "investigations": ["Fasting Plasma Glucose (FPG)", "Postprandial Glucose (PPBS)", "HbA1c (3-month average sugar)", "Lipid Profile & Urine microalbumin"],
        "treatment": "Lifestyle modification (low glycemic index diet, 30 mins daily walking), oral antidiabetic therapy (Metformin initial drug of choice), glucose self-monitoring.",
        "medications": ["Metformin 500 mg with or after meals", "Dietary control", "Daily physical exercise"],
        "generic_drug": "Metformin Hydrochloride",
        "indian_brands": ["Glycomet 500", "Obimet 500", "Cetapin 500"],
        "strength_mg": "500 mg",
        "dosage_frequency": "BD (Twice daily with meals)",
        "meal_timing": "With Food / Immediately After Food",
        "duration_days": "Ongoing under medical supervision",
        "supportive_medicines": ["Low carbohydrate high fiber diet", "B-complex vitamins", "Foot care inspection"],
        "max_safe_limit_24h": "2000 mg daily (as prescribed by doctor)",
        "prescription_type": "Rx (Schedule H - Doctor prescription mandatory)",
        "precautions": "Always take Metformin with or immediately after meals to prevent gastric upset or nausea. Contraindicated in severe renal impairment (eGFR < 30). Monitor for hypoglycemia if combined with other secretagogues. Inspect feet daily.",
        "home_care_advice": [
            "Reduce refined sugars, sweets, white rice, and refined flour (maida)",
            "Walk briskly for at least 30 minutes 5 days a week",
            "Monitor blood glucose regularly with a home glucometer",
            "Inspect feet daily for cuts, blisters, or redness"
        ],
        "emergency_flags": [
            "Hypoglycemia signs: trembling, profuse sweating, confusion, dizziness, hunger pangs (take sugar/juice immediately)",
            "Very high sugar with persistent vomiting, deep rapid breathing, fruity breath (DKA / HHS risk)",
            "Non-healing foot ulcer or blackening of toes"
        ],
        "medication_card": {
            "disease": "Type 2 Diabetes Mellitus",
            "generic_drug": "Metformin Hydrochloride",
            "indian_brands": ["Glycomet 500", "Obimet 500", "Cetapin 500"],
            "strength_mg": "500 mg",
            "dosage_frequency": "BD (Twice daily with meals)",
            "meal_timing": "With Meals",
            "duration_days": "Ongoing under medical care",
            "supportive_medicines": ["Low glycemic diet", "Daily 30 min brisk walk"],
            "max_safe_limit_24h": "2000 mg",
            "prescription_type": "Rx",
            "precautions": "Take with meals to avoid stomach upset; avoid in severe kidney failure; monitor blood sugar regularly.",
            "home_care": [
                "Follow a low-carb, high-fiber diabetic diet",
                "Walk briskly for 30 minutes daily",
                "Check blood sugar regularly",
                "Inspect feet daily for wounds"
            ],
            "lab_tests": ["Fasting & PP Blood Sugar", "HbA1c", "Kidney function (eGFR)"],
            "emergency_red_flags": [
                "Shaking, sweating, confusion (low sugar / hypoglycemia)",
                "Fruity breath, vomiting, confusion (DKA)",
                "Non-healing foot sore"
            ],
            "clarifying_questions": [
                "1. Raat me peshab baar-baar aata hai?",
                "2. Pyaas aur bhookh zyada lagti hai?",
                "3. Dhundhla dikhta hai ya zakhm dheere bharta hai?"
            ]
        }
    },

    "Dizziness & Vertigo Evaluation": {
        "name": "Dizziness & Vertigo Evaluation",
        "hindi_names": "चक्कर आना और संतुलन में कमी (Chakkar / Sar Ghumna)",
        "specialty_category": "ENT & Neurology",
        "typical_duration": "Episodic (seconds to minutes) or persistent",
        "symptoms": "Feeling of head spinning, unsteadiness, lightheadedness on standing, loss of balance, nausea, feeling faint",
        "symptoms_list": ["Spinning sensation", "Lightheadedness", "Unsteadiness", "Nausea", "Postural instability"],
        "clarifying_questions": [
            "Kya sar ghumne ka ehsaas gardan ghumane ya let kar uthne par hota hai? (BPPV / Inner ear check)",
            "Kya achanak khade hone par aankhon ke aage andhera chha jata hai? (Orthostatic hypotension / Low BP check)",
            "Kya kaano me seeti jaisi aawaz (tinnitus) ya sunne me koi kami mehsus hoti hai?",
            "Kya paani kam peene se dehydration ya kamzori aur thakan lag rahi hai?",
            "Kya chest discomfort, ghabrahat ya irregular heartbeat mehsus hoti hai?"
        ],
        "differential_diagnoses": [
            "Benign Paroxysmal Positional Vertigo (BPPV)",
            "Orthostatic Hypotension (Low BP on standing)",
            "Vestibular Migraine",
            "Dehydration / Electrolyte Imbalance",
            "Inner Ear Labyrinthitis"
        ],
        "investigations": [
            "Supine and standing blood pressure (Orthostatic BP check)",
            "Dix-Hallpike clinical test for inner ear vertigo",
            "Audiometry (hearing test) if ear ringing present",
            "Complete blood count & serum electrolytes"
        ],
        "treatment": "Canalith repositioning maneuvers (Epley maneuver) for positional vertigo, vestibular suppressants short-term, hydration, and gradual positional changes.",
        "medications": ["Betahistine 16 mg TDS (for true spinning vertigo)", "Adequate hydration", "Electrolyte fluids"],
        "generic_drug": "Betahistine Dihydrochloride",
        "indian_brands": ["Vertin 16", "Betavert 16", "Zevert 16"],
        "strength_mg": "16 mg",
        "dosage_frequency": "TDS (8 hourly) after food",
        "meal_timing": "After Food",
        "duration_days": "5 to 7 days as advised by doctor",
        "supportive_medicines": ["Oral Rehydration Salts (ORS)", "Epley maneuver exercises", "Ginger tea"],
        "max_safe_limit_24h": "48 mg daily",
        "prescription_type": "Rx (Doctor prescription advised)",
        "precautions": "Caution in patients with bronchial asthma or peptic ulcer disease. Do not drive or operate machinery during dizzy spells. Sit down immediately if room begins spinning.",
        "home_care_advice": [
            "When waking up, sit on bed for 1-2 minutes before standing up",
            "Avoid sudden, jerky head movements",
            "Stay well hydrated with at least 2.5 liters of water daily",
            "Keep pathways clear of tripping hazards"
        ],
        "emergency_flags": [
            "Sudden severe dizziness with double vision, slurred speech, or weakness in face/arms (stroke red flag)",
            "Sudden complete hearing loss in one ear",
            "Dizziness accompanied by chest pain or shortness of breath",
            "Loss of consciousness or seizures"
        ],
        "medication_card": {
            "disease": "Dizziness & Vertigo Evaluation",
            "generic_drug": "Betahistine 16 mg",
            "indian_brands": ["Vertin 16", "Betavert 16", "Zevert 16"],
            "strength_mg": "16 mg",
            "dosage_frequency": "TDS (8 hourly)",
            "meal_timing": "After Food",
            "duration_days": "5 to 7 days",
            "supportive_medicines": ["Hydration", "Epley maneuver under doctor guidance"],
            "max_safe_limit_24h": "48 mg",
            "prescription_type": "Rx",
            "precautions": "Caution in asthma or peptic ulcer; avoid driving during dizzy episodes; sit down immediately if balance lost.",
            "home_care": [
                "Sit up slowly from lying down position",
                "Avoid sudden neck or head jerks",
                "Drink 2-3 liters water daily",
                "Rest in a quiet seated position until spell passes"
            ],
            "lab_tests": ["Standing & sitting blood pressure", "Dix-Hallpike test", "CBC & electrolytes"],
            "emergency_red_flags": [
                "Dizziness with slurred speech, facial droop, or arm weakness (Stroke warning)",
                "Chest pain or fainting",
                "Sudden total hearing loss"
            ],
            "clarifying_questions": [
                "1. Sar ghumta hai ya andhera chha jata hai?",
                "2. Khade hone par badhta hai ya gardan hilane par?",
                "3. Kaano me seeti ya sunne me dikkat hai?"
            ]
        }
    }
}


def main():
    if not KNOWLEDGE_FILE.exists():
        print(f"Error: {KNOWLEDGE_FILE} not found!")
        return

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        kb = json.load(f)

    print(f"Current KB entries: {len(kb)}")
    updated = 0
    for name, data in ENRICHMENTS.items():
        if name in kb:
            kb[name].update(data)
            updated += 1
            print(f"Updated: {name}")
        else:
            kb[name] = data
            updated += 1
            print(f"Added new: {name}")

    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)

    print(f"Successfully saved {updated} enriched conditions to {KNOWLEDGE_FILE}")


if __name__ == "__main__":
    main()
