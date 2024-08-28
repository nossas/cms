document.addEventListener("DOMContentLoaded", function () {
  const items = [
    { icon: "ds-icon-compromisso-laranja-1", text: "Políticas de adaptação das cidades para reduzir tragédias" },
    { icon: "ds-icon-compromisso-laranja-2", text: "Políticas para redução de emissões e transição energética" },
    { icon: "ds-icon-compromisso-laranja-3", text: "Políticas sociais de apoio às populações atingidas" },
    { icon: "ds-icon-compromisso-laranja-4", text: "Transição climática com justiça social, racial e de gênero" },
    { icon: "ds-icon-compromisso-laranja-5", text: "Proteção ambiental e de recursos naturais" },
    { icon: "ds-icon-compromisso-laranja-6", text: "Incentivo à participação popular e ao engajamento da juventude" },
    { icon: "ds-icon-compromisso-laranja-7", text: "Investimentos em pesquisa e inovação para enfrentar a crise climática" },
    { icon: "ds-icon-compromisso-laranja-8", text: "Valorização de saberes tradicionais e tecnologias sociais na busca de soluções" },
  ];
 
  const carouselInner = document.querySelector(".carousel-inner");
  const carouselIndicators = document.querySelector(".carousel-indicators");

  function createSlides(itemsPerSlide) {
    carouselInner.innerHTML = "";
    carouselIndicators.innerHTML = "";

    for (let i = 0; i < items.length; i += itemsPerSlide) {
      const slide = document.createElement("div");
      slide.className = "carousel-item" + (i === 0 ? " active" : "");

      const container = document.createElement("div");
      container.className = "d-flex justify-content-center align-items-center";

      for (let j = i; j < i + itemsPerSlide && j < items.length; j++) {
        const col = document.createElement("div");
        col.className = "d-flex flex-column align-items-center text-center";
        col.innerHTML = `
          <i class="${items[j].icon}"></i>
          <p class="mt-2 text-uppercase fw-bold w-75">${items[j].text}</p>
        `;
        container.appendChild(col);
      }

      slide.appendChild(container);
      carouselInner.appendChild(slide);

      // Cria indicadores
      const indicator = document.createElement("button");
      indicator.type = "button";
      indicator.setAttribute("data-bs-target", "#carouselControls");
      indicator.setAttribute("data-bs-slide-to", (i / itemsPerSlide).toString());
      if (i === 0) indicator.className = "active";
      carouselIndicators.appendChild(indicator);
    }
  }

  // Inicializa o carousel com base na largura da tela
  function initializeCarousel() {
    const itemsPerSlide = window.innerWidth < 992 ? 1 : 4;
    createSlides(itemsPerSlide);
  }

  initializeCarousel();

  // Reajusta o número de itens por slide
  window.addEventListener("resize", function () {
    initializeCarousel();
  });
});
