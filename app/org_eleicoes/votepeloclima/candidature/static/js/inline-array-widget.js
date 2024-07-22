(function ($) {
    "use strict";
    $(function () {
        const maxSize = $('#inline-array-add').data('size');
        const name = $('#inline-array').data('name');
        
        function updateInlineArray() {
            const totalInputs = $('#inline-array .d-flex').length;
            if (totalInputs === 1) {
                $('#inline-array .d-flex').find('button').hide();
            } else {
                $('#inline-array .d-flex').find('button').show();
            }

            if (totalInputs === maxSize) {
                $('#inline-array-add').attr('disabled', 'disabled');
            } else {
                $('#inline-array-add').removeAttr('disabled');
            }

            $('#inline-array .d-flex').each((i, item) => {
                $(item).find('input').attr('name', `${name}_${i}`)
            })
        }

        $('#inline-array-add').click(() => {
            const totalInputs = $('#inline-array .d-flex').length;
            if (totalInputs < maxSize) {
                const $div = $('#inline-array .d-flex').first().clone();
                $div.find('input').val('');
                $div.find('button').show();
                $('#inline-array').append($div);
                updateInlineArray();
            }
        });

        function inlineDelete(target) {
            $(target).parent().remove();
            updateInlineArray();
        };

        updateInlineArray();
        window.inlineDelete = inlineDelete;
    });
}(jQuery));