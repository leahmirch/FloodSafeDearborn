// Initialize the map and load flood data
function initMap() {
    const mapOptions = {
        zoom: 12,
        center: { lat: 42.3221, lng: -83.1763 }
    };

    const map = new google.maps.Map(document.getElementById("map"), mapOptions);

    // Load Dearborn boundary
    loadDearbornBoundary(map);

    // Load flood data
    loadFloodData(map);
}
