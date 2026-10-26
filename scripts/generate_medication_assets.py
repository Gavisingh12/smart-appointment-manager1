import os
import json

# Ensure directory exists
output_dir = os.path.join("app", "static", "images", "medications")
os.makedirs(output_dir, exist_ok=True)

# Catalog path
catalog_path = os.path.join("app", "data", "pharmacy_catalog.json")
with open(catalog_path, "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Visual theme configurations for different medicine forms
def make_strip_svg(brand, salt, count, primary_color, secondary_color, badge="TABLET"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EDF2F7"/>
    </linearGradient>
    <linearGradient id="foilGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#E2E8F0"/>
      <stop offset="35%" stop-color="#FFFFFF"/>
      <stop offset="70%" stop-color="#CBD5E1"/>
      <stop offset="100%" stop-color="#E2E8F0"/>
    </linearGradient>
    <linearGradient id="stripBrand" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{primary_color}"/>
      <stop offset="100%" stop-color="{secondary_color}"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.12"/>
    </filter>
  </defs>
  <rect width="280" height="200" rx="16" fill="url(#bgGrad)"/>
  
  <!-- Blister Pack Outer -->
  <g filter="url(#cardShadow)">
    <rect x="40" y="28" width="200" height="144" rx="12" fill="url(#foilGrad)" stroke="#CBD5E1" stroke-width="1.5"/>
    <rect x="44" y="32" width="192" height="42" rx="8" fill="url(#stripBrand)"/>
    
    <!-- Brand on Pack -->
    <text x="56" y="52" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="13" font-weight="bold">{brand[:18]}</text>
    <text x="56" y="66" fill="#F1F5F9" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="9">{salt[:24]}</text>
    <rect x="195" y="44" width="32" height="16" rx="4" fill="#FFFFFF" fill-opacity="0.25"/>
    <text x="211" y="55" fill="#FFFFFF" font-family="sans-serif" font-size="7.5" font-weight="bold" text-anchor="middle">{badge}</text>
    
    <!-- Blister Pockets (2 rows of 5) -->
    <!-- Row 1 -->
    <ellipse cx="68" cy="100" rx="15" ry="15" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1"/>
    <ellipse cx="68" cy="98" rx="11" ry="11" fill="{primary_color}" fill-opacity="0.25"/>
    <line x1="61" y1="98" x2="75" y2="98" stroke="{primary_color}" stroke-width="1.2" stroke-linecap="round"/>

    <ellipse cx="104" cy="100" rx="15" ry="15" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1"/>
    <ellipse cx="104" cy="98" rx="11" ry="11" fill="{primary_color}" fill-opacity="0.25"/>
    <line x1="97" y1="98" x2="111" y2="98" stroke="{primary_color}" stroke-width="1.2" stroke-linecap="round"/>

    <ellipse cx="140" cy="100" rx="15" ry="15" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1"/>
    <ellipse cx="140" cy="98" rx="11" ry="11" fill="{primary_color}" fill-opacity="0.25"/>
    <line x1="133" y1="98" x2="147" y2="98" stroke="{primary_color}" stroke-width="1.2" stroke-linecap="round"/>

    <ellipse cx="176" cy="100" rx="15" ry="15" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1"/>
    <ellipse cx="176" cy="98" rx="11" ry="11" fill="{primary_color}" fill-opacity="0.25"/>
    <line x1="169" y1="98" x2="183" y2="98" stroke="{primary_color}" stroke-width="1.2" stroke-linecap="round"/>

    <ellipse cx="212" cy="100" rx="15" ry="15" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1"/>
    <ellipse cx="212" cy="98" rx="11" ry="11" fill="{primary_color}" fill-opacity="0.25"/>
    <line x1="205" y1="98" x2="219" y2="98" stroke="{primary_color}" stroke-width="1.2" stroke-linecap="round"/>

    <!-- Row 2 -->
    <ellipse cx="68" cy="142" rx="15" ry="15" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1"/>
    <ellipse cx="68" cy="140" rx="11" ry="11" fill="{primary_color}" fill-opacity="0.25"/>
    <line x1="61" y1="140" x2="75" y2="140" stroke="{primary_color}" stroke-width="1.2" stroke-linecap="round"/>

    <ellipse cx="104" cy="142" rx="15" ry="15" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1"/>
    <ellipse cx="104" cy="140" rx="11" ry="11" fill="{primary_color}" fill-opacity="0.25"/>
    <line x1="97" y1="140" x2="111" y2="140" stroke="{primary_color}" stroke-width="1.2" stroke-linecap="round"/>

    <ellipse cx="140" cy="142" rx="15" ry="15" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1"/>
    <ellipse cx="140" cy="140" rx="11" ry="11" fill="{primary_color}" fill-opacity="0.25"/>
    <line x1="133" y1="140" x2="147" y2="140" stroke="{primary_color}" stroke-width="1.2" stroke-linecap="round"/>

    <ellipse cx="176" cy="142" rx="15" ry="15" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1"/>
    <ellipse cx="176" cy="140" rx="11" ry="11" fill="{primary_color}" fill-opacity="0.25"/>
    <line x1="169" y1="140" x2="183" y2="140" stroke="{primary_color}" stroke-width="1.2" stroke-linecap="round"/>

    <ellipse cx="212" cy="142" rx="15" ry="15" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1"/>
    <ellipse cx="212" cy="140" rx="11" ry="11" fill="{primary_color}" fill-opacity="0.25"/>
    <line x1="205" y1="140" x2="219" y2="140" stroke="{primary_color}" stroke-width="1.2" stroke-linecap="round"/>
  </g>
</svg>'''

def make_capsule_strip_svg(brand, salt, primary_color, secondary_color, badge="CAPSULE"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EDF2F7"/>
    </linearGradient>
    <linearGradient id="foilGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#E2E8F0"/>
      <stop offset="40%" stop-color="#FFFFFF"/>
      <stop offset="70%" stop-color="#CBD5E1"/>
      <stop offset="100%" stop-color="#E2E8F0"/>
    </linearGradient>
    <linearGradient id="capBrand" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{primary_color}"/>
      <stop offset="100%" stop-color="{secondary_color}"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.12"/>
    </filter>
  </defs>
  <rect width="280" height="200" rx="16" fill="url(#bgGrad)"/>
  
  <g filter="url(#cardShadow)">
    <rect x="45" y="28" width="190" height="144" rx="12" fill="url(#foilGrad)" stroke="#CBD5E1" stroke-width="1.5"/>
    <rect x="49" y="32" width="182" height="38" rx="8" fill="url(#capBrand)"/>
    <text x="60" y="51" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="12.5" font-weight="bold">{brand[:18]}</text>
    <text x="60" y="63" fill="#F1F5F9" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="8.5">{salt[:22]}</text>
    
    <!-- 6 Capsule Slots -->
    <g transform="translate(68, 80)">
      <!-- Cap 1 -->
      <rect x="0" y="0" width="14" height="16" rx="7" fill="{primary_color}"/>
      <rect x="0" y="14" width="14" height="16" rx="7" fill="{secondary_color}"/>
      <!-- Cap 2 -->
      <rect x="46" y="0" width="14" height="16" rx="7" fill="{primary_color}"/>
      <rect x="46" y="14" width="14" height="16" rx="7" fill="{secondary_color}"/>
      <!-- Cap 3 -->
      <rect x="92" y="0" width="14" height="16" rx="7" fill="{primary_color}"/>
      <rect x="92" y="14" width="14" height="16" rx="7" fill="{secondary_color}"/>
      <!-- Cap 4 -->
      <rect x="134" y="0" width="14" height="16" rx="7" fill="{primary_color}"/>
      <rect x="134" y="14" width="14" height="16" rx="7" fill="{secondary_color}"/>
      
      <!-- Row 2 -->
      <rect x="23" y="44" width="14" height="16" rx="7" fill="{primary_color}"/>
      <rect x="23" y="58" width="14" height="16" rx="7" fill="{secondary_color}"/>
      <rect x="69" y="44" width="14" height="16" rx="7" fill="{primary_color}"/>
      <rect x="69" y="58" width="14" height="16" rx="7" fill="{secondary_color}"/>
      <rect x="113" y="44" width="14" height="16" rx="7" fill="{primary_color}"/>
      <rect x="113" y="58" width="14" height="16" rx="7" fill="{secondary_color}"/>
    </g>
  </g>
</svg>'''

def make_bottle_svg(brand, salt, primary_color, secondary_color, badge="SYRUP"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EDF2F7"/>
    </linearGradient>
    <linearGradient id="glassGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#78350F"/>
      <stop offset="45%" stop-color="#B45309"/>
      <stop offset="80%" stop-color="#92400E"/>
      <stop offset="100%" stop-color="#451A03"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.12"/>
    </filter>
  </defs>
  <rect width="280" height="200" rx="16" fill="url(#bgGrad)"/>
  
  <g filter="url(#cardShadow)" transform="translate(100, 15)">
    <!-- Cap -->
    <rect x="25" y="0" width="30" height="18" rx="3" fill="#E2E8F0" stroke="#94A3B8" stroke-width="1"/>
    <line x1="28" y1="6" x2="52" y2="6" stroke="#CBD5E1"/>
    <line x1="28" y1="12" x2="52" y2="12" stroke="#CBD5E1"/>
    <!-- Neck -->
    <rect x="30" y="18" width="20" height="12" fill="#78350F"/>
    <!-- Body -->
    <rect x="10" y="30" width="60" height="135" rx="12" fill="url(#glassGrad)"/>
    <!-- Liquid Highlight -->
    <path d="M15 42 Q40 46 65 42 L65 155 Q40 162 15 155 Z" fill="#D97706" opacity="0.4"/>
    
    <!-- Label -->
    <rect x="12" y="65" width="56" height="75" rx="4" fill="#FFFFFF" stroke="#E2E8F0"/>
    <rect x="14" y="67" width="52" height="14" fill="{primary_color}"/>
    <text x="40" y="77" fill="#FFFFFF" font-family="sans-serif" font-size="7" font-weight="bold" text-anchor="middle">{badge}</text>
    <text x="40" y="94" fill="#0F172A" font-family="sans-serif" font-size="7.5" font-weight="bold" text-anchor="middle">{brand[:10]}</text>
    <text x="40" y="104" fill="#64748B" font-family="sans-serif" font-size="5.5" text-anchor="middle">{salt[:12]}</text>
    <circle cx="40" cy="120" r="7" fill="{secondary_color}" fill-opacity="0.2"/>
    <path d="M40 115 v10 M35 120 h10" stroke="{primary_color}" stroke-width="1.5" stroke-linecap="round"/>
  </g>
</svg>'''

def make_tube_svg(brand, salt, primary_color, secondary_color, badge="GEL / TUBE"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EDF2F7"/>
    </linearGradient>
    <linearGradient id="tubeBody" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#F1F5F9"/>
      <stop offset="100%" stop-color="#CBD5E1"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.12"/>
    </filter>
  </defs>
  <rect width="280" height="200" rx="16" fill="url(#bgGrad)"/>
  
  <g filter="url(#cardShadow)" transform="rotate(-25 140 100) translate(60, 65)">
    <!-- Tube Cap -->
    <rect x="0" y="16" width="22" height="36" rx="4" fill="#0F172A"/>
    <!-- Tube Nozzle -->
    <rect x="22" y="24" width="8" height="20" fill="#E2E8F0"/>
    <!-- Tube Body -->
    <path d="M30 18 L160 8 L165 60 L30 50 Z" fill="url(#tubeBody)" stroke="#94A3B8" stroke-width="1"/>
    <!-- Crimped end -->
    <rect x="160" y="8" width="8" height="52" rx="1" fill="#94A3B8"/>
    <!-- Tube Stripe -->
    <path d="M40 20 L150 12 L150 40 L40 45 Z" fill="{primary_color}"/>
    <text x="85" y="32" fill="#FFFFFF" font-family="sans-serif" font-size="9" font-weight="bold">{brand[:14]}</text>
    <text x="85" y="42" fill="#FEF08A" font-family="sans-serif" font-size="6.5">{salt[:16]}</text>
  </g>
</svg>'''

def make_device_svg(brand, salt, primary_color, secondary_color, badge="DEVICE"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 200" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EDF2F7"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.12"/>
    </filter>
  </defs>
  <rect width="280" height="200" rx="16" fill="url(#bgGrad)"/>
  
  <!-- Device Console -->
  <g filter="url(#cardShadow)">
    <rect x="65" y="30" width="150" height="140" rx="16" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
    <rect x="80" y="45" width="120" height="70" rx="8" fill="#0F172A"/>
    <!-- LCD Display -->
    <text x="95" y="75" fill="#38BDF8" font-family="monospace" font-size="20" font-weight="bold">120</text>
    <text x="145" y="75" fill="#38BDF8" font-family="monospace" font-size="11">SYS</text>
    <text x="95" y="100" fill="#4ADE80" font-family="monospace" font-size="20" font-weight="bold">80</text>
    <text x="145" y="100" fill="#4ADE80" font-family="monospace" font-size="11">DIA</text>
    <text x="175" y="88" fill="#F43F5E" font-family="monospace" font-size="14" font-weight="bold">72</text>
    
    <!-- Start Button -->
    <circle cx="140" cy="142" r="16" fill="{primary_color}"/>
    <text x="140" y="146" fill="#FFFFFF" font-family="sans-serif" font-size="8" font-weight="bold" text-anchor="middle">START</text>
    <text x="140" y="162" fill="#64748B" font-family="sans-serif" font-size="7" font-weight="bold" text-anchor="middle">{brand[:18]}</text>
  </g>
</svg>'''

# Map each product to its visual representation
color_map = {
    "pain-fever": ("#DC2626", "#EA580C"),
    "cold-respiratory": ("#0284C7", "#0D9488"),
    "antibiotics": ("#7C3AED", "#C026D3"),
    "digestive-gastro": ("#D97706", "#F59E0B"),
    "heart-bp": ("#E11D48", "#BE123C"),
    "diabetes": ("#0891B2", "#0284C7"),
    "vitamins-supplements": ("#059669", "#10B981"),
    "skin-hair": ("#9333EA", "#C084FC"),
    "first-aid-devices": ("#1E293B", "#334155"),
}

# Detailed About info per medicine
about_database = {
    1: {  # Crocin 650
        "uses_hindi": "बुखार, तेज सिरदर्द, दांत दर्द और बदन दर्द को जल्दी कम करने में असरदार।",
        "what_it_does": "Crocin 650 is a fast-acting paracetamol formulation designed to reduce elevated body temperature (fever) and alleviate mild to moderate pain.",
        "how_to_take": "Take 1 tablet after food with water. Maintain at least 4-6 hours between doses. Maximum 4 tablets in 24 hours.",
        "safety_tip": "Avoid consuming with other paracetamol-containing products or excessive alcohol."
    },
    2: {  # Dolo 650
        "uses_hindi": "तेज बुखार, वायरल बुखार, सिरदर्द और मांसपेशियों के दर्द में सबसे ज्यादा इस्तेमाल की जाने वाली दवा।",
        "what_it_does": "Dolo 650 contains 650mg paracetamol with antipyretic and analgesic action, commonly recommended for viral fevers, flu, and body ache.",
        "how_to_take": "Take 1 tablet with a glass of water after meals. Do not exceed the prescribed frequency.",
        "safety_tip": "Overdose can cause serious liver injury. Safe for most adults when used as instructed."
    },
    3: {  # Combiflam
        "uses_hindi": "जोड़ों का दर्द, मांसपेशियों में खिंचाव, दांत दर्द और सूजन के साथ होने वाले दर्द में तुरंत राहत।",
        "what_it_does": "Combiflam combines Ibuprofen (NSAID) and Paracetamol for dual pain relief and anti-inflammatory action on swollen joints or muscles.",
        "how_to_take": "Always take strictly after food or with milk to protect your stomach lining.",
        "safety_tip": "Not recommended for patients with active stomach ulcers or severe kidney disorders."
    },
    4: {  # Volini Pain Relief Gel
        "uses_hindi": "कमर दर्द, गर्दन दर्द, मोच और जोड़ों के दर्द पर सीधे लगाने वाला असरदार पेन रिलीफ जेल।",
        "what_it_does": "Volini Gel contains Diclofenac and Methyl Salicylate which penetrate deep through the skin to relax tense muscles and reduce acute inflammation.",
        "how_to_take": "Gently apply a thin layer onto the affected area 3-4 times daily. Do not massage vigorously.",
        "safety_tip": "For external use only. Do not apply on open cuts, wounds, or sensitive mucous membranes."
    },
    5: {  # Naprosyn 500
        "uses_hindi": "गठिया (Arthritis), स्पॉन्डिलाइटिस और पुराने जोड़ों के तेज दर्द व सूजन में राहत।",
        "what_it_does": "Naprosyn is a long-acting NSAID (Naproxen) providing 12-hour relief from joint stiffness and inflammatory swelling.",
        "how_to_take": "Take 1 tablet twice daily with food or as prescribed by your orthopedist.",
        "safety_tip": "May cause acidity or GI discomfort; often prescribed with an antacid."
    },
    6: {  # Cetzine 10mg
        "uses_hindi": "एलर्जी, छींक आना, बहती नाक, आंखों में खुजली और त्वचा पर चकत्ते (Urticaria) में राहत।",
        "what_it_does": "Cetzine contains Cetirizine, a non-drowsy second-generation antihistamine that blocks allergic histamine receptors.",
        "how_to_take": "Take 1 tablet once daily in the evening with water, with or without food.",
        "safety_tip": "May cause mild drowsiness in some individuals. Avoid driving after your first dose."
    },
    7: {  # Montair-LC
        "uses_hindi": "सांस लेने में दिक्कत, मौसमी जुकाम, लगातार छींकें और दमा (Asthma) के एलर्जी लक्षणों में।",
        "what_it_does": "Montair-LC combines Levocetirizine and Montelukast to prevent airway narrowing and allergic airway inflammation.",
        "how_to_take": "Take 1 tablet once daily at night before sleeping.",
        "safety_tip": "Best taken consistently at the same time each evening for peak respiratory protection."
    },
    8: {  # Ascoril D Plus Cough Syrup
        "uses_hindi": "सूखी खांसी, गले की खराश और बार-बार उठने वाली खांसी को शांत करने वाला सिरप।",
        "what_it_does": "A triple-action dry cough syrup with Dextromethorphan (cough suppressant), Phenylephrine (decongestant), and Chlorpheniramine.",
        "how_to_take": "Take 5-10 ml using the measuring cup, 2 to 3 times a day as directed.",
        "safety_tip": "Avoid drinking cold water immediately after taking the syrup to allow the throat soothing coating to work."
    },
    9: {  # Asthalin Inhaler
        "uses_hindi": "दमा (Asthma) या सांस फूलने पर तुरंत सांस की नली खोलने वाला इमरजेंसी इनहेलर।",
        "what_it_does": "Asthalin delivers Salbutamol directly into the bronchial tubes, opening airways within 2-5 minutes during sudden bronchospasm.",
        "how_to_take": "Inhale 1-2 puffs as required during wheezing or breathlessness, holding breath for 10 seconds after inhalation.",
        "safety_tip": "Rinse mouth with water after use. Always keep this reliever inhaler within easy reach."
    },
    10: {  # Otrivin Oxy Nasal Spray
        "uses_hindi": "बंद नाक को 25 सेकंड में खोलने और सर्दी-जुकाम में आसान सांस लेने के लिए।",
        "what_it_does": "Fast-acting nasal decongestant (Oxymetazoline) that constricts swollen blood vessels in nasal passages.",
        "how_to_take": "Spray 1 puff into each nostril 2-3 times daily.",
        "safety_tip": "Do not use for more than 5-7 consecutive days to avoid rebound nasal congestion (rhinitis medicamentosa)."
    },
    11: {  # Augmentin 625 Duo
        "uses_hindi": "गले, कान, छाती (निमोनिया), त्वचा और यूरिनरी ट्रैक्ट के बैक्टीरियल इन्फेक्शन में।",
        "what_it_does": "Broad-spectrum antibiotic combining Amoxicillin with Clavulanic acid to overcome bacterial enzyme resistance.",
        "how_to_take": "Take 1 tablet twice daily after a meal at fixed 12-hour intervals.",
        "safety_tip": "Complete the full course prescribed by your doctor even if you feel better after 2 days."
    },
    12: {  # Azithral 500
        "uses_hindi": "गले का संक्रमण (Tonsillitis), ब्रोंकाइटिस और श्वसन तंत्र के बैक्टीरियल इन्फेक्शन में।",
        "what_it_does": "Azithromycin 500mg macrolide antibiotic with high tissue penetration, usually prescribed for 3 or 5 days.",
        "how_to_take": "Take 1 tablet daily 1 hour before or 2 hours after meals.",
        "safety_tip": "Prescription antibiotic; do not discontinue course early without consulting your physician."
    },
    13: {  # Cifran 500
        "uses_hindi": "यूरिन इन्फेक्शन (UTI), पेट के इन्फेक्शन और टाइफाइड बुखार के इलाज में उपयोगी।",
        "what_it_does": "Ciprofloxacin fluoroquinolone antibiotic that halts bacterial DNA synthesis.",
        "how_to_take": "Take 1 tablet every 12 hours with plenty of fluids to protect kidney function.",
        "safety_tip": "Avoid taking antacids, calcium, or iron supplements within 2 hours of this medicine."
    },
    14: {  # Taxim-O 200
        "uses_hindi": "कान, साइनस, गले और फेफड़ों के बैक्टीरियल इन्फेक्शन में ली जाने वाली एंटीबायोटिक।",
        "what_it_does": "Cefixime 200mg third-generation cephalosporin active against resistant gram-negative bacteria.",
        "how_to_take": "Take 1 tablet twice daily after food.",
        "safety_tip": "Take strictly under medical guidance."
    },
    15: {  # Pantocid DSR
        "uses_hindi": "एसिडिटी, सीने में जलन (Heartburn), खट्टी डकारें और उल्टी-मितली की शिकायत में।",
        "what_it_does": "Combines Pantoprazole (reduces acid secretion) with Domperidone (prevents reflux and nausea).",
        "how_to_take": "Take 1 capsule on an empty stomach in the morning, 30 minutes before breakfast.",
        "safety_tip": "Swallow whole; do not chew or crush the capsule pellets."
    },
    16: {  # Pan 40
        "uses_hindi": "पेट में गैस, एसिडिटी, पेट के अल्सर और भारीपन को शांत करने के लिए।",
        "what_it_does": "Pantoprazole 40mg proton pump inhibitor that provides 24-hour gastric acid suppression.",
        "how_to_take": "Take 1 tablet once daily in the morning before food.",
        "safety_tip": "Safe for regular use when prescribed for GERD or acid reflux."
    },
    17: {  # Digene Mint Antacid Gel
        "uses_hindi": "तुरंत एसिडिटी और पेट की जलन को शांत करने वाला कूलिंग मिंट जेल।",
        "what_it_does": "Quickly neutralizes excess stomach acid within 60 seconds with magnesium and aluminum hydroxides.",
        "how_to_take": "Take 1-2 teaspoonfuls (5-10 ml) after meals or when feeling heartburn.",
        "safety_tip": "Shake bottle well before use."
    },
    18: {  # Sporlac-DS
        "uses_hindi": "दस्त (Loose motions), पेट खराब, और एंटीबायोटिक लेने के बाद आंतों के गुड बैक्टीरिया को वापस लाने में।",
        "what_it_does": "Probiotic formulation with Lactic Acid Bacillus to restore healthy gut microflora balance.",
        "how_to_take": "Take 1 tablet twice daily with water or buttermilk.",
        "safety_tip": "Can be taken safely alongside or after antibiotic treatments."
    },
    19: {  # Telma 40
        "uses_hindi": "हाई ब्लड प्रेशर (High BP) को कंट्रोल करने और दिल को सुरक्षित रखने वाली दवा।",
        "what_it_does": "Telmisartan 40mg angiotensin receptor blocker that relaxes blood vessels to lower blood pressure.",
        "how_to_take": "Take 1 tablet daily at the exact same time every morning.",
        "safety_tip": "Do not stop taking abruptly even when blood pressure reads normal."
    },
    20: {  # Amlong 5
        "uses_hindi": "हाई ब्लड प्रेशर और सीने के दर्द (एंजाइना) में रक्त प्रवाह को सुचारू करने के लिए।",
        "what_it_does": "Amlodipine 5mg calcium channel blocker that dilates coronary and peripheral arteries.",
        "how_to_take": "Take 1 tablet once daily with water.",
        "safety_tip": "Inform doctor if you notice mild swelling in your feet or ankles."
    },
    21: {  # Ecosprin 75
        "uses_hindi": "खून को पतला रखकर हार्ट अटैक और स्ट्रोक के खतरे से बचाने वाली जरूरी दवा।",
        "what_it_does": "Low-dose Aspirin 75mg that inhibits platelet clumping to prevent blood clots in coronary arteries.",
        "how_to_take": "Take 1 tablet daily strictly after a full meal.",
        "safety_tip": "Consult doctor before dental procedures or surgery."
    },
    22: {  # Rosuvas 10
        "uses_hindi": "बैड कोलेस्ट्रॉल (LDL) और ट्राइग्लिसराइड्स को कम करके नसों को ब्लॉक होने से बचाने के लिए।",
        "what_it_does": "Rosuvastatin 10mg statin that inhibits liver cholesterol production and improves arterial elasticity.",
        "how_to_take": "Take 1 tablet once daily, preferably at bedtime.",
        "safety_tip": "Maintain a healthy low-fat diet and exercise routine for best lipid control."
    },
    23: {  # Glycomet 500 SR
        "uses_hindi": "टाइप-2 डायबिटीज में ब्लड शुगर लेवल को नियंत्रित करने की पहली और सबसे भरोसेमंद दवा।",
        "what_it_does": "Metformin 500mg sustained release that improves insulin sensitivity and lowers liver glucose output.",
        "how_to_take": "Take 1 tablet with or immediately after meals.",
        "safety_tip": "Sustained release formulation: swallow whole without chewing."
    },
    24: {  # Glycomet-GP 2
        "uses_hindi": "शुगर लेवल जब सिंगल दवा से कंट्रोल न हो, तब इंसुलिन रिलीज बढ़ाने के लिए।",
        "what_it_does": "Combination of Glimepiride (stimulates insulin) and Metformin (lowers insulin resistance).",
        "how_to_take": "Take 1 tablet in the morning with your main breakfast.",
        "safety_tip": "Always carry a source of glucose/sugar in case of hypoglycemia."
    },
    25: {  # Januvia 100mg
        "uses_hindi": "भोजन के बाद अचानक शुगर बढ़ने (Post-meal spike) को रोकने वाली एडवांस डायबिटीज दवा।",
        "what_it_does": "Sitagliptin 100mg DPP-4 inhibitor that increases incretin hormones only when blood sugar rises.",
        "how_to_take": "Take 1 tablet once daily with or without food.",
        "safety_tip": "Lower risk of causing hypoglycemia or weight gain."
    },
    26: {  # Accu-Chek Active Test Strips
        "uses_hindi": "घर पर एक बूंद खून से केवल 5 सेकंड में सटीक ब्लड शुगर चेक करने के लिए।",
        "what_it_does": "50 capillary blood glucose test strips compatible with Accu-Chek Active glucometer.",
        "how_to_take": "Insert strip, apply tiny blood droplet to the designated green test pad.",
        "safety_tip": "Keep the vial tightly closed to protect strips from humidity."
    },
    27: {  # Shelcal 500
        "uses_hindi": "कमजोर हड्डियों, जोड़ों के दर्द और कैल्शियम व विटामिन D3 की कमी को पूरा करने के लिए।",
        "what_it_does": "Elemental Calcium 500mg plus Vitamin D3 250 IU for maximum bone mineral density.",
        "how_to_take": "Take 1 tablet daily after lunch or dinner with water.",
        "safety_tip": "Maintain good daily hydration."
    },
    28: {  # Becosules Z
        "uses_hindi": "मुंह के छालों (Mouth Ulcers), कमजोरी, बालों के झड़ने और रोग प्रतिरोधक क्षमता बढ़ाने में।",
        "what_it_does": "Therapeutic B-Complex vitamins (B1, B2, B6, B12, Niacinamide, Folic Acid) fortified with Zinc and Vitamin C.",
        "how_to_take": "Take 1 capsule daily after breakfast.",
        "safety_tip": "Safe for regular daily nutritional maintenance."
    },
    29: {  # Uprise-D3 60K
        "uses_hindi": "विटामिन D की भारी कमी, हड्डियों की कमजोरी और बदन में लगातार सुस्ती-थकान के लिए।",
        "what_it_does": "High-potency Cholecalciferol (60,000 IU) softgel to quickly replenish vitamin D stores.",
        "how_to_take": "Take 1 capsule ONCE A WEEK with milk or food, for 4-8 weeks as prescribed.",
        "safety_tip": "Take strictly once weekly, NOT daily."
    },
    30: {  # Zincovit
        "uses_hindi": "इम्यूनिटी बढ़ाने, कमजोरी दूर करने और रिकवरी तेज करने वाला संपूर्ण मल्टीविटामिन।",
        "what_it_does": "Multivitamin, multimineral and grape seed extract tablet for energy, stamina, and cellular protection.",
        "how_to_take": "Take 1 tablet daily after food.",
        "safety_tip": "Ideal daily supplement for adults."
    },
    31: {  # Betnovate-N Cream
        "uses_hindi": "त्वचा पर खुजली, एक्जिमा, लाल दाने और बैक्टीरियल इन्फेक्शन में आराम देने वाली क्रीम।",
        "what_it_does": "Betamethasone (anti-inflammatory steroid) and Neomycin (antibiotic) for infected dermatoses.",
        "how_to_take": "Apply a thin layer to the affected clean skin area 2 times daily.",
        "safety_tip": "Do not apply on face or use continuously for more than 7 days without doctor advice."
    },
    32: {  # Candid-B Cream
        "uses_hindi": "फंगल इन्फेक्शन, दाद, खाज, खुजली और रिंगवर्म में तुरंत राहत देने वाली क्रीम।",
        "what_it_does": "Clotrimazole (antifungal) and Beclomethasone (soothing steroid) to eradicate fungal skin infections.",
        "how_to_take": "Gently massage into the affected skin twice a day after washing and drying the area.",
        "safety_tip": "Continue application for 2-3 days after symptoms clear to prevent fungal relapse."
    },
    33: {  # Clindac A 1% Gel
        "uses_hindi": "चेहरे के कील-मुंहासे (Acne & Pimples) और पस वाले दानों को सुखाने वाला असरदार जेल।",
        "what_it_does": "Clindamycin topical antibiotic that eradicates acne-causing bacteria and unclogs inflamed pores.",
        "how_to_take": "Wash face with mild cleanser, pat dry, and apply a small pea-sized amount onto pimples at night.",
        "safety_tip": "Avoid contact with eyes, lips, and corners of the nose."
    },
    34: {  # Omron Digital BP Monitor
        "uses_hindi": "घर पर सटीक ब्लड प्रेशर और पल्स रेट नापने की क्लीनिकली वैलिडेटेड ऑटोमैटिक मशीन।",
        "what_it_does": "Oscillometric digital blood pressure monitor with Intellisense technology for comfortable, accurate readings.",
        "how_to_take": "Wrap cuff around upper arm at heart level, sit calmly for 5 minutes, and press START.",
        "safety_tip": "Do not smoke, drink caffeine, or exercise 30 minutes before measurement."
    },
    35: {  # Dettol Antiseptic Liquid
        "uses_hindi": "चोट, खरोंच, घाव धोने, शेविंग के बाद और नहाने के पानी में कीटाणु खत्म करने के लिए।",
        "what_it_does": "Chloroxylenol-based medical antiseptic that kills 99.9% of bacteria on wounds and surfaces.",
        "how_to_take": "Dilute 1 tablespoon in a cup of water to cleanse minor cuts and grazes.",
        "safety_tip": "Never apply undiluted liquid directly onto open deep wounds."
    },
    36: {  # Hansaplast Washproof Bandages
        "uses_hindi": "छोटी-मोटी चोट व खरोंच पर पानी और धूल-मिट्टी से बचाने वाली वॉटरप्रूफ पट्टी।",
        "what_it_does": "Breathable, skin-friendly washproof adhesive plasters with antiseptic wound pad.",
        "how_to_take": "Clean and dry wound, peel protective film, and apply pad directly over wound.",
        "safety_tip": "Change bandage at least once daily or if it becomes wet."
    }
}

# Generate SVG files and enrich products
for prod in catalog["products"]:
    pid = prod["id"]
    name = prod["name"]
    salt = prod["salt"]
    form = prod.get("dosage_form", "Tablet")
    cat_id = prod.get("category_id", "pain-fever")
    p_col, s_col = color_map.get(cat_id, ("#2563EB", "#38BDF8"))
    
    filename = f"prod_{pid}.svg"
    filepath = os.path.join(output_dir, filename)
    
    if form in ("Syrup", "Liquid", "Liquid Gel"):
        svg_content = make_bottle_svg(name, salt, p_col, s_col, badge=form.upper())
    elif form in ("Gel", "Cream"):
        svg_content = make_tube_svg(name, salt, p_col, s_col, badge=form.upper())
    elif form in ("Capsule", "Softgel Capsule"):
        svg_content = make_capsule_strip_svg(name, salt, p_col, s_col, badge=form.upper())
    elif form in ("Medical Device", "Diagnostic Strips", "Adhesive Plaster"):
        svg_content = make_device_svg(name, salt, p_col, s_col, badge=form.upper())
    else:
        svg_content = make_strip_svg(name, salt, 10, p_col, s_col, badge=form.upper())
        
    with open(filepath, "w", encoding="utf-8") as svg_file:
        svg_file.write(svg_content)
        
    # Update catalog data
    prod["image"] = f"images/medications/{filename}"
    if pid in about_database:
        prod["about"] = about_database[pid]
    else:
        prod["about"] = {
            "uses_hindi": f"{name} ke clinical upyog aur upchar.",
            "what_it_does": f"Verified formulation for {prod.get('category_name', 'healthcare')}.",
            "how_to_take": "Take as directed by your physician or pharmacist.",
            "safety_tip": "Read label carefully before use."
        }

# Save updated catalog
with open(catalog_path, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {len(catalog['products'])} product visual SVGs and updated catalog JSON!")
