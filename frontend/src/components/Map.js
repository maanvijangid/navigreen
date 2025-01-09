import React from 'react';
import { MapContainer, TileLayer, Polyline } from 'react-leaflet';

function Map({ routes }) {
    return (
        <MapContainer center={[12.9716, 77.5946]} zoom={10} style={{ height: "400px", width: "100%" }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {routes.map((route, idx) => (
                <Polyline key={idx} positions={route.geometry} color={idx === 0 ? 'blue' : 'green'} />
            ))}
        </MapContainer>
    );
}

export default Map;
