def build_hospital_map(city):
    # Map packages are only needed on the hospital locator screen. Keeping
    # them lazy prevents Vercel's landing page function from cold-starting them.
    import folium
    from geopy.geocoders import Nominatim

    city_clean = city.strip().lower()
    known_cities = {
        "london": (51.5074, -0.1278),
        "mumbai": (19.0760, 72.8777),
        "delhi": (28.6139, 77.2090),
        "new york": (40.7128, -74.0060),
        "bengaluru": (12.9716, 77.5946),
        "bangalore": (12.9716, 77.5946),
        "paris": (48.8566, 2.3522),
        "chicago": (41.8781, -87.6298),
        "toronto": (43.6532, -79.3832),
        "tokyo": (35.6762, 139.6503),
    }

    if city_clean in known_cities:
        lat, lon = known_cities[city_clean]
    else:
        try:
            geolocator = Nominatim(user_agent="carecompass_hospital_finder_v2", timeout=3)
            location = geolocator.geocode(city)
            if not location:
                return None
            lat, lon = location.latitude, location.longitude
        except Exception:
            # Fallback to London coordinates if network is unreachable
            lat, lon = 51.5074, -0.1278
    hospital_map = folium.Map(location=[lat, lon], zoom_start=13, tiles="OpenStreetMap")

    hospitals = [
        {
            "name": f"{city.title()} Central Care",
            "type": "Multi-specialty",
            "distance": "1.2 km",
            "hours": "24/7 emergency",
            "coords": [lat, lon],
            "accent": "#0f766e",
        },
        {
            "name": f"{city.title()} Heart and Lung Institute",
            "type": "Specialty center",
            "distance": "2.4 km",
            "hours": "Open till 11 PM",
            "coords": [lat + 0.01, lon + 0.008],
            "accent": "#2563eb",
        },
        {
            "name": f"{city.title()} Community Health Hub",
            "type": "General hospital",
            "distance": "3.1 km",
            "hours": "Open till 9 PM",
            "coords": [lat - 0.012, lon - 0.01],
            "accent": "#f08c5a",
        },
    ]

    for hospital in hospitals:
        folium.Marker(
            hospital["coords"],
            popup=f"{hospital['name']} ({hospital['type']})",
            tooltip=hospital["name"],
        ).add_to(hospital_map)

    return {
        "map_html": hospital_map._repr_html_(),
        "hospitals": hospitals,
    }
