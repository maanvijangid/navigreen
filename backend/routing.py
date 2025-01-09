import requests
import polyline
import logging

# API Keys (Replace with your own keys)
AQICN_API_KEY = "5b6d42c5719e741e60d107595ecc34ec74145f6a"
TOMTOM_API_KEY = "A0Y9n2qfdbNt0Nd3Fh64dRFUJZ5nxhjg"
OSRM_BASE_URL = "http://router.project-osrm.org/route/v1/driving"

CO2_PER_LITER = 2.31  # kg CO2 per liter of gasoline

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_weather_data(lat, lon):
    try:
        url = f"https://api.waqi.info/feed/geo:{lat};{lon}/"
        params = {"token": AQICN_API_KEY}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Will raise HTTPError for bad responses
        data = response.json()
        if data["status"] == "ok":
            return data["data"]["aqi"]
        else:
            logging.warning(f"Unable to fetch AQI for coordinates: {lat}, {lon}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        return None

def calculate_routes(origin, destination):
    url = f"{OSRM_BASE_URL}/{origin};{destination}"
    params = {"overview": "full", "alternatives": "true"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "routes" in data and len(data["routes"]) > 0:
            route = data["routes"][0]
            if route["distance"] > 0:
                return [
                    {
                        "geometry": polyline.decode(route["geometry"]),
                        "distance": route["distance"] / 1000,  # Convert to km
                        "duration": route["duration"] / 60  # Convert to minutes
                    }
                ]
    return None


def estimate_emissions(distance_km, fuel_efficiency):
    total_fuel_used = distance_km * fuel_efficiency
    emissions = total_fuel_used * CO2_PER_LITER
    return emissions

def get_routes_and_emissions(origin, destination, fuel_efficiency, vehicle_type):
    routes = calculate_routes(origin, destination)
    if not routes:
        raise Exception("Unable to fetch routes")

    # Get AQI at origin
    origin_coords = tuple(map(float, origin.split(",")))
    aqi = get_weather_data(*origin_coords) or "Unknown"

    # Estimate emissions for each route
    for route in routes:
        route["emissions"] = estimate_emissions(route["distance"], fuel_efficiency)

    return {"aqi": aqi, "routes": routes}

# Example usage
if __name__ == "__main__":
    origin = "28.7041,77.1025"  # Latitude, Longitude of origin
    destination = "19.0760,72.8777"  # Latitude, Longitude of destination
    fuel_efficiency = 15.0  # in km per liter (example)
    vehicle_type = "car"  # Not used in this code but might be used for future enhancements

    try:
        result = get_routes_and_emissions(origin, destination, fuel_efficiency, vehicle_type)
        print(result)
    except Exception as e:
        logging.error(f"Failed to get routes and emissions: {e}")
