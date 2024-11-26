const API_KEY = CONFIG.API_KEY;


let id_punto_partida = ""

let map = L.map('map').setView(
    [-32.574249, -56.096027], 7.3);

const waypoints = [
    /* [-30.4, -56.46667],
    [-30.9056, -55.55012],
    [-31.73333, -55.98333],
    [-32.37028, -54.1675],
    [-33.23333, -54.38333],
    [-34.48333, -54.33333],
    [-34.9, -54.95],
    [-34.37589, -55.23771],
    [-34.852, -56.183],
    [-34.52278, -56.27778],
    [-34.09556, -56.21417],
    [-33.38056, -56.52361],
    [-33.5165, -56.89957],
    [-34.3375, -56.71361],
    [-34.46262, -57.83976],
    [-33.25203, -58.03093],
    [-33.13278, -58.295],
    [-32.32139, -58.07556],
    [-31.38333, -57.96667],
    [-30.4, -56.46667] */
];

var ciudades = []
var ciudadTour = []

const markers = []; // Almacenar los marcadores
const polylines = []; // Almacenar las polilíneas


$(document).ready(async function () {
    await obtenerCiudadesDisponibles();

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map);
});

async function obtenerCiudadesDisponibles() {
    const url = `http://localhost:5000/ciudades_disponibles`;

    try {
        const response = await $.getJSON(url);
        console.log(response);

        ciudades = response


        // Ordenar alfabéticamente por city_name
        ciudades.sort((a, b) => {
            // Convertir a UTF-8 (función encodeURIComponent)
            const cityA = a.city_name.toLowerCase();
            const cityB = b.city_name.toLowerCase();


            if (cityA < cityB) return -1;
            if (cityA > cityB) return 1;
            return 0;
        });

        ciudades.forEach(ciudad => {
            let op = `<option value="${ciudad['id']}">${ciudad['city_name']}</option>`
            $("#select-ciudades").append(op)
        });

    } catch (error) {
        console.error("Error al obtener las ciudades disponibles:", error);
    }
}



/* Invoca al back para que le calcule por TSP la ruta
optima según las ciudades elegidas y el punto de partida */
async function pedirRecorrido() {
    // Recoger todos los valores de los checkboxes marcados
    const checkedItems = $('input[name="ciudades_elegidas[]"]:checked').map(function () {
        return Number.parseInt($(this).val());
    }).get();

    console.log(checkedItems)

    // Verificar si no hay checkboxes marcados
    if (checkedItems.length === 0) {
        alert('Por favor, selecciona al menos un elemento.');
        return;
    }

    lanzarLoader()
    $.ajax({
        url: 'http://localhost:5000/calcular_tsp', // Cambia esto por tu URL
        method: 'POST',
        data: JSON.stringify({ puntos: checkedItems, punto_partida: Number.parseInt(id_punto_partida) }), // Envía los datos como un array
        contentType: 'application/json',
        success: function (response) {

            limpiarMapa()
            ciudadTour = []

            // Armamos el waypoints
            response.forEach(ciudad => {
                ciudadTour.push(ciudad)
                waypoints.push([ciudad['latitude'], ciudad['longitud']])
            })

            ocultarLoader()

            // Ahora llamos al trazado del mapa
            trazarRecorridoEnMapa()
        },
        error: function (xhr, status, error) {
            console.error('Error en la petición:', error);
            alert('Hubo un error al enviar los datos.');
        }
    });
}


/*  */
function mostrarOpciones() {
    id_punto_partida = $("#select-ciudades").val()

    if (id_punto_partida.length == 0) {
        // No hay nada seleccionado, por ende ocultamos la opción de destinos
        $("#opciones-destinos").addClass('no-visible')
        $("#destinos-posibles").addClass('no-visible')
    } else {
        $("#opciones-destinos").removeClass('no-visible')

        // Debemos actualizar los destinos
        cargarDestinos()
        $("#destinos-posibles").removeClass('no-visible')
    }
}



function cargarDestinos() {
    // Cargamos las opciones en el destinos posibles
    $("#destinos-posibles").html("")

    ciudades.forEach(ciudad => {
        if (ciudad["id"] != id_punto_partida) {
            let check = `<input type="checkbox" name="ciudades_elegidas[]" value="${ciudad['id']}" id="">`
            let label = `<label for="">${ciudad['state_name']} - ${ciudad['city_name']}</label>`
            let element = ` <div class="elmento-destino checkbox-container"> ${check} ${label} </div>`
            $("#destinos-posibles").append(element)
        }
    })


}

async function trazarRecorridoEnMapa() {
    const busIcon = L.icon({
        iconUrl: IMG_AUTO,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    });

    const ruta = await obtenerRuta(waypoints[0], waypoints[1]);
    const autoMarker = L.marker(ruta[0], { icon: busIcon }).addTo(map);
    markers.push(autoMarker)

    for (let i = 0; i < waypoints.length - 1; i++) {
        const ruta = await obtenerRuta(waypoints[i], waypoints[i + 1]);
        if (ruta.length > 0) {

            let idCiudad = ciudadTour[i]['id']
            let idCiudad_string = `${idCiudad}`
            const puntoIcono = L.divIcon({
                className: 'punto-icono',
                html: `<img src="${POINTS[i]}" 
                         style="width: 2rem; cursor: pointer;" 
                         onclick="mostrarModalInformacion(${idCiudad_string})">`
            });

            let marcadorLugar = L.marker(waypoints[i], { icon: puntoIcono }).addTo(map);
            markers.push(marcadorLugar)

            await animarLineaConBus(map, ruta, autoMarker);
        }

        if (i == waypoints.length - 2) {
            markers[0].remove()
        } else {
            await delay(1000);
        }
    }

}

async function obtenerRuta(origen, destino) {

    console.log({ origin: origen, dest: destino })

    const url = `https://api.openrouteservice.org/v2/directions/driving-car?api_key=${API_KEY}&start=${origen[1]},${origen[0]}&end=${destino[1]},${destino[0]}`;
    try {
        const response = await $.getJSON(url);
        return response.features[0].geometry.coordinates.map(([lng, lat]) => [lat, lng]);
    } catch (error) {
        console.error("Error al obtener la ruta:", error);
        return [];
    }
}

function animarLineaConBus(map, coordinates, autoMarker) {
    return new Promise(resolve => {
        const polyline = L.polyline([], { color: 'red', weight: 5 }).addTo(map);
        polylines.push(polyline)

        let i = 0;

        function dibujarSegmento() {
            if (i < coordinates.length) {
                polyline.addLatLng(L.latLng(coordinates[i]));
                autoMarker.setLatLng(coordinates[i]);
                i++;
                setTimeout(dibujarSegmento, 5);
            } else {
                setTimeout(resolve, 100);
            }
        }
        dibujarSegmento();
    });
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function limpiarMapa() {
    // Eliminar todos los marcadores
    markers.forEach(marker => marker.remove());
    markers.length = 0; // Vaciar la lista de marcadores

    // Eliminar todas las líneas
    polylines.forEach(polyline => polyline.remove());
    polylines.length = 0; // Vaciar la lista de líneas

    // Opcional: limpiar los waypoints
    waypoints.length = 0; // Limpiar la lista de waypoints
}


function mostrarModalInformacion(id) {

    const $grid = $('.image-grid');
    $grid.empty(); // Limpiar el contenido previo

    const images = IMGS_CIUDADES[id]

    if (images.length === 1) {
        $grid.append(`
    <div class="row">

      <div class="col-12">
        <img src="${images[0]}" class="img-fluid img-very-tall" alt="Imagen 1">
      </div>
      </div>
    `);
    } else if (images.length === 2) {
        $grid.append(`
             <div class="row">
        <div class="col-6">
          <img src="${images[0]}" class="img-fluid img-tall" alt="Imagen">
        </div>
        <div class="col-6">
          <img src="${images[1]}" class="img-fluid img-tall" alt="Imagen">
        </div>
        </div>
            `)

    } else if (images.length === 3) {
        $grid.append(`
            <div class="row">
                <div class="col-12">
                    <img src="${images[0]}" class="img-fluid img-tall" alt="Imagen 1">
                </div>
            </div>
            `);
        $grid.append(`
        <div class="row">
            <div class="col-6">
                <img src="${images[1]}" class="img-fluid img-small" alt="Imagen 2">
            </div>
            <div class="col-6">
                <img src="${images[2]}"  class="img-fluid img-small" alt="Imagen 3">
            </div>
      </div>
    `);
    } else if (images.length === 4) {

        $grid.append(`
            <div class="row">
                <div class="col-6">
                    <img src="${images[0]}" class="img-fluid img-small" alt="Imagen 2">
                </div>
                <div class="col-6">
                    <img src="${images[1]}"  class="img-fluid img-small" alt="Imagen 3">
                </div>
          </div>
            <div class="row">
                <div class="col-6">
                    <img src="${images[2]}" class="img-fluid img-small" alt="Imagen 2">
                </div>
                <div class="col-6">
                    <img src="${images[3]}"  class="img-fluid img-small" alt="Imagen 3">
                </div>
          </div>
        `);

    } else if (images.length === 5) {
        $grid.append(`
            <div class="row">

      <div class="col-6">
        <img src="${images[0]}" class="img-fluid img-tall" alt="Imagen 1">
      </div>
      <div class="col-6">
        <img src="${images[1]}" class="img-fluid img-tall" alt="Imagen 2">
      </div>
      </div>
    `);
        $grid.append(`
            <div class="row">

      <div class="col-4">
        <img src="${images[2]}"  class="img-fluid img-small" alt="Imagen 3">
      </div>
      <div class="col-4">
        <img src="${images[3]}"  class="img-fluid img-small" alt="Imagen 4">
      </div>
      <div class="col-4">
        <img src="${images[4]}"  class="img-fluid img-small" alt="Imagen 5">
      </div>
      </div>
    `);
    } else {
        images.forEach(image => {
            $grid.append(`
        <div class="col-4">
          <img src="${image}" alt="Imagen">
        </div>
      `);
        });
    }

    // Agregamos el texto
    let textos = TEXTOS[id]

    // Agregamos el titulo de la ciudad
    $("#nombre-ciudad").html(textos['title'])

    $(".text-content").empty()
    $(".text-content").html(`<p> ${textos['bodyMessage']} </p>`)

    const myModal = new bootstrap.Modal($('#myModal')[0]);
    myModal.show();
}
