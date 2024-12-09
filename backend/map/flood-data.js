let eventMarkers = {};

async function loadFloodData(map) {
    try {
        const response = await fetch('/api/events');
        const data = await response.json();
        const events = data.events;

        const currentTime = new Date();

        // Define custom icons for each event type
        const eventIcons = {
            water_levels: "/static/img/water-levels.png",
            flood_severity: "/static/img/flood-severity.png",
            closed_roads: "/static/img/closed-roads.png",
            flood_reports: "/static/img/flood-report.png",
            traffic_conditions: "/static/img/traffic-conditions.png",
            flood_history: "/static/img/flood-history.png"
        };

        // Define human-readable names for event types
        const eventNames = {
            water_levels: "Water Level Alert",
            flood_severity: "Flood Severity Alert",
            closed_roads: "Closed Road Alert",
            flood_reports: "Flood Report",
            traffic_conditions: "Traffic Conditions Alert",
            flood_history: "Historical Flood Event"
        };

        // Initialize marker storage
        Object.keys(eventIcons).forEach(type => {
            eventMarkers[type] = [];
        });

        // Create markers for each event
        for (const event of events) {
            if (event.type === "flood_history") {
                addFloodHistoryMarker(map, event, eventIcons, eventNames);
            } else {
                addStandardEventMarker(map, event, eventIcons, eventNames, currentTime);
            }
        }

        setupFilterListeners();
    } catch (error) {
        console.error("Error loading flood data:", error);
    }
}

function addFloodHistoryMarker(map, event, eventIcons, eventNames) {
    const marker = new google.maps.Marker({
        position: { lat: event.latitude, lng: event.longitude },
        map: map,
        title: eventNames[event.type],
        icon: {
            url: eventIcons[event.type],
            scaledSize: new google.maps.Size(40, 40)
        }
    });

    const infoWindow = new google.maps.InfoWindow({
        content: `
            <div>
                <strong>Type:</strong> ${eventNames[event.type]}<br>
                <strong>Date:</strong> ${event.time || "Unknown Date"}<br>
                <strong>Info:</strong> ${event.info || "N/A"}
            </div>
        `
    });

    marker.addListener("click", () => {
        infoWindow.open(map, marker);
    });

    eventMarkers[event.type].push(marker);
}

function addStandardEventMarker(map, event, eventIcons, eventNames, currentTime) {
    const eventEndTime = new Date(event.time);
    eventEndTime.setHours(eventEndTime.getHours() + event.duration);

    if (currentTime < eventEndTime) {
        const eventTypeName = eventNames[event.type] || "Unknown Event";

        const eventDate = new Date(event.time);
        const formattedDate = `${(eventDate.getMonth() + 1).toString().padStart(2, '0')}/${
            eventDate.getDate().toString().padStart(2, '0')
        }/${eventDate.getFullYear()}`;
        const hours = eventDate.getHours() % 12 || 12;
        const minutes = eventDate.getMinutes().toString().padStart(2, '0');
        const ampm = eventDate.getHours() >= 12 ? "PM" : "AM";

        const marker = new google.maps.Marker({
            position: { lat: event.latitude, lng: event.longitude },
            map: map,
            title: eventTypeName,
            icon: {
                url: eventIcons[event.type],
                scaledSize: new google.maps.Size(40, 40)
            }
        });

        const infoWindow = new google.maps.InfoWindow({
            content: `
                <div>
                    <strong>Type:</strong> ${eventTypeName}<br>
                    <strong>Address:</strong> ${event.street}, ${event.city}, ${event.state}, ${event.zip}<br>
                    <strong>Posted At:</strong> ${formattedDate} ${hours}:${minutes} ${ampm}<br>
                    <strong>Duration:</strong> ${event.duration} hour(s)<br>
                    <strong>Info:</strong> ${event.info || "N/A"}
                </div>
            `
        });

        marker.addListener("click", () => {
            infoWindow.open(map, marker);
        });

        eventMarkers[event.type].push(marker);
    }
}

function setupFilterListeners() {
    document.getElementById("toggle-water-levels").addEventListener("change", (e) => toggleMarkers("water_levels", e.target.checked));
    document.getElementById("toggle-flood-severity").addEventListener("change", (e) => toggleMarkers("flood_severity", e.target.checked));
    document.getElementById("toggle-closed-roads").addEventListener("change", (e) => toggleMarkers("closed_roads", e.target.checked));
    document.getElementById("toggle-flood-reports").addEventListener("change", (e) => toggleMarkers("flood_reports", e.target.checked));
    document.getElementById("toggle-traffic-conditions").addEventListener("change", (e) => toggleMarkers("traffic_conditions", e.target.checked));
    document.getElementById("toggle-flood-history").addEventListener("change", (e) => toggleMarkers("flood_history", e.target.checked));
}

function toggleMarkers(type, isVisible) {
    eventMarkers[type].forEach(marker => {
        marker.setVisible(isVisible);
    });
}
