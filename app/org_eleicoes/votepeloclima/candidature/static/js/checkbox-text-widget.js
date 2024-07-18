(function ($) {
    "use strict";
    $(function () {
        // Init
        $("[data-checktext]").each((index, element) => {
            $(element).parent().prev().remove();
            if (!$(element).attr("checked")) {
                $(element).parent().next().hide();
            }
        });
        // Event
        $("[data-checktext]").change((evt) => {
            if ($(evt.target).is(":checked")) {
                $(evt.target).attr("checked", "checked");
                $(evt.target).parent().next().show();
            } else {
                $(evt.target).removeAttr("checked");
                $(evt.target).parent().next().hide();
            }
        });
    });
}(jQuery));