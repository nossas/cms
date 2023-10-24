/* eslint-disable no-undef */
/**
 * autocomplete with geojson
 */

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
  const map = L.map("map", config).setView([lat, lng], zoom);

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
          <input type="text" id="local" autocomplete="off" placeholder="${searchPlaceholder}" />
        </div>`
      );

      return container;
    },
  });

  new L.Control.Search().addTo(map);

  let geojsonarray = [];

  let popupText = (properties) => {
    let ifObsProperty = !!properties?.observacoes ? `<span><strong>Obs:</strong> ${properties.observacoes}</span><br>` : "";

    return `<span><strong>Número:</strong> ${properties.ln_codigo}</span><br>` +
    `<span><strong>Nome:</strong> ${properties.title}</span><br>` +
    `<span><strong>Empresa responsável:</strong> ${properties.ln_empresa}</span><br>` +
    `<span><strong>Viagens em 2019:</strong> ${properties.viagens_em_2019}</span><br>` +
    `<span><strong>Viagens em 2023:</strong> ${properties.viagens_em_2023}</span><br>` +
    `<span><strong>Variação da linha:</strong> ${properties.reducao_linha}%</span><br>` +
    ifObsProperty;
  }



  new Autocomplete("local", {
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

    onResults: ({ matches, template }) => {
      return matches === 0
        ? template
        : matches
            .map((el) => {
              return `
                <li>
                  <div class="title">${el.properties.ln_codigo} - ${el.properties.title}</div>
                </li>`;
            })
            .join("");
    },

    onSubmit: ({ object }) => {
      const properties = object.properties;
      const coordinates = object.geometry.coordinates;
      const lineColor = mapWrapper.dataset.mapsLinecolor;

      const geojsonlayer = L.geoJSON(object, {
        style: function (feature) {
          return {
            color: lineColor || "red",
            weight: 7,
            opacity: 1,
            fillOpacity: 0.7,
          };
        },
        onEachFeature: function (feature, layer) {
          layer.bindPopup(popupText(properties));
        },
      });

      const geojsonmarkers = (properties, coordinates) => {

        let LeafIcon = L.Icon.extend({
          options: {
              iconSize:     [40, 40],
              iconAnchor:   [22, 50],
              popupAnchor:  [-3, -76]
          }
        });

        if (mapWrapper.dataset.mapsIconsPointA) {
          const startIcon = new LeafIcon({ iconUrl: mapWrapper.dataset.mapsIconsPointA });
          startPoint = L.marker([coordinates[0][1], coordinates[0][0]], { icon: startIcon }).addTo(map);
        } else {
          startPoint = L.marker([coordinates[0][1], coordinates[0][0]]).addTo(map);
        }
        
        if (mapWrapper.dataset.mapsIconsPointB) {
          const endIcon = new LeafIcon({ iconUrl: mapWrapper.dataset.mapsIconsPointB }).addTo(map);
          endPoint = L.marker([coordinates[coordinates.length - 1][1], coordinates[coordinates.length - 1][0]], { icon: endIcon }).addTo(map);
        } else {
          endPoint = L.marker([coordinates[coordinates.length - 1][1], coordinates[coordinates.length - 1][0]]).addTo(map);
        }

        [startPoint, endPoint].forEach(marker => {
          marker.bindPopup(popupText(properties))
        });
      }

      map.fitBounds(geojsonlayer.getBounds(), { padding: [150, 150] });

      if (geojsonarray.includes(object.properties.id)) return;
      geojsonarray.push(object.properties.id);


      geojsonmarkers(properties, coordinates);
      geojsonlayer.addTo(map);
    },

    noResults: ({ currentValue, template }) =>
      template(`<li>Sem resultados: "${currentValue}"</li>`),

    onReset: () => {
      // remove all layers
      map.eachLayer(function (layer) {
        if (!!layer.toGeoJSON) {
          map.removeLayer(layer);
        }
      });
      geojsonarray = [];
    },
  });
}
