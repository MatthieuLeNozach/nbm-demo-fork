import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import React from "react";
import { Position } from "@/models/site";

type Props = {
  position: Position;
};

const Map: React.FC<Props> = ({ position }) => {
  const latLng = L.latLng(position.latitude, position.longitude);
  return (
    <MapContainer
      center={latLng}
      zoom={13}
      scrollWheelZoom={false}
      style={{ height: "300px", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={latLng}>
        <Popup>
          A pretty CSS3 popup. <br /> Easily customizable.
        </Popup>
      </Marker>
    </MapContainer>
  );
};

export default Map;
