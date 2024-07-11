(function ($) {
  "use strict";

  $(function () {
    const $stateField = $('[data-address-fields="state"]');
    const $cityField = $('[data-address-fields="city"]');
    console.log("oiee")

    if ($stateField.length) {
      $stateField.select2({ dropdownAutoWidth: true, width: 'auto', placeholder: 'Selecione seu estado' });
      $cityField.select2({ allowClear: true, dropdownAutoWidth: true, width: 'auto', placeholder: 'Selecione sua cidade' });

      var uf;
      $stateField.on("change", (evt) => {
        uf = evt.target.value;
        const url = $stateField.data("address-url");

        $.get(url + "?state=" + uf, (data) => {
          $cityField.empty();
          $cityField.append('<option value="">Selecione sua cidade</option>');
          $.each(data, (index, value) => {
            $cityField.append(
              '<option value="' + value.code + '">' + value.name + '</option>'
            );
          });
        });
      });
    }
  });
}(window.jQuery));
