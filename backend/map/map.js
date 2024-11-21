function createMarker(map, position, infoContent) {
    const marker = new google.maps.Marker({
      position: position,
      map: map,
      title: infoContent
    });
    
    const infowindow = new google.maps.InfoWindow({
      content: infoContent
    });
  
    marker.addListener('click', function() {
      infowindow.open(map, marker);
    });
  }
  