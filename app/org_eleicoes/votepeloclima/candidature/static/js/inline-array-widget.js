(function ($) {
    "use strict";
    $(function () {
        const maxSize = $('#inline-array-add').data('size');
        const name = $('#inline-array').data('name');
        
        function updateInlineArray() {
            const totalInputs = $('#inline-array li').length;
            if (totalInputs === 1) {
                $('#inline-array li').find('button').hide();
            } else {
                $('#inline-array li').find('button').show();
            }

            if (totalInputs === maxSize) {
                $('#inline-array-add').attr('disabled', 'disabled');
            } else {
                $('#inline-array-add').removeAttr('disabled');
            }

            $('#inline-array li').each((i, item) => {
                $(item).find('input').attr('name', `${name}_${i}`)
            })
        }

        $('#inline-array-add').on("click", () => {
            const totalInputs = $('#inline-array li').length;
            if (totalInputs < maxSize) {
                const $div = $('#inline-array li').first().clone();
                console.log($div);
                console.log("asdadasdasd")
                $div.find('input').val('');
                $div.find('button').show();
                $('#inline-array ol').append($div);
                updateInlineArray();
            }
        });

        function inlineDelete(target) {
            $(target).parent().parent().remove();
            updateInlineArray();
        };

        updateInlineArray();
        window.inlineDelete = inlineDelete;
    });
}(jQuery));