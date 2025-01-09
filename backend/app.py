from flask import Flask, request, jsonify
from routing import get_routes_and_emissions
from database import init_db, save_request
import logging

app = Flask(__name__)

# Initialize database
init_db()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Home route
@app.route("/")
def home():
    return "Welcome to NAVIGREEN Backend!"

# Route to optimize route and calculate emissions
@app.route("/optimize-route", methods=["POST"])
def optimize_route():
    try:
        # Parse input data
        data = request.json
        origin = data.get("origin")
        destination = data.get("destination")
        fuel_efficiency = data.get("fuel_efficiency")
        vehicle_type = data.get("vehicle_type")

        # Check for missing required parameters
        if not all([origin, destination, fuel_efficiency, vehicle_type]):
            return jsonify({"error": "Missing required parameters"}), 400

        # Log the incoming request for debugging
        logging.info(f"Optimizing route from {origin} to {destination} with fuel efficiency {fuel_efficiency} for vehicle type {vehicle_type}")

        # Get optimized routes and emissions from the routing module
        response = get_routes_and_emissions(origin, destination, float(fuel_efficiency), vehicle_type)

        # Save the request in the database
        save_request(origin, destination, fuel_efficiency, vehicle_type, response)

        return jsonify(response), 200
    except Exception as e:
        # Log and return errors
        logging.error(f"Error processing route optimization: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Run the app only if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
