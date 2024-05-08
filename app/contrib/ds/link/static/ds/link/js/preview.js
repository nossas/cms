$(function () {

    function mountPreviewHtml() {
        //here goes your code
        const label = $('[name="label"]').val();
        const context = $('[name="context"]').val();
        const styled = $('[name="styled"]').val();
        const size = $('[name="size"]').val();
        const icon = $('[name="icon"]').val();
        const icon_position = $('[name="icon_position"]').val();

        let newClass = "btn"

        if (styled !== "") {
            newClass += "-" + styled
        }

        if (context !== "") {
            newClass += "-" + context
        }

        if (size !== "") {
            newClass += " btn-" + size
        }

        let html = '<div class="btn ' + newClass + '">'

        if (icon !== "" && icon_position == "left") {
            html += '<i class="bi bi-' + icon + '"></i> '
        }

        html += label

        if (icon !== "" && icon_position == "right") {
            html += ' <i class="bi bi-' + icon + '"></i>'
        }
        
        html += '</div>'

        return html
    }

    $('[name="label"]').on("change", function (evt) {
        $('#btn-preview').html(mountPreviewHtml());
    });

    $('[name="context"]').on("change", function (evt) {
        $('#btn-preview').html(mountPreviewHtml());
    });

    $('[name="styled"]').on("change", function (evt) {
        $('#btn-preview').html(mountPreviewHtml());
    });

    $('[name="size"]').on("change", function (evt) {
        $('#btn-preview').html(mountPreviewHtml());
    });

    $('[name="icon"]').on("change", function (evt) {
        $('#btn-preview').html(mountPreviewHtml());
    });

    $('[name="icon_position"]').on("change", function (evt) {
        $('#btn-preview').html(mountPreviewHtml());
    });

    $('#content-main').append('<div id="btn-preview" style="background-color:#c7c7c7;padding:10px;">' + mountPreviewHtml() + '</div>');
});