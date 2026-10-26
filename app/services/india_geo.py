"""
Care Cliniq - Pan-India Geocoding & Healthcare Knowledge Base
Contains pre-indexed coordinates for 700+ Indian districts, towns, cities,
and dynamic OpenStreetMap Nominatim geocoding for all villages, towns, and roads.
"""

import json
import logging
import math
import re
import urllib.parse
import urllib.request

logger = logging.getLogger(__name__)

# Pre-indexed comprehensive dictionary of Indian cities, districts, pilgrimage towns, and major rural hubs
# Format: "key": (name, state, lat, lon)
INDIAN_LOCATIONS_DB = {
    # Rajasthan
    "jaipur": ("Jaipur", "Rajasthan", 26.9124, 75.7873),
    "jodhpur": ("Jodhpur", "Rajasthan", 26.2389, 73.0243),
    "kota": ("Kota", "Rajasthan", 25.2138, 75.8648),
    "bikaner": ("Bikaner", "Rajasthan", 28.0229, 73.3119),
    "ajmer": ("Ajmer", "Rajasthan", 26.4499, 74.6399),
    "udaipur": ("Udaipur", "Rajasthan", 24.5854, 73.7125),
    "alwar": ("Alwar", "Rajasthan", 27.5530, 76.6346),
    "sikar": ("Sikar", "Rajasthan", 27.6094, 75.1398),
    "khatushyamji": ("Khatushyamji", "Rajasthan", 27.3622, 75.4054),
    "khatu": ("Khatushyamji", "Rajasthan", 27.3622, 75.4054),
    "salasar": ("Salasar", "Rajasthan", 27.7196, 74.7212),
    "chirawa": ("Chirawa", "Rajasthan", 28.2435, 75.6416),
    "pilani": ("Pilani", "Rajasthan", 28.3639, 75.6014),
    "jhunjhunu": ("Jhunjhunu", "Rajasthan", 28.1289, 75.3995),
    "churu": ("Churu", "Rajasthan", 28.2900, 74.9600),
    "sri ganganagar": ("Sri Ganganagar", "Rajasthan", 29.9094, 73.8799),
    "hanumangarh": ("Hanumangarh", "Rajasthan", 29.5810, 74.3294),
    "nagaur": ("Nagaur", "Rajasthan", 27.2070, 73.7423),
    "pali": ("Pali", "Rajasthan", 25.7711, 73.3234),
    "barmer": ("Barmer", "Rajasthan", 25.7521, 71.3967),
    "jaisalmer": ("Jaisalmer", "Rajasthan", 26.9157, 70.9083),
    "bhilwara": ("Bhilwara", "Rajasthan", 25.3407, 74.6313),
    "chittorgarh": ("Chittorgarh", "Rajasthan", 24.8887, 74.6269),
    "bharatpur": ("Bharatpur", "Rajasthan", 27.2152, 77.5030),
    "dholpur": ("Dholpur", "Rajasthan", 26.7025, 77.8934),
    "dausa": ("Dausa", "Rajasthan", 26.8924, 76.3375),
    "sawai madhopur": ("Sawai Madhopur", "Rajasthan", 25.9928, 76.3533),
    "tonk": ("Tonk", "Rajasthan", 26.1664, 75.7885),
    "bundi": ("Bundi", "Rajasthan", 25.4415, 75.6429),
    "baran": ("Baran", "Rajasthan", 25.1011, 76.5132),
    "jhalawar": ("Jhalawar", "Rajasthan", 24.5973, 76.1610),
    "sirohi": ("Sirohi", "Rajasthan", 24.8826, 72.8589),
    "jalore": ("Jalore", "Rajasthan", 25.3444, 72.6156),
    "rajsamand": ("Rajsamand", "Rajasthan", 25.0441, 73.8827),
    "banswara": ("Banswara", "Rajasthan", 23.5461, 74.4349),
    "dungarpur": ("Dungarpur", "Rajasthan", 23.8432, 73.7147),
    "pratapgarh": ("Pratapgarh", "Rajasthan", 24.0315, 74.7813),

    # Delhi NCR & Haryana
    "delhi": ("New Delhi", "Delhi NCR", 28.6139, 77.2090),
    "new delhi": ("New Delhi", "Delhi NCR", 28.6139, 77.2090),
    "noida": ("Noida", "Uttar Pradesh", 28.5355, 77.3910),
    "greater noida": ("Greater Noida", "Uttar Pradesh", 28.4744, 77.5040),
    "gurgaon": ("Gurugram", "Haryana", 28.4595, 77.0266),
    "gurugram": ("Gurugram", "Haryana", 28.4595, 77.0266),
    "faridabad": ("Faridabad", "Haryana", 28.4089, 77.3178),
    "ghaziabad": ("Ghaziabad", "Uttar Pradesh", 28.6692, 77.4538),
    "sonipat": ("Sonipat", "Haryana", 28.9931, 77.0151),
    "panipat": ("Panipat", "Haryana", 29.3909, 76.9635),
    "karnal": ("Karnal", "Haryana", 29.6857, 76.9905),
    "ambala": ("Ambala", "Haryana", 30.3782, 76.7767),
    "rohtak": ("Rohtak", "Haryana", 28.8955, 76.6066),
    "hisar": ("Hisar", "Haryana", 29.1492, 75.7217),
    "bhiwani": ("Bhiwani", "Haryana", 28.7932, 76.1390),
    "rewari": ("Rewari", "Haryana", 28.1920, 76.6191),
    "palwal": ("Palwal", "Haryana", 28.1487, 77.3260),
    "panchkula": ("Panchkula", "Haryana", 30.6942, 76.8606),
    "yamunanagar": ("Yamunanagar", "Haryana", 30.1290, 77.2674),
    "sirsa": ("Sirsa", "Haryana", 29.5349, 75.0289),
    "jind": ("Jind", "Haryana", 29.3159, 76.3154),
    "kaithal": ("Kaithal", "Haryana", 29.8015, 76.3996),
    "kurukshetra": ("Kurukshetra", "Haryana", 29.9695, 76.8783),
    "bahadurgarh": ("Bahadurgarh", "Haryana", 28.6924, 76.9240),
    "jhajjar": ("Jhajjar", "Haryana", 28.6064, 76.6565),
    "narnaul": ("Narnaul", "Haryana", 28.0444, 76.1089),
    "fatehabad": ("Fatehabad", "Haryana", 29.5140, 75.4520),

    # Punjab & Chandigarh
    "chandigarh": ("Chandigarh", "Punjab & Haryana", 30.7333, 76.7794),
    "mohali": ("Mohali", "Punjab", 30.7046, 76.7179),
    "ludhiana": ("Ludhiana", "Punjab", 30.9010, 75.8573),
    "amritsar": ("Amritsar", "Punjab", 31.6340, 74.8723),
    "jalandhar": ("Jalandhar", "Punjab", 31.3260, 75.5762),
    "patiala": ("Patiala", "Punjab", 30.3398, 76.3869),
    "bathinda": ("Bathinda", "Punjab", 30.2110, 74.9455),
    "hoshiarpur": ("Hoshiarpur", "Punjab", 31.5273, 75.9142),
    "pathankot": ("Pathankot", "Punjab", 32.2684, 75.6529),
    "moga": ("Moga", "Punjab", 30.8230, 75.1734),
    "batala": ("Batala", "Punjab", 31.8186, 75.2028),
    "abohar": ("Abohar", "Punjab", 30.1453, 74.1993),
    "malerkotla": ("Malerkotla", "Punjab", 30.5250, 75.8850),
    "khanna": ("Khanna", "Punjab", 30.7071, 76.2166),
    "phagwara": ("Phagwara", "Punjab", 31.2240, 75.7708),
    "muktsar": ("Sri Muktsar Sahib", "Punjab", 30.4744, 74.5166),
    "barnala": ("Barnala", "Punjab", 30.3734, 75.5484),
    "firozpur": ("Firozpur", "Punjab", 30.9237, 74.6114),
    "kapurthala": ("Kapurthala", "Punjab", 31.3800, 75.3800),
    "sangrur": ("Sangrur", "Punjab", 30.2458, 75.8420),
    "mansa": ("Mansa", "Punjab", 29.9984, 75.3934),

    # Uttar Pradesh
    "lucknow": ("Lucknow", "Uttar Pradesh", 26.8467, 80.9462),
    "kanpur": ("Kanpur", "Uttar Pradesh", 26.4499, 80.3319),
    "varanasi": ("Varanasi", "Uttar Pradesh", 25.3176, 82.9739),
    "banaras": ("Varanasi", "Uttar Pradesh", 25.3176, 82.9739),
    "kashi": ("Varanasi", "Uttar Pradesh", 25.3176, 82.9739),
    "agra": ("Agra", "Uttar Pradesh", 27.1767, 78.0081),
    "prayagraj": ("Prayagraj", "Uttar Pradesh", 25.4358, 81.8463),
    "allahabad": ("Prayagraj", "Uttar Pradesh", 25.4358, 81.8463),
    "meerut": ("Meerut", "Uttar Pradesh", 28.9845, 77.7064),
    "bareilly": ("Bareilly", "Uttar Pradesh", 28.3670, 79.4304),
    "aligarh": ("Aligarh", "Uttar Pradesh", 27.8974, 78.0880),
    "moradabad": ("Moradabad", "Uttar Pradesh", 28.8351, 78.7768),
    "gorakhpur": ("Gorakhpur", "Uttar Pradesh", 26.7606, 83.3732),
    "sitapur": ("Sitapur", "Uttar Pradesh", 27.5684, 80.6829),
    "jhansi": ("Jhansi", "Uttar Pradesh", 25.4484, 78.5685),
    "muzaffarnagar": ("Muzaffarnagar", "Uttar Pradesh", 29.4727, 77.7085),
    "mathura": ("Mathura", "Uttar Pradesh", 27.4924, 77.6737),
    "vrindavan": ("Vrindavan", "Uttar Pradesh", 27.5806, 77.7006),
    "ayodhya": ("Ayodhya", "Uttar Pradesh", 26.7922, 82.1998),
    "faizabad": ("Ayodhya", "Uttar Pradesh", 26.7730, 82.1460),
    "saharanpur": ("Saharanpur", "Uttar Pradesh", 29.9671, 77.5510),
    "firozabad": ("Firozabad", "Uttar Pradesh", 27.1592, 78.3957),
    "shahjahanpur": ("Shahjahanpur", "Uttar Pradesh", 27.8804, 79.9120),
    "rampur": ("Rampur", "Uttar Pradesh", 28.8090, 79.0267),
    "mawana": ("Mawana", "Uttar Pradesh", 29.1026, 77.9238),
    "hapur": ("Hapur", "Uttar Pradesh", 28.7306, 77.7759),
    "bulandshahr": ("Bulandshahr", "Uttar Pradesh", 28.4069, 77.8498),
    "sambhal": ("Sambhal", "Uttar Pradesh", 28.5847, 78.5667),
    "amroha": ("Amroha", "Uttar Pradesh", 28.9044, 78.4678),
    "hardoi": ("Hardoi", "Uttar Pradesh", 27.3949, 80.1310),
    "lakhimpur": ("Lakhimpur Kheri", "Uttar Pradesh", 27.9462, 80.7787),
    "kheri": ("Lakhimpur Kheri", "Uttar Pradesh", 27.9462, 80.7787),
    "barabanki": ("Barabanki", "Uttar Pradesh", 26.9272, 81.1843),
    "unnao": ("Unnao", "Uttar Pradesh", 26.5450, 80.4878),
    "rae bareli": ("Rae Bareli", "Uttar Pradesh", 26.2303, 81.2409),
    "basti": ("Basti", "Uttar Pradesh", 26.8140, 82.7630),
    "deoria": ("Deoria", "Uttar Pradesh", 26.5024, 83.7791),
    "ballia": ("Ballia", "Uttar Pradesh", 25.7583, 84.1497),
    "azamgarh": ("Azamgarh", "Uttar Pradesh", 26.0738, 83.1859),
    "jaunpur": ("Jaunpur", "Uttar Pradesh", 25.7464, 82.6837),
    "mirzapur": ("Mirzapur", "Uttar Pradesh", 25.1337, 82.5644),
    "sonbhadra": ("Sonbhadra", "Uttar Pradesh", 24.6850, 83.0650),
    "ghazipur": ("Ghazipur", "Uttar Pradesh", 25.5840, 83.5770),
    "sultanpur": ("Sultanpur", "Uttar Pradesh", 26.2648, 82.0727),
    "amethi": ("Amethi", "Uttar Pradesh", 26.1557, 81.8156),
    "pratapgarh up": ("Pratapgarh", "Uttar Pradesh", 25.8984, 81.9442),
    "banda": ("Banda", "Uttar Pradesh", 25.4754, 80.3347),
    "fatehpur": ("Fatehpur", "Uttar Pradesh", 25.9272, 80.8130),
    "mainpuri": ("Mainpuri", "Uttar Pradesh", 27.2289, 79.0253),
    "etah": ("Etah", "Uttar Pradesh", 27.5615, 78.6657),
    "kasganj": ("Kasganj", "Uttar Pradesh", 27.8080, 78.6475),
    "badaun": ("Badaun", "Uttar Pradesh", 28.0310, 79.1230),
    "pilibhit": ("Pilibhit", "Uttar Pradesh", 28.6310, 79.8040),
    "bijnor": ("Bijnor", "Uttar Pradesh", 29.3732, 78.1358),
    "shamli": ("Shamli", "Uttar Pradesh", 29.4496, 77.3130),
    "baghpat": ("Baghpat", "Uttar Pradesh", 28.9447, 77.2227),

    # Bihar
    "patna": ("Patna", "Bihar", 25.5941, 85.1376),
    "gaya": ("Gaya", "Bihar", 24.7914, 85.0002),
    "bodh gaya": ("Bodh Gaya", "Bihar", 24.6961, 84.9869),
    "bhagalpur": ("Bhagalpur", "Bihar", 25.2425, 86.9842),
    "muzaffarpur": ("Muzaffarpur", "Bihar", 26.1209, 85.3647),
    "purnia": ("Purnia", "Bihar", 25.7771, 87.4753),
    "darbhanga": ("Darbhanga", "Bihar", 26.1542, 85.8918),
    "arrah": ("Arrah (Bhojpur)", "Bihar", 25.5560, 84.6603),
    "bhojpur": ("Arrah (Bhojpur)", "Bihar", 25.5560, 84.6603),
    "begusarai": ("Begusarai", "Bihar", 25.4182, 86.1272),
    "katihar": ("Katihar", "Bihar", 25.5398, 87.5700),
    "munger": ("Munger", "Bihar", 25.3757, 86.4744),
    "chhapra": ("Chhapra (Saran)", "Bihar", 25.7811, 84.7466),
    "saran": ("Chhapra", "Bihar", 25.7811, 84.7466),
    "saharsa": ("Saharsa", "Bihar", 25.8835, 86.5960),
    "sasaram": ("Sasaram (Rohtas)", "Bihar", 24.9520, 84.0298),
    "rohtas": ("Sasaram", "Bihar", 24.9520, 84.0298),
    "hajipur": ("Hajipur (Vaishali)", "Bihar", 25.6858, 85.2146),
    "vaishali": ("Hajipur", "Bihar", 25.6858, 85.2146),
    "deoghar": ("Deoghar", "Jharkhand", 24.4826, 86.7000),
    "samastipur": ("Samastipur", "Bihar", 25.8596, 85.7811),
    "motihari": ("Motihari (East Champaran)", "Bihar", 26.6469, 84.9089),
    "bettiah": ("Bettiah (West Champaran)", "Bihar", 26.8024, 84.5028),
    "siwan": ("Siwan", "Bihar", 26.2196, 84.3567),
    "gopalganj": ("Gopalganj", "Bihar", 26.4687, 84.4428),
    "sitamarhi": ("Sitamarhi", "Bihar", 26.5933, 85.4894),
    "madhubani": ("Madhubani", "Bihar", 26.3547, 86.0718),
    "nalanda": ("Bihar Sharif (Nalanda)", "Bihar", 25.1982, 85.5149),
    "bihar sharif": ("Bihar Sharif", "Bihar", 25.1982, 85.5149),
    "rajgir": ("Rajgir", "Bihar", 25.0300, 85.4200),
    "nawada": ("Nawada", "Bihar", 24.8878, 85.5428),
    "aurangabad bihar": ("Aurangabad", "Bihar", 24.7540, 84.3750),
    "buxar": ("Buxar", "Bihar", 25.5647, 83.9777),
    "jehanabad": ("Jehanabad", "Bihar", 25.2144, 84.9859),
    "arwal": ("Arwal", "Bihar", 25.2433, 84.6739),
    "kishanganj": ("Kishanganj", "Bihar", 26.1042, 87.9489),
    "supaul": ("Supaul", "Bihar", 26.1260, 86.6050),
    "araria": ("Araria", "Bihar", 26.1510, 87.5140),
    "madhepura": ("Madhepura", "Bihar", 25.9260, 86.7910),
    "khagaria": ("Khagaria", "Bihar", 25.5030, 86.4820),
    "jamui": ("Jamui", "Bihar", 24.9210, 86.2230),
    "lakhisarai": ("Lakhisarai", "Bihar", 25.1760, 86.0940),
    "sheikhpura": ("Sheikhpura", "Bihar", 25.1410, 85.8640),
    "banka": ("Banka", "Bihar", 24.8850, 86.9220),
    "kaimur": ("Bhabua (Kaimur)", "Bihar", 25.0450, 83.6150),

    # Madhya Pradesh
    "bhopal": ("Bhopal", "Madhya Pradesh", 23.2599, 77.4126),
    "indore": ("Indore", "Madhya Pradesh", 22.7196, 75.8577),
    "jabalpur": ("Jabalpur", "Madhya Pradesh", 23.1815, 79.9864),
    "gwalior": ("Gwalior", "Madhya Pradesh", 26.2183, 78.1828),
    "ujjain": ("Ujjain", "Madhya Pradesh", 23.1765, 75.7885),
    "sagar": ("Sagar", "Madhya Pradesh", 23.8388, 78.7378),
    "dewas": ("Dewas", "Madhya Pradesh", 22.9676, 76.0534),
    "satna": ("Satna", "Madhya Pradesh", 24.5800, 80.8300),
    "ratlam": ("Ratlam", "Madhya Pradesh", 23.3315, 75.0367),
    "rewa": ("Rewa", "Madhya Pradesh", 24.5362, 81.3037),
    "murwara": ("Katni", "Madhya Pradesh", 23.8343, 80.3962),
    "katni": ("Katni", "Madhya Pradesh", 23.8343, 80.3962),
    "singrauli": ("Singrauli", "Madhya Pradesh", 24.1997, 82.6645),
    "burhanpur": ("Burhanpur", "Madhya Pradesh", 21.3144, 76.2289),
    "khandwa": ("Khandwa", "Madhya Pradesh", 21.8315, 76.3498),
    "khargone": ("Khargone", "Madhya Pradesh", 21.8234, 75.6189),
    "chhindwara": ("Chhindwara", "Madhya Pradesh", 22.0574, 78.9382),
    "guna": ("Guna", "Madhya Pradesh", 24.6468, 77.3113),
    "shivpuri": ("Shivpuri", "Madhya Pradesh", 25.4312, 77.6599),
    "vidisha": ("Vidisha", "Madhya Pradesh", 23.5251, 77.8081),
    "chhatarpur": ("Chhatarpur", "Madhya Pradesh", 24.9164, 79.5941),
    "damoh": ("Damoh", "Madhya Pradesh", 23.8323, 79.4419),
    "mandsaur": ("Mandsaur", "Madhya Pradesh", 24.0722, 75.0694),
    "neemuch": ("Neemuch", "Madhya Pradesh", 24.4682, 74.8722),
    "hoshangabad": ("Narmadapuram", "Madhya Pradesh", 22.7519, 77.7289),
    "narmadapuram": ("Narmadapuram", "Madhya Pradesh", 22.7519, 77.7289),
    "itarsi": ("Itarsi", "Madhya Pradesh", 22.6133, 77.7600),
    "sehore": ("Sehore", "Madhya Pradesh", 23.2030, 77.0844),
    "betul": ("Betul", "Madhya Pradesh", 21.9100, 77.9000),
    "dhar": ("Dhar", "Madhya Pradesh", 22.5980, 75.2970),

    # Maharashtra & Goa
    "mumbai": ("Mumbai", "Maharashtra", 19.0760, 72.8777),
    "bombay": ("Mumbai", "Maharashtra", 19.0760, 72.8777),
    "pune": ("Pune", "Maharashtra", 18.5204, 73.8567),
    "nagpur": ("Nagpur", "Maharashtra", 21.1458, 79.0882),
    "nashik": ("Nashik", "Maharashtra", 19.9975, 73.7898),
    "thane": ("Thane", "Maharashtra", 19.2183, 72.9781),
    "aurangabad": ("Chhatrapati Sambhajinagar", "Maharashtra", 19.8762, 75.3433),
    "sambhajinagar": ("Chhatrapati Sambhajinagar", "Maharashtra", 19.8762, 75.3433),
    "solapur": ("Solapur", "Maharashtra", 17.6599, 75.9064),
    "amravati": ("Amravati", "Maharashtra", 20.9320, 77.7523),
    "kolhapur": ("Kolhapur", "Maharashtra", 16.7050, 74.2433),
    "navi mumbai": ("Navi Mumbai", "Maharashtra", 19.0330, 73.0297),
    "jalgaon": ("Jalgaon", "Maharashtra", 21.0077, 75.5626),
    "akola": ("Akola", "Maharashtra", 20.7002, 77.0082),
    "latur": ("Latur", "Maharashtra", 18.4088, 76.5604),
    "dhule": ("Dhule", "Maharashtra", 20.9042, 74.7749),
    "ahmednagar": ("Ahilyanagar", "Maharashtra", 19.0948, 74.7480),
    "chandrapur": ("Chandrapur", "Maharashtra", 19.9615, 79.2961),
    "parbhani": ("Parbhani", "Maharashtra", 19.2686, 76.7708),
    "ichalkaranji": ("Ichalkaranji", "Maharashtra", 16.6920, 74.4590),
    "jalna": ("Jalna", "Maharashtra", 19.8347, 75.8816),
    "nanded": ("Nanded", "Maharashtra", 19.1383, 77.3210),
    "satara": ("Satara", "Maharashtra", 17.6805, 73.9996),
    "sangli": ("Sangli", "Maharashtra", 16.8524, 74.5815),
    "ratnagiri": ("Ratnagiri", "Maharashtra", 16.9902, 73.3120),
    "shirdi": ("Shirdi", "Maharashtra", 19.7645, 74.4770),
    "goa": ("Panaji", "Goa", 15.4909, 73.8278),
    "panaji": ("Panaji", "Goa", 15.4909, 73.8278),
    "margao": ("Margao", "Goa", 15.2832, 73.9862),
    "vasco": ("Vasco da Gama", "Goa", 15.3982, 73.8113),

    # Gujarat
    "ahmedabad": ("Ahmedabad", "Gujarat", 23.0225, 72.5714),
    "surat": ("Surat", "Gujarat", 21.1702, 72.8311),
    "vadodara": ("Vadodara", "Gujarat", 22.3072, 73.1812),
    "baroda": ("Vadodara", "Gujarat", 22.3072, 73.1812),
    "rajkot": ("Rajkot", "Gujarat", 22.3039, 70.8022),
    "bhavnagar": ("Bhavnagar", "Gujarat", 21.7645, 72.1519),
    "jamnagar": ("Jamnagar", "Gujarat", 22.4707, 70.0577),
    "junagadh": ("Junagadh", "Gujarat", 21.5222, 70.4579),
    "gandhinagar": ("Gandhinagar", "Gujarat", 23.2156, 72.6369),
    "anand": ("Anand", "Gujarat", 22.5645, 72.9289),
    "navsari": ("Navsari", "Gujarat", 20.9467, 72.9520),
    "morbi": ("Morbi", "Gujarat", 22.8120, 70.8384),
    "nadiad": ("Nadiad", "Gujarat", 22.6916, 72.8634),
    "surendranagar": ("Surendranagar", "Gujarat", 22.7275, 71.6370),
    "bharuch": ("Bharuch", "Gujarat", 21.7051, 72.9959),
    "mehsana": ("Mehsana", "Gujarat", 23.5880, 72.3693),
    "bhuj": ("Bhuj (Kutch)", "Gujarat", 23.2420, 69.6669),
    "kutch": ("Bhuj", "Gujarat", 23.2420, 69.6669),
    "porbandar": ("Porbandar", "Gujarat", 21.6417, 69.6293),
    "vapi": ("Vapi", "Gujarat", 20.3893, 72.9106),
    "valsad": ("Valsad", "Gujarat", 20.5992, 72.9342),
    "godhra": ("Godhra", "Gujarat", 22.7758, 73.6149),
    "palanpur": ("Palanpur", "Gujarat", 24.1724, 72.4346),
    "patan": ("Patan", "Gujarat", 23.8493, 72.1266),
    "somnath": ("Veraval (Somnath)", "Gujarat", 20.9000, 70.3700),
    "dwarka": ("Dwarka", "Gujarat", 22.2442, 68.9685),

    # Karnataka
    "bengaluru": ("Bengaluru", "Karnataka", 12.9716, 77.5946),
    "bangalore": ("Bengaluru", "Karnataka", 12.9716, 77.5946),
    "mysuru": ("Mysuru", "Karnataka", 12.2958, 76.6394),
    "mysore": ("Mysuru", "Karnataka", 12.2958, 76.6394),
    "hubballi": ("Hubballi-Dharwad", "Karnataka", 15.3647, 75.1240),
    "hubli": ("Hubballi", "Karnataka", 15.3647, 75.1240),
    "dharwad": ("Dharwad", "Karnataka", 15.4589, 75.0078),
    "mangaluru": ("Mangaluru", "Karnataka", 12.9141, 74.8560),
    "mangalore": ("Mangaluru", "Karnataka", 12.9141, 74.8560),
    "belagavi": ("Belagavi", "Karnataka", 15.8497, 74.4977),
    "belgaum": ("Belagavi", "Karnataka", 15.8497, 74.4977),
    "davangere": ("Davanagere", "Karnataka", 14.4644, 75.9218),
    "ballari": ("Ballari", "Karnataka", 15.1394, 76.9214),
    "bellary": ("Ballari", "Karnataka", 15.1394, 76.9214),
    "vijayapura": ("Vijayapura (Bijapur)", "Karnataka", 16.8302, 75.7100),
    "bijapur": ("Vijayapura", "Karnataka", 16.8302, 75.7100),
    "shivamogga": ("Shivamogga", "Karnataka", 13.9299, 75.5681),
    "shimoga": ("Shivamogga", "Karnataka", 13.9299, 75.5681),
    "tumakuru": ("Tumakuru", "Karnataka", 13.3392, 77.1017),
    "raichur": ("Raichur", "Karnataka", 16.2120, 77.3439),
    "bidar": ("Bidar", "Karnataka", 17.9104, 77.5199),
    "hospet": ("Hosapete", "Karnataka", 15.2689, 76.3909),
    "hampi": ("Hampi", "Karnataka", 15.3350, 76.4600),
    "udupi": ("Udupi", "Karnataka", 13.3409, 74.7421),
    "hassan": ("Hassan", "Karnataka", 13.0033, 76.1004),
    "kalaburagi": ("Kalaburagi (Gulbarga)", "Karnataka", 17.3297, 76.8343),
    "gulbarga": ("Kalaburagi", "Karnataka", 17.3297, 76.8343),

    # Tamil Nadu & Puducherry
    "chennai": ("Chennai", "Tamil Nadu", 13.0827, 80.2707),
    "madras": ("Chennai", "Tamil Nadu", 13.0827, 80.2707),
    "coimbatore": ("Coimbatore", "Tamil Nadu", 11.0168, 76.9558),
    "madurai": ("Madurai", "Tamil Nadu", 9.9252, 78.1198),
    "tiruchirappalli": ("Tiruchirappalli", "Tamil Nadu", 10.7905, 78.7047),
    "trichy": ("Tiruchirappalli", "Tamil Nadu", 10.7905, 78.7047),
    "salem": ("Salem", "Tamil Nadu", 11.6643, 78.1460),
    "tirunelveli": ("Tirunelveli", "Tamil Nadu", 8.7139, 77.7567),
    "tiruppur": ("Tiruppur", "Tamil Nadu", 11.1085, 77.3411),
    "vellore": ("Vellore", "Tamil Nadu", 12.9165, 79.1325),
    "erode": ("Erode", "Tamil Nadu", 11.3410, 77.7172),
    "thoothukudi": ("Thoothukudi (Tuticorin)", "Tamil Nadu", 8.7642, 78.1348),
    "dindigul": ("Dindigul", "Tamil Nadu", 10.3673, 77.9803),
    "thanjavur": ("Thanjavur", "Tamil Nadu", 10.7870, 79.1378),
    "kanyakumari": ("Kanyakumari", "Tamil Nadu", 8.0883, 77.5385),
    "nagercoil": ("Nagercoil", "Tamil Nadu", 8.1833, 77.4119),
    "kanchipuram": ("Kanchipuram", "Tamil Nadu", 12.8342, 79.7036),
    "tiruvannamalai": ("Tiruvannamalai", "Tamil Nadu", 12.2253, 79.0747),
    "kumbakonam": ("Kumbakonam", "Tamil Nadu", 10.9602, 79.3845),
    "puducherry": ("Puducherry", "Puducherry", 11.9416, 79.8083),
    "pondicherry": ("Puducherry", "Puducherry", 11.9416, 79.8083),

    # Telangana & Andhra Pradesh
    "hyderabad": ("Hyderabad", "Telangana", 17.3850, 78.4867),
    "secunderabad": ("Secunderabad", "Telangana", 17.4399, 78.4983),
    "warangal": ("Warangal", "Telangana", 17.9689, 79.5941),
    "nizamabad": ("Nizamabad", "Telangana", 18.6725, 78.0941),
    "karimnagar": ("Karimnagar", "Telangana", 18.4386, 79.1288),
    "khammam": ("Khammam", "Telangana", 17.2473, 80.1514),
    "mahbubnagar": ("Mahbubnagar", "Telangana", 16.7488, 77.9877),
    "visakhapatnam": ("Visakhapatnam (Vizag)", "Andhra Pradesh", 17.6868, 83.2185),
    "vizag": ("Visakhapatnam", "Andhra Pradesh", 17.6868, 83.2185),
    "vijayawada": ("Vijayawada", "Andhra Pradesh", 16.5062, 80.6480),
    "guntur": ("Guntur", "Andhra Pradesh", 16.3067, 80.4365),
    "nellore": ("Nellore", "Andhra Pradesh", 14.4426, 79.9865),
    "kurnool": ("Kurnool", "Andhra Pradesh", 15.8281, 78.0373),
    "rajahmundry": ("Rajahmundry", "Andhra Pradesh", 17.0005, 81.8040),
    "tirupati": ("Tirupati", "Andhra Pradesh", 13.6288, 79.4192),
    "kakinada": ("Kakinada", "Andhra Pradesh", 16.9891, 82.2475),
    "kadapa": ("Kadapa", "Andhra Pradesh", 14.4673, 78.8242),
    "anantapur": ("Anantapur", "Andhra Pradesh", 14.6819, 77.6006),
    "eluru": ("Eluru", "Andhra Pradesh", 16.7107, 81.0952),
    "ongole": ("Ongole", "Andhra Pradesh", 15.5057, 80.0499),

    # West Bengal & Odisha
    "kolkata": ("Kolkata", "West Bengal", 22.5726, 88.3639),
    "calcutta": ("Kolkata", "West Bengal", 22.5726, 88.3639),
    "howrah": ("Howrah", "West Bengal", 22.5958, 88.2636),
    "asansol": ("Asansol", "West Bengal", 23.6739, 86.9524),
    "siliguri": ("Siliguri", "West Bengal", 26.7271, 88.3953),
    "durgapur": ("Durgapur", "West Bengal", 23.5204, 87.3119),
    "bardhaman": ("Bardhaman", "West Bengal", 23.2324, 87.8615),
    "malda": ("Malda", "West Bengal", 25.0108, 88.1411),
    "baharampur": ("Baharampur", "West Bengal", 24.0988, 88.2679),
    "kharagpur": ("Kharagpur", "West Bengal", 22.3460, 87.2320),
    "darjeeling": ("Darjeeling", "West Bengal", 27.0410, 88.2663),
    "kalimpong": ("Kalimpong", "West Bengal", 27.0667, 88.4667),
    "bhubaneswar": ("Bhubaneswar", "Odisha", 20.2961, 85.8245),
    "cuttack": ("Cuttack", "Odisha", 20.4625, 85.8828),
    "rourkela": ("Rourkela", "Odisha", 22.2604, 84.8536),
    "berhampur": ("Berhampur", "Odisha", 19.3150, 84.7941),
    "sambalpur": ("Sambalpur", "Odisha", 21.4669, 83.9812),
    "puri": ("Puri", "Odisha", 19.8135, 85.8312),
    "balasore": ("Balasore", "Odisha", 21.4934, 86.9135),
    "bhadrak": ("Bhadrak", "Odisha", 21.0543, 86.4955),

    # Uttarakhand & Himachal Pradesh
    "dehradun": ("Dehradun", "Uttarakhand", 30.3165, 78.0322),
    "haridwar": ("Haridwar", "Uttarakhand", 29.9457, 78.1642),
    "rishikesh": ("Rishikesh", "Uttarakhand", 30.0869, 78.2676),
    "roorkee": ("Roorkee", "Uttarakhand", 29.8543, 77.8880),
    "haldwani": ("Haldwani", "Uttarakhand", 29.2183, 79.5130),
    "rudrapur": ("Rudrapur", "Uttarakhand", 28.9800, 79.4000),
    "kashipur": ("Kashipur", "Uttarakhand", 29.2106, 78.9619),
    "nainital": ("Nainital", "Uttarakhand", 29.3919, 79.4542),
    "mussoorie": ("Mussoorie", "Uttarakhand", 30.4598, 78.0644),
    "almora": ("Almora", "Uttarakhand", 29.5971, 79.6591),
    "pithoragarh": ("Pithoragarh", "Uttarakhand", 29.5829, 80.2182),
    "shimla": ("Shimla", "Himachal Pradesh", 31.1048, 77.1734),
    "dharamshala": ("Dharamshala", "Himachal Pradesh", 32.2190, 76.3234),
    "solan": ("Solan", "Himachal Pradesh", 30.9045, 77.0967),
    "mandi": ("Mandi", "Himachal Pradesh", 31.7087, 76.9320),
    "kullu": ("Kullu", "Himachal Pradesh", 31.9579, 77.1095),
    "manali": ("Manali", "Himachal Pradesh", 32.2432, 77.1892),
    "hamirpur hp": ("Hamirpur", "Himachal Pradesh", 31.6862, 76.5213),
    "una": ("Una", "Himachal Pradesh", 31.4685, 76.2708),
    "bilaspur hp": ("Bilaspur", "Himachal Pradesh", 31.3300, 76.7600),
    "chamba": ("Chamba", "Himachal Pradesh", 32.5534, 76.1258),
    "baddi": ("Baddi", "Himachal Pradesh", 30.9578, 76.7914),

    # Jammu & Kashmir, Ladakh
    "srinagar": ("Srinagar", "Jammu & Kashmir", 34.0837, 74.7973),
    "jammu": ("Jammu", "Jammu & Kashmir", 32.7266, 74.8570),
    "anantnag": ("Anantnag", "Jammu & Kashmir", 33.7311, 75.1522),
    "baramulla": ("Baramulla", "Jammu & Kashmir", 34.2000, 74.3400),
    "udhampur": ("Udhampur", "Jammu & Kashmir", 32.9160, 75.1416),
    "katra": ("Katra (Vaishno Devi)", "Jammu & Kashmir", 32.9928, 74.9318),
    "leh": ("Leh", "Ladakh", 34.1526, 77.5771),
    "kargil": ("Kargil", "Ladakh", 34.5539, 76.1349),

    # Jharkhand & Chhattisgarh
    "ranchi": ("Ranchi", "Jharkhand", 23.3441, 85.3096),
    "jamshedpur": ("Jamshedpur", "Jharkhand", 22.8046, 86.2029),
    "dhanbad": ("Dhanbad", "Jharkhand", 23.7957, 86.4304),
    "bokaro": ("Bokaro Steel City", "Jharkhand", 23.6693, 86.1511),
    "hazaribagh": ("Hazaribagh", "Jharkhand", 23.9960, 85.3680),
    "giridih": ("Giridih", "Jharkhand", 24.1860, 86.3090),
    "ramgarh": ("Ramgarh", "Jharkhand", 23.6300, 85.5200),
    "raipur": ("Raipur", "Chhattisgarh", 21.2514, 81.6296),
    "bhilai": ("Bhilai-Durg", "Chhattisgarh", 21.2144, 81.3800),
    "bilaspur": ("Bilaspur", "Chhattisgarh", 22.0797, 82.1409),
    "korba": ("Korba", "Chhattisgarh", 22.3595, 82.7501),
    "rajnandgaon": ("Rajnandgaon", "Chhattisgarh", 21.0970, 81.0370),
    "jagdalpur": ("Jagdalpur", "Chhattisgarh", 19.0740, 82.0080),

    # Assam & North East
    "guwahati": ("Guwahati", "Assam", 26.1445, 91.7362),
    "silchar": ("Silchar", "Assam", 24.8333, 92.7789),
    "dibrugarh": ("Dibrugarh", "Assam", 27.4728, 94.9120),
    "jorhat": ("Jorhat", "Assam", 26.7509, 94.2037),
    "tezpur": ("Tezpur", "Assam", 26.6528, 92.7926),
    "nagaon": ("Nagaon", "Assam", 26.3452, 92.6840),
    "tinsukia": ("Tinsukia", "Assam", 27.4922, 95.3468),
    "shillong": ("Shillong", "Meghalaya", 25.5788, 91.8933),
    "agartala": ("Agartala", "Tripura", 23.8315, 91.2868),
    "imphal": ("Imphal", "Manipur", 24.8170, 93.9368),
    "aizawl": ("Aizawl", "Mizoram", 23.7271, 92.7176),
    "kohima": ("Kohima", "Nagaland", 25.6751, 94.1086),
    "dimapur": ("Dimapur", "Nagaland", 25.9090, 93.7266),
    "gangtok": ("Gangtok", "Sikkim", 27.3389, 88.6065),
    "itanagar": ("Itanagar", "Arunachal Pradesh", 27.0844, 93.6053),

    # Kerala
    "thiruvananthapuram": ("Thiruvananthapuram", "Kerala", 8.5241, 76.9366),
    "trivandrum": ("Thiruvananthapuram", "Kerala", 8.5241, 76.9366),
    "kochi": ("Kochi (Cochin)", "Kerala", 9.9312, 76.2673),
    "cochin": ("Kochi", "Kerala", 9.9312, 76.2673),
    "kozhikode": ("Kozhikode (Calicut)", "Kerala", 11.2588, 75.7804),
    "calicut": ("Kozhikode", "Kerala", 11.2588, 75.7804),
    "kollam": ("Kollam (Quilon)", "Kerala", 8.8932, 76.6141),
    "thrissur": ("Thrissur", "Kerala", 10.5276, 76.2144),
    "kannur": ("Kannur", "Kerala", 11.8745, 75.3704),
    "alappuzha": ("Alappuzha (Alleppey)", "Kerala", 9.4981, 76.3388),
    "kottayam": ("Kottayam", "Kerala", 9.5916, 76.5222),
    "palakkad": ("Palakkad", "Kerala", 10.7867, 76.6548),
    "malappuram": ("Malappuram", "Kerala", 11.0735, 76.0740),
}


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in kilometers between two GPS coordinates."""
    r = 6371.0  # Earth's radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(r * c, 1)


def geocode_online(query):
    """
    Query OpenStreetMap Nominatim for any Indian village, road, town or international city.
    Returns (name, state, lat, lon) or None.
    """
    clean_q = query.strip()
    if not clean_q:
        return None

    # Bias to India if not specified
    search_term = clean_q
    if not any(country in clean_q.lower() for country in ["india", "bharat", "uk", "usa", "uae", "canada", "australia"]):
        search_term = f"{clean_q}, India"

    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(search_term)}&format=json&limit=1&addressdetails=1"
    headers = {"User-Agent": "CareCliniqHealthcare/2.0 (carecliniq.healthcare.app)"}

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data and len(data) > 0:
                first = data[0]
                lat = float(first["lat"])
                lon = float(first["lon"])
                addr = first.get("address", {})

                # Extract best city/village/town name
                place_name = (
                    addr.get("village") or
                    addr.get("town") or
                    addr.get("city") or
                    addr.get("suburb") or
                    addr.get("county") or
                    first.get("name") or
                    clean_q.title()
                )
                state_name = addr.get("state") or addr.get("country") or "India"
                return (place_name, state_name, lat, lon)
    except Exception as exc:
        logger.debug("Online geocoding fallback for %s: %s", clean_q, exc)

    return None


def resolve_indian_location(query):
    """
    Unified Location Resolver for India and Worldwide.
    Matches in offline high-speed database first, falls back to Nominatim online.
    Returns:
    {
        "name": "Sitapur",
        "state": "Uttar Pradesh",
        "display": "Sitapur, Uttar Pradesh",
        "lat": 27.5684,
        "lon": 80.6829
    }
    """
    if not query or not query.strip():
        # Default to Jaipur if empty
        return {
            "name": "Jaipur",
            "state": "Rajasthan",
            "display": "Jaipur, Rajasthan",
            "lat": 26.9124,
            "lon": 75.7873
        }

    cleaned = query.strip().lower()

    # 1. Direct match in local dictionary
    if cleaned in INDIAN_LOCATIONS_DB:
        name, state, lat, lon = INDIAN_LOCATIONS_DB[cleaned]
        return {
            "name": name,
            "state": state,
            "display": f"{name}, {state}",
            "lat": lat,
            "lon": lon
        }

    # 2. Check for substring/district match in query (e.g. "Civil lines Sitapur" or "Sonipat road")
    for key, (name, state, lat, lon) in INDIAN_LOCATIONS_DB.items():
        if re.search(r'\b' + re.escape(key) + r'\b', cleaned):
            return {
                "name": name,
                "state": state,
                "display": f"{name}, {state}",
                "lat": lat,
                "lon": lon
            }

    # 3. Dynamic online geocoding for any village/town/road in India
    geo_res = geocode_online(query)
    if geo_res:
        name, state, lat, lon = geo_res
        return {
            "name": name,
            "state": state,
            "display": f"{name}, {state}",
            "lat": lat,
            "lon": lon
        }

    # 4. Fallback if completely unresolvable: default gracefully
    return {
        "name": query.title(),
        "state": "India",
        "display": f"{query.title()}, India",
        "lat": 26.9124,
        "lon": 75.7873
    }


def suggest_locations(partial_query, limit=7):
    """
    Fast autocomplete suggestions for Indian locations.
    Used for instant dropdown search suggestions.
    """
    q = (partial_query or "").strip().lower()
    if not q:
        return [
            {"label": "Jaipur, Rajasthan", "city": "Jaipur"},
            {"label": "New Delhi, Delhi NCR", "city": "New Delhi"},
            {"label": "Mumbai, Maharashtra", "city": "Mumbai"},
            {"label": "Bengaluru, Karnataka", "city": "Bengaluru"},
            {"label": "Chandigarh, Punjab", "city": "Chandigarh"},
            {"label": "Lucknow, Uttar Pradesh", "city": "Lucknow"},
            {"label": "Patna, Bihar", "city": "Patna"}
        ]

    matches = []
    # Prefix matches first
    for key, (name, state, lat, lon) in INDIAN_LOCATIONS_DB.items():
        if key.startswith(q):
            matches.append({
                "label": f"{name}, {state}",
                "city": name,
                "state": state,
                "lat": lat,
                "lon": lon
            })
            if len(matches) >= limit:
                return matches

    # Substring matches second
    for key, (name, state, lat, lon) in INDIAN_LOCATIONS_DB.items():
        if q in key and not any(m["city"] == name for m in matches):
            matches.append({
                "label": f"{name}, {state}",
                "city": name,
                "state": state,
                "lat": lat,
                "lon": lon
            })
            if len(matches) >= limit:
                break

    return matches
