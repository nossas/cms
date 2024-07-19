(function ($) {
    "use strict";
    $(function () {
        $('#inline-array-add').click(() => {
            const $div = $('#inline-array .d-flex').first().clone();
            $div.find('input').val('');
            $('#inline-array').append($div);
        });

        function inlineDelete(target) {
            $(target).parent().remove();
        };

        window.inlineDelete=inlineDelete;
    });
}(jQuery));