(function ($) {
  "use strict";

  $(function () {
    $('#id_year').select2({
      allowClean: true, dropdownAutoWidth: true, width: 'auto', placeholder: 'Selecione o ano'
    });

    $('#id_year').on('select2:select select2:clear', function(e) {
        $(this).closest('form').submit();
    });
  });
}(window.jQuery));
