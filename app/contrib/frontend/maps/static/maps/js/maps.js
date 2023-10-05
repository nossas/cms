let config = {
  minZoom: 7,
  maxZoom: 18,
  zoomControl: false,
  autoPan: false,
  scrollWheelZoom: false
};

const zoom = 18;
const lat = -23.55016;
const lng = -46.63366;

const mapWrapper = document.querySelector("#map");

// Adiciona o mapa
const map = L.map("map", config).setView([lat, lng], zoom);

// Carrega e mostra o layer
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// ------------------------------------------------------------

L.control.zoom({ position: "topright" }).addTo(map);

// --------------------------------------------------------------
L.Control.Search = L.Control.extend({
  options: {
    position: "topleft",
  },
  onAdd: function () {
    const container = L.DomUtil.create("div", "autocomplete-container");

    L.DomEvent.disableClickPropagation(container);

    container.insertAdjacentHTML(
      "beforeend",
      `<div class="auto-search-wrapper loupe">
        <input type="text" id="local" autocomplete="off" placeholder="Encontre a linha" />
      </div>`
    );

    return container;
  },
});

new L.Control.Search().addTo(map);

// --------------------------------------------------------------
let startPoint, endPoint, polylineGeoJSON;
let geojsonarray = [];

function addMarkers(coordinates) {
  let LeafIcon = L.Icon.extend({
    options: {
        iconSize:     [40, 40],
        iconAnchor:   [22, 50],
        popupAnchor:  [-3, -76]
    }
  });
  
  // Remove marcadores existentes
  if (startPoint) map.removeLayer(startPoint);
  if (endPoint) map.removeLayer(endPoint);

  startPoint = L.marker([coordinates[0][1], coordinates[0][0]]);
  endPoint = L.marker([coordinates[coordinates.length - 1][1], coordinates[coordinates.length - 1][0]]);

  // Adiciona marcadores nos pontos inicial e final
  if (mapWrapper.dataset.mapsIconsPointA) {
    let startIcon = new LeafIcon({iconUrl: mapWrapper.dataset.mapsIconsPointA})
    startPoint = L.marker([coordinates[0][1], coordinates[0][0]], {icon: startIcon});
  }
  if (mapWrapper.dataset.mapsIconsPointB) {
    let endIcon = new LeafIcon({iconUrl: mapWrapper.dataset.mapsIconsPointB})
    endPoint = L.marker([coordinates[coordinates.length - 1][1], coordinates[coordinates.length - 1][0]], {icon: endIcon});
  }

  // Adiciona marcadores ao mapa
  startPoint.addTo(map);
  endPoint.addTo(map);
}

function addPolyline(coordinates, properties) {
  const lineColor = mapWrapper.dataset.mapsLinecolor;

  // Remove linha existente
  if (polylineGeoJSON) map.removeLayer(polylineGeoJSON);

  // Adiciona linha ao mapa
  polylineGeoJSON = L.geoJSON({
    type: "LineString",
    coordinates: coordinates,
  }, {
    style: {
      color: lineColor || "red",
      weight: 3,
      opacity: 1,
      fillOpacity: 0.5,
    },
    onEachFeature: function (feature, layer) {
        const linhaNum = properties.ln_codigo.toString();
        const linhaName = properties.title.toString();
        const linhaEmpresa = properties.ln_empresa.toString();

        layer.bindPopup(
          "<span>Número:\n" + linhaNum + "</span><br>" +
          "<span>Nome:\n" + linhaName + "</span><br>" +
          "<span>Empresa responsável:\n" + linhaEmpresa + "</span><br>"
        );
    },
  }).addTo(map);
}

new Autocomplete("local", {
  onSearch: ({ currentValue }) => {
    const api = mapWrapper.dataset.mapsGeojson;
    return new Promise((resolve) => {
      fetch(api)
        .then((response) => response.json())
        .then((data) => {
          const result = data.features
            .sort((a, b) =>
              a.properties.title.localeCompare(b.properties.title)
            )
            .filter((element) => {
              return element.properties.title.match(
                new RegExp(currentValue, "gi")
              );
            });
          resolve(result);
        })
        .catch((error) => {
          console.error(error);
        });
    });
  },

  onResults: ({ matches, template }) => {
    return matches === 0
      ? template
      : matches
        .map((el) => {
          return `
            <li>
              <div class="title">${el.properties.title}</div>
            </li>`;
        })
        .join("");
  },

  onSubmit: ({ object }) => {
    const coordinates = object.geometry.coordinates;
    const properties = object.properties;

    // Adiciona marcadores nos pontos inicial e final
    addMarkers(coordinates);

    // Adiciona linha ao mapa
    addPolyline(coordinates, properties);

    map.fitBounds(polylineGeoJSON.getBounds(), { padding: [150, 150] });

    if (geojsonarray.includes(object.properties.id)) return;
    geojsonarray.push(object.properties.id);
  },

  noResults: ({ currentValue, template }) =>
    template(`<li>Sem resultados: "${currentValue}"</li>`),

  onReset: () => {
    // Remove marcadores e linha
    if (startPoint) map.removeLayer(startPoint);
    if (endPoint) map.removeLayer(endPoint);
    if (polylineGeoJSON) map.removeLayer(polylineGeoJSON);

    geojsonarray = [];
  },
});
