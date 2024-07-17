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

      $stateField.on("change", function(evt) {
        const uf = $(this).val();
        const url = $(this).data("address-url");

        $cityField.empty().append('<option value="">Selecione sua cidade</option>').val("");

        if (uf) {
          $.get(url + "?state=" + uf, function(data) {
            $.each(data, function(index, value) {
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
