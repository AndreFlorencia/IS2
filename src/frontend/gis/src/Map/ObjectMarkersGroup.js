import React, { useEffect, useState } from 'react';
import { LayerGroup, useMap } from 'react-leaflet';
import { ObjectMarker } from "./ObjectMarker";

function ObjectMarkersGroup() {
    const map = useMap();
    const [geom, setGeom] = useState([]);
    const [bounds, setBounds] = useState(map.getBounds());

    // Setup the event to update the bounds automatically
    useEffect(() => {
        const cb = () => {
            setBounds(map.getBounds());
        }
        map.on('moveend', cb);

        return () => {
            map.off('moveend', cb);
        }
    }, []);

    // Fetch data for the current bounds
    useEffect(() => {
        console.log(`> getting data for bounds`, bounds);
        const ne = bounds.getNorthEast();
        const sw = bounds.getSouthWest();
        const url = `http://localhost:20002/api/tile?neLat=${ne.lat}&neLng=${ne.lng}&swLat=${sw.lat}&swLng=${sw.lng}`;
        fetch(url)
            .then(response => response.json())
            .then(data => setGeom(data.features))
            .catch(error => console.error(error));
    }, [bounds])

    return (
        <LayerGroup>
            {
                geom.map(geoJSON => <ObjectMarker key={geoJSON.properties.id} geoJSON={geoJSON} />)
            }
        </LayerGroup>
    );
}

export default ObjectMarkersGroup;