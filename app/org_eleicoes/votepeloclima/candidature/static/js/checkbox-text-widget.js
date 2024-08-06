(function ($) {
    "use strict";
    $(function () {
        const $dropzone = $("#dropzone");
        const $selectzone = $("#selectzone");
        // Init
        $("[data-checktext]").each((index, element) => {
            console.log($(element));
            if (!$(element).attr("checked")) {
                $(element).parent().next().hide();
            } else if ($dropzone.length) {
                const $field = $(element).parent().parent();
                $field.appendTo($dropzone);
            }
        });
        // Event
        $("[data-checktext]").change((evt) => {
            if ($(evt.target).is(":checked")) {
                if ($dropzone.length) {
                    const $field = $(evt.target).parent().parent();
                    $field.appendTo($dropzone);
                }
                $(evt.target).attr("checked", "checked");
                const $item = $(evt.target).parent().next();
                $item.show()
            } else {
                if ($selectzone.length) {
                    const $field = $(evt.target).parent().parent();
                    $field.appendTo($selectzone);
                }
                $(evt.target).removeAttr("checked");
                const $item = $(evt.target).parent().next();
                $item.hide();
            }
        });
    });
}(jQuery));