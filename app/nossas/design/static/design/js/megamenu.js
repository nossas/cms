(function ($) {
    "use strict";
  
    $(function () {
        $('[data-bs-toggle="dropdown"]').on('show.bs.dropdown', (evt) => {
            const limitHeight = 125.966;
            let height = $(evt.target).next().children('ul').height();
            if (height > limitHeight && (height - limitHeight) < limitHeight) {
                height = 125.966;
            } else if (height > limitHeight) {
                height = height - 125.966;
            }
            $(evt.target).next().css("height", height + 20);
        });

        $('[data-bs-toggle="dropdown"]').on('hide.bs.dropdown', (evt) => {
            $(evt.target).next().removeAttr("style");
        });
    });
}(window.jQuery));