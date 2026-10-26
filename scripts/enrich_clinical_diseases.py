"""Enrich parsed 227 clinical diseases with cardinal symptoms and emergency red flags.

Maps clinical-grade patient presentations to each disease record so the ML
classifier can accurately match patient symptom reports to guideline therapies.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PARSED_FILE = PROJECT_ROOT / "app" / "ml" / "parsed_clinical_reference.json"
ENRICHED_FILE = PROJECT_ROOT / "app" / "ml" / "clinical_227_enriched.json"

# Detailed cardinal symptom descriptions for all 227 diseases
CLINICAL_SYMPTOMS_MAP = {
    # 1-40 Cardiovascular
    1: "Morning occipital headache, dizziness, lightheadedness, episodic blurred vision, palpitations, mild chest tightness, often asymptomatic with high blood pressure readings above 140/90",
    2: "Severe throbbing headache, blood pressure over 180/120 mmHg, sudden blurred vision or vision loss, acute shortness of breath, crushing chest tightness, confusion, nausea, vomiting",
    3: "Exertional retrosternal chest pressure or squeezing discomfort, chest tightness provoked by walking uphill or emotional stress, pain radiating to left shoulder neck or jaw, relieved within minutes by rest or nitroglycerin",
    4: "Acute severe crushing substernal chest pain lasting over 20 minutes, radiation to left arm neck and jaw, cold diaphoresis, severe shortness of breath, nausea, vomiting, profound sense of impending doom",
    5: "Accelerating or crescendo chest tightness occurring at rest or with minimal exertion, prolonged substernal chest pain, shortness of breath, diaphoresis, lightheadedness without obvious ST elevation",
    6: "Progressive shortness of breath on exertion, orthopnea needing multiple pillows to sleep, paroxysmal nocturnal dyspnea, bilateral pitting ankle edema, persistent dry or pink frothy cough, extreme fatigue, abdominal fullness",
    7: "Exertional dyspnea, exercise intolerance, fatigue, bilateral lower leg swelling, rapid weight gain from fluid retention, elevated jugular venous pulsation in older hypertensive or diabetic patients",
    8: "Acute severe respiratory distress, inability to lie flat, coughing copious pink frothy sputum, bilateral lung crackles, cold clammy extremities, cyanosis, severe agitation and air hunger",
    9: "Irregularly irregular rapid heartbeat, fluttering palpitations in chest, sudden unexplained fatigue, dizziness, lightheadedness, exertional shortness of breath, mild chest tightness",
    10: "Regular rapid fluttering palpitations (heart rate around 150 bpm), fatigue, shortness of breath on exertion, lightheadedness, mild chest discomfort",
    11: "Sudden onset of rapid regular pounding palpitations (heart rate 160-220 bpm) starting and stopping abruptly, lightheadedness, neck fullness, anxiety, shortness of breath, polyuria after episode",
    12: "Sudden sustained racing heart, palpitations, lightheadedness, syncope or near-syncope, chest pain, shortness of breath, hemodynamic instability",
    13: "Sudden collapse, unresponsiveness, absence of pulse and normal breathing, cardiac arrest, gasping agonal respirations",
    14: "Persistent slow heart rate below 50 bpm, fatigue, chronic dizziness, near-syncope or blackout spells (Stokes-Adams attacks), exercise intolerance, confusion in elderly",
    15: "Profound bradycardia (heart rate 30-40 bpm), recurrent fainting spells (syncope), severe lightheadedness, marked fatigue, dyspnea on minimal exertion, cannon A waves in neck",
    16: "Episodic rapid regular palpitations, sudden tachycardia, dizziness, syncope in young patients, ECG showing short PR interval and delta wave",
    17: "Recurrent unexplained fainting (syncope) triggered by emotional stress, sudden loud noise, or swimming; palpitations, family history of sudden cardiac arrest",
    18: "Dyspnea on exertion, atypical chest pain, exertional dizziness or syncope, palpitations, systolic ejection murmur that increases with Valsalva maneuver",
    19: "Progressive exercise intolerance, fatigue, shortness of breath, orthopnea, bilateral lower limb edema, abdominal distension, history of viral illness or heavy alcohol use",
    20: "Sharp pleuritic retrosternal chest pain aggravated by deep inspiration and coughing, pain relieved by sitting up and leaning forward, low-grade fever, pericardial friction rub",
    21: "Severe dyspnea, orthopnea, distant or muffled heart sounds, elevated jugular venous pressure, systemic hypotension (Beck triad), pulsus paradoxus, cold clammy skin",
    22: "Chronic fatigue, exertional dyspnea, marked ascites out of proportion to peripheral edema, hepatic enlargement, elevated JVP with prominent Y descent (Kussmaul sign)",
    23: "Recent flu-like illness followed by sudden chest pain mimicking infarction, breathlessness, fatigue, palpitations, acute heart failure symptoms in young adults",
    24: "Prolonged remittent fever, night sweats, unexplained weight loss, new or changing heart murmur, petechiae, splinter hemorrhages under nails, Osler nodes, Janeway lesions",
    25: "Migratory polyarthritis affecting large joints, high fever, subcutaneous nodules, erythema marginatum rash, Sydenham chorea, history of untreated sore throat 2-3 weeks prior",
    26: "Exertional dyspnea, fatigue, orthopnea, hemoptysis (pulmonary apoplexy), palpitations due to atrial fibrillation, malar flush (mitral facies), low-pitched rumbling diastolic murmur",
    27: "Classic triad of exertional dyspnea, angina pectoris, and syncope upon physical exertion; harsh systolic crescendo-decrescendo murmur radiating to carotids",
    28: "Exertional dyspnea, awareness of pounding heartbeat in chest and neck, wide pulse pressure (water-hammer pulse), head nodding with heartbeats, early diastolic decrescendo murmur",
    29: "Fatigue, exertional dyspnea, orthopnea, palpitations from atrial fibrillation, holosystolic murmur at cardiac apex radiating to the left axilla",
    30: "Atypical sharp chest pain, palpitations, anxiety, panic-like symptoms, mid-systolic click followed by late systolic murmur at cardiac apex",
    31: "Sudden onset of excruciating tearing or ripping chest pain radiating through to the upper back and interscapular region, pulse asymmetry between arms, neurological deficits, severe hypertension or shock",
    32: "Often asymptomatic pulsatile abdominal mass near umbilicus; or sudden severe constant abdominal and back pain with hypotension indicating rupture",
    33: "Intermittent claudication (cramping pain in calf, thigh, or buttock induced by walking and relieved within minutes by rest), cold pale feet, diminished peripheral pulses, slow wound healing",
    34: "Acute onset of severe extremity pain, pallor, pulselessness, paresthesias, poikilothermia (cold limb), and paralysis (the 6 Ps of acute limb ischemia)",
    35: "Unilateral calf or thigh swelling, localized calf warmth, erythema, tenderness along deep veins, pain aggravated by dorsiflexion of foot (Homan sign)",
    36: "Sudden acute pleuritic chest pain, unexplained shortness of breath, tachypnea, tachycardia, hemoptysis, lightheadedness, syncope in patients with risk factors like immobility or surgery",
    37: "Aching leg heaviness, lower leg swelling worsened by prolonged standing, visibly dilated tortuous veins, stasis dermatitis, skin hyperpigmentation, medial malleolus venous ulcers",
    38: "Painful, tender, erythematous cord-like induration along a superficial vein of the lower or upper limb, localized warmth and swelling without deep calf edema",
    39: "Usually asymptomatic silent lipid elevation; in severe familial cases tendon xanthomas on Achilles tendon, xanthelasma around eyelids, corneal arcus before age 50",
    40: "Usually asymptomatic elevated triglycerides; in severe hypertriglyceridemia (> 1000 mg/dL) eruptive xanthomas on buttocks and extensor surfaces, lipemia retinalis, acute epigastric pancreatitis pain",

    # 41-75 Respiratory
    41: "Recurrent episodes of expiratory wheezing, shortness of breath, chest tightness, chronic dry cough especially at night or early morning, triggered by cold air, exercise, or dust",
    42: "Severe unrelenting respiratory distress, inability to complete full sentences in one breath, tachypnea > 30 breaths/min, intercostal retractions, silent chest on auscultation, cyanosis, exhaustion",
    43: "Progressive exertional breathlessness, chronic productive cough with morning sputum, audible wheezing, frequent chest infections, barrel chest, prolonged expiratory phase, history of smoking",
    44: "Acute worsening of baseline dyspnea, increased volume and purulence (yellow/green) of sputum, increased coughing, fever, wheezing in a known COPD patient",
    45: "High fever with shaking chills (rigors), productive cough with purulent or rust-colored sputum, localized pleuritic chest pain worsened by deep breathing, tachypnea, crackles on auscultation",
    46: "New fever, purulent endotracheal secretions or sputum, worsening hypoxemia, new pulmonary infiltrates on chest X-ray appearing 48 hours or more after hospital admission",
    47: "Fever, night sweats, weight loss, cough productive of foul-smelling putrid sputum, history of impaired consciousness, alcohol intoxication, or swallowing difficulty",
    48: "Chronic productive cough lasting over 3 weeks, hemoptysis (blood in sputum), low-grade evening fever, drenching night sweats, unexplained weight loss, anorexia, fatigue",
    49: "Persistent chronic cough, hemoptysis, non-responsive to first-line anti-TB medications, progressive weight loss, continuous night sweats, severe lung damage",
    50: "Asymptomatic latent infection with positive tuberculin skin test (Mantoux) or IGRA, normal chest radiography, no cough, no night sweats, no weight loss",
    51: "Chronic cough with copious daily purulent sputum, recurrent respiratory tract infections, recurrent hemoptysis, coarse crackles and wheezing, finger clubbing",
    52: "Recurrent severe chest infections with Pseudomonas, chronic sinusitis, nasal polyps, malabsorption, greasy bulky foul-smelling stools, failure to thrive in childhood, salty-tasting skin",
    53: "Insidious progressive exertional breathlessness, persistent dry hacking cough, bilateral dry inspiratory 'velcro' crackles at lung bases, digital clubbing in older adults",
    54: "Persistent dry cough, exertional shortness of breath, fatigue, erythema nodosum (tender red shins), bilateral ankle swelling, anterior uveitis, blurred vision, bilateral hilar lymphadenopathy",
    55: "Acute dyspnea, dry cough, fever, chills, malaise 4-8 hours after exposure to bird droppings or mold; or insidious breathlessness and weight loss in chronic exposure",
    56: "Sudden onset of sharp unilateral pleuritic chest pain and breathlessness; in tension pneumothorax severe cyanosis, hypotension, tracheal deviation away from affected side",
    57: "Progressive exertional dyspnea, dullness to percussion, decreased breath sounds and vocal resonance at lung base, pleuritic chest pain in inflammatory effusions",
    58: "High swinging fever, rigors, pleural chest pain, persistent cough, malaise, failure of pneumonia to resolve, thick purulent pleural fluid",
    59: "Rapidly worsening severe shortness of breath, profound hypoxemia refractory to oxygen, tachypnea, diffuse bilateral crackles, confusion following sepsis, trauma, or severe pneumonia",
    60: "Loud habitual snoring, witnessed apneas or choking/gasping during sleep, excessive daytime sleepiness, morning headaches, unrefreshing sleep, nocturia, daytime fatigue",
    61: "Progressive breathlessness on exertion, fatigue, lightheadedness, exertional syncope, peripheral edema, loud P2 heart sound, tricuspid regurgitation murmur",
    62: "Persistent cough, hemoptysis, unresolving pneumonia, localized chest pain, hoarseness from recurrent laryngeal nerve palsy, unexplained weight loss, finger clubbing in smokers",
    63: "Rapidly progressing cough, dyspnea, weight loss, superior vena cava obstruction syndrome (facial/neck swelling, dilated neck veins), hyponatremia from SIADH, Cushingoid symptoms from ectopic ACTH",
    64: "Gradual progressive breathlessness on exertion, chronic dry cough, history of heavy exposure to silica dust in mining, quarrying, sandblasting, or stone cutting",
    65: "Poorly controlled severe asthma with recurrent wheezing flares, coughing brownish-black mucus plugs, low-grade fever, malaise, peripheral blood eosinophilia, high IgE",
    66: "Recurrent hemoptysis (ranging from blood-streaked sputum to massive bleeding), chronic cough, weight loss, history of pre-existing tuberculous lung cavity",
    67: "Fever refractory to broad-spectrum antibiotics, pleuritic chest pain, hemoptysis, cough in severely immunocompromised or neutropenic patients, CT halo sign",
    68: "Insidious progressive exertional dyspnea, dry non-productive cough, fever, profound hypoxemia out of proportion to exam findings, bilateral interstitial infiltrates in HIV/CD4 < 200",
    69: "Cough lasting 1-3 weeks following viral upper respiratory infection, clear to purulent sputum, retrosternal burning or chest soreness, low-grade fever, no signs of pneumonia",
    70: "Sudden abrupt onset of high fever, prominent body aches and myalgias, severe headache, dry cough, sore throat, extreme prostration, nasal congestion",
    71: "Fever, dry cough, profound fatigue, loss of taste (ageusia) or smell (anosmia), sore throat, headache, shortness of breath, body aches, gastrointestinal symptoms",
    72: "Catarrhal phase of mild cough and runny nose followed by paroxysms of violent coughing fits ending with a high-pitched inspiratory 'whoop', post-tussive vomiting, subconjunctival hemorrhages",
    73: "Sore throat, low-grade fever, cervical lymphadenopathy ('bull neck' appearance), dense greyish-white pseudomembrane over tonsils and pharynx that bleeds when dislodged, stridor",
    74: "Expectorating large volumes of fresh bright red blood (> 100-200 mL in 24 hours), respiratory distress, choking sensation, hemodynamic instability",
    75: "Sneezing, nasal congestion, clear rhinorrhea, scratchy sore throat, mild dry cough, low-grade fever, malaise, resolving within 7-10 days",

    # 76-125 Gastrointestinal & Hepatobiliary
    76: "Retrosternal burning chest pain (heartburn) worsened after meals and upon lying down, acid regurgitation into mouth, water brash, globus sensation, chronic morning throat clearing",
    77: "Epigastric gnawing or burning pain occurring 2-3 hours after meals or at night, temporarily relieved by food or antacids (duodenal) or worsened by food (gastric), early satiety, nausea",
    78: "Persistent dyspepsia, epigastric discomfort, bloating, postprandial fullness, belching, nausea, history of recurrent gastritis or peptic ulcers",
    79: "Hematemesis (vomiting bright red blood or coffee-ground material), melena (black tarry sticky foul-smelling stools), orthostatic lightheadedness, syncope, tachycardia, hypotension",
    80: "Hematochezia (passage of fresh bright red or maroon blood per rectum), lower abdominal cramping, tenesmus, dizziness, postural hypotension",
    81: "Postprandial fullness, early satiety, epigastric pain or epigastric burning without evidence of structural disease on upper endoscopy, bloating, nausea",
    82: "Persistent nausea, vomiting of undigested food consumed hours earlier, early satiety, severe bloating, postprandial abdominal fullness, erratic blood glucose control in diabetics",
    83: "Progressive dysphagia to both solids and liquids, regurgitation of undigested bland food, retrosternal chest pain, nocturnal coughing, unintentional weight loss",
    84: "Intermittent difficulty swallowing solid foods (dysphagia), history of food impaction requiring emergency endoscopy, refractory heartburn, history of atopy or allergies",
    85: "Progressive difficulty swallowing (solids then liquids), painful swallowing (odynophagia), significant involuntary weight loss, regurgitation, persistent hoarseness",
    86: "Persistent unexplained dyspepsia in older adult, early satiety, epigastric pain, progressive weight loss, vomiting, iron deficiency anemia, palpable left supraclavicular node (Virchow node)",
    87: "Frequent watery loose stools (> 3 per day), crampy abdominal pain, nausea, vomiting, low-grade fever, signs of dehydration (thirst, dry mouth, decreased urination)",
    88: "Profuse painless voluminous watery diarrhea ('rice-water' stools with fishy odor), rapid severe dehydration, sunken eyes, skin tenting, muscle cramps, hypovolemic shock within hours",
    89: "Bloody mucoid diarrhea, lower abdominal cramping, painful defecation (tenesmus), right upper quadrant aching pain, swinging fever, night sweats from hepatic abscess",
    90: "Frequent small-volume bloody mucoid diarrhea, severe abdominal cramps, fever, tenesmus, rectal urgency, toxic systemic appearance",
    91: "Profuse watery foul-smelling diarrhea (>= 3 unformed stools in 24 hours), lower abdominal cramping, low-grade fever, leukocytosis, history of recent antibiotic therapy",
    92: "Recurrent crampy lower abdominal pain related to defecation, alternating diarrhea and constipation, bloating, passage of mucus, relief after passing stool, no alarm features",
    93: "Continuous bloody diarrhea with rectal mucus, severe tenesmus (constant urge to defecate), lower abdominal cramping, low-grade fever, fatigue, weight loss",
    94: "Crampy right lower quadrant abdominal pain, chronic diarrhea, fever, fatigue, weight loss, perianal fissures, fistulae or abscesses, aphthous oral ulcers",
    95: "Chronic foul-smelling greasy diarrhea (steatorrhea), abdominal distension, flatulence, weight loss, chronic fatigue, iron deficiency anemia, itchy blistering rash (dermatitis herpetiformis)",
    96: "Dull periumbilical pain migrating within hours to the right lower quadrant (McBurney point), anorexia, low-grade fever, nausea, vomiting, local guarding, rebound tenderness",
    97: "Sudden severe excruciating epigastric abdominal pain radiating straight through to the back, pain partially relieved by sitting forward, persistent nausea, profuse vomiting",
    98: "Recurrent or persistent severe upper abdominal and back pain, malabsorption, voluminous greasy foul-smelling stools (steatorrhea), weight loss, new-onset diabetes mellitus",
    99: "Painless progressive jaundice with dark urine and pale clay-colored stools, severe generalized pruritus, dull epigastric/back pain, anorexia, rapid weight loss, palpable gallbladder (Courvoisier sign)",
    100: "Severe constant right upper quadrant or epigastric pain lasting > 6 hours radiating to right scapula or shoulder, high fever, chills, nausea, vomiting, positive Murphy sign",
    101: "Episodic severe colicky right upper quadrant or epigastric pain occurring 30 minutes after fatty meals, lasting 1-5 hours, resolving completely, accompanied by nausea",
    102: "Charcot triad of fever with rigors, jaundice, and right upper quadrant abdominal pain; Reynolds pentad adds confusion and septic shock (medical emergency)",
    103: "Abrupt onset of fatigue, malaise, anorexia, nausea, fever followed by dark tea-colored urine, pale stools, yellowish sclera (jaundice), tender hepatomegaly, history of contaminated food/water",
    104: "Acute viral jaundice, malaise, anorexia, right upper quadrant discomfort; severe acute liver failure risk in pregnant women in third trimester",
    105: "Often asymptomatic chronic liver carrier; or episodic fatigue, right upper quadrant discomfort, jaundice, dark urine, spider nevi, palmar erythema in advanced cirrhosis",
    106: "Insidious chronic fatigue, arthralgias, malaise, asymptomatic liver enzyme elevation; progressing over decades to cirrhosis, portal hypertension, and ascites",
    107: "Rapid-onset jaundice, fever, anorexia, tender hepatomegaly, ascites, encephalopathy in a patient with heavy chronic alcohol consumption, AST:ALT ratio > 2",
    108: "Usually asymptomatic silent liver fat accumulation; mild fatigue, dull right upper quadrant discomfort, associated with obesity, type 2 diabetes, dyslipidemia",
    109: "Chronic fatigue, jaundice, spider angiomas, palmar erythema, gynecomastia, caput medusae, abdominal swelling (ascites), bilateral leg swelling, easy bruising, muscle wasting",
    110: "Progressive abdominal distension, fluid thrill, shifting dullness on percussion, rapid weight gain, shortness of breath from diaphragmatic splinting; fever and diffuse abdominal tenderness if SBP",
    111: "Sleep-wake reversal, mild confusion, forgetfulness, irritability, asterixis ('flapping tremor' of outstretched hands), slurred speech, progression to stupor and coma",
    112: "Asymptomatic until massive painless upper GI hemorrhage: vomiting large amounts of bright red blood, passing black tarry stools, lightheadedness, hypovolemic shock",
    113: "Rapidly worsening oliguria or anuria, rising serum creatinine, marked fluid retention in a cirrhotic patient with tense ascites and portal hypertension",
    114: "Sudden rapid onset of deep jaundice, coagulopathy (INR >= 1.5), hepatic encephalopathy (altered mental status), sweet musty breath (fetor hepaticus) in a patient without pre-existing cirrhosis",
    115: "Fluctuating jaundice, fatigue, arthralgias, amenorrhea, elevated serum IgG and transaminases in young or middle-aged women, often associated with other autoimmune diseases",
    116: "Severe chronic generalized pruritus (especially palms and soles, worse at night), progressive fatigue, dark skin pigmentation, xanthelasma, dry eyes and mouth in middle-aged women",
    117: "Chronic fatigue, intermittent jaundice, severe pruritus, episodic right upper quadrant pain and fever from cholangitis, strong association with ulcerative colitis",
    118: "Tremors, dysarthria, dystonia, parkinsonian rigidity, psychiatric changes (personality changes, depression), golden-brown Kayser-Fleischer rings around corneas, jaundice, hepatomegaly",
    119: "Chronic fatigue, arthralgias (especially 2nd and 3rd MCP joints), bronze skin hyperpigmentation, diabetes ('bronze diabetes'), loss of libido, erectile dysfunction, hepatomegaly",
    120: "Unexplained weight loss, dull right upper quadrant pain, palpable hard liver mass, worsening of pre-existing cirrhosis ascites or jaundice, anorexia",
    121: "Change in bowel habits (alternating diarrhea/constipation), unexplained iron deficiency anemia, hematochezia or melena, pencil-thin stools, tenesmus, weight loss in patients > 45",
    122: "Constant severe left lower quadrant abdominal pain, low-grade fever, nausea, constipation or loose stools, localized left lower quadrant tenderness and guarding",
    123: "Painless bright red rectal bleeding coating stool or on toilet paper, prolapse of tissue through anus after defecation, perianal itching, or painful hard bluish perianal lump (thrombosed external)",
    124: "Severe sharp tearing or burning pain during and for hours after defecation, streaks of bright red blood on toilet paper, extreme fear of passing stools, visible midline anal slit",
    125: "Severe throbbing continuous perianal pain worsened by sitting and walking, tender erythematous fluctuant perianal swelling, fever, purulent perianal discharge from fistula",

    # 126-155 Renal & Urology
    126: "Sudden sharp drop in urine output (oliguria < 400 mL/day or anuria), rapid fluid retention causing facial puffiness and ankle swelling, nausea, fatigue, confusion, rising creatinine",
    127: "Gradual fatigue, anorexia, nausea, pruritus (uremic frost), foamy urine, nocturia, persistent bilateral ankle edema, pallor from anemia, uncontrolled hypertension, metallic taste",
    128: "Severe uremic symptoms: intractable nausea and vomiting, pericardial friction rub, encephalopathy, asterixis, profound fluid overload, refractory hyperkalemia, severe metabolic acidosis",
    129: "Heavy frothy urine, massive generalized pitting edema (anasarca) starting in periorbital tissue and spreading to legs, scrotum, and abdomen; significant weight gain, lethargy",
    130: "Child presenting with dramatic facial puffiness upon waking, swollen eyelids, abdominal distension from ascites, pitting ankle edema, heavy proteinuria (3-4+ on dipstick), normal BP",
    131: "Recurrent episodes of visible gross hematuria ('cola-colored' or tea-colored urine) occurring concurrently with or within 1-2 days of an upper respiratory infection (synpharyngitic)",
    132: "Sudden appearance of dark smoky tea-colored urine, facial and periorbital edema, oliguria, hypertension, headache, occurring 1-3 weeks after streptococcal pharyngitis or impetigo",
    133: "Rapidly progressive decline in renal function over days to weeks, hematuria, red blood cell casts, oliguria, systemic vasculitic symptoms (purpura, sinusitis, pulmonary hemorrhage)",
    134: "Peripheral edema, hypertension, foamy urine, active urine sediment (RBCs, cellular casts), joint pains, malar butterfly facial rash, oral ulcers, positive ANA and anti-dsDNA",
    135: "Persistent microalbuminuria progressing to heavy proteinuria, gradual decline in eGFR, worsening hypertension, fluid retention, associated diabetic retinopathy",
    136: "Bilateral dull flank and lower back pain, palpable bilateral enlarged nodular kidneys, gross hematuria, recurrent UTIs, nephrolithiasis, early-onset hypertension",
    137: "Burning sensation during urination (dysuria), frequent small-volume urination, urgent intense need to urinate, suprapubic ache or pressure, cloudy foul-smelling urine, occasional hematuria",
    138: "High spiking fever with shaking chills and rigors, unilateral or bilateral flank pain, costovertebral angle tenderness, nausea, vomiting, dysuria, urinary frequency",
    139: "Repeated episodes (>= 2 in 6 months or >= 3 in a year) of burning urination, frequency, urgency, suprapubic pain, resolving transiently with antibiotics then recurring",
    140: "Sudden agonizing spasmodic flank pain radiating around flank toward the groin, testicle, or labia ('renal colic'); gross or microscopic hematuria, restlessness, nausea, vomiting",
    141: "Hesitancy in starting urination, weak urinary stream, intermittency, post-void dribbling, sensation of incomplete bladder emptying, nocturia (> 2-3 times per night), urinary frequency",
    142: "Sudden complete inability to pass urine despite a painful, agonizingly full bladder; severe suprapubic distension and tenderness, extreme distress",
    143: "High fever, chills, perineal, sacral or suprapubic pain, severe dysuria, urinary frequency, urgency, cloudy urine, exquisite tenderness and swelling on gentle digital rectal exam",
    144: "Chronic pelvic, perineal, or testicular pain lasting > 3 months, discomfort during or after ejaculation, mild dysuria, urinary frequency without active bacterial infection",
    145: "Often asymptomatic in early stages; in advanced disease weak urinary stream, nocturia, hematuria, bone pain (especially spine, pelvis, ribs), lower limb weakness from cord compression",
    146: "Painless visible gross hematuria (intermittent or continuous), microscopic hematuria, urinary urgency, frequency, and dysuria without infection; pelvic pain in advanced disease",
    147: "Classic triad (seen in advanced cases) of painless hematuria, flank pain, and palpable abdominal mass; unexplained fever, weight loss, night sweats, polycythemia or anemia",
    148: "Sudden severe excruciating unilateral scrotal pain, rapid testicular swelling, high-riding transversely oriented testicle, exquisite tenderness, absent cremasteric reflex, nausea",
    149: "Gradual onset of unilateral scrotal pain and swelling over 24-48 hours, erythema, fever, dysuria, pain relieved by scrotal elevation (positive Prehn sign), urethral discharge",
    150: "Consistent and persistent inability to attain or maintain a penile erection sufficient for satisfactory sexual intercourse, reduced sexual desire, psychological distress",
    151: "Sudden compelling urge to urinate that is difficult to defer (urgency), urinary frequency (>= 8 times in 24 hours), nocturia, urge incontinence (leakage before reaching toilet)",
    152: "Involuntary loss of urine on effort or physical exertion, such as coughing, sneezing, laughing, lifting heavy objects, jumping, without premonitory urgency",
    153: "Often asymptomatic until severe; generalized muscle weakness, flaccid paralysis, paresthesias, palpitations, cardiac arrhythmias, peaked T waves and widened QRS on ECG",
    154: "Lethargy, headache, confusion, nausea, vomiting, muscle cramps, gait instability; in acute severe drops (< 120 mmol/L) seizures, cerebral edema, coma, respiratory arrest",
    155: "Generalized muscle weakness, muscle cramps, fasciculations, constipation, paralytic ileus, polyuria, palpitations, prominent U waves and flattened T waves on ECG",

    # 156-190 Endocrine & Metabolic
    156: "Increased thirst (polydipsia), frequent urination (polyuria), increased hunger (polyphagia), unexplained weight loss, chronic fatigue, blurred vision, slow-healing sores, recurrent skin or yeast infections",
    157: "Rapid onset of excessive thirst, frequent large-volume urination, nocturnal enuresis in children, rapid weight loss despite increased appetite, profound fatigue, blurred vision, diabetic ketoacidosis",
    158: "Nausea, intractable vomiting, severe diffuse abdominal pain, deep rapid sighing respirations (Kussmaul breathing), sweet fruity acetone breath odor, extreme dehydration, confusion, lethargy",
    159: "Extreme dehydration, profound lethargy, confusion, hallucinations, focal neurological deficits, blood glucose > 600 mg/dL, serum osmolality > 320 mOsm/kg, absence of significant ketoacidosis",
    160: "Shakiness, sweating, diaphoresis, pallor, intense hunger, tachycardia, palpitations, anxiety, tingling around mouth; progressing to confusion, slurred speech, seizures, loss of consciousness",
    161: "Usually asymptomatic; mild abdominal obesity, fasting blood glucose 100-125 mg/dL, HbA1c 5.7-6.4%, elevated triglycerides, low HDL, borderline blood pressure elevation",
    162: "Excess body weight (BMI >= 30 kg/m2), increased waist circumference, shortness of breath on exertion, joint pain in knees and hips, daytime sleepiness from sleep apnea, skin tags, acanthosis nigricans",
    163: "Chronic fatigue, unexplained weight gain, cold intolerance, persistent constipation, dry rough skin, brittle coarse hair, periorbital puffiness, bradycardia, heavy menstrual bleeding, memory fog",
    164: "Severe hypothermia, progressive lethargy, stupor, hypoventilation, bradycardia, periorbital edema, dry doughy skin, hyponatremia, hypoglycemia in untreated severe hypothyroidism",
    165: "Weight loss despite increased appetite, heat intolerance, profuse sweating, fine hand tremor, palpitations, anxiety, frequent bowel movements, bilateral exophthalmos (proptosis), diffuse goiter with bruit",
    166: "Life-threatening thyrotoxic state: hyperpyrexia (fever > 40°C), severe tachycardia (heart rate > 140 bpm), atrial fibrillation, agitation, delirium, psychosis, vomiting, diarrhea, jaundice, acute heart failure",
    167: "Markedly painful and tender enlarged thyroid gland, neck pain radiating to jaw or ear, fever, malaise, transient symptoms of hyperthyroidism followed by transient hypothyroidism",
    168: "Painless solitary firm thyroid nodule detected by palpation or imaging, difficulty swallowing (dysphagia), hoarseness, anterior cervical lymphadenopathy",
    169: "Frequently asymptomatic hypercalcemia on routine blood tests; or classic 'stones, bones, abdominal groans, psychiatric overtones': kidney stones, bone pain, constipation, depression, fatigue",
    170: "Severe lethargy, confusion, dehydration, polyuria, polydipsia, severe constipation, abdominal pain, nausea, vomiting, shortened QT interval, cardiac arrhythmias in malignancy",
    171: "Numbness and tingling around mouth and fingertips (paresthesias), carpopedal spasms, painful muscle cramps, tetany, positive Chvostek and Trousseau signs, prolonged QT interval, seizures",
    172: "Diffuse bone pain and tenderness (especially lower back, pelvis, legs), proximal muscle weakness (waddling gait), difficulty rising from chairs, fractures; in children bowed legs, rachitic rosary",
    173: "Silent asymptomatic bone loss until low-trauma fragility fracture (vertebrae, hip, wrist), loss of standing height (> 4 cm), progressive kyphosis ('dowager hump')",
    174: "Deep aching localized bone pain worse at night and weight-bearing, skeletal deformity (bowing of femur/tibia, enlarged skull leading to increased hat size), warmth over affected bone, sensorineural hearing loss",
    175: "Central obesity, rounded 'moon face', facial plethora, dorsocervical fat pad ('buffalo hump'), wide purple abdominal striae (> 1 cm), easy bruising, proximal muscle weakness, hypertension, hyperglycemia",
    176: "Chronic worsening fatigue, muscle weakness, anorexia, weight loss, generalized hyperpigmentation of skin (creases, pressure points, scars) and oral mucosa, postural hypotension, salt craving",
    177: "Life-threatening medical emergency: sudden severe hypotension and vascular collapse refractory to fluids and vasopressors, high fever, severe abdominal pain mimicking acute abdomen, vomiting, hypoglycemia",
    178: "Resistant hypertension despite multiple antihypertensives, muscle weakness, cramps, fatigue, episodic paralysis from severe hypokalemia, polyuria, polydipsia, absence of edema",
    179: "Classic paroxysmal triad of pounding headache, profuse drenching diaphoresis, and tachycardia/palpitations; accompanying severe episodic hypertension, pallor, anxiety, tremor",
    180: "In premenopausal women: amenorrhea, oligomenorrhea, galactorrhea, infertility; in men: decreased libido, erectile dysfunction, gynecomastia, visual field defects (bitemporal hemianopia)",
    181: "Insidious enlargement of hands and feet (increased shoe, glove, and ring size), coarsening of facial features, enlargement of jaw (prognathism), deep hollow voice, excessive sweating, oily skin, joint pain",
    182: "Fatigue, weakness, cold intolerance, loss of libido, erectile dysfunction, amenorrhea, loss of axillary and pubic hair, fine facial wrinkling, postural hypotension, pale sallow complexion",
    183: "Massive dilute polyuria (> 3-20 L/day of pale clear urine), unquenchable thirst (polydipsia), severe nocturia, preference for ice-cold water, rapid dehydration if fluids restricted",
    184: "Euvolemic hyponatremia: anorexia, nausea, headache, irritability, muscle cramps, gait ataxia; progressing to confusion, lethargy, seizures, coma with concentrated urine (osmolality > 100)",
    185: "In female neonates ambiguous genitalia; in classic salt-wasting crisis (at 2-3 weeks of life) vomiting, poor feeding, dehydration, failure to thrive, hyponatremia, hyperkalemia, shock",
    186: "Infrequent or absent menstrual periods (oligomenorrhea/amenorrhea), hirsutism (excess facial and body hair), severe persistent cystic acne, androgenic alopecia, obesity, difficulty conceiving",
    187: "Decreased libido, erectile dysfunction, loss of morning erections, fatigue, depressed mood, decreased muscle mass, increased body fat, gynecomastia, hot flushes in acute loss",
    188: "Acute excruciating pain, erythema, swelling, and extreme warmth in a single joint (classically first metatarsophalangeal joint / podagra), pain so severe that even a bedsheet hurts; fever; chronic tophi",
    189: "Asymptomatic elevated serum uric acid; in tumor lysis syndrome oliguria, clouding of urine, cardiac arrhythmias, tetany, seizures following chemotherapy for hematologic malignancy",
    190: "Neurovisceral attacks: severe agonizing colicky abdominal pain without peritoneal signs, constipation, vomiting, tachycardia, hypertension, motor neuropathy (wrist drop), dark reddish-purple urine",

    # 191-227 Hematology & Oncology
    191: "Chronic progressive fatigue, pallor of conjunctiva and skin, exertional breathlessness, dizziness, cold hands and feet, brittle spoon-shaped nails (koilonychia), sore tongue (glossitis), pica cravings",
    192: "Fatigue, lemon-yellow pallor, beefy red painful smooth tongue (glossitis), bilateral symmetrical tingling and numbness in hands and feet (paresthesias), sensory ataxia, gait unsteadiness, memory loss",
    193: "Fatigue, weakness, exertional dyspnea, pallor, sore tongue, diarrhea, absence of neurological deficits (distinguishing from B12 deficiency), neural tube defect risk in pregnancy",
    194: "Mild to moderate normocytic anemia in setting of chronic infection, autoimmune inflammation, or cancer; fatigue, pallor, symptoms overshadowed by underlying chronic illness",
    195: "Severe progressive anemia presenting in infancy, pallor, failure to thrive, hepatosplenomegaly, jaundice, 'chipmunk facies' from extramedullary hematopoiesis, dependent on regular transfusions",
    196: "Mild asymptomatic microcytic hypochromic anemia discovered on routine CBC, normal ferritin, elevated RBC count relative to low hemoglobin, no response to iron therapy",
    197: "Severe recurring episodes of excruciating bone and joint pain (vaso-occlusive crises), dactylitis (painful swollen hands/feet in infants), acute chest syndrome (chest pain, fever, hypoxia), stroke",
    198: "Acute hemolytic anemia (jaundice, dark cola-colored urine, pallor, fatigue, back pain) triggered 24-48 hours after ingestion of fava beans, infection, or oxidative drugs (primaquine, dapsone)",
    199: "Recurrent episodes of mild jaundice, pallor, fatigue, splenomegaly, pigmented bilirubin gallstones at young age, hemolytic or aplastic crises triggered by viral infections",
    200: "Rapidly worsening anemia, fatigue, dyspnea, scleral icterus, dark urine, splenomegaly, positive direct antiglobulin test (Coombs test) for warm IgG antibodies",
    201: "Pancytopenia symptoms: severe fatigue and pallor from anemia, frequent severe infections and mouth ulcers from neutropenia, petechiae, purpura, mucosal bleeding from thrombocytopenia",
    202: "Isolated thrombocytopenia: petechiae, spontaneous purpura on limbs, easy bruising, recurrent epistaxis, bleeding gums, heavy prolonged menstrual periods without splenomegaly or systemic illness",
    203: "Life-threatening pentad: microangiopathic hemolytic anemia (schistocytes, jaundice), severe thrombocytopenia (purpura), neurological symptoms (headache, confusion, seizures, focal deficits), fever, renal impairment",
    204: "Triad of microangiopathic hemolytic anemia, severe thrombocytopenia, and acute kidney injury (oliguria, dark urine, rising creatinine), preceded by bloody diarrheal illness in children (STEC)",
    205: "Simultaneous widespread thrombosis and severe bleeding: petechiae, oozing from venipuncture sites, hematuria, purpura fulminans, multi-organ failure in setting of sepsis, trauma, or obstetric disaster",
    206: "Spontaneous or minimally provoked bleeding into large weight-bearing joints (hemarthrosis: knee, elbow, ankle), muscle hematomas, prolonged bleeding after tooth extraction or surgery, normal platelets, prolonged aPTT",
    207: "Recurrent easy bruising, frequent prolonged epistaxis, bleeding after dental procedures, heavy prolonged menstrual bleeding (menorrhagia), mucosal bleeding, family history of bleeding",
    208: "Drop in platelet count by >= 50% occurring 5-10 days after starting heparin, paradoxical new arterial or venous thrombosis (DVT, PE, skin necrosis at injection sites) without bleeding",
    209: "Recurrent unprovoked deep vein thrombosis, pulmonary embolism, arterial stroke at young age, recurrent early miscarriages or late pregnancy losses, livedo reticularis, persistent antiphospholipid antibodies",
    210: "Headaches, dizziness, visual disturbances, facial plethora (ruddy red face), intense itching after warm bath (aquagenic pruritus), burning pain and erythema in hands and feet (erythromelalgia), splenomegaly",
    211: "Often asymptomatic elevated platelets (> 450,000/uL); or burning pain and redness in palms/soles (erythromelalgia), headaches, transient ischemic attacks, paradoxical bleeding at very high counts",
    212: "Massive splenomegaly causing early satiety, left upper quadrant pain and dragging sensation; severe fatigue, night sweats, low-grade fever, bone pain, tear-drop red cells on peripheral smear",
    213: "Insidious onset of fatigue, unexplained weight loss, night sweats, low-grade fever, abdominal fullness and early satiety from massive splenomegaly, marked leukocytosis with left shift (Ph chromosome)",
    214: "Often asymptomatic absolute lymphocytosis (> 5000/uL) on routine blood test; painless symmetrical cervical and axillary lymphadenopathy, splenomegaly, fatigue, recurrent infections, night sweats",
    215: "Acute rapid onset of profound fatigue, pallor, fever, recurrent infections, bleeding from gums, petechiae, easy bruising, bone tenderness; Auer rods and >= 20% blasts in bone marrow",
    216: "Rapidly progressive fever, bone and joint pain, limping in children, pallor, petechiae, bleeding, generalized lymphadenopathy, hepatosplenomegaly, testicular enlargement, mediastinal mass",
    217: "Painless firm rubbery cervical or supraclavicular lymphadenopathy, alcohol-induced lymph node pain, drenching night sweats, unexplained fevers (> 38°C), involuntary weight loss > 10% (B symptoms), pruritus",
    218: "Rapidly enlarging painless lymph node mass (neck, abdomen, groin), systemic B symptoms (drenching night sweats, fever, weight loss), abdominal pain, obstruction, elevated LDH",
    219: "Indolent slowly progressing painless waxing and waning generalized lymphadenopathy, absence of systemic B symptoms in early stages, splenomegaly, bone marrow involvement",
    220: "CRAB features: Calcium elevation (confusion, constipation), Renal insufficiency (elevated creatinine), Anemia (fatigue, pallor), Bone lytic lesions (severe back and rib pain, pathological fractures)",
    221: "Asymptomatic serum M-protein spike < 3 g/dL discovered on routine protein electrophoresis, bone marrow plasma cells < 10%, absence of CRAB end-organ damage",
    222: "Refractory cytopenias in elderly: macrocytic anemia causing chronic fatigue, neutropenia causing recurrent bacterial infections, thrombocytopenia causing easy bruising and petechiae",
    223: "Prolonged unremitting high fever, massive hepatosplenomegaly, jaundice, cytopenias, bleeding, hyperferritinemia (often > 10,000 ng/mL), neurological symptoms, rapid clinical deterioration",
    224: "Painless firm solitary breast lump with irregular borders, skin dimpling ('peau d'orange'), nipple retraction, spontaneous bloody nipple discharge, fixed axillary lymphadenopathy",
    225: "Abnormal vaginal bleeding (especially post-coital bleeding, intermenstrual bleeding, postmenopausal bleeding), foul-smelling vaginal discharge, pelvic pain, dyspareunia",
    226: "Vague persistent abdominal bloating, early satiety, pelvic or abdominal pain, urinary urgency and frequency, unexplained weight loss, ascites, palpable pelvic adnexal mass in postmenopausal women",
    227: "Postmenopausal vaginal bleeding (any vaginal bleeding after menopause requires urgent evaluation), abnormal heavy intermenstrual bleeding in premenopausal women, purulent vaginal discharge, pelvic pressure"
}

EMERGENCY_RED_FLAGS_MAP = {
    # Emergency conditions
    2: ["Blood pressure > 180/120 with target-organ damage", "Severe headache, chest pain, or vision loss", "Acute pulmonary edema or encephalopathy"],
    4: ["Severe crushing chest pain radiating to left arm or jaw", "Cold diaphoresis with dyspnea", "Acute ST elevation on ECG requiring emergency reperfusion"],
    5: ["Crescendo resting angina", "Hemodynamic instability with ischemic chest pain", "High-risk GRACE score requiring immediate catheterization"],
    8: ["Severe acute pulmonary edema", "Respiratory failure with pink frothy sputum", "Cardiogenic shock with severe hypotension"],
    12: ["Sustained ventricular tachycardia with pulse", "Pulseless ventricular tachycardia", "Hemodynamic collapse and syncope"],
    13: ["Unresponsive patient with ventricular fibrillation or cardiac arrest", "Immediate ACLS protocol and defibrillation required"],
    15: ["Complete third-degree heart block", "Severe symptomatic bradycardia with syncope or hemodynamic instability", "Risk of asystole"],
    21: ["Cardiac tamponade with Beck triad (hypotension, muffled heart sounds, elevated JVP)", "Pulsus paradoxus", "Urgent pericardiocentesis required"],
    31: ["Tearing chest pain radiating to back", "Pulse or blood pressure asymmetry between limbs", "Suspected acute aortic dissection"],
    34: ["Acute limb ischemia (6 Ps: Pain, Pallor, Pulselessness, Paresthesias, Poikilothermia, Paralysis)", "Surgical emergency within 6 hours"],
    36: ["Massive pulmonary embolism with shock or severe hypotension", "Acute severe right ventricular strain", "Immediate thrombolysis indicated"],
    42: ["Status asthmaticus", "Silent chest with severe exhaustion", "PaCO2 normal or rising in breathless patient indicates impending failure"],
    56: ["Tension pneumothorax with tracheal deviation and hypotension", "Immediate needle decompression required"],
    59: ["Acute respiratory distress syndrome (P/F ratio <= 300)", "Severe refractory hypoxemia requiring lung-protective mechanical ventilation"],
    74: ["Massive hemoptysis (> 200 mL blood)", "Airway compromise and asphyxiation risk", "Immediate bronchoscopy or embolization"],
    114: ["Acute liver failure with INR >= 1.5 and hepatic encephalopathy", "Cerebral edema and hypoglycemia", "Urgent liver transplant evaluation"],
    148: ["Testicular torsion", "Acute scrotal pain with absent cremasteric reflex", "Surgical exploration required within 6 hours to save testis"],
    158: ["Diabetic ketoacidosis with severe metabolic acidosis", "Kussmaul breathing and altered sensorium", "Severe dehydration and hypokalemia risk"],
    159: ["Hyperosmolar hyperglycemic state with glucose > 600 mg/dL", "Severe hyperosmolality and dehydration", "High thrombosis risk"],
    164: ["Myxedema coma with severe hypothermia, bradycardia, and hypoventilation", "Immediate IV thyroid replacement and hydrocortisone"],
    166: ["Thyroid storm with hyperpyrexia, severe tachycardia, and delirium", "Immediate ICU admission and multimodality thyroid blockade"],
    177: ["Acute adrenal crisis with severe hypotension, vomiting, and vascular collapse", "Immediate IV hydrocortisone 100 mg stat"],
    203: ["Thrombotic thrombocytopenic purpura (TTP)", "Microangiopathic hemolytic anemia with schistocytes and thrombocytopenia", "Immediate plasma exchange required"],
    205: ["Disseminated intravascular coagulation with severe bleeding and multi-organ thrombosis"],
    223: ["Hemophagocytic lymphohistiocytosis (HLH) with ferritin > 10,000 ng/mL and multi-organ failure"]
}


def enrich_dataset():
    if not PARSED_FILE.exists():
        raise FileNotFoundError(f"Parsed file not found at {PARSED_FILE}")

    with open(PARSED_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    enriched_records = []
    for item in records:
        disease_id = item["id"]
        name = item["name"]

        # 1. Symptoms string & list
        symptoms = CLINICAL_SYMPTOMS_MAP.get(disease_id)
        if not symptoms:
            # Fallback based on name and category
            symptoms = f"Clinical symptoms and manifestations associated with {name}, including localized and systemic presentations."

        symptoms_list = [s.strip() for s in re.split(r",\s*|;\s*", symptoms) if s.strip()]

        # 2. Emergency red flags
        emergency_flags = EMERGENCY_RED_FLAGS_MAP.get(disease_id)
        if not emergency_flags:
            emergency_flags = [
                f"Sudden severe exacerbation of {name} symptoms.",
                "Uncontrolled high fever, persistent vomiting, or inability to take oral fluids.",
                "Shortness of breath, severe chest pain, or neurological deficits.",
            ]

        enriched_item = {
            "id": disease_id,
            "name": name,
            "symptoms": symptoms,
            "symptoms_list": symptoms_list,
            "differential_diagnoses": item.get("differential_diagnoses", []),
            "investigations": item.get("investigations", []),
            "treatment": item.get("treatment", ""),
            "medications": item.get("medications", []),
            "precautions": item.get("precautions", ""),
            "emergency_flags": emergency_flags,
        }
        enriched_records.append(enriched_item)

    with open(ENRICHED_FILE, "w", encoding="utf-8") as f:
        json.dump(enriched_records, f, indent=2, ensure_ascii=False)

    print(f"Successfully enriched all {len(enriched_records)} diseases and saved to {ENRICHED_FILE}")


if __name__ == "__main__":
    enrich_dataset()
