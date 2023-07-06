(function ($) {
  "use strict";

  $(function () {
    $(".pressure-plugin form").on("submit", function (evt) {
      const $form = $(this)

      function handleResponse(data) {
        if (data.success) {
          alert("success")
        } else {
          $form.find('.errorlist').empty();

          $.each(data, function (key, value) {
            const $field = $form.find("input[name=" + key + "]").first();
            $field.parents(".form-control").find(".errorlist").html(
              $.each(value, function (item) {
                return "<li>" + item + "</li>"
              })
            )
          })
        }
      }

      evt.preventDefault();
      $.ajax($form.attr('action'), {
        type: 'POST',
        data: $form.serialize(),
      }).always(handleResponse);
    });
  });
}(window.jQuery));