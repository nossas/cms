$(function () {

    function mountPreviewHtml() {
        //here goes your code
        const label = $('[name="label"]').val();
        const context = $('[name="context"]:checked').val();
        const styled = $('[name="styled"]:checked').val();
        const size = $('[name="size"]:checked').val();
        const icon = $('[name="icon"]').val();
        const icon_position = $('[name="icon_position"]').val();

        // console.log("Settings: ", { label, context, styled, size, icon, icon_position });

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
        // console.log("change label: ", evt);
        $('#preview').html(mountPreviewHtml());
    });

    $('[name="context"]').on("change", function (evt) {
        // console.log("change context: ", evt);
        $('#preview').html(mountPreviewHtml());
    });

    $('[name="styled"]').on("change", function (evt) {
        // console.log("change styled: ", evt);
        $('#preview').html(mountPreviewHtml());
    });

    $('[name="size"]').on("change", function (evt) {
        // console.log("change size: ", evt);
        $('#preview').html(mountPreviewHtml());
    });

    $('[name="icon"]').on("change", function (evt) {
        // console.log("change icon: ", evt);
        $('#preview').html(mountPreviewHtml());
    });

    $('[name="icon_position"]').on("change", function (evt) {
        // console.log("change icon_position: ", evt);
        $('#preview').html(mountPreviewHtml());
    });

    $('#preview').append(mountPreviewHtml());
});