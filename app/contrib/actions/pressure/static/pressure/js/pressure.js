(function ($) {
  "use strict";

  $(function () {
    $(".pressure-plugin form").on("submit", function (evt) {
      const $form = $(this);

      function showTooltip() {
        const tooltip = $("#copyToClipboardTooltip");
        tooltip.toggleClass("tooltip-open hover:before:block hover:after:block");

        // hide after 3 seconds
        window.setTimeout(function () {
          tooltip.removeClass("tooltip-open hover:before:block hover:after:block");
        }, 2000);
      }

      function failResponse({ responseJSON }) {
        $form.find('.errorlist').empty();

        $.each(responseJSON.errors, function (key, value) {
          if (key === '__all__') {
            const $errorlist = $form.find("[type='submit'] + .errorlist");
            $errorlist.html(
              $.each(value, function (item) {
                return "<li>" + item + "</li>"
              })
            );
          } else {
            const $field = $form.find("input[name=" + key + "]").first();
            $field.parents(".form-control").find(".errorlist").html(
              $.each(value, function (item) {
                return "<li>" + item + "</li>"
              })
            );
          }
        });
        window.gtag("event", "form_submit_failed", { form_id: $form.attr("id") });
      }

      function doneResponse({ success, html }) {
        var instanceId = $('.pressure-plugin').data('instance-id');

        $('#pressureWrapper-' + instanceId).empty();
        $('#pressureWrapper-' + instanceId).html(html);

        $("#copyToClipboard").on("click", function () {
          const textToCopy = window.location.href;

          navigator.clipboard
            .writeText(textToCopy)
            .then(showTooltip)
            .catch(() => console.error("Erro ao copiar link, tente novamente."));
        });
        window.gtag("event", "form_submit_success", { form_id: $form.attr("id") });
      }

      evt.preventDefault();
      $("#id_referrer_path").val(window.location.href);
      $.ajax($form.attr('action'), { type: 'POST', data: $form.serialize() })
        .fail(failResponse)
        .done(doneResponse);
    });
  });
}(window.jQuery));
