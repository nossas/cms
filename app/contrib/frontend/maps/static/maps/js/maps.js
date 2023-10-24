let config = {
  minZoom: 7,
  maxZoom: 18,
  zoomControl: false,
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

  let startPoint, endPoint, geojsonLayer, markersGeoJSON;
  let geojsonarray = [];

  let popupText = (properties) => {
    let ifObsProperty = !!properties?.observacoes ? `<span>Obs: ${properties.observacoes}</span><br>` : "";

    return `<span><strong>Número:</strong> ${properties.ln_codigo}</span><br>` +
    `<span><strong>Nome:</strong> ${properties.title}</span><br>` +
    `<span><strong>Empresa responsável:</strong> ${properties.ln_empresa}</span><br>` +
    `<span><strong>Viagens em 2019:</strong> ${properties.viagens_em_2019}</span><br>` +
    `<span><strong>Viagens em 2023:</strong> ${properties.viagens_em_2023}</span><br>` +
    `<span><strong>Variação da linha:</strong> ${properties.reducao_linha}%</span><br>` +
    ifObsProperty;
  }

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

    function createMarker(iconUrl, coordinates) {
      const icon = iconUrl ? new LeafIcon({ iconUrl }) : null;
      return L.marker([coordinates[1], coordinates[0]], { icon });
    }

    startPoint = createMarker(mapWrapper.dataset.mapsIconsPointA, coordinates[0]);

    endPoint = createMarker(mapWrapper.dataset.mapsIconsPointB, coordinates[coordinates.length -1])


    [startPoint, endPoint].forEach(marker => {
      marker.bindPopup(popupText(properties))
    });
  }

  function addPolyline(coordinates, properties) {
    const lineColor = mapWrapper.dataset.mapsLinecolor;

    if (geojsonLayer) map.removeLayer(geojsonLayer);

    geojsonLayer = L.geoJSON({
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
        layer.bindPopup(popupText(properties));
      },
    })
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
            .filter((element) => {
              const lnCodigoMatch = element.properties.ln_codigo.toString().match(
                new RegExp(currentValue, "gi")
              );
              const titleMatch = element.properties.title.match(
                  new RegExp(currentValue, "gi")
              );
              return titleMatch || lnCodigoMatch;
            })
            .sort((a, b) => {
                const aCombination = `${a.properties.ln_codigo} - ${a.properties.title}`;
                const bCombination = `${b.properties.ln_codigo} - ${b.properties.title}`;
                
                return aCombination.localeCompare(bCombination);
            });
          resolve(result);
        })
        .catch((error) => console.error(error))
      });
    },

    onResults: ({ matches, template }) =>
      matches === 0 ? template : matches.map((el) => `<li><div class="title">${el.properties.ln_codigo} - ${el.properties.title}</div></li>`).join(""),

    onSubmit: ({ object }) => {
      console.log("maps on submit", object)
      const coordinates = object.geometry.coordinates;
      const properties = object.properties;

      addPolyline(coordinates, properties);

      map.fitBounds(geojsonLayer.getBounds(), { padding: [150, 150] });

      if (geojsonarray.includes(object.properties.id)) return;
      geojsonarray.push(object.properties.id);

      geojsonLayer.addTo(map);
      // startPoint.addTo(map);
      // endPoint.addTo(map);
    },

    noResults: ({ currentValue, template }) => template(`<li>Sem resultados: "${currentValue}"</li>`),

    onReset: () => {
      // Remove marcadores e linha
      [startPoint, endPoint, geojsonLayer].forEach(layer => {
        if (layer) map.removeLayer(layer);
      });

      geojsonarray = [];
    },
  }); 
}
