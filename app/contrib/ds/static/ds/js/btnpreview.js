$(function () {

    function mountPreviewHtml() {
        //here goes your code
        const label = $('[name="label"]').val();
        const context = $('[name="context"]').val();
        const styled = $('[name="styled"]').val();

        let newClass = "btn"

        if (styled !== "") {
            newClass += "-" + styled
        }

        if (context !== "") {
            newClass += "-" + context
        }

        return '<div class="btn ' + newClass + '">' + label + '</div>'
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

    $('#content-main').append('<div id="btn-preview" style="background-color:#c7c7c7;padding:10px;">' + mountPreviewHtml() + '</div>');
});