import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export default function RiskMap({ districts, onDistrictClick }) {
  // Simple GeoJSON placeholder for demonstration
  const geoJsonData = {
    type: "FeatureCollection",
    features: districts.map(d => ({
      type: "Feature",
      properties: { name: d.name, id: d.id },
      geometry: {
        type: "Point",
        coordinates: [d.lon, d.lat]
      }
    }))
  };

  return (
    <div className="h-96 w-full mt-6">
      <MapContainer center={[11.1271, 78.6569]} zoom={7} className="h-full">
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <GeoJSON
            data={geoJsonData}
            eventHandlers={{
                click: (e) => onDistrictClick(e.target.feature.properties.id)
            }}
        />
      </MapContainer>
    </div>
  );
}
