function getDirections() {
    const origin = "48.8566,2.3522";  // Coordonnées de départ (Paris)
    const destination = "48.8584,2.2945";  // Coordonnées d'arrivée (Tour Eiffel)

    // Faire une requête GET à l'API Python
    fetch(`/directions?origin=${origin}&destination=${destination}`)
        .then(response => response.json())
        .then(data => {
            let directionsHtml = `<h2>Directions de ${origin} à ${destination}</h2>`;
            data.directions.forEach(step => {
                directionsHtml += `<p>${step.instruction} (${step.distance}, ${step.duration})</p>`;
            });
            document.getElementById("directions").innerHTML = directionsHtml;
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
}
