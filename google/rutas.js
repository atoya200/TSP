let map;
let directionsService;
let directionsRenderer;
let routes = [
    { start: { lat: 37.7749, lng: -122.4194 }, end: { lat: 34.0522, lng: -118.2437 } }, // Ruta 1
    { start: { lat: 34.0522, lng: -118.2437 }, end: { lat: 36.1699, lng: -115.1398 } }, // Ruta 2
    // Agrega más rutas si es necesario
];
let currentRouteIndex = 0;

function initMap() {
    // Inicializa el mapa centrado en el primer punto de partida
    map = new google.maps.Map(document.getElementById("map"), {
        center: routes[0].start,
        zoom: 6,
    });
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({ map: map });

    // Inicia la animación de las rutas
    animateRoutes();
}

function animateRoutes() {
    if (currentRouteIndex >= routes.length) return; // Finaliza si no hay más rutas

    const { start, end } = routes[currentRouteIndex];
    const request = {
        origin: start,
        destination: end,
        travelMode: google.maps.TravelMode.DRIVING,
    };

    directionsService.route(request, (result, status) => {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsRenderer.setDirections(result);

            // Espera unos segundos y luego continúa con la siguiente ruta
            setTimeout(() => {
                currentRouteIndex++;
                animateRoutes(); // Llama a la siguiente ruta
            }, 2000); // Cambia el tiempo (2000 ms) según el ritmo de animación que prefieras
        } else {
            console.error("Error al obtener la ruta:", status);
        }
    });
}

// Ejecuta la función de inicialización
window.initMap = initMap;
