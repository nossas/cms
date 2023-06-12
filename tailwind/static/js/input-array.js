(function ($) {
    function getInputElement(index, name) {
      return `
        <div data-fieldset class="flex flex-row">
          <input type="text" name="${name}_${index}" />
          <button type="button">Remover</button>
        </div>
      `;
    }

    $(document).ready(function () {
      $div = $("[data-fieldset-id]");
      const id = $div.data().fieldsetId;
      const name = $div.data().fieldsetName;
      const limit = Number($div.data().fieldsetLimit) - 1;

      // console.log("data", { id, name, limit });

      const $addElement = $(`[data-fieldset-id="${id}"] > button`);

      // Evento para adicionar novo INPUT
      $addElement.on("click", function (evt) {
        const index = $(`[data-fieldset-id="${id}"] div[data-fieldset]`).length;
        $(getInputElement(index, name)).insertBefore(evt.target);

        // Desabilitar botão quando chegar no limite
        if (index === limit) {
          $addElement.prop("disabled", true);
        }

        // Evento para remover INPUT
        $(`[data-fieldset-id="${id}"] div[data-fieldset] > button`).on("click", function (evt) {
          $(evt.target).parent().remove();

          // Habilita botão ao remover um itme da lista
          $addElement.prop("disabled", false);
        });
      });

      // Evento para remover INPUT
      $(`[data-fieldset-id="${id}"] div[data-fieldset] > button`).on("click", function (evt) {
        $(evt.target).parent().remove();

        // Habilita botão ao remover um itme da lista
        $addElement.prop("disabled", false);
      });
    });
  })(django.jQuery);