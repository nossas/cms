$(document).ready(function() {
    function initializeSelect2WithOrdering(selectId) {
        var selectionOrder = [];

        // Inicializa o Select2 para o campo especificado
        $('#' + selectId).select2();

        $('#' + selectId).on("select2:select", function(e) {
            selectionOrder.push(e.params.data.id);
            reorderSelection(selectId, selectionOrder);
        });

        $('#' + selectId).on("select2:unselect", function(e) {
            var index = selectionOrder.indexOf(e.params.data.id);
            if (index !== -1) {
                selectionOrder.splice(index, 1);
            }
            reorderSelection(selectId, selectionOrder);
        });
    }

    // Função para converter hífens em espaços no attr value
    function normalizeValue(value) {
        return value.replace(/-/g, " ");
    }

    function reorderSelection(selectId, selectionOrder) {
        var $selectionContainer = $('#' + selectId).next('.select2').find('.select2-selection__rendered');
        var orderedItems = [];
    
        selectionOrder.forEach(function(value) {
            var normalizedValue = normalizeValue(value);
            var $item = $selectionContainer.find(".select2-selection__choice").filter(function() {
                return $(this).attr('title') === normalizedValue;
            });
            if ($item.length) {
                orderedItems.push($item.detach());
            }
        });
    
        orderedItems.forEach(function($item) {
            $selectionContainer.append($item);
        });
    
        // Move o campo de pesquisa para o final
        var $searchField = $selectionContainer.find('.select2-search--inline');
        $searchField.detach().appendTo($selectionContainer);
    }

    // Inicializa o Select2 nos campos do form de filtro de Campanhas
    initializeSelect2WithOrdering('id_tags');
    initializeSelect2WithOrdering('id_campaign_group_id');
    initializeSelect2WithOrdering('id_release_date');
});
