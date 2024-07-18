(function ($) {
    "use strict";
    $(function () {
        // Init
        $("[data-checktext]").each((index, element) => {
            console.log(element);
            if (!$(element).attr("checked")) {
                $(element).next().hide();
            }
        });
        // Event
        $("[data-checktext]").change((evt) => {
            if ($(evt.target).is(":checked")) {
                $(evt.target).attr("checked", "checked");
                $(evt.target).next().show();
            } else {
                $(evt.target).removeAttr("checked");
                $(evt.target).next().hide();
            }
        });
    });
}(jQuery));