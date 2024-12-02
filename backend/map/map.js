async function loadDearbornBoundary(map) {
  try {
      const response = await fetch('/static/data/dearborn-boundary.json');
      const geojson = await response.json();

      map.data.addGeoJson(geojson);

      // Style the Dearborn boundary polygon
      map.data.setStyle({
        strokeColor: "#FF0000",  
        strokeOpacity: 1.0,      
        strokeWeight: 2,         
        fillColor: "#f5c6cb",    
        fillOpacity: 0.2         
    });    
  } catch (error) {
      console.error("Failed to load Dearborn boundary:", error);
  }
}