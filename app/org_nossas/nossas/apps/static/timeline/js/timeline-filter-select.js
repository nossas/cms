(function ($) {
  "use strict";

  $(document).ready(function () {
    $('#id_year').selectpicker();

    $('#id_year').change(function() {
        $(this).closest('form').submit();
    });
  });
}(window.jQuery));
