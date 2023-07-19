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

          function getGeolocation(data) {
            function success(position) {
              const latitude = position.coords.latitude;
              const longitude = position.coords.longitude;

              data.geolocation.latitude = latitude;
              data.geolocation.longitude = longitude;  
            }
            
            function error(error) {
              console.error("Error", error)
            }
            return navigator.geolocation.getCurrentPosition(success, error);
            }   


        function handleResponse(data) {
            if (data.success) {
            $("#pressureWrapper").empty();
            $("#pressureWrapper").html(data.html);

            getGeolocation(data);
            
            
            $("#copyToClipboard").on("click", function () {
                const textToCopy = window.location.href;
        
                navigator.clipboard
                  .writeText(textToCopy)
                  .then(showTooltip)
                  .catch(() => console.error("Erro ao copiar link, tente novamente."));
              });
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
      $("#id_referrer_path").val(window.location.href);
      $.ajax($form.attr('action'), {
        type: 'POST',
        data: $form.serialize(),
      }).always(handleResponse);
    });
  });
}(window.jQuery));
