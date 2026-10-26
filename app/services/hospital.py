import urllib.parse

def get_facility_dataset(city_clean, lat, lon, state_name="India", location_display=None):
    title_city = city_clean.title()

    if city_clean == "jaipur":
        return [
            {
                "id": "fac-1",
                "name": "City Care Hospital & Trauma Unit",
                "type": "hospital",
                "category_label": "Multispecialty Hospital",
                "specialty": "Multispecialty • Trauma & Critical Care",
                "address": "MI Road, Near Ajmeri Gate, Jaipur",
                "distance": "1.2 km away",
                "distance_km": 1.2,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.8,
                "reviews_count": "340",
                "phone": "+91 141 236 8000",
                "coords": [26.9174, 75.8123],
                "image": "images/facility_hospital1.jpg",
                "badges": ["24/7 Emergency", "ICU", "Trauma Care"],
                "doctors": ["Dr. Rajesh Sharma, MD", "Dr. Alok Sharma, DM"],
            },
            {
                "id": "fac-2",
                "name": "Apex Multispeciality Hospital",
                "type": "hospital",
                "category_label": "Super Specialty Hospital",
                "specialty": "Cardiology • Orthopedics • Neurology",
                "address": "Sector 5, Malviya Nagar, Jaipur",
                "distance": "3.4 km away",
                "distance_km": 3.4,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.7,
                "reviews_count": "215",
                "phone": "+91 141 275 1871",
                "coords": [26.8528, 75.8236],
                "image": "images/facility_hospital1.jpg",
                "badges": ["Cardiac Care", "Orthopedics", "Neurology"],
                "doctors": ["Dr. Sanjay Bhatt, MD", "Dr. Vikram Malhotra, MS"],
            },
            {
                "id": "fac-3",
                "name": "Shree Balaji Clinic & Diagnostic",
                "type": "clinic",
                "category_label": "Consultation Clinic",
                "specialty": "General Medicine • Pediatrics • Lab Services",
                "address": "Tonk Road, Bapu Nagar, Jaipur",
                "distance": "2.1 km away",
                "distance_km": 2.1,
                "hours": "Open till 9:30 PM",
                "is_24_7": False,
                "rating": 4.9,
                "reviews_count": "180",
                "phone": "+91 141 270 4500",
                "coords": [26.8850, 75.8050],
                "image": "images/facility_clinic1.jpg",
                "badges": ["Family Medicine", "Pediatrics", "On-site Lab"],
                "doctors": ["Dr. Ananya Mehta, MD", "Dr. Pooja Singhal, MD"],
            },
            {
                "id": "fac-4",
                "name": "Narayana Multispeciality Hospital",
                "type": "hospital",
                "category_label": "Tertiary Care Hospital",
                "specialty": "Oncology • Cardiology • Emergency Surgery",
                "address": "Kumbha Marg, Sector 28, Pratap Nagar, Jaipur",
                "distance": "5.6 km away",
                "distance_km": 5.6,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.8,
                "reviews_count": "490",
                "phone": "+91 141 712 2222",
                "coords": [26.8041, 75.8362],
                "image": "images/facility_hospital1.jpg",
                "badges": ["Cancer Care", "Cath Lab", "Dialysis Unit"],
                "doctors": ["Dr. Alok Sharma, DM", "Dr. Vivek Mehra, MD"],
            },
            {
                "id": "fac-5",
                "name": "Fortis Escorts Hospital",
                "type": "hospital",
                "category_label": "Apex Heart & Neuro Institute",
                "specialty": "Cardiac Sciences • Neurosciences • Kidney Care",
                "address": "Jawaharlal Nehru Marg, Malviya Nagar, Jaipur",
                "distance": "4.1 km away",
                "distance_km": 4.1,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.9,
                "reviews_count": "610",
                "phone": "+91 141 254 7000",
                "coords": [26.8612, 75.8115],
                "image": "images/facility_hospital1.jpg",
                "badges": ["NABH Accredited", "24/7 Stroke Unit", "Cardiac ICU"],
                "doctors": ["Dr. Alok Gupta, DM", "Dr. Ritu Kapoor, DNB"],
            },
            {
                "id": "fac-6",
                "name": "Dr. Mehta Family Wellness Clinic",
                "type": "clinic",
                "category_label": "Primary Care Clinic",
                "specialty": "Internal Medicine • Diabetes • Senior Health",
                "address": "C-Scheme, Ashok Nagar, Jaipur",
                "distance": "1.8 km away",
                "distance_km": 1.8,
                "hours": "Open till 8:00 PM",
                "is_24_7": False,
                "rating": 4.9,
                "reviews_count": "240",
                "phone": "+91 141 237 9100",
                "coords": [26.9080, 75.7950],
                "image": "images/facility_clinic1.jpg",
                "badges": ["Diabetes Care", "Vaccinations", "Health Checkups"],
                "doctors": ["Dr. Suresh Kulkarni, MD", "Dr. Sneha Iyer, DNB"],
            },
            {
                "id": "fac-7",
                "name": "Care Cliniq Derma & Skin Centre",
                "type": "clinic",
                "category_label": "Skin & Aesthetics Clinic",
                "specialty": "Dermatology • Trichology • Laser & Allergy",
                "address": "Lane 4, Raja Park, Jaipur",
                "distance": "2.7 km away",
                "distance_km": 2.7,
                "hours": "Open till 8:30 PM",
                "is_24_7": False,
                "rating": 4.8,
                "reviews_count": "195",
                "phone": "+91 141 262 1450",
                "coords": [26.8920, 75.8280],
                "image": "images/facility_clinic1.jpg",
                "badges": ["Skin Allergy", "Acne Laser", "Hair Restoration"],
                "doctors": ["Dr. Priya Nair, MD", "Dr. Rohan Verma, MD"],
            },
            {
                "id": "fac-8",
                "name": "Jaipur Heart & Chest Care Center",
                "type": "specialist",
                "category_label": "Specialist Doctors Clinic",
                "specialty": "Cardiology • Pulmonology • Asthma & Sleep Clinic",
                "address": "Queens Road, Vaishali Nagar, Jaipur",
                "distance": "4.5 km away",
                "distance_km": 4.5,
                "hours": "Open till 9:00 PM",
                "is_24_7": False,
                "rating": 4.9,
                "reviews_count": "310",
                "phone": "+91 141 235 6200",
                "coords": [26.9050, 75.7480],
                "image": "images/facility_clinic1.jpg",
                "badges": ["ECG & Echo", "Spirometry", "Sleep Apnea"],
                "doctors": ["Dr. Sanjay Bhatt, MD", "Dr. Vivek Mehra, MD"],
            },
            {
                "id": "fac-9",
                "name": "Metropolis Diagnostic & Imaging",
                "type": "diagnostic",
                "category_label": "Advanced Diagnostic Center",
                "specialty": "MRI • CT Scan • Digital X-Ray • Pathology",
                "address": "Opposite GPO, MI Road, Jaipur",
                "distance": "1.5 km away",
                "distance_km": 1.5,
                "hours": "Open till 9:00 PM",
                "is_24_7": False,
                "rating": 4.8,
                "reviews_count": "420",
                "phone": "+91 141 400 5500",
                "coords": [26.9190, 75.8080],
                "image": "images/facility_clinic1.jpg",
                "badges": ["3T MRI", "NABL Lab", "Same Day Reports"],
                "doctors": ["Dr. Harish Chandra, MS"],
            },
            {
                "id": "fac-10",
                "name": "Dr. Lal PathLabs Excellence Center",
                "type": "diagnostic",
                "category_label": "Pathology & Blood Diagnostics",
                "specialty": "Comprehensive Blood Panels • Thyroid • Hormones",
                "address": "Near University, JLN Marg, Jaipur",
                "distance": "3.0 km away",
                "distance_km": 3.0,
                "hours": "Open till 8:00 PM",
                "is_24_7": False,
                "rating": 4.7,
                "reviews_count": "280",
                "phone": "+91 141 270 9900",
                "coords": [26.8780, 75.8160],
                "image": "images/facility_clinic1.jpg",
                "badges": ["Home Sample Collection", "Automated Testing", "Online Reports"],
                "doctors": ["Dr. Sunita Agarwal, MD"],
            },
            {
                "id": "fac-11",
                "name": "Apollo 24/7 Super Pharmacy",
                "type": "pharmacy",
                "category_label": "24/7 Retail Pharmacy",
                "specialty": "Prescription Refills • Cold-chain Vaccines • Surgical",
                "address": "Near Gandhi Nagar Station, Tonk Road, Jaipur",
                "distance": "2.4 km away",
                "distance_km": 2.4,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.8,
                "reviews_count": "510",
                "phone": "+91 141 271 3344",
                "coords": [26.8720, 75.8010],
                "image": "images/facility_hospital1.jpg",
                "badges": ["24/7 Open", "Home Delivery", "Verified Meds"],
                "doctors": [],
            },
            {
                "id": "fac-12",
                "name": "MedPlus 24x7 Healthcare Pharmacy",
                "type": "pharmacy",
                "category_label": "Healthcare & Drugstore",
                "specialty": "Discount Generic Drugs • Wellness Products • Diagnostics",
                "address": "Calgiri Road, Malviya Nagar, Jaipur",
                "distance": "3.8 km away",
                "distance_km": 3.8,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.7,
                "reviews_count": "330",
                "phone": "+91 141 275 8899",
                "coords": [26.8500, 75.8190],
                "image": "images/facility_clinic1.jpg",
                "badges": ["Prescription Dispensing", "Medical Supplies", "Vaccine Storage"],
                "doctors": [],
            },
        ]

    if city_clean in ("delhi", "new delhi", "ncr"):
        return [
            {
                "id": "del-1",
                "name": "AIIMS New Delhi (Apex Trauma Centre)",
                "type": "hospital",
                "category_label": "Premier Tertiary Institute",
                "specialty": "Trauma & Emergency • Cardiology • Neurology • Oncology",
                "address": "Sri Aurobindo Marg, Ansari Nagar, New Delhi",
                "distance": "1.5 km away",
                "distance_km": 1.5,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.9,
                "reviews_count": "1,420",
                "phone": "+91 11 2658 8500",
                "coords": [28.5672, 77.2100],
                "image": "images/facility_hospital1.jpg",
                "badges": ["24/7 Emergency", "ICU & Trauma", "Organ Transplant"],
                "doctors": ["Dr. Rajesh Sharma, MD", "Dr. Alok Sharma, DM"],
            },
            {
                "id": "del-2",
                "name": "Max Super Speciality Hospital, Saket",
                "type": "hospital",
                "category_label": "Quaternary Care Hospital",
                "specialty": "Cardiology • Orthopedics • Critical Care • Oncology",
                "address": "1, 2, Press Enclave Marg, Saket, New Delhi",
                "distance": "3.8 km away",
                "distance_km": 3.8,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.8,
                "reviews_count": "980",
                "phone": "+91 11 2651 5050",
                "coords": [28.5284, 77.2126],
                "image": "images/facility_hospital1.jpg",
                "badges": ["Cardiac ICU", "JCI Accredited", "24/7 Stroke Unit"],
                "doctors": ["Dr. Sanjay Bhatt, MD", "Dr. Vikram Malhotra, MS"],
            },
            {
                "id": "del-3",
                "name": "Fortis Escorts Heart Institute",
                "type": "hospital",
                "category_label": "Apex Cardiology Hospital",
                "specialty": "Cardiology • Cardiac Surgery • Pediatric Heart Care",
                "address": "Okhla Road, New Friends Colony, New Delhi",
                "distance": "4.2 km away",
                "distance_km": 4.2,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.9,
                "reviews_count": "890",
                "phone": "+91 11 4713 5000",
                "coords": [28.5603, 77.2728],
                "image": "images/facility_hospital1.jpg",
                "badges": ["Cath Lab", "Pediatric Heart", "Heart Transplant"],
                "doctors": ["Dr. Alok Gupta, DM", "Dr. Ritu Kapoor, DNB"],
            },
            {
                "id": "del-4",
                "name": "Indraprastha Apollo Hospital",
                "type": "hospital",
                "category_label": "Multispeciality Hospital",
                "specialty": "Nephrology • Liver Transplant • Robotic Surgery",
                "address": "Sarita Vihar, Delhi Mathura Road, New Delhi",
                "distance": "5.6 km away",
                "distance_km": 5.6,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.8,
                "reviews_count": "1,100",
                "phone": "+91 11 2692 5858",
                "coords": [28.5376, 77.2882],
                "image": "images/facility_hospital1.jpg",
                "badges": ["Liver Transplant", "Robotic ICU", "Emergency 24/7"],
                "doctors": ["Dr. Suresh Kulkarni, MD"],
            },
            {
                "id": "del-5",
                "name": "Medanta Mediclinic South Delhi",
                "type": "clinic",
                "category_label": "Premium Consultation Clinic",
                "specialty": "Internal Medicine • Endocrinology • Preventive Health",
                "address": "E-18, Defence Colony, New Delhi",
                "distance": "2.2 km away",
                "distance_km": 2.2,
                "hours": "Open till 8:30 PM",
                "is_24_7": False,
                "rating": 4.9,
                "reviews_count": "340",
                "phone": "+91 11 4411 4411",
                "coords": [28.5714, 77.2345],
                "image": "images/facility_clinic1.jpg",
                "badges": ["Executive Checkup", "Diabetes Center", "Senior Health"],
                "doctors": ["Dr. Ananya Mehta, MD", "Dr. Priya Nair, MD"],
            },
            {
                "id": "del-6",
                "name": "Dr. Lal PathLabs National Reference Lab",
                "type": "diagnostic",
                "category_label": "Advanced Diagnostics Center",
                "specialty": "NABL Accredited Blood Panels • Genomic • Pathology",
                "address": "Block E, Sector 18, Rohini, New Delhi",
                "distance": "6.1 km away",
                "distance_km": 6.1,
                "hours": "Open till 9:00 PM",
                "is_24_7": False,
                "rating": 4.8,
                "reviews_count": "520",
                "phone": "+91 11 3988 5050",
                "coords": [28.7180, 77.1260],
                "image": "images/facility_clinic1.jpg",
                "badges": ["NABL Accredited", "Home Sample Pickup", "Express Reports"],
                "doctors": ["Dr. Sunita Agarwal, MD"],
            },
            {
                "id": "del-7",
                "name": "Apollo 24/7 Pharmacy Connaught Place",
                "type": "pharmacy",
                "category_label": "24/7 Super Pharmacy",
                "specialty": "Prescription Refills • Cold Chain Vaccines • Critical Meds",
                "address": "Inner Circle, Connaught Place, New Delhi",
                "distance": "1.1 km away",
                "distance_km": 1.1,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.8,
                "reviews_count": "640",
                "phone": "+91 11 2332 4500",
                "coords": [28.6328, 77.2197],
                "image": "images/facility_hospital1.jpg",
                "badges": ["24/7 Open", "Home Delivery", "Verified Meds"],
                "doctors": [],
            },
            {
                "id": "del-8",
                "name": "Delhi Heart & Pulmonary Speciality Clinic",
                "type": "specialist",
                "category_label": "Chest & Cardiac Clinic",
                "specialty": "Pulmonology • Asthma & Allergy • Sleep Lab",
                "address": "A-Block, Green Park Main, New Delhi",
                "distance": "2.9 km away",
                "distance_km": 2.9,
                "hours": "Open till 9:00 PM",
                "is_24_7": False,
                "rating": 4.9,
                "reviews_count": "290",
                "phone": "+91 11 2686 4200",
                "coords": [28.5580, 77.2060],
                "image": "images/facility_clinic1.jpg",
                "badges": ["PFT & Spirometry", "Sleep Apnea", "Allergy Tests"],
                "doctors": ["Dr. Vivek Mehra, MD"],
            },
        ]

    if city_clean in ("mumbai", "bombay"):
        return [
            {
                "id": "mum-1",
                "name": "Lilavati Hospital & Research Centre",
                "type": "hospital",
                "category_label": "Apex Multispecialty Hospital",
                "specialty": "Cardiology • Neurosciences • Critical Care",
                "address": "A-791, Bandra Reclamation, Bandra West, Mumbai",
                "distance": "1.4 km away",
                "distance_km": 1.4,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.8,
                "reviews_count": "1,250",
                "phone": "+91 22 2675 1000",
                "coords": [19.0512, 72.8290],
                "image": "images/facility_hospital1.jpg",
                "badges": ["24/7 Emergency", "ICU", "NABH Accredited"],
                "doctors": ["Dr. Rajesh Sharma, MD", "Dr. Alok Sharma, DM"],
            },
            {
                "id": "mum-2",
                "name": "Kokilaben Dhirubhai Ambani Hospital",
                "type": "hospital",
                "category_label": "Quaternary Care Hospital",
                "specialty": "Robotic Surgery • Oncology • Pediatric Surgery",
                "address": "Rao Saheb Achutrao Patwardhan Marg, Andheri West, Mumbai",
                "distance": "4.2 km away",
                "distance_km": 4.2,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.9,
                "reviews_count": "1,600",
                "phone": "+91 22 4269 6969",
                "coords": [19.1311, 72.8252],
                "image": "images/facility_hospital1.jpg",
                "badges": ["Robotic Care", "Children Hospital", "Cath Lab"],
                "doctors": ["Dr. Sanjay Bhatt, MD", "Dr. Vikram Malhotra, MS"],
            },
            {
                "id": "mum-3",
                "name": "P. D. Hinduja Hospital & Medical Research",
                "type": "hospital",
                "category_label": "Multispeciality Hospital",
                "specialty": "Internal Medicine • Pulmonology • Nephrology",
                "address": "Veer Savarkar Marg, Mahim, Mumbai",
                "distance": "3.1 km away",
                "distance_km": 3.1,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.8,
                "reviews_count": "940",
                "phone": "+91 22 2445 1515",
                "coords": [19.0330, 72.8397],
                "image": "images/facility_hospital1.jpg",
                "badges": ["Stroke Center", "Dialysis Unit", "Emergency Care"],
                "doctors": ["Dr. Suresh Kulkarni, MD"],
            },
            {
                "id": "mum-4",
                "name": "Metropolis Healthcare Reference Laboratory",
                "type": "diagnostic",
                "category_label": "Central Pathology Diagnostics",
                "specialty": "Molecular Pathology • Genetics • Full Body Profiles",
                "address": "Commercial Hub, Worli, Mumbai",
                "distance": "2.8 km away",
                "distance_km": 2.8,
                "hours": "Open till 8:30 PM",
                "is_24_7": False,
                "rating": 4.8,
                "reviews_count": "410",
                "phone": "+91 22 6668 5555",
                "coords": [19.0150, 72.8180],
                "image": "images/facility_clinic1.jpg",
                "badges": ["NABL / CAP", "Home Sample Collection", "Smart Reports"],
                "doctors": ["Dr. Sunita Agarwal, MD"],
            },
            {
                "id": "mum-5",
                "name": "Wellness Forever 24/7 Pharmacy Bandra",
                "type": "pharmacy",
                "category_label": "24/7 Super Chemist",
                "specialty": "Imported Medicines • Surgical Equipment • Emergency Drugs",
                "address": "Linking Road, Bandra West, Mumbai",
                "distance": "1.2 km away",
                "distance_km": 1.2,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.8,
                "reviews_count": "580",
                "phone": "+91 22 2640 1200",
                "coords": [19.0590, 72.8340],
                "image": "images/facility_hospital1.jpg",
                "badges": ["24/7 Open", "Home Delivery", "Verified Meds"],
                "doctors": [],
            },
        ]

    if city_clean in ("chandigarh", "punjab", "mohali"):
        return [
            {
                "id": "chd-1",
                "name": "PGIMER Apex Hospital & Research Institute",
                "type": "hospital",
                "category_label": "Premier Teaching & Trauma Hospital",
                "specialty": "Multispecialty • Trauma & Critical Care • Organ Transplant • Cardiology",
                "address": "Sector 12, Madhya Marg, Chandigarh, Punjab",
                "distance": "1.4 km away",
                "distance_km": 1.4,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.9,
                "reviews_count": "1,850",
                "phone": "+91 172 274 7585",
                "coords": [30.7656, 76.7745],
                "image": "images/facility_hospital1.jpg",
                "badges": ["24/7 Emergency", "ICU & Trauma", "Apex Research Institute"],
                "doctors": ["Dr. Rajesh Sharma, MD", "Dr. Alok Sharma, DM"],
            },
            {
                "id": "chd-2",
                "name": "Max Super Speciality Hospital, Mohali",
                "type": "hospital",
                "category_label": "Quaternary Care Hospital",
                "specialty": "Cardiology • Oncology • Neurosciences • Orthopedics",
                "address": "Near Civil Hospital, Phase 6, Mohali, Punjab",
                "distance": "3.8 km away",
                "distance_km": 3.8,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.8,
                "reviews_count": "920",
                "phone": "+91 172 521 2000",
                "coords": [30.7228, 76.7118],
                "image": "images/facility_hospital1.jpg",
                "badges": ["Cardiac ICU", "NABH Accredited", "Cancer Care"],
                "doctors": ["Dr. Sanjay Bhatt, MD", "Dr. Vikram Malhotra, MS"],
            },
            {
                "id": "chd-3",
                "name": "Fortis Hospital Mohali",
                "type": "hospital",
                "category_label": "Multispeciality Hospital",
                "specialty": "Cardiac Sciences • Joint Replacement • Emergency Medicine",
                "address": "Sector 62, Phase 8, SAS Nagar, Mohali, Punjab",
                "distance": "4.5 km away",
                "distance_km": 4.5,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.8,
                "reviews_count": "1,120",
                "phone": "+91 172 469 2222",
                "coords": [30.6975, 76.7265],
                "image": "images/facility_hospital1.jpg",
                "badges": ["Cath Lab", "24/7 Stroke Unit", "Emergency 24/7"],
                "doctors": ["Dr. Alok Gupta, DM", "Dr. Ritu Kapoor, DNB"],
            },
            {
                "id": "chd-4",
                "name": "Mukat Hospital & Heart Institute",
                "type": "hospital",
                "category_label": "Heart & Critical Care Hospital",
                "specialty": "Interventional Cardiology • Heart Surgery • Critical Care",
                "address": "SCO 47-49, Sector 34-A, Chandigarh, Punjab",
                "distance": "2.1 km away",
                "distance_km": 2.1,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.7,
                "reviews_count": "430",
                "phone": "+91 172 434 4444",
                "coords": [30.7214, 76.7681],
                "image": "images/facility_hospital1.jpg",
                "badges": ["24/7 Cardiac Unit", "Emergency Care", "ICU"],
                "doctors": ["Dr. Vivek Mehra, MD"],
            },
            {
                "id": "chd-5",
                "name": "Apollo Clinic & Diagnostics Sector 8",
                "type": "clinic",
                "category_label": "Premium Consultation Clinic",
                "specialty": "Internal Medicine • Pediatrics • Lab Services • Diabetes",
                "address": "SCO 147-148, Madhya Marg, Sector 8-C, Chandigarh, Punjab",
                "distance": "1.8 km away",
                "distance_km": 1.8,
                "hours": "Open till 8:30 PM",
                "is_24_7": False,
                "rating": 4.9,
                "reviews_count": "310",
                "phone": "+91 172 278 1234",
                "coords": [30.7410, 76.7970],
                "image": "images/facility_clinic1.jpg",
                "badges": ["Executive Health", "Pediatrics", "Diabetes Care"],
                "doctors": ["Dr. Ananya Mehta, MD", "Dr. Pooja Singhal, MD"],
            },
            {
                "id": "chd-6",
                "name": "Dr. Lal PathLabs Regional Reference Lab",
                "type": "diagnostic",
                "category_label": "NABL Diagnostics Center",
                "specialty": "Pathology • MRI & CT • Full Body Blood Panels",
                "address": "SCO 80-81, Sector 35-B, Chandigarh, Punjab",
                "distance": "2.9 km away",
                "distance_km": 2.9,
                "hours": "Open till 9:00 PM",
                "is_24_7": False,
                "rating": 4.8,
                "reviews_count": "480",
                "phone": "+91 172 398 8505",
                "coords": [30.7230, 76.7570],
                "image": "images/facility_clinic1.jpg",
                "badges": ["NABL Accredited", "Home Collection", "Digital Reports"],
                "doctors": ["Dr. Sunita Agarwal, MD"],
            },
            {
                "id": "chd-7",
                "name": "Apollo 24/7 Pharmacy Sector 22",
                "type": "pharmacy",
                "category_label": "24/7 Super Pharmacy",
                "specialty": "Emergency Medications • Cold-Chain Vaccines • Refills",
                "address": "SCO 2411, Sector 22-C, Chandigarh, Punjab",
                "distance": "1.2 km away",
                "distance_km": 1.2,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.8,
                "reviews_count": "590",
                "phone": "+91 172 270 9988",
                "coords": [30.7320, 76.7720],
                "image": "images/facility_hospital1.jpg",
                "badges": ["24/7 Open", "Home Delivery", "Verified Meds"],
                "doctors": [],
            },
            {
                "id": "chd-8",
                "name": "Chandigarh Chest & Pulmonary Specialty Clinic",
                "type": "specialist",
                "category_label": "Pulmonology & Asthma Center",
                "specialty": "Pulmonology • Asthma & Allergy • Sleep Apnea • Critical Lung Care",
                "address": "SCO 112-113, Sector 17-C, Chandigarh, Punjab",
                "distance": "1.6 km away",
                "distance_km": 1.6,
                "hours": "Open till 8:00 PM",
                "is_24_7": False,
                "rating": 4.9,
                "reviews_count": "275",
                "phone": "+91 172 270 4123",
                "coords": [30.7412, 76.7820],
                "image": "images/facility_clinic1.jpg",
                "badges": ["Asthma Clinic", "Sleep Study", "Chest Specialists"],
                "doctors": ["Dr. Suresh Kulkarni, MD", "Dr. Priya Nair, MD"],
            },
        ]
    # Dynamic Pan-India Facilities Generator for any village, town, or city
    from app.services.india_geo import haversine_distance

    disp_title = (location_display or title_city)
    if "," in disp_title:
        disp_title = disp_title.split(",")[0].strip()

    std_code = "141"
    if lat > 28:
        std_code = "124"
    elif lat > 25:
        std_code = "522"
    elif lat > 20:
        std_code = "755"
    else:
        std_code = "80"

    return [
            {
                "id": "fac-dyn-1",
                "name": f"{disp_title} Civil Hospital & Trauma Centre",
                "type": "hospital",
                "category_label": "Government District Hospital",
                "specialty": "24/7 Emergency • ICU • Trauma & Critical Care",
                "address": f"Hospital Road, Civil Lines, {disp_title}, {state_name}",
                "distance": "0.9 km away",
                "distance_km": 0.9,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.8,
                "reviews_count": "480",
                "phone": f"+91 {std_code} 234 5001",
                "coords": [round(lat + 0.0042, 5), round(lon + 0.0035, 5)],
                "image": "images/facility_hospital1.jpg",
                "badges": ["24/7 Emergency", "ICU & Trauma", "Ayushman Bharat", "Ambulance"],
                "doctors": ["Dr. Rajesh Sharma, MD", "Dr. Anita Desai, MS"],
            },
            {
                "id": "fac-dyn-2",
                "name": f"{disp_title} Community Health Centre (CHC)",
                "type": "hospital",
                "category_label": "Community Hospital",
                "specialty": "General Medicine • Maternal Care • Emergency Response",
                "address": f"Near Main Bus Stand, Station Road, {disp_title}",
                "distance": "1.4 km away",
                "distance_km": 1.4,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.7,
                "reviews_count": "310",
                "phone": f"+91 {std_code} 234 5002",
                "coords": [round(lat - 0.0051, 5), round(lon + 0.0062, 5)],
                "image": "images/facility_hospital1.jpg",
                "badges": ["24/7 Emergency", "Maternity Unit", "Free Medicines"],
                "doctors": ["Dr. Sanjay Verma, MBBS", "Dr. Sunita Sharma, DGO"],
            },
            {
                "id": "fac-dyn-3",
                "name": f"{disp_title} Apex Multispecialty Hospital",
                "type": "hospital",
                "category_label": "Super Specialty Hospital",
                "specialty": "Cardiology • Orthopedics • Neurology • Intensive Care",
                "address": f"Bypass Road, Medical Enclave, {disp_title}",
                "distance": "2.2 km away",
                "distance_km": 2.2,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.9,
                "reviews_count": "540",
                "phone": f"+91 {std_code} 234 5003",
                "coords": [round(lat + 0.0085, 5), round(lon - 0.0071, 5)],
                "image": "images/facility_hospital1.jpg",
                "badges": ["Cath Lab", "Advanced ICU", "Cashless Insurance", "NABH Accredited"],
                "doctors": ["Dr. Alok Sharma, DM", "Dr. Vikram Malhotra, MS"],
            },
            {
                "id": "fac-dyn-4",
                "name": f"{disp_title} Primary Health Centre (PHC)",
                "type": "clinic",
                "category_label": "Primary Care Clinic",
                "specialty": "Family Health • Immunization • Child & Maternal Care",
                "address": f"Panchayat Circle, Main Bazar, {disp_title}",
                "distance": "1.1 km away",
                "distance_km": 1.1,
                "hours": "Open till 8:00 PM",
                "is_24_7": False,
                "rating": 4.6,
                "reviews_count": "195",
                "phone": f"+91 {std_code} 234 5004",
                "coords": [round(lat - 0.0038, 5), round(lon - 0.0049, 5)],
                "image": "images/facility_clinic1.jpg",
                "badges": ["Routine Checkups", "Child Vaccines", "OPD Care"],
                "doctors": ["Dr. Neha Agarwal, MBBS", "Dr. Manoj Joshi, MD"],
            },
            {
                "id": "fac-dyn-5",
                "name": f"Sanjivani Family Care & Child Clinic",
                "type": "clinic",
                "category_label": "Consultation Clinic",
                "specialty": "Pediatrics • Diabetes Care • Blood Pressure Management",
                "address": f"Shop 4, Gandhi Chowk, Market Road, {disp_title}",
                "distance": "1.9 km away",
                "distance_km": 1.9,
                "hours": "Open till 9:00 PM",
                "is_24_7": False,
                "rating": 4.9,
                "reviews_count": "260",
                "phone": f"+91 {std_code} 234 5005",
                "coords": [round(lat + 0.0062, 5), round(lon + 0.0084, 5)],
                "image": "images/facility_clinic1.jpg",
                "badges": ["Pediatrician", "ECG On-site", "Online Appointments"],
                "doctors": ["Dr. Ananya Mehta, MD", "Dr. Pooja Singhal, MD"],
            },
            {
                "id": "fac-dyn-6",
                "name": f"{disp_title} Apollo 24/7 Pharmacy",
                "type": "pharmacy",
                "category_label": "24/7 Pharmacy",
                "specialty": "Prescription Refills • Vaccines • Health Essentials",
                "address": f"Railway Road, Near State Bank, {disp_title}",
                "distance": "1.2 km away",
                "distance_km": 1.2,
                "hours": "Open 24/7",
                "is_24_7": True,
                "rating": 4.8,
                "reviews_count": "380",
                "phone": f"+91 {std_code} 234 5006",
                "coords": [round(lat - 0.0025, 5), round(lon + 0.0039, 5)],
                "image": "images/facility_hospital1.jpg",
                "badges": ["24/7 Open", "Home Delivery", "Verified Salts"],
                "doctors": [],
            },
            {
                "id": "fac-dyn-7",
                "name": f"MedPlus Pharmacy & Wellness Centre",
                "type": "pharmacy",
                "category_label": "Retail Pharmacy",
                "specialty": "Prescription Refills • Baby Care • Health Monitors",
                "address": f"Main Market, Opposite Clock Tower, {disp_title}",
                "distance": "1.6 km away",
                "distance_km": 1.6,
                "hours": "Open till 11:00 PM",
                "is_24_7": False,
                "rating": 4.7,
                "reviews_count": "220",
                "phone": f"+91 {std_code} 234 5007",
                "coords": [round(lat + 0.0051, 5), round(lon - 0.0032, 5)],
                "image": "images/facility_hospital1.jpg",
                "badges": ["Discounted Medicines", "Surgical Supplies"],
                "doctors": [],
            },
            {
                "id": "fac-dyn-8",
                "name": f"{disp_title} Diagnostic Imaging & Pathology Centre",
                "type": "diagnostic",
                "category_label": "Diagnostic Center",
                "specialty": "Digital X-Ray • Ultrasound • Full Body Blood Tests • Pathology",
                "address": f"Commercial Complex, 1st Floor, Court Road, {disp_title}",
                "distance": "2.0 km away",
                "distance_km": 2.0,
                "hours": "Open till 8:30 PM",
                "is_24_7": False,
                "rating": 4.8,
                "reviews_count": "310",
                "phone": f"+91 {std_code} 234 5008",
                "coords": [round(lat - 0.0071, 5), round(lon - 0.0068, 5)],
                "image": "images/facility_clinic1.jpg",
                "badges": ["NABL Accredited", "Home Sample Collection", "Same Day Reports"],
                "doctors": [],
            },
            {
                "id": "fac-dyn-9",
                "name": f"LifeLine Heart & Chest Specialist Clinic",
                "type": "specialist",
                "category_label": "Specialist Doctors Clinic",
                "specialty": "Cardiology • Respiratory Care • Hypertension Clinic",
                "address": f"Apex Towers, 2nd Floor, Civil Lines, {disp_title}",
                "distance": "2.7 km away",
                "distance_km": 2.7,
                "hours": "Open till 8:00 PM",
                "is_24_7": False,
                "rating": 4.9,
                "reviews_count": "180",
                "phone": f"+91 {std_code} 234 5009",
                "coords": [round(lat + 0.0091, 5), round(lon + 0.0055, 5)],
                "image": "images/facility_clinic1.jpg",
                "badges": ["Cardiologist", "Pulmonologist", "Echocardiography"],
                "doctors": ["Dr. Suresh Kulkarni, DM", "Dr. Vivek Mehra, MD"],
            },
            {
                "id": "fac-dyn-10",
                "name": f"{disp_title} Dental Care & Maxillofacial Centre",
                "type": "specialist",
                "category_label": "Specialist Clinic",
                "specialty": "Dental Implants • Root Canal • Orthodontics • Oral Surgery",
                "address": f"Shop 12, Main Road, Near Old Bus Stand, {disp_title}",
                "distance": "1.3 km away",
                "distance_km": 1.3,
                "hours": "Open till 9:00 PM",
                "is_24_7": False,
                "rating": 4.9,
                "reviews_count": "240",
                "phone": f"+91 {std_code} 234 5010",
                "coords": [round(lat - 0.0044, 5), round(lon + 0.0028, 5)],
                "image": "images/facility_clinic1.jpg",
                "badges": ["Dental Surgeon", "Painless Root Canal", "Digital OPG"],
                "doctors": ["Dr. Amit Saxena, MDS", "Dr. Ritu Saxena, BDS"],
            }
        ]


def build_hospital_map(location_query="Jaipur", category_filter="all", search_query="", sort_by="relevance"):
    """
    Advanced Python GIS Map Builder for Care Cliniq Find Doctors & Healthcare Centers.
    Resolves any Indian village, town, city, or road via the Pan-India Geocoding system.
    Generates Folium Map with custom SVG DivIcons, rich HTML popups, interactive layers,
    and returns filtered facility data.
    """
    import folium
    from app.services.india_geo import resolve_indian_location

    loc = resolve_indian_location(location_query or "Jaipur")
    lat, lon = loc["lat"], loc["lon"]
    display_name = loc["display"]
    city_name = loc["name"]
    state_name = loc["state"]

    all_facilities = get_facility_dataset(city_name.lower(), lat, lon, state_name=state_name, location_display=display_name)

    # 1. Category Filtering
    filtered_facilities = []
    category_clean = (category_filter or "all").lower().strip()

    for fac in all_facilities:
        if category_clean == "all":
            category_match = True
        elif category_clean in ("hospital", "hospitals") and fac["type"] == "hospital":
            category_match = True
        elif category_clean in ("clinic", "clinics") and fac["type"] == "clinic":
            category_match = True
        elif category_clean in ("specialist", "doctor", "doctors") and fac["type"] in ("specialist", "clinic", "hospital") and fac.get("doctors"):
            category_match = True
        elif category_clean in ("diagnostic", "diagnostics") and fac["type"] == "diagnostic":
            category_match = True
        elif category_clean in ("pharmacy", "pharmacies") and fac["type"] == "pharmacy":
            category_match = True
        else:
            category_match = False

        if not category_match:
            continue

        # 2. Text Search Query Match
        if search_query:
            sq = search_query.lower()
            text_corpus = f"{fac['name']} {fac['specialty']} {fac['address']} {' '.join(fac.get('badges', []))} {' '.join(fac.get('doctors', []))}".lower()
            if sq not in text_corpus:
                continue

        filtered_facilities.append(fac)

    # If filters left no result, fallback to all so user always sees the map pins
    if not filtered_facilities:
        display_facilities = all_facilities
    else:
        display_facilities = filtered_facilities

    # Sorting
    if sort_by == "distance":
        display_facilities = sorted(display_facilities, key=lambda x: x.get("distance_km", 99))
    elif sort_by == "rating":
        display_facilities = sorted(display_facilities, key=lambda x: x.get("rating", 0), reverse=True)
    elif sort_by == "reviews":
        display_facilities = sorted(display_facilities, key=lambda x: int(str(x.get("reviews_count", "0")).replace(",", "")), reverse=True)

    # Build Folium Interactive Map centered on resolved coordinates
    hospital_map = folium.Map(
        location=[lat, lon],
        zoom_start=13,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    # Inject CSS into map to remove default leaflet-div-icon border/box
    map_css = """
    <style>
        .custom-map-pin {
            background: transparent !important;
            border: none !important;
        }
        .leaflet-popup-content-wrapper {
            border-radius: 12px !important;
            box-shadow: 0 8px 30px rgba(0,0,0,0.18) !important;
            padding: 2px !important;
        }
        .leaflet-popup-content {
            margin: 8px 10px !important;
        }
    </style>
    """
    hospital_map.get_root().html.add_child(folium.Element(map_css))

    # Category Marker Color & Icon Map
    marker_config = {
        "hospital": {
            "bg": "#E11D48",
            "icon": '<span style="font-size: 13px; font-weight: 800; font-family: Arial, sans-serif; line-height: 1;">H</span>',
            "name": "Hospital"
        },
        "clinic": {
            "bg": "#15803D",
            "icon": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
            "name": "Clinic"
        },
        "specialist": {
            "bg": "#15803D",
            "icon": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><circle cx="12" cy="7" r="4"/><path d="M6 21v-2a6 6 0 0 1 12 0v2"/></svg>',
            "name": "Specialist"
        },
        "diagnostic": {
            "bg": "#2563EB",
            "icon": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><path d="M10 2v7.31L4.62 19.3A2 2 0 0 0 6.38 22h11.24a2 2 0 0 0 1.76-2.7L14 9.31V2"/><path d="M8.5 2h7"/></svg>',
            "name": "Diagnostic"
        },
        "pharmacy": {
            "bg": "#9333EA",
            "icon": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5"><path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/></svg>',
            "name": "Pharmacy"
        },
    }

    # Add facility markers with Custom DivIcon and Rich Popups
    for fac in display_facilities:
        cfg = marker_config.get(fac["type"], {
            "bg": "#135234",
            "icon": '<span style="font-weight: 800;">+</span>',
            "name": "Medical Center"
        })
        encoded_name = urllib.parse.quote(fac["name"])
        google_maps_url = f"https://www.google.com/maps/search/?api=1&query={fac['coords'][0]},{fac['coords'][1]}"
        status_color = "#16A34A" if fac.get("is_24_7") else "#EA580C"
        status_bg = "#ECFDF5" if fac.get("is_24_7") else "#FFF7ED"

        # Beautiful Custom HTML Popup
        popup_html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; width: 255px; padding: 2px;">
            <div style="position: relative; border-radius: 8px; overflow: hidden; height: 85px; margin-bottom: 8px;">
                <img src="/static/{fac['image']}" alt="{fac['name']}" style="width: 100%; height: 100%; object-fit: cover;">
                <span style="position: absolute; top: 6px; right: 6px; background: {status_bg}; color: {status_color}; font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 6px; border: 1px solid currentColor;">
                    ● {fac['hours']}
                </span>
            </div>
            <div style="font-size: 13.5px; font-weight: 700; color: #151D22; line-height: 1.3; margin-bottom: 2px;">
                {fac['name']} <span style="color: #16A34A; font-size: 12px;" title="Verified Provider">✓</span>
            </div>
            <div style="font-size: 11px; color: #135234; font-weight: 600; margin-bottom: 4px;">{fac.get('category_label', cfg['name'])}</div>
            <div style="font-size: 11px; color: #64748B; margin-bottom: 8px; line-height: 1.3;">{fac['address']}</div>
            <div style="display: flex; align-items: center; justify-content: space-between; font-size: 11px; margin-bottom: 10px; padding: 4px 6px; background: #F8FAF9; border-radius: 6px;">
                <span style="color: #D97706; font-weight: 700;">★ {fac['rating']} ({fac['reviews_count']})</span>
                <span style="color: #475569; font-weight: 600;">📍 {fac['distance']}</span>
            </div>
            <div style="display: flex; gap: 6px;">
                <a href="/appointment?doctor={encoded_name}" target="_parent" style="flex: 1.2; text-align: center; background: #135234; color: #FFFFFF; padding: 7px 8px; border-radius: 6px; text-decoration: none; font-size: 11px; font-weight: 700; display: inline-block;">Book Visit</a>
                <a href="{google_maps_url}" target="_blank" rel="noopener noreferrer" style="flex: 1; text-align: center; background: #FFFFFF; color: #334155; border: 1px solid #CBD5E1; padding: 6px 8px; border-radius: 6px; text-decoration: none; font-size: 11px; font-weight: 600; display: inline-block;">Directions</a>
            </div>
        </div>
        """

        # Custom DivIcon (Pin)
        div_html = f"""
        <div style="background-color: {cfg['bg']}; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; box-shadow: 0 3px 12px rgba(0,0,0,0.35); border: 2.5px solid #FFFFFF; cursor: pointer; transition: transform 0.15s ease;">
            {cfg['icon']}
        </div>
        """
        custom_icon = folium.DivIcon(html=div_html, icon_size=(32, 32), icon_anchor=(16, 16), class_name="custom-map-pin")

        folium.Marker(
            location=fac["coords"],
            popup=folium.Popup(popup_html, max_width=290),
            tooltip=f"{fac['name']} ({fac['specialty']})",
            icon=custom_icon,
        ).add_to(hospital_map)

    # Map Legend Overlay (Top Right so it never overlaps Leaflet controls or attribution)
    legend_html = """
    <div style="position: absolute; top: 12px; right: 12px; z-index: 999; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(8px); padding: 6px 14px; border-radius: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.12); display: flex; align-items: center; gap: 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11.5px; font-weight: 600; border: 1px solid #E2E8F0; white-space: nowrap;">
        <div style="display: flex; align-items: center; gap: 5px;"><span style="width: 15px; height: 15px; border-radius: 50%; background: #E11D48; color: white; display: flex; align-items: center; justify-content: center; font-size: 9.5px; font-weight: 800; font-family: Arial, sans-serif;">H</span> Hospital</div>
        <div style="display: flex; align-items: center; gap: 5px;"><span style="width: 15px; height: 15px; border-radius: 50%; background: #15803D; color: white; display: flex; align-items: center; justify-content: center;"><svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><circle cx="12" cy="7" r="4"/><path d="M6 21v-2a6 6 0 0 1 12 0v2"/></svg></span> Clinic</div>
        <div style="display: flex; align-items: center; gap: 5px;"><span style="width: 15px; height: 15px; border-radius: 50%; background: #2563EB; color: white; display: flex; align-items: center; justify-content: center;"><svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M10 2v7.31L4.62 19.3A2 2 0 0 0 6.38 22h11.24a2 2 0 0 0 1.76-2.7L14 9.31V2"/><path d="M8.5 2h7"/></svg></span> Diagnostic</div>
        <div style="display: flex; align-items: center; gap: 5px;"><span style="width: 15px; height: 15px; border-radius: 50%; background: #9333EA; color: white; display: flex; align-items: center; justify-content: center;"><svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/></svg></span> Pharmacy</div>
    </div>
    """
    hospital_map.get_root().html.add_child(folium.Element(legend_html))

    return {
        "map_html": hospital_map._repr_html_(),
        "hospitals": display_facilities,
        "total_count": len(all_facilities),
        "filtered_count": len(display_facilities),
        "center_coords": [lat, lon],
        "resolved_location": display_name,
        "city_name": city_name,
        "state_name": state_name,
    }
