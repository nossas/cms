(function ($) {
    "use strict";
    $(document).ready(function () {
        const $inlineArrayAdd = $('#inline-array-add');
        const maxSize = $inlineArrayAdd.data('size');
        const name = $('#inline-array').data('name');

        function updateInlineArray() {
            const $inputs = $('#inline-array li input');
            const totalInputs = $inputs.length;
            const lastInputValue = $inputs.last().val().trim();

            if (totalInputs === 1) {
                $('#inline-array li').find('button').hide();
            } else {
                $('#inline-array li').find('button').show();
            }

            if (totalInputs >= maxSize || lastInputValue === "") {
                $inlineArrayAdd.attr('disabled', 'disabled');
            } else {
                $inlineArrayAdd.removeAttr('disabled');
            }

            // Atualizar os nomes dos inputs
            $('#inline-array li').each((i, item) => {
                $(item).find('input').attr('name', `${name}_${i}`);
            });
        }

        $inlineArrayAdd.off("click").on("click", () => {
            const $inputs = $('#inline-array li input');
            const lastInputValue = $inputs.last().val().trim();
            const totalInputs = $inputs.length;

            if (lastInputValue !== "" && totalInputs < maxSize) {
                const $firstItem = $('#inline-array li').first().clone();
                $firstItem.find('input').val('');
                $firstItem.find('button').show();
                $('#inline-array ol').append($firstItem);
                updateInlineArray();
            }
        });

        function inlineDelete(target) {
            $(target).closest('li').remove();
            updateInlineArray();
        }

        updateInlineArray();

        // Adicionar eventos para atualização em tempo real dos campos
        $('#inline-array').on('input', 'input', function() {
            updateInlineArray();
        });

        window.inlineDelete = inlineDelete;
    });
}(jQuery));
