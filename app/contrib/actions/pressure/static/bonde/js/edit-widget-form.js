(function ($) {
    "use strict";

    $(function () {
        let actived = 0;

        function toggle(index) {
            if (index == actived) {
                $(".tabs-content > fieldset").eq(index).show();
            } else {
                $(".tabs-content > fieldset").hide();
                $(".tabs > h2").removeClass("tab-active");

                $(".tabs > h2").eq(index).addClass("tab-active");
                $(".tabs-content > fieldset").eq(index).show();
            }
            actived = index
        }

        // Cria estrutura básica para tabs
        $("fieldset").eq(0).before('<div class="tabs"></div>');
        $("fieldset").eq(0).before('<div class="tabs-content"></div>');

        $(".tabs").append($("fieldset > h2").detach());
        $(".tabs-content").append($("fieldset").detach());

        // Adiciona eventos
        $(".tabs > h2").each(function(index) {
            // Default is first open
            if (index !== 0) {
                $(".tabs-content > fieldset").eq(index).hide();
            } else {
                $(".tabs > h2").eq(index).addClass("tab-active");
            }

            $(".tabs > h2").eq(index).on("click", function() {
                toggle(index)
                // $(".tabs-content > fieldset").eq(index).show();
            });
        });
    });
}(window.jQuery));