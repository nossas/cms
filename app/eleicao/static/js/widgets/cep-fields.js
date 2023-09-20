(function ($) {
  "use strict";

  $(function () {
    const $stateField = $('[data-cep-fields="state"]');
    const $cityField = $('[data-cep-fields="city"]');
    const $placeField = $('[data-cep-fields="place"]');

    if ($stateField.length) {
      $stateField.select2({ dropdownAutoWidth: true, width: 'auto', placeholder: 'Selecione seu estado' });
    
      $cityField.select2({ allowClean: true, dropdownAutoWidth: true, width: 'auto', placeholder: 'Selecione sua cidade' });
    
      $placeField.select2({ dropdownAutoWidth: true, width: 'auto', placeholder: 'Selecione o CT' });

      var uf;
      $stateField.on("change", (evt) => {
        uf = evt.target.value
        const url = $stateField.data("cep-url");

        $.get(url + "?state=" + uf, (data) => {
          $cityField.empty()
          $cityField.append('<option value="">----</option>')
          $.each(data.choices, (index, value) => {
            $cityField.append(
              '<option value="' + value[0] + '">' + value[1] + '</option>'
            )
          });
        });
      });

      var city
      $cityField.on("change", (evt) => {
        city = evt.target.value;
        const url = $cityField.data("cep-url");

        $.get(url + "?city=" + city + "&state=" + uf, (data) => {
          $placeField.empty()
          $placeField.append('<option value="">----</option>')
          $.each(data.choices, (index, value) => {
            $placeField.append('<option value="' + value[0] + '">' + value[1] + "</option>")
          });
        });
      });
    }
  });
}(window.jQuery));