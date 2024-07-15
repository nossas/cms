(function ($) {
  "use strict";

  $(function () {
    const $stateField = $('[data-address-fields="state"]');
    const $cityField = $('[data-address-fields="city"]');

    if ($stateField.length) {
      $stateField.prepend('<option value=""></option>').val("");
      $stateField.select2({
        allowClear: true,
        dropdownAutoWidth: true,
        width: "auto",
        placeholder: "Selecione seu estado"
      });

      $cityField.prepend('<option value=""></option>').val("");
      $cityField.select2({
        allowClear: true,
        dropdownAutoWidth: true,
        width: "auto",
        placeholder: "Selecione sua cidade"
      });

      var uf;
      $stateField.on("change", (evt) => {
        uf = evt.target.value;
        const url = $stateField.data("address-url");

        $cityField.empty();
        $cityField.append('<option value="">Selecione sua cidade</option>');

        if (uf) {
          $.get(url + "?state=" + uf, (data) => {
            $.each(data, (index, value) => {
              $cityField.append(
                '<option value="' + value.code + '">' + value.name + '</option>'
              );
            });
          });
        }
      });
    }
  });
}(jQuery));
