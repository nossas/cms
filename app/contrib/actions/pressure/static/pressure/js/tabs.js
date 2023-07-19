(function ($) {
    "use strict";
  
    $(function () {
        $(".tab").on("click", function() {
            $(".tab.tab-active").removeClass("tab-active");
            $(".tab-panel:not(.hidden)").addClass("hidden");

            const index = $(this).attr("tab-index");
            $(this).addClass("tab-active")
            $("#tab-panel-" + index).removeClass("hidden");
        });
    });
  }(window.jQuery));