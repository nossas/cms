(function ($) {
  "use strict";

  $(function () {
    console.log("window.gtag", window.gtag);

    $(".pressure-plugin form").on("submit", function (evt) {
      const $form = $(this);

      function handleResponse(data) {
        if (data.success) {
          alert("success");
          window.gtag("event", "form_submit_success", { form_id: $form.attr("id") });
        } else {
          $form.find('.errorlist').empty();

          $.each(data, function (key, value) {
            const $field = $form.find("input[name=" + key + "]").first();
            $field.parents(".form-control").find(".errorlist").html(
              $.each(value, function (item) {
                return "<li>" + item + "</li>"
              })
            );
          });
          window.gtag("event", "form_submit_failed", { form_id: $form.attr("id") });
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