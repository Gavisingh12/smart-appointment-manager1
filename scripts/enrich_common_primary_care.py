"""
scripts/enrich_common_primary_care.py
======================================
Enriches essential primary care conditions in disease_knowledge.json:
- Tension Headache
- Upper Respiratory Tract Infection (Common Cold)
- Acute Gastroenteritis
- Gastritis
- Influenza
Ensures every common presentation has complete medication card, Indian brands,
OTC/Rx status, dosage, home care, and safe red flags.
"""

import json
from pathlib import Path

KNOWLEDGE_FILE = Path(__file__).resolve().parent.parent / "app" / "ml" / "disease_knowledge.json"

ENRICHMENTS = {
    "Tension Headache": {
        "name": "Tension Headache",
        "hindi_names": "तनाव सिरदर्द (Sir Dard / Tension Se Matha Bhari Hona)",
        "specialty_category": "Neurology & General Medicine",
        "typical_duration": "A few hours to 2-3 days",
        "symptoms": "Dull aching head pain, sensation of tightness or band-like pressure across forehead and temples, neck and shoulder muscle tenderness, head heaviness",
        "symptoms_list": ["Head heaviness", "Band-like pressure across forehead", "Dull aching pain", "Neck tenderness", "Mild scalp sensitivity"],
        "clarifying_questions": [
            "Sir me dard dono taraf band jaisa lagta hai ya ek taraf thak-thak karta hai?",
            "Kya pichle kuch dino se neend kam ya screen time bohot zyada hai?",
            "Aankhon me khinchao ya gardan me jakdan mehsus hoti hai?"
        ],
        "differential_diagnoses": ["Migraine", "Sinusitis", "Cervicogenic Headache", "Eye Strain / Refractive Error"],
        "investigations": ["Blood pressure measurement", "Visual acuity & eye refraction check", "Neurological clinical examination"],
        "treatment": "Rest in a quiet dimly lit room, hydration, gentle neck stretching, stress reduction techniques, and short-term analgesic therapy.",
        "medications": ["Paracetamol 650 mg SOS", "Ibuprofen 400 mg SOS (with food)", "Combiflam SOS"],
        "generic_drug": "Paracetamol OR Ibuprofen",
        "indian_brands": ["Combiflam", "Crocin Pain Relief", "Brufen 400", "Dolo 650"],
        "strength_mg": "Paracetamol 650 mg OR Ibuprofen 400 mg",
        "dosage_frequency": "SOS (When needed, minimum 6 to 8 hours apart)",
        "meal_timing": "After Food",
        "duration_days": "1 to 3 days as needed",
        "supportive_medicines": ["Adequate hydration (2-3 L water)", "Gentle neck & shoulder stretching", "Magnesium supplement"],
        "max_safe_limit_24h": "Paracetamol 3000 mg / Ibuprofen 1200 mg",
        "prescription_type": "OTC",
        "precautions": "Avoid daily frequent analgesic use to prevent medication overuse headache (rebound headache). Always take Ibuprofen after meals to avoid gastric irritation. Avoid excessive caffeine and sleep deprivation.",
        "home_care_advice": [
            "Rest in a quiet, dark and cool room",
            "Drink plenty of water to rule out dehydration",
            "Apply a warm or cool compress to forehead and neck muscles",
            "Take regular breaks from digital screens and ensure 7-8 hours sleep"
        ],
        "emergency_flags": [
            "Sudden severe 'thunderclap' headache reaching peak intensity in seconds",
            "Headache accompanied by high fever, stiff neck, confusion, or rash",
            "New onset headache accompanied by blurred vision, limb weakness, or difficulty speaking"
        ],
        "medication_card": {
            "disease": "Tension Headache",
            "generic_drug": "Paracetamol OR Ibuprofen",
            "indian_brands": ["Combiflam", "Crocin Pain Relief", "Brufen 400", "Dolo 650"],
            "strength_mg": "Paracetamol 650 mg OR Ibuprofen 400 mg",
            "dosage_frequency": "SOS (When needed, minimum 6 to 8 hours apart)",
            "meal_timing": "After Food",
            "duration_days": "1 to 3 days as needed",
            "supportive_medicines": ["Adequate hydration (2-3 L water)", "Gentle neck stretching", "Magnesium supplement"],
            "max_safe_limit_24h": "Paracetamol 3000 mg / Ibuprofen 1200 mg",
            "prescription_type": "OTC",
            "precautions": "Avoid frequent overuse to prevent rebound headache; take Ibuprofen with food; avoid dehydration.",
            "home_care": [
                "Rest in a quiet, dark room",
                "Stay well hydrated",
                "Apply cold or warm compress to forehead or back of neck",
                "Reduce screen time and get adequate 7-8 hours sleep"
            ],
            "lab_tests": ["Blood pressure measurement", "Visual acuity & refraction check"],
            "emergency_red_flags": [
                "Sudden thunderclap headache",
                "Headache with stiff neck, high fever, or confusion",
                "Focal neurological weakness or vision loss"
            ],
            "clarifying_questions": [
                "1. Sir me dard dono taraf tight band jaisa lagta hai ya ek taraf?",
                "2. Kya neend puri ho rahi hai aur screen time zyada hai?",
                "3. Aankhon me jalan ya khichao mehsus hota hai?"
            ]
        }
    },

    "Upper Respiratory Tract Infection (Common Cold)": {
        "name": "Upper Respiratory Tract Infection (Common Cold)",
        "hindi_names": "सामान्य जुकाम और सर्दी (Sardi, Zukham Aur Khansi)",
        "specialty_category": "Pulmonology & General Medicine",
        "typical_duration": "5 to 7 days (self-limiting)",
        "symptoms": "Nasal congestion, runny nose (rhinorrhea), sneezing, sore throat, mild dry cough, low-grade fever, malaise, head heaviness",
        "symptoms_list": ["Runny nose", "Sneezing", "Nasal congestion", "Sore throat", "Mild dry cough", "Low grade fever", "Malaise"],
        "clarifying_questions": [
            "Sardi-zukham kitne din se hai?",
            "Kya saans lene me koi takleef ya chaati me seeti jaisi aawaz aati hai?",
            "Balgam ka rang kaisa hai — paani jaisa ya peela/hara?"
        ],
        "differential_diagnoses": ["Acute Bronchitis", "Influenza", "Allergic Rhinitis", "Acute Pharyngitis"],
        "investigations": ["Clinical ENT and chest examination", "CBC if symptoms persist beyond 7-10 days"],
        "treatment": "Symptomatic relief, steam inhalation, warm saline gargles, adequate hydration, rest, and OTC antihistamine/decongestant combination.",
        "medications": ["Cetirizine + Phenylephrine + Paracetamol", "Steam inhalation", "Saline nasal drops"],
        "generic_drug": "Cetirizine + Phenylephrine + Paracetamol",
        "indian_brands": ["Sinarest", "Cheston Cold", "Alex-P", "D-Cold Total"],
        "strength_mg": "Paracetamol 500 mg + Phenylephrine 5 mg + Cetirizine 5 mg",
        "dosage_frequency": "BD (Twice daily) or SOS",
        "meal_timing": "After Food",
        "duration_days": "3 to 5 days",
        "supportive_medicines": ["Saline Nasal Drops (Otrivin S / Solspre)", "Steam Inhalation 2-3 times daily", "Warm saline gargle"],
        "max_safe_limit_24h": "2 tablets per 24 hours (consult doctor for higher doses)",
        "prescription_type": "OTC",
        "precautions": "May cause mild drowsiness; avoid driving or operating heavy machinery. Caution in patients with uncontrolled hypertension. Stay well hydrated. Do not take antibiotics for uncomplicated viral common cold.",
        "home_care_advice": [
            "Steam inhalation 2-3 times daily to relieve congestion",
            "Warm salt water gargles 3 times daily for sore throat",
            "Drink plenty of warm liquids (herbal tea, warm water, soups)",
            "Get adequate rest and sleep"
        ],
        "emergency_flags": [
            "Severe shortness of breath, rapid breathing, or wheezing",
            "High fever exceeding 102F that does not subside after 3 days",
            "Inability to swallow liquids or severe earache"
        ],
        "medication_card": {
            "disease": "Upper Respiratory Tract Infection (Common Cold)",
            "generic_drug": "Cetirizine + Phenylephrine + Paracetamol",
            "indian_brands": ["Sinarest", "Cheston Cold", "Alex-P", "D-Cold Total"],
            "strength_mg": "Paracetamol 500 mg + Phenylephrine 5 mg + Cetirizine 5 mg",
            "dosage_frequency": "BD (Twice daily) or SOS",
            "meal_timing": "After Food",
            "duration_days": "3 to 5 days",
            "supportive_medicines": ["Saline Nasal Drops (Otrivin S)", "Steam Inhalation", "Warm saline gargle"],
            "max_safe_limit_24h": "2 tablets in 24 hours",
            "prescription_type": "OTC",
            "precautions": "May cause mild drowsiness; avoid driving; caution in hypertension; do not take antibiotics without prescription.",
            "home_care": [
                "Steam inhalation 2-3 times daily",
                "Warm salt water gargles for throat discomfort",
                "Drink warm fluids, herbal tea with honey and ginger",
                "Adequate rest and sleep"
            ],
            "lab_tests": ["Clinical throat examination and vital signs", "CBC if symptoms persist > 7 days"],
            "emergency_red_flags": [
                "Severe shortness of breath or persistent chest tightness",
                "High fever above 102F lasting over 3 days",
                "Severe throat swelling or inability to swallow fluids"
            ],
            "clarifying_questions": [
                "1. Sardi-khansi kitne din se hai?",
                "2. Saans lene me koi takleef ya chaati me jakdan toh nahi hai?",
                "3. Balgam ka rang peela/hara toh nahi hai?"
            ]
        }
    },

    "Acute Gastroenteritis": {
        "name": "Acute Gastroenteritis",
        "hindi_names": "तीव्र आंत्रशोथ (Dast / Pet Kharab / Loose Motion)",
        "specialty_category": "Gastroenterology & General Medicine",
        "typical_duration": "2 to 4 days",
        "symptoms": "Frequent watery or loose stools, abdominal cramps, nausea, vomiting, mild low-grade fever, malaise, dehydration",
        "symptoms_list": ["Watery loose stools", "Abdominal cramping", "Nausea", "Vomiting", "Dehydration", "Loss of appetite"],
        "clarifying_questions": [
            "Dast din me kitni baar ho rahe hain aur paani jaisa hai ya nahi?",
            "Kya dast me khoon ya pet me tez marod hai?",
            "Ulti bhi ho rahi hai aur paani ruk pa raha hai ya nahi?"
        ],
        "differential_diagnoses": ["Food Poisoning", "Irritable Bowel Syndrome", "Acute Gastritis", "Amoebiasis"],
        "investigations": ["Clinical assessment of hydration and vital signs", "Stool routine and microscopy if diarrhea persists > 48 hours", "Serum electrolytes if moderate/severe dehydration"],
        "treatment": "Aggressive oral rehydration therapy with WHO-formula ORS, oral zinc supplementation, probiotics, and light bland diet.",
        "medications": ["Oral Rehydration Salts (ORS)", "Zinc 20 mg OD", "Probiotics (Darolac / Enterogermina)"],
        "generic_drug": "Oral Rehydration Salts (ORS) + Zinc",
        "indian_brands": ["Electral ORS", "Wintrolyte", "Prolyte ORS", "Darolac"],
        "strength_mg": "1 sachet in 1 Litre drinking water",
        "dosage_frequency": "Sip continuously after every loose stool",
        "meal_timing": "Throughout the day",
        "duration_days": "3 to 5 days until loose stools resolve",
        "supportive_medicines": ["Probiotics (Darolac / Enterogermina)", "Zinc 20 mg OD for 14 days", "Paracetamol 650 mg SOS for fever"],
        "max_safe_limit_24h": "Drink minimum 2 to 3 Litres ORS per day",
        "prescription_type": "OTC",
        "precautions": "Do not take anti-motility drugs (like Loperamide) if there is fever or blood in stool. Avoid fruit juices, cow milk, and oily foods until gut recovers. Maintain strict hand washing.",
        "home_care_advice": [
            "Dissolve 1 sachet Electral in 1 Litre clean boiled & cooled water; drink small frequent sips",
            "Eat light, easily digestible food (Khichdi, curd-rice, bananas, boiled potatoes)",
            "Strict hand hygiene with soap and water",
            "Rest and avoid dehydration"
        ],
        "emergency_flags": [
            "Signs of severe dehydration: sunken eyes, extreme dry mouth, dizziness on standing, no urination for > 8 hours",
            "Blood in stool or black tarry stools",
            "Inability to keep any fluids down due to persistent vomiting",
            "High fever exceeding 102F or severe continuous abdominal pain"
        ],
        "medication_card": {
            "disease": "Acute Gastroenteritis",
            "generic_drug": "Oral Rehydration Salts (ORS) + Zinc",
            "indian_brands": ["Electral ORS", "Wintrolyte", "Prolyte ORS", "Darolac"],
            "strength_mg": "1 sachet in 1 Litre drinking water",
            "dosage_frequency": "Sip continuously after every loose stool",
            "meal_timing": "Throughout the day",
            "duration_days": "3 to 5 days until loose stools resolve",
            "supportive_medicines": ["Probiotics (Darolac / Enterogermina)", "Zinc 20 mg OD for 14 days"],
            "max_safe_limit_24h": "Drink minimum 2 to 3 Litres ORS per day",
            "prescription_type": "OTC",
            "precautions": "Avoid anti-motility drugs if fever/blood in stool; avoid oily food, dairy milk; maintain strict hydration.",
            "home_care": [
                "Prepare ORS in clean drinking water and drink small frequent sips",
                "Eat light, easily digestible food (Khichdi, curd-rice, banana)",
                "Strict hand hygiene with soap before eating and after toilet",
                "Rest and avoid dehydration"
            ],
            "lab_tests": ["Stool routine and microscopy if > 48 hours", "Serum electrolytes if dehydrated"],
            "emergency_red_flags": [
                "Severe dehydration (sunken eyes, no urination > 8 hours)",
                "Blood in stool",
                "Persistent vomiting preventing fluid intake",
                "High grade fever exceeding 102F"
            ],
            "clarifying_questions": [
                "1. Dast din me kitni baar ho rahe hain?",
                "2. Kya dast me khoon ya pet me tez marod hai?",
                "3. Ulti bhi ho rahi hai aur paani ruk pa raha hai?"
            ]
        }
    },

    "Gastritis": {
        "name": "Gastritis",
        "hindi_names": "गैस्ट्र्रिटिस / पेट में जलन और एसिडिटी (Pet Me Jalan, Gas Aur Acidity)",
        "specialty_category": "Gastroenterology & General Medicine",
        "typical_duration": "3 to 7 days",
        "symptoms": "Upper abdominal burning or gnawing pain, bloating, belching, early satiety, nausea, acid reflux, loss of appetite",
        "symptoms_list": ["Upper abdominal burning pain", "Acid reflux", "Bloating", "Belching", "Nausea", "Indigestion"],
        "clarifying_questions": [
            "Pet me jalan ya dard khana khane se pehle hota hai ya baad me?",
            "Kya pichle kuch dino me painkiller dawai ya bohot teekha/oily khana khaya tha?",
            "Ulti jaisa lagta hai ya khata paani gale me aata hai?"
        ],
        "differential_diagnoses": ["Gastroesophageal Reflux Disease (GERD)", "Peptic Ulcer Disease", "Non-Ulcer Dyspepsia", "Biliary Colic"],
        "investigations": ["Clinical abdominal palpation", "H. pylori stool antigen or urea breath test if chronic", "Upper GI endoscopy if persistent > 2 weeks or red flags"],
        "treatment": "Proton pump inhibitor (PPI) therapy 30 minutes before breakfast, antacid gel for instant relief, dietary modification, and avoiding NSAID painkillers.",
        "medications": ["Pantoprazole 40 mg OD before breakfast", "Antacid oral suspension (Gelusil / Mucaine)"],
        "generic_drug": "Pantoprazole 40 mg",
        "indian_brands": ["Pan 40", "Pantocid 40", "Pantodac 40"],
        "strength_mg": "40 mg",
        "dosage_frequency": "OD (Once daily, 30 minutes before morning breakfast)",
        "meal_timing": "Empty Stomach (Before Breakfast)",
        "duration_days": "7 to 14 days",
        "supportive_medicines": ["Antacid gel (Gelusil / Digene 10 ml after food SOS)", "Prokinetics if bloating severe"],
        "max_safe_limit_24h": "80 mg daily",
        "prescription_type": "Schedule H (Doctor prescription advised)",
        "precautions": "Take strictly 30-45 minutes before morning breakfast on empty stomach for maximum acid suppression. Avoid NSAIDs (brufen, aspirin) without gastroprotection. Stop smoking and alcohol. Eat smaller frequent meals.",
        "home_care_advice": [
            "Eat smaller, more frequent meals rather than large heavy meals",
            "Avoid extremely spicy, oily, deep-fried food and citrus/caffeine",
            "Do not lie down immediately after eating (wait at least 2 hours)",
            "Drink adequate water between meals rather than large quantities during meals"
        ],
        "emergency_flags": [
            "Vomiting coffee-ground material or fresh blood (hematemesis)",
            "Black tarry stools (melena)",
            "Severe persistent burning pain radiating to the back",
            "Difficulty or painful swallowing (dysphagia)"
        ],
        "medication_card": {
            "disease": "Gastritis",
            "generic_drug": "Pantoprazole 40 mg",
            "indian_brands": ["Pan 40", "Pantocid 40", "Pantodac 40"],
            "strength_mg": "40 mg",
            "dosage_frequency": "OD (Once daily, 30 mins before breakfast)",
            "meal_timing": "Before Breakfast (Empty Stomach)",
            "duration_days": "7 to 14 days",
            "supportive_medicines": ["Antacid gel (Gelusil / Digene SOS after meals)"],
            "max_safe_limit_24h": "80 mg",
            "prescription_type": "Rx",
            "precautions": "Take on empty stomach before breakfast; avoid NSAID painkillers; avoid spicy and deep-fried food.",
            "home_care": [
                "Eat smaller, frequent light meals",
                "Avoid spicy, acidic, and oily foods",
                "Do not lie down immediately after eating",
                "Limit caffeine and tea intake"
            ],
            "lab_tests": ["Clinical evaluation", "H. pylori test if recurrent", "Endoscopy if persistent"],
            "emergency_red_flags": [
                "Vomiting blood or coffee-ground material",
                "Black tarry stools",
                "Unexplained rapid weight loss",
                "Severe constant abdominal pain"
            ],
            "clarifying_questions": [
                "1. Dard khana khane se pehle badhta hai ya baad me?",
                "2. Teekha/oily khana ya painkiller dawai li thi?",
                "3. Ulti ya khatta paani aata hai?"
            ]
        }
    },

    "Influenza": {
        "name": "Influenza",
        "hindi_names": "इन्फ्लुएंजा / फ्लू (Viral Flu / Tez Bukhar Aur Badan Dard)",
        "specialty_category": "Infectious Diseases & Pulmonology",
        "typical_duration": "5 to 7 days",
        "symptoms": "Abrupt high fever, severe generalized body aches and myalgias, headache, dry cough, sore throat, nasal congestion, profound fatigue",
        "symptoms_list": ["High fever", "Severe body ache", "Profound fatigue", "Dry cough", "Headache", "Chills", "Sore throat"],
        "clarifying_questions": [
            "Kya bukhar achanak tez aaya aur poori body me tez dard hai?",
            "Saans lene me koi dikkat ya chaati me dard toh nahi hai?",
            "Ghar me ya aas-paas kisi aur ko bhi flu ke lakshan hain?"
        ],
        "differential_diagnoses": ["Acute Viral Fever", "Upper Respiratory Tract Infection (Common Cold)", "COVID-19", "Acute Bronchitis"],
        "investigations": ["Rapid influenza diagnostic test (RIDT) or RT-PCR if high-risk", "CBC and vital signs"],
        "treatment": "Strict bed rest, aggressive hydration, antipyretics (Paracetamol) for fever/myalgia, antiviral therapy (Oseltamivir) within 48h for high-risk patients.",
        "medications": ["Paracetamol 650 mg TDS/SOS", "Oseltamivir 75 mg (high risk / confirmed)", "Steam inhalation", "Adequate fluids"],
        "generic_drug": "Paracetamol 650 mg (Symptomatic) / Oseltamivir 75 mg (Antiviral)",
        "indian_brands": ["Dolo 650", "Calpol 650", "Fluvir 75", "Antiflu 75"],
        "strength_mg": "Paracetamol 650 mg / Oseltamivir 75 mg",
        "dosage_frequency": "Paracetamol TDS (8 hourly SOS); Oseltamivir BD if prescribed by doctor",
        "meal_timing": "After Food",
        "duration_days": "5 days",
        "supportive_medicines": ["Oral Rehydration Salts (ORS)", "Steam Inhalation", "Vitamin C and Zinc"],
        "max_safe_limit_24h": "Paracetamol maximum 4000 mg in 24 hours",
        "prescription_type": "Paracetamol OTC; Oseltamivir Rx",
        "precautions": "Isolate from high-risk family members (elderly, infants, pregnant women). Avoid Aspirin in children and adolescents due to Reye's syndrome risk. Seek immediate emergency care if breathing difficulty develops.",
        "home_care_advice": [
            "Strict bed rest for first 3-5 days to allow immune recovery",
            "Drink plenty of fluids: warm water, soups, ORS, herbal tea",
            "Wear a mask around vulnerable household members",
            "Use steam inhalation 2-3 times daily for airway comfort"
        ],
        "emergency_flags": [
            "Shortness of breath, rapid breathing, or oxygen saturation < 94%",
            "Persistent chest pain or pressure",
            "Confusion, dizziness, or inability to wake up",
            "Fever that improves then returns with a worse cough"
        ],
        "medication_card": {
            "disease": "Influenza",
            "generic_drug": "Paracetamol 650 mg / Oseltamivir 75 mg",
            "indian_brands": ["Dolo 650", "Calpol 650", "Fluvir 75", "Antiflu 75"],
            "strength_mg": "Paracetamol 650 mg / Oseltamivir 75 mg",
            "dosage_frequency": "Paracetamol TDS (8 hourly SOS)",
            "meal_timing": "After Food",
            "duration_days": "5 days",
            "supportive_medicines": ["ORS for hydration", "Steam inhalation", "Vitamin C"],
            "max_safe_limit_24h": "Paracetamol 4000 mg",
            "prescription_type": "OTC (Paracetamol) / Rx (Oseltamivir)",
            "precautions": "Isolate at home; drink plenty of liquids; do not give aspirin to children; watch for respiratory distress.",
            "home_care": [
                "Strict bed rest",
                "Drink 2-3 liters of warm fluids daily",
                "Steam inhalation for chest and nasal comfort",
                "Monitor temperature and stay well rested"
            ],
            "lab_tests": ["Rapid Flu test / RT-PCR if indicated", "CBC and pulse oximetry"],
            "emergency_red_flags": [
                "Difficulty breathing or blue lips",
                "Chest pain or pressure",
                "Confusion or extreme lethargy",
                "Fever exceeding 103F not responding to medicine"
            ],
            "clarifying_questions": [
                "1. Bukhar achanak tez aaya aur body me dard hai?",
                "2. Saans lene me takleef toh nahi hai?",
                "3. Ghar me kisi aur ko flu hai?"
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
            # Update existing entry with full rich fields and medication card
            kb[name].update(data)
            updated += 1
            print(f"Updated: {name}")
        else:
            kb[name] = data
            updated += 1
            print(f"Added new: {name}")

    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)

    print(f"Successfully saved {updated} enriched primary care conditions to {KNOWLEDGE_FILE}")


if __name__ == "__main__":
    main()
