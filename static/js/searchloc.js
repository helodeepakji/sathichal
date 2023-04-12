
const input = document.getElementById("destination");

const autocomplete = new google.maps.places.Autocomplete(input);

// Bind the map's bounds (viewport) property to the autocomplete object,
// so that the autocomplete requests use the current map bounds for the
// bounds option in the request.
autocomplete.bindTo("bounds", map);


function calculateAndDisplayRoute(directionsService, directionsRenderer,source,destination) {
  // const selectedMode = document.getElementById("mode").value;
  const selectedMode = "DRIVING";

  directionsService
    .route({
      origin: source,
      destination: destination,
      travelMode: google.maps.TravelMode[selectedMode],
    })
    .then((response) => {
      directionsRenderer.setDirections(response);
    })
    .catch((e) => window.alert("Directions is not avaliable"));
}


const marker = new google.maps.Marker({
  map,
  anchorPoint: new google.maps.Point(0, -29),
});

autocomplete.addListener("place_changed", () => {
  marker.setVisible(false);

  const place = autocomplete.getPlace();

  if (!place.geometry || !place.geometry.location) {
    // User entered the name of a Place that was not suggested and
    // pressed the Enter key, or the Place Details request failed.
    window.alert("No details available for input: '" + place.name + "'");
    return;
  }

  // If the place has a geometry, then present it on a map.
  if (place.geometry.viewport) {
    map.fitBounds(place.geometry.viewport);
    const directionsRenderer = new google.maps.DirectionsRenderer();
    const directionsService = new google.maps.DirectionsService();
    directionsRenderer.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsRenderer, current_pos ,place.geometry.location);
  } else {
    map.setCenter(place.geometry.location);
    map.setZoom(17);
  }

  marker.setPosition(place.geometry.location);
  marker.setVisible(true);
});
