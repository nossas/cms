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

if (mapWrapper) {
  // Adiciona o mapa
  const map = L.map("map", config).setView([lat, lng], zoom);

  // Carrega e mostra o layer
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);


  L.control.zoom({ position: "topright" }).addTo(map);

  L.Control.Search = L.Control.extend({
    options: {
      position: "topleft",
    },
    onAdd: function () {
      const container = L.DomUtil.create("div", "autocomplete-container");
      const searchPlaceholder = mapWrapper.dataset.mapsSearchplaceholder;

      L.DomEvent.disableClickPropagation(container);

      container.insertAdjacentHTML(
        "beforeend",
        `<div class="auto-search-wrapper loupe">
          <input type="text" id="show-all-values" autocomplete="off" placeholder="${searchPlaceholder}" />
        </div>`
      );

      return container;
    },
  });

  new L.Control.Search().addTo(map);

  let startPoint, endPoint, polylineGeoJSON;
  let geojsonarray = [];

  function addMarkers(coordinates, properties) {
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

    // Adiciona marcadores custom nos pontos inicial e final
    if (mapWrapper.dataset.mapsIconsPointA) {
      let startIcon = new LeafIcon({iconUrl: mapWrapper.dataset.mapsIconsPointA})
      startPoint = L.marker([coordinates[0][1], coordinates[0][0]], {icon: startIcon});
    }
    if (mapWrapper.dataset.mapsIconsPointB) {
      let endIcon = new LeafIcon({iconUrl: mapWrapper.dataset.mapsIconsPointB})
      endPoint = L.marker([coordinates[coordinates.length - 1][1], coordinates[coordinates.length - 1][0]], {icon: endIcon});
    }

    let ifObsProperty = !!properties?.observacoes ? `<span>Obs: ${properties.observacoes}</span><br>` : "";

    [startPoint, endPoint].forEach(marker => {
      marker.bindPopup(
        `<span>Número: ${properties.ln_codigo}</span><br>` +
        `<span>Nome: ${properties.title}</span><br>` +
        `<span>Empresa responsável: ${properties.ln_empresa}</span><br>` +
        `<span>Viagens em 2019: ${properties.viagens_em_2019}</span><br>` +
        `<span>Viagens em 2023: ${properties.viagens_em_2023}</span><br>` +
        `<span>Redução: ${properties.reducao_linha}</span><br>` +
        ifObsProperty
      ).addTo(map);
    });
  }

  function addPolyline(coordinates, properties) {
    const lineColor = mapWrapper.dataset.mapsLinecolor;

    if (polylineGeoJSON) map.removeLayer(polylineGeoJSON);

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
        layer.bindPopup(
          `<span>Número: ${properties.ln_codigo}</span><br>` +
          `<span>Nome: ${properties.title}</span><br>` +
          `<span>Empresa responsável: ${properties.ln_empresa}</span><br>`
        );
      },
    }).addTo(map);
  }

  new Autocomplete("show-all-values", {
    clearButton: true,
    cache: true,
    showAllValues: true,

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
          .catch((error) => console.error(error));
      });
    },

    onResults: ({ matches, template }) =>
      matches === 0 ? template : matches.map((el) => `<li><div class="title">${el.properties.title}</div></li>`).join(""),

    onSubmit: ({ object }) => {
      const coordinates = object.geometry.coordinates;
      const properties = object.properties;

      addMarkers(coordinates, properties);
      addPolyline(coordinates, properties);

      map.fitBounds(polylineGeoJSON.getBounds(), { padding: [150, 150] });

      if (geojsonarray.includes(object.properties.id)) return;
      geojsonarray.push(object.properties.id);
    },

    noResults: ({ currentValue, template }) => template(`<li>Sem resultados: "${currentValue}"</li>`),

    onReset: () => {
      // Remove marcadores e linha
      [startPoint, endPoint, polylineGeoJSON].forEach(layer => {
        if (layer) map.removeLayer(layer);
      });

      geojsonarray = [];
    },
  }); 
}
