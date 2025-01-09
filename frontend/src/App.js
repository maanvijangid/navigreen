import React, { useState } from 'react';
import axios from 'axios';
import Map from './components/Map';
import Form from './components/Form';

function App() {
    const [routes, setRoutes] = useState([]);
    const [aqi, setAqi] = useState(null);

    const fetchRoutes = async (data) => {
        try {
            const response = await axios.post("http://127.0.0.1:5000/optimize-route", data);
            setRoutes(response.data.routes);
            setAqi(response.data.aqi);
        } catch (error) {
            console.error("Error fetching routes:", error);
        }
    };

    return (
        <div>
            <h1>Dynamic Route Optimization</h1>
            <Form onSubmit={fetchRoutes} />
            {aqi && <p>AQI at Origin: {aqi}</p>}
            <Map routes={routes} />
        </div>
    );
}

export default App;
