// Example of flood event data
const floodEvents = [
    { lat: 42.3221, lng: -83.1759, info: 'Flood event on Jan 2024' },
    { lat: 42.2800, lng: -83.2700, info: 'Flood event on Feb 2024' }
];

// Example of flood hotspots
const floodHotspots = [
    { lat: 42.3200, lng: -83.1700, radius: 500 },
    { lat: 42.2900, lng: -83.2100, radius: 700 },
    { lat: 42.2800, lng: -83.2700, radius: 800 },
    { lat: 42.3000, lng: -83.2500, radius: 600 }
];

// Load flood data and create markers on the map
function loadFloodData(map) {
    floodEvents.forEach(event => {
        createMarker(map, { lat: event.lat, lng: event.lng }, event.info);
    });

    // Add flood hotspots as circles
    floodHotspots.forEach(hotspot => {
        const circle = new google.maps.Circle({
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            map: map,
            center: { lat: hotspot.lat, lng: hotspot.lng },
            radius: hotspot.radius
        });
    });
}
