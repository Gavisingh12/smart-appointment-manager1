import json
import os
import re

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "pharmacy_catalog.json")

DEFAULT_CATEGORIES = [
    {
        "id": "all",
        "name": "All Medicines",
        "icon": "pill",
        "accent": "cat-green",
        "description": "Browse complete range of genuine medicines & wellness products"
    },
    {
        "id": "pain-fever",
        "name": "Pain & Fever",
        "icon": "thermometer",
        "accent": "cat-coral",
        "description": "Rapid relief for headaches, body ache, fever and inflammation"
    },
    {
        "id": "cold-respiratory",
        "name": "Cold & Cough",
        "icon": "wind",
        "accent": "cat-teal",
        "description": "Inhalers, syrups, decongestants and allergy relievers"
    },
    {
        "id": "antibiotics",
        "name": "Antibiotics & Infections",
        "icon": "shield",
        "accent": "cat-rose",
        "description": "Targeted therapies for bacterial and microbial infections"
    },
    {
        "id": "digestive-gastro",
        "name": "Digestion & Acidity",
        "icon": "flame",
        "accent": "cat-amber",
        "description": "Antacids, proton pump inhibitors, probiotics & digestive enzymes"
    },
    {
        "id": "heart-bp",
        "name": "Heart & Blood Pressure",
        "icon": "heart",
        "accent": "cat-rose",
        "description": "Hypertension control, cholesterol management & cardiovascular care"
    },
    {
        "id": "diabetes",
        "name": "Diabetes Care",
        "icon": "activity",
        "accent": "cat-cyan",
        "description": "Oral hypoglycemics, insulin support & blood glucose monitors"
    },
    {
        "id": "vitamins-supplements",
        "name": "Vitamins & Nutrition",
        "icon": "sun",
        "accent": "cat-peach",
        "description": "Daily multivitamins, Calcium D3, Zinc & immunity boosters"
    },
    {
        "id": "skin-hair",
        "name": "Skin & Dermatology",
        "icon": "sparkles",
        "accent": "cat-purple",
        "description": "Medicated creams, antifungal lotions & topical treatments"
    },
    {
        "id": "first-aid-devices",
        "name": "Devices & First Aid",
        "icon": "box",
        "accent": "cat-slate",
        "description": "BP monitors, thermometers, bandages, ointments & surgicals"
    }
]

# Initial Seed Data drawn from the 525-disease clinical dataset + top pharmacy brands
INITIAL_PRODUCTS = [
    # 1. Pain & Fever
    {
        "id": 1,
        "name": "Crocin 650 Tablet",
        "salt": "Paracetamol 650 mg",
        "category_id": "pain-fever",
        "category_name": "Pain & Fever",
        "dosage_form": "Tablet",
        "pack_size": "15 tablets per strip",
        "mrp": 38,
        "price": 32,
        "discount_percent": 15,
        "rating": 4.8,
        "rating_count": 2840,
        "is_rx_required": False,
        "is_bestseller": True,
        "manufacturer": "GlaxoSmithKline",
        "indications": ["fever", "headache", "body pain", "toothache", "mild arthritis", "temperature"],
        "stock": 140
    },
    {
        "id": 2,
        "name": "Dolo 650 Tablet",
        "salt": "Paracetamol 650 mg",
        "category_id": "pain-fever",
        "category_name": "Pain & Fever",
        "dosage_form": "Tablet",
        "pack_size": "15 tablets per strip",
        "mrp": 52,
        "price": 45,
        "discount_percent": 13,
        "rating": 4.9,
        "rating_count": 3950,
        "is_rx_required": False,
        "is_bestseller": True,
        "manufacturer": "Micro Labs Ltd",
        "indications": ["fever", "body ache", "flu symptoms", "headache", "viral fever"],
        "stock": 210
    },
    {
        "id": 3,
        "name": "Combiflam Tablet",
        "salt": "Ibuprofen 400 mg + Paracetamol 325 mg",
        "category_id": "pain-fever",
        "category_name": "Pain & Fever",
        "dosage_form": "Tablet",
        "pack_size": "20 tablets per strip",
        "mrp": 58,
        "price": 48,
        "discount_percent": 17,
        "rating": 4.6,
        "rating_count": 1420,
        "is_rx_required": False,
        "is_bestseller": False,
        "manufacturer": "Sanofi India",
        "indications": ["dental pain", "joint pain", "muscle pain", "fever", "inflammation"],
        "stock": 95
    },
    {
        "id": 4,
        "name": "Volini Pain Relief Gel",
        "salt": "Diclofenac Diethylamine + Methyl Salicylate",
        "category_id": "pain-fever",
        "category_name": "Pain & Fever",
        "dosage_form": "Gel",
        "pack_size": "50 g tube",
        "mrp": 180,
        "price": 155,
        "discount_percent": 14,
        "rating": 4.7,
        "rating_count": 1820,
        "is_rx_required": False,
        "is_bestseller": True,
        "manufacturer": "Sun Pharmaceutical",
        "indications": ["back pain", "sprain", "joint strain", "neck pain", "knee pain"],
        "stock": 80
    },
    {
        "id": 5,
        "name": "Naprosyn 500 Tablet",
        "salt": "Naproxen 500 mg",
        "category_id": "pain-fever",
        "category_name": "Pain & Fever",
        "dosage_form": "Tablet",
        "pack_size": "15 tablets per strip",
        "mrp": 120,
        "price": 99,
        "discount_percent": 18,
        "rating": 4.5,
        "rating_count": 640,
        "is_rx_required": True,
        "is_bestseller": False,
        "manufacturer": "RPG Life Sciences",
        "indications": ["osteoarthritis", "ankylosing spondylitis", "severe pain", "gout", "migraine"],
        "stock": 60
    },

    # 2. Cold & Cough
    {
        "id": 6,
        "name": "Cetzine 10mg Tablet",
        "salt": "Cetirizine Hydrochloride 10 mg",
        "category_id": "cold-respiratory",
        "category_name": "Cold & Cough",
        "dosage_form": "Tablet",
        "pack_size": "10 tablets per strip",
        "mrp": 42,
        "price": 35,
        "discount_percent": 16,
        "rating": 4.7,
        "rating_count": 1650,
        "is_rx_required": False,
        "is_bestseller": True,
        "manufacturer": "Dr. Reddy's Laboratories",
        "indications": ["runny nose", "sneezing", "allergic rhinitis", "watery eyes", "itching", "hives", "cold"],
        "stock": 190
    },
    {
        "id": 7,
        "name": "Montair-LC Tablet",
        "salt": "Montelukast 10 mg + Levocetirizine 5 mg",
        "category_id": "cold-respiratory",
        "category_name": "Cold & Cough",
        "dosage_form": "Tablet",
        "pack_size": "15 tablets per strip",
        "mrp": 210,
        "price": 175,
        "discount_percent": 16,
        "rating": 4.8,
        "rating_count": 1280,
        "is_rx_required": True,
        "is_bestseller": True,
        "manufacturer": "Cipla Ltd",
        "indications": ["asthma", "allergic rhinitis", "chronic cough", "breathlessness", "allergy"],
        "stock": 115
    },
    {
        "id": 8,
        "name": "Ascoril D Plus Cough Syrup",
        "salt": "Dextromethorphan + Phenylephrine + Chlorpheniramine",
        "category_id": "cold-respiratory",
        "category_name": "Cold & Cough",
        "dosage_form": "Syrup",
        "pack_size": "100 ml bottle",
        "mrp": 135,
        "price": 115,
        "discount_percent": 15,
        "rating": 4.6,
        "rating_count": 920,
        "is_rx_required": False,
        "is_bestseller": False,
        "manufacturer": "Glenmark Pharmaceuticals",
        "indications": ["dry cough", "throat tickle", "congestion", "cold", "sneezing"],
        "stock": 70
    },
    {
        "id": 9,
        "name": "Asthalin 100mcg Inhaler",
        "salt": "Salbutamol 100 mcg / dose",
        "category_id": "cold-respiratory",
        "category_name": "Cold & Cough",
        "dosage_form": "Inhaler",
        "pack_size": "200 metered doses",
        "mrp": 165,
        "price": 142,
        "discount_percent": 14,
        "rating": 4.9,
        "rating_count": 2100,
        "is_rx_required": True,
        "is_bestseller": True,
        "manufacturer": "Cipla Ltd",
        "indications": ["asthma attack", "bronchospasm", "wheezing", "shortness of breath", "copd"],
        "stock": 130
    },
    {
        "id": 10,
        "name": "Otrivin Oxy Fast Relief Nasal Spray",
        "salt": "Oxymetazoline 0.05% w/v",
        "category_id": "cold-respiratory",
        "category_name": "Cold & Cough",
        "dosage_form": "Nasal Spray",
        "pack_size": "10 ml spray",
        "mrp": 110,
        "price": 95,
        "discount_percent": 13,
        "rating": 4.7,
        "rating_count": 1540,
        "is_rx_required": False,
        "is_bestseller": False,
        "manufacturer": "GlaxoSmithKline",
        "indications": ["blocked nose", "sinus congestion", "nasal blockage", "cold"],
        "stock": 85
    },

    # 3. Antibiotics & Infections
    {
        "id": 11,
        "name": "Augmentin 625 Duo Tablet",
        "salt": "Amoxicillin 500 mg + Clavulanic Acid 125 mg",
        "category_id": "antibiotics",
        "category_name": "Antibiotics & Infections",
        "dosage_form": "Tablet",
        "pack_size": "10 tablets per strip",
        "mrp": 225,
        "price": 192,
        "discount_percent": 15,
        "rating": 4.8,
        "rating_count": 3100,
        "is_rx_required": True,
        "is_bestseller": True,
        "manufacturer": "GlaxoSmithKline",
        "indications": ["bacterial infection", "throat infection", "tonsillitis", "dental infection", "pneumonia", "sinusitis"],
        "stock": 160
    },
    {
        "id": 12,
        "name": "Azithral 500 Tablet",
        "salt": "Azithromycin 500 mg",
        "category_id": "antibiotics",
        "category_name": "Antibiotics & Infections",
        "dosage_form": "Tablet",
        "pack_size": "5 tablets per strip",
        "mrp": 128,
        "price": 108,
        "discount_percent": 16,
        "rating": 4.7,
        "rating_count": 2780,
        "is_rx_required": True,
        "is_bestseller": True,
        "manufacturer": "Alembic Pharmaceuticals",
        "indications": ["chest infection", "throat infection", "typhoid", "bronchitis", "chlamydia", "skin infection"],
        "stock": 140
    },
    {
        "id": 13,
        "name": "Cifran 500 Tablet",
        "salt": "Ciprofloxacin 500 mg",
        "category_id": "antibiotics",
        "category_name": "Antibiotics & Infections",
        "dosage_form": "Tablet",
        "pack_size": "10 tablets per strip",
        "mrp": 95,
        "price": 79,
        "discount_percent": 17,
        "rating": 4.5,
        "rating_count": 890,
        "is_rx_required": True,
        "is_bestseller": False,
        "manufacturer": "Sun Pharmaceutical",
        "indications": ["urinary tract infection", "uti", "gastroenteritis", "bacterial diarrhea", "typhoid"],
        "stock": 90
    },
    {
        "id": 14,
        "name": "Taxim-O 200 Tablet",
        "salt": "Cefixime 200 mg",
        "category_id": "antibiotics",
        "category_name": "Antibiotics & Infections",
        "dosage_form": "Tablet",
        "pack_size": "10 tablets per strip",
        "mrp": 175,
        "price": 149,
        "discount_percent": 15,
        "rating": 4.6,
        "rating_count": 1150,
        "is_rx_required": True,
        "is_bestseller": False,
        "manufacturer": "Alkem Laboratories",
        "indications": ["typhoid fever", "ear infection", "uti", "bronchitis", "respiratory tract infection"],
        "stock": 105
    },

    # 4. Digestion & Acidity
    {
        "id": 15,
        "name": "Pantocid DSR Capsule",
        "salt": "Pantoprazole 40 mg + Domperidone 30 mg SR",
        "category_id": "digestive-gastro",
        "category_name": "Digestion & Acidity",
        "dosage_form": "Capsule",
        "pack_size": "15 capsules per strip",
        "mrp": 155,
        "price": 132,
        "discount_percent": 15,
        "rating": 4.8,
        "rating_count": 3400,
        "is_rx_required": True,
        "is_bestseller": True,
        "manufacturer": "Sun Pharmaceutical",
        "indications": ["acidity", "acid reflux", "gerd", "heartburn", "indigestion", "nausea", "gastritis"],
        "stock": 200
    },
    {
        "id": 16,
        "name": "Pan 40 Tablet",
        "salt": "Pantoprazole 40 mg",
        "category_id": "digestive-gastro",
        "category_name": "Digestion & Acidity",
        "dosage_form": "Tablet",
        "pack_size": "15 tablets per strip",
        "mrp": 140,
        "price": 118,
        "discount_percent": 16,
        "rating": 4.7,
        "rating_count": 2150,
        "is_rx_required": True,
        "is_bestseller": True,
        "manufacturer": "Alkem Laboratories",
        "indications": ["acidity", "peptic ulcer", "stomach pain", "acid reflux", "gastritis"],
        "stock": 170
    },
    {
        "id": 17,
        "name": "Digene Mint Antacid Gel",
        "salt": "Magnesium Hydroxide + Aluminium Hydroxide + Simethicone",
        "category_id": "digestive-gastro",
        "category_name": "Digestion & Acidity",
        "dosage_form": "Liquid Gel",
        "pack_size": "200 ml bottle",
        "mrp": 160,
        "price": 135,
        "discount_percent": 15,
        "rating": 4.8,
        "rating_count": 2980,
        "is_rx_required": False,
        "is_bestseller": True,
        "manufacturer": "Abbott India",
        "indications": ["gas", "acidity", "bloating", "stomach burn", "indigestion"],
        "stock": 140
    },
    {
        "id": 18,
        "name": "Sporlac-DS Tablet",
        "salt": "Lactobacillus acidophilus (Probiotic)",
        "category_id": "digestive-gastro",
        "category_name": "Digestion & Acidity",
        "dosage_form": "Tablet",
        "pack_size": "20 tablets per strip",
        "mrp": 125,
        "price": 105,
        "discount_percent": 16,
        "rating": 4.7,
        "rating_count": 940,
        "is_rx_required": False,
        "is_bestseller": False,
        "manufacturer": "Sanzyme Biogenics",
        "indications": ["diarrhea", "gut flora balance", "antibiotic-associated diarrhea", "loose motions", "stomach upset"],
        "stock": 110
    },

    # 5. Heart & Blood Pressure
    {
        "id": 19,
        "name": "Telma 40 Tablet",
        "salt": "Telmisartan 40 mg",
        "category_id": "heart-bp",
        "category_name": "Heart & Blood Pressure",
        "dosage_form": "Tablet",
        "pack_size": "30 tablets per strip",
        "mrp": 240,
        "price": 204,
        "discount_percent": 15,
        "rating": 4.9,
        "rating_count": 3200,
        "is_rx_required": True,
        "is_bestseller": True,
        "manufacturer": "Glenmark Pharmaceuticals",
        "indications": ["high blood pressure", "hypertension", "heart attack prevention", "cardiac health"],
        "stock": 250
    },
    {
        "id": 20,
        "name": "Amlong 5 Tablet",
        "salt": "Amlodipine 5 mg",
        "category_id": "heart-bp",
        "category_name": "Heart & Blood Pressure",
        "dosage_form": "Tablet",
        "pack_size": "15 tablets per strip",
        "mrp": 62,
        "price": 52,
        "discount_percent": 16,
        "rating": 4.7,
        "rating_count": 1840,
        "is_rx_required": True,
        "is_bestseller": False,
        "manufacturer": "Micro Labs Ltd",
        "indications": ["hypertension", "angina", "chest pain", "high bp"],
        "stock": 180
    },
    {
        "id": 21,
        "name": "Ecosprin 75 Tablet",
        "salt": "Aspirin 75 mg",
        "category_id": "heart-bp",
        "category_name": "Heart & Blood Pressure",
        "dosage_form": "Tablet",
        "pack_size": "14 tablets per strip",
        "mrp": 12,
        "price": 10,
        "discount_percent": 17,
        "rating": 4.9,
        "rating_count": 4800,
        "is_rx_required": True,
        "is_bestseller": True,
        "manufacturer": "USV Pvt Ltd",
        "indications": ["blood thinner", "heart attack prevention", "stroke prevention", "clot prevention"],
        "stock": 400
    },
    {
        "id": 22,
        "name": "Rosuvas 10 Tablet",
        "salt": "Rosuvastatin 10 mg",
        "category_id": "heart-bp",
        "category_name": "Heart & Blood Pressure",
        "dosage_form": "Tablet",
        "pack_size": "15 tablets per strip",
        "mrp": 260,
        "price": 218,
        "discount_percent": 16,
        "rating": 4.8,
        "rating_count": 1750,
        "is_rx_required": True,
        "is_bestseller": False,
        "manufacturer": "Sun Pharmaceutical",
        "indications": ["high cholesterol", "triglycerides", "lipid control", "atherosclerosis"],
        "stock": 120
    },

    # 6. Diabetes Care
    {
        "id": 23,
        "name": "Glycomet 500 SR Tablet",
        "salt": "Metformin Hydrochloride 500 mg SR",
        "category_id": "diabetes",
        "category_name": "Diabetes Care",
        "dosage_form": "Tablet",
        "pack_size": "20 tablets per strip",
        "mrp": 48,
        "price": 40,
        "discount_percent": 17,
        "rating": 4.8,
        "rating_count": 4100,
        "is_rx_required": True,
        "is_bestseller": True,
        "manufacturer": "USV Pvt Ltd",
        "indications": ["type 2 diabetes", "high blood sugar", "insulin resistance", "pcos"],
        "stock": 350
    },
    {
        "id": 24,
        "name": "Glycomet-GP 2 Tablet",
        "salt": "Glimepiride 2 mg + Metformin 500 mg SR",
        "category_id": "diabetes",
        "category_name": "Diabetes Care",
        "dosage_form": "Tablet",
        "pack_size": "15 tablets per strip",
        "mrp": 145,
        "price": 122,
        "discount_percent": 16,
        "rating": 4.8,
        "rating_count": 2890,
        "is_rx_required": True,
        "is_bestseller": True,
        "manufacturer": "USV Pvt Ltd",
        "indications": ["diabetes mellitus", "high fasting sugar", "hba1c control", "sugar spike"],
        "stock": 210
    },
    {
        "id": 25,
        "name": "Januvia 100mg Tablet",
        "salt": "Sitagliptin 100 mg",
        "category_id": "diabetes",
        "category_name": "Diabetes Care",
        "dosage_form": "Tablet",
        "pack_size": "7 tablets per strip",
        "mrp": 320,
        "price": 275,
        "discount_percent": 14,
        "rating": 4.7,
        "rating_count": 860,
        "is_rx_required": True,
        "is_bestseller": False,
        "manufacturer": "MSD Pharmaceuticals",
        "indications": ["dpp-4 inhibitor", "type 2 diabetes", "blood sugar regulation"],
        "stock": 80
    },
    {
        "id": 26,
        "name": "Accu-Chek Active Test Strips (50 Strips)",
        "salt": "Blood Glucose Test Strips",
        "category_id": "diabetes",
        "category_name": "Diabetes Care",
        "dosage_form": "Diagnostic Strips",
        "pack_size": "50 strips box",
        "mrp": 1150,
        "price": 920,
        "discount_percent": 20,
        "rating": 4.9,
        "rating_count": 5200,
        "is_rx_required": False,
        "is_bestseller": True,
        "manufacturer": "Roche Diabetes Care",
        "indications": ["sugar check", "blood glucose test", "glucometer test", "diabetes check"],
        "stock": 150
    },

    # 7. Vitamins & Nutrition
    {
        "id": 27,
        "name": "Shelcal 500 Tablet",
        "salt": "Calcium 500 mg + Vitamin D3 250 IU",
        "category_id": "vitamins-supplements",
        "category_name": "Vitamins & Nutrition",
        "dosage_form": "Tablet",
        "pack_size": "15 tablets per strip",
        "mrp": 138,
        "price": 116,
        "discount_percent": 16,
        "rating": 4.8,
        "rating_count": 3650,
        "is_rx_required": False,
        "is_bestseller": True,
        "manufacturer": "Torrent Pharmaceuticals",
        "indications": ["calcium deficiency", "bone health", "osteoporosis", "joint weakness", "pregnancy calcium"],
        "stock": 260
    },
    {
        "id": 28,
        "name": "Becosules Z Capsules",
        "salt": "B-Complex + Vitamin C + Zinc",
        "category_id": "vitamins-supplements",
        "category_name": "Vitamins & Nutrition",
        "dosage_form": "Capsule",
        "pack_size": "20 capsules per strip",
        "mrp": 55,
        "price": 46,
        "discount_percent": 16,
        "rating": 4.8,
        "rating_count": 4200,
        "is_rx_required": False,
        "is_bestseller": True,
        "manufacturer": "Pfizer Ltd",
        "indications": ["mouth ulcers", "fatigue", "general weakness", "vitamin b deficiency", "immunity"],
        "stock": 310
    },
    {
        "id": 29,
        "name": "Uprise-D3 60K Capsule",
        "salt": "Cholecalciferol (Vitamin D3) 60,000 IU",
        "category_id": "vitamins-supplements",
        "category_name": "Vitamins & Nutrition",
        "dosage_form": "Softgel Capsule",
        "pack_size": "4 capsules per pack",
        "mrp": 140,
        "price": 118,
        "discount_percent": 16,
        "rating": 4.9,
        "rating_count": 2850,
        "is_rx_required": False,
        "is_bestseller": True,
        "manufacturer": "Alkem Laboratories",
        "indications": ["vitamin d deficiency", "bone density", "fatigue", "muscle weakness", "immunity boost"],
        "stock": 190
    },
    {
        "id": 30,
        "name": "Zincovit Tablet",
        "salt": "Multivitamin + Multimineral with Grape Seed Extract",
        "category_id": "vitamins-supplements",
        "category_name": "Vitamins & Nutrition",
        "dosage_form": "Tablet",
        "pack_size": "15 tablets per strip",
        "mrp": 110,
        "price": 92,
        "discount_percent": 16,
        "rating": 4.7,
        "rating_count": 2100,
        "is_rx_required": False,
        "is_bestseller": False,
        "manufacturer": "Apex Laboratories",
        "indications": ["daily wellness", "low stamina", "immunity", "nutritional deficiency", "recovery"],
        "stock": 180
    },

    # 8. Skin & Dermatology
    {
        "id": 31,
        "name": "Betnovate-N Cream",
        "salt": "Betamethasone Valerate + Neomycin Skin Cream",
        "category_id": "skin-hair",
        "category_name": "Skin & Dermatology",
        "dosage_form": "Cream",
        "pack_size": "20 g tube",
        "mrp": 58,
        "price": 49,
        "discount_percent": 15,
        "rating": 4.6,
        "rating_count": 1890,
        "is_rx_required": True,
        "is_bestseller": True,
        "manufacturer": "GlaxoSmithKline",
        "indications": ["eczema", "skin infection", "rash", "dermatitis", "itchy skin", "red patches"],
        "stock": 140
    },
    {
        "id": 32,
        "name": "Candid-B Cream",
        "salt": "Clotrimazole + Beclomethasone Dipropionate",
        "category_id": "skin-hair",
        "category_name": "Skin & Dermatology",
        "dosage_form": "Cream",
        "pack_size": "20 g tube",
        "mrp": 145,
        "price": 122,
        "discount_percent": 16,
        "rating": 4.8,
        "rating_count": 2340,
        "is_rx_required": True,
        "is_bestseller": True,
        "manufacturer": "Glenmark Pharmaceuticals",
        "indications": ["fungal infection", "ringworm", "sweat rash", "jock itch", "athlete foot", "skin itching"],
        "stock": 160
    },
    {
        "id": 33,
        "name": "Clindac A 1% Gel",
        "salt": "Clindamycin Phosphate 1% w/w",
        "category_id": "skin-hair",
        "category_name": "Skin & Dermatology",
        "dosage_form": "Gel",
        "pack_size": "20 g tube",
        "mrp": 210,
        "price": 178,
        "discount_percent": 15,
        "rating": 4.7,
        "rating_count": 1120,
        "is_rx_required": True,
        "is_bestseller": False,
        "manufacturer": "Alkem Laboratories",
        "indications": ["acne", "pimples", "facial blemishes", "skin breakouts"],
        "stock": 90
    },

    # 9. Health Devices & First Aid
    {
        "id": 34,
        "name": "Omron HEM-7120 Digital BP Monitor",
        "salt": "Fully Automatic Upper Arm Blood Pressure Monitor",
        "category_id": "first-aid-devices",
        "category_name": "Devices & First Aid",
        "dosage_form": "Medical Device",
        "pack_size": "1 Unit with Medium Cuff",
        "mrp": 2640,
        "price": 1999,
        "discount_percent": 24,
        "rating": 4.9,
        "rating_count": 4820,
        "is_rx_required": False,
        "is_bestseller": True,
        "manufacturer": "Omron Healthcare",
        "indications": ["blood pressure monitoring", "hypertension check", "pulse rate", "heart monitor"],
        "stock": 45
    },
    {
        "id": 35,
        "name": "Dettol Antiseptic Liquid (500 ml)",
        "salt": "Chloroxylenol Antiseptic Disinfectant",
        "category_id": "first-aid-devices",
        "category_name": "Devices & First Aid",
        "dosage_form": "Liquid",
        "pack_size": "500 ml bottle",
        "mrp": 215,
        "price": 189,
        "discount_percent": 12,
        "rating": 4.9,
        "rating_count": 6200,
        "is_rx_required": False,
        "is_bestseller": True,
        "manufacturer": "Reckitt Benckiser",
        "indications": ["cuts", "wounds", "antiseptic wash", "first aid", "hygiene"],
        "stock": 190
    },
    {
        "id": 36,
        "name": "Hansaplast Washproof Bandages",
        "salt": "Breathable Sterile Medicated Bandages",
        "category_id": "first-aid-devices",
        "category_name": "Devices & First Aid",
        "dosage_form": "Adhesive Plaster",
        "pack_size": "Pack of 30 Strips",
        "mrp": 90,
        "price": 75,
        "discount_percent": 17,
        "rating": 4.8,
        "rating_count": 3100,
        "is_rx_required": False,
        "is_bestseller": False,
        "manufacturer": "Beiersdorf",
        "indications": ["minor cuts", "blisters", "scrapes", "wound dressing"],
        "stock": 250
    }
]


def _ensure_catalog_file():
    """Ensure data/pharmacy_catalog.json exists with valid data."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        payload = {
            "categories": DEFAULT_CATEGORIES,
            "products": INITIAL_PRODUCTS,
            "next_id": len(INITIAL_PRODUCTS) + 1
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)


def load_catalog_data():
    """Load catalog from file or initialize defaults."""
    _ensure_catalog_file()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception:
        return {"categories": DEFAULT_CATEGORIES, "products": INITIAL_PRODUCTS, "next_id": 100}


def save_catalog_data(data):
    """Save catalog back to JSON store."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_categories():
    """Return all product categories."""
    data = load_catalog_data()
    return data.get("categories", DEFAULT_CATEGORIES)


def get_category_by_id(cat_id):
    """Find a category by id."""
    cats = get_categories()
    for c in cats:
        if c["id"] == cat_id:
            return c
    return None


def get_all_products(category=None, search=None, rx_filter=None, sort_by=None):
    """
    Search and filter pharmacy products.
    Matches across Name, Salt, Category, Indications/Symptoms, and Dosage Form.
    """
    data = load_catalog_data()
    products = data.get("products", [])

    # Filter by category
    if category and category != "all":
        products = [p for p in products if p.get("category_id") == category]

    # Filter by Rx / OTC
    if rx_filter == "otc":
        products = [p for p in products if not p.get("is_rx_required")]
    elif rx_filter == "rx":
        products = [p for p in products if p.get("is_rx_required")]

    # Search keyword filtering
    if search:
        q = search.strip().casefold()
        tokens = [t for t in re.split(r"\s+", q) if len(t) > 1]
        if not tokens:
            tokens = [q]

        def match_score(p):
            score = 0
            name_low = p.get("name", "").casefold()
            salt_low = p.get("salt", "").casefold()
            cat_low = p.get("category_name", "").casefold()
            mfg_low = p.get("manufacturer", "").casefold()
            indications = [str(x).casefold() for x in p.get("indications", [])]

            for tok in tokens:
                if tok in name_low:
                    score += 10
                if tok in salt_low:
                    score += 8
                if any(tok in ind for ind in indications):
                    score += 6
                if tok in cat_low:
                    score += 4
                if tok in mfg_low:
                    score += 3
            return score

        matched = []
        for p in products:
            score = match_score(p)
            if score > 0:
                matched.append((score, p))
        matched.sort(key=lambda x: x[0], reverse=True)
        products = [m[1] for m in matched]

    # Sorting
    if sort_by == "price_low":
        products.sort(key=lambda x: x.get("price", 0))
    elif sort_by == "price_high":
        products.sort(key=lambda x: x.get("price", 0), reverse=True)
    elif sort_by == "discount":
        products.sort(key=lambda x: x.get("discount_percent", 0), reverse=True)
    elif sort_by == "rating":
        products.sort(key=lambda x: x.get("rating", 0), reverse=True)

    return products


def get_product_by_id(product_id):
    """Find a product by its integer id."""
    data = load_catalog_data()
    for p in data.get("products", []):
        if p.get("id") == int(product_id):
            return p
    return None


def add_product(product_dict):
    """Add a new product to the catalog."""
    data = load_catalog_data()
    next_id = data.get("next_id", 100)

    # Determine category name
    cat_id = product_dict.get("category_id", "pain-fever")
    cat = get_category_by_id(cat_id)
    cat_name = cat["name"] if cat else "General Medicine"

    # Compute discount
    mrp = float(product_dict.get("mrp", 0))
    price = float(product_dict.get("price", mrp))
    discount = int(round(((mrp - price) / mrp) * 100)) if mrp > price > 0 else 0

    indications_raw = product_dict.get("indications", [])
    if isinstance(indications_raw, str):
        indications = [x.strip() for x in indications_raw.split(",") if x.strip()]
    else:
        indications = list(indications_raw)

    new_prod = {
        "id": next_id,
        "name": product_dict.get("name", "").strip(),
        "salt": product_dict.get("salt", "").strip(),
        "category_id": cat_id,
        "category_name": cat_name,
        "dosage_form": product_dict.get("dosage_form", "Tablet").strip(),
        "pack_size": product_dict.get("pack_size", "10 tablets").strip(),
        "mrp": mrp,
        "price": price,
        "discount_percent": discount,
        "rating": float(product_dict.get("rating", 4.8)),
        "rating_count": int(product_dict.get("rating_count", 150)),
        "is_rx_required": bool(product_dict.get("is_rx_required", False)),
        "is_bestseller": bool(product_dict.get("is_bestseller", False)),
        "manufacturer": product_dict.get("manufacturer", "Care Cliniq Pharma").strip(),
        "indications": indications,
        "stock": int(product_dict.get("stock", 100))
    }

    data["products"].insert(0, new_prod)
    data["next_id"] = next_id + 1
    save_catalog_data(data)
    return new_prod


def update_product(product_id, update_dict):
    """Update an existing product."""
    data = load_catalog_data()
    for idx, p in enumerate(data.get("products", [])):
        if p.get("id") == int(product_id):
            mrp = float(update_dict.get("mrp", p.get("mrp", 0)))
            price = float(update_dict.get("price", p.get("price", mrp)))
            discount = int(round(((mrp - price) / mrp) * 100)) if mrp > price > 0 else 0

            cat_id = update_dict.get("category_id", p.get("category_id"))
            cat = get_category_by_id(cat_id)
            cat_name = cat["name"] if cat else p.get("category_name")

            indications_raw = update_dict.get("indications", p.get("indications", []))
            if isinstance(indications_raw, str):
                indications = [x.strip() for x in indications_raw.split(",") if x.strip()]
            else:
                indications = list(indications_raw)

            p.update({
                "name": update_dict.get("name", p.get("name")),
                "salt": update_dict.get("salt", p.get("salt")),
                "category_id": cat_id,
                "category_name": cat_name,
                "dosage_form": update_dict.get("dosage_form", p.get("dosage_form")),
                "pack_size": update_dict.get("pack_size", p.get("pack_size")),
                "mrp": mrp,
                "price": price,
                "discount_percent": discount,
                "is_rx_required": bool(update_dict.get("is_rx_required", p.get("is_rx_required"))),
                "is_bestseller": bool(update_dict.get("is_bestseller", p.get("is_bestseller"))),
                "manufacturer": update_dict.get("manufacturer", p.get("manufacturer")),
                "indications": indications,
                "stock": int(update_dict.get("stock", p.get("stock", 100)))
            })
            save_catalog_data(data)
            return p
    return None


def delete_product(product_id):
    """Delete a product from the catalog."""
    data = load_catalog_data()
    initial_len = len(data.get("products", []))
    data["products"] = [p for p in data["products"] if p.get("id") != int(product_id)]
    if len(data["products"]) < initial_len:
        save_catalog_data(data)
        return True
    return False


def get_category_stats():
    """Return dictionary of category IDs with product count and average price."""
    data = load_catalog_data()
    products = data.get("products", [])
    categories = data.get("categories", DEFAULT_CATEGORIES)

    stats = {}
    for c in categories:
        cid = c["id"]
        if cid == "all":
            matching = products
        else:
            matching = [p for p in products if p.get("category_id") == cid]

        prices = [p.get("price", 0) for p in matching]
        avg_price = round(sum(prices) / len(prices), 1) if prices else 0
        stats[cid] = {
            "name": c["name"],
            "count": len(matching),
            "avg_price": avg_price
        }
    return stats
