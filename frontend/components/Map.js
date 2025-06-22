'use client';

import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import { useEffect, useRef } from 'react'; 

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const Map = ({ geoJsonData, selectedItem }) => {
  const mapRef = useRef(null); 
  useEffect(() => {
    if (selectedItem && mapRef.current) {
      const { geometry } = selectedItem;
      const [longitude, latitude] = geometry.coordinates;
      
      mapRef.current.flyTo([latitude, longitude], 13);
    }
  }, [selectedItem]); 

  return (
    <MapContainer
      center={[20.5937, 78.9629]}
      zoom={5}
      style={{ height: '100%', width: '100%' }}
      whenCreated={map => mapRef.current = map} 
    >
      <TileLayer
        attribution='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/attributions">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
      />

      {geoJsonData.map((feature, index) => {
        const { geometry, properties } = feature;
        const [longitude, latitude] = geometry.coordinates;

        return (
          <Marker key={index} position={[latitude, longitude]}>
            <Popup>
              
              <div className="popup-title">{properties.place_name}</div>
              <div className="popup-info"><strong>City:</strong> {properties.city}</div>
              <div className="popup-info"><strong>Type:</strong> {properties.entity_type}</div>
            </Popup>
          </Marker>
);
      })}
    </MapContainer>
  );
};

export default Map;