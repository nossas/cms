// static/js/add_social_media.js
(function ($) {
  "use strict";

  $(function () {
    const $btn = $(".social-media-fields button[type='button']");

    $btn.on("click", () => {
      const $beforeField = $(".social-media-fields .social-media-field-item").last();
      const countFields = $(".social-media-fields .social-media-field-item").length;

      if (countFields < 3) {
        const newSocialMediaField = `
          <div class="social-media-field-item flex gap-5">
            <div class="max-w-xs">
              <select name="0-social_media.${countFields}.kind">
                <option value="">Selecione</option>
                <option value="twitter">Twitter</option>
                <option value="facebook">Facebook</option>
                <option value="instagram">Instagram</option>
              </select>
            </div>
            <div class="gap-1 font-bold max-w-xs">
              <input type="text" name="0-social_media.${countFields}.url" placeholder="Link do seu perfil" />
            </div>
          </div>
        `;

        $beforeField.after(newSocialMediaField);
      }
    });
  });
}(window.jQuery));
