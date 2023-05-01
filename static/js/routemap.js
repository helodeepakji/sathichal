function calculateAndDisplayRoute(directionsService,directionsRenderer,source,destination) {
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