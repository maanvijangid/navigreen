import React, { useState } from 'react';

function Form({ onSubmit }) {
    const [origin, setOrigin] = useState("");
    const [destination, setDestination] = useState("");
    const [fuelEfficiency, setFuelEfficiency] = useState("");
    const [vehicleType, setVehicleType] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ origin, destination, fuel_efficiency: fuelEfficiency, vehicle_type: vehicleType });
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" placeholder="Origin (lat,lon)" value={origin} onChange={(e) => setOrigin(e.target.value)} required />
            <input type="text" placeholder="Destination (lat,lon)" value={destination} onChange={(e) => setDestination(e.target.value)} required />
            <input type="number" placeholder="Fuel Efficiency (liters/km)" value={fuelEfficiency} onChange={(e) => setFuelEfficiency(e.target.value)} required />
            <input type="text" placeholder="Vehicle Type" value={vehicleType} onChange={(e) => setVehicleType(e.target.value)} required />
            <button type="submit">Optimize</button>
        </form>
    );
}

export default Form;
