(function ($) {
    "use strict";

    const patternTargetEmail = /[a-zà-úA-ZÀ-Ú\s]+<(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))>/

    // function validate (value) {
    //     const patternTargetEmail = /[a-zà-úA-ZÀ-Ú\s]+<(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))>/
    //     return patternTargetEmail.test(value)
    // }

    // function add (value) {
    //     const name = value.split("<")[0].trim();
    //     const email = value.split("<")[1].trim().replace(">", "");

    //     console.log({ name, email });
    //     $("input.array-widget").after("<p>" + name + " " + email + "</p>");
    // }

  
    $(function () {
        $("input.array-widget")
            .tagify({
                pattern: patternTargetEmail
            })
            .on("add", function (e, tagData) {
                console.log("add", { e, tagData });
            })
            .on("remove", function(e, tagData) {
                console.log("remove", { e, tagData });
            })
            .on("invalid", function(e, tagData) {
                console.log("invalid", { e, tagData });
            });

        $("input.array-widget").on("change", function (evt) {
            console.log(evt.target)
        });
        // $("input.array-widget").on("keydown", function(evt) {
        //     if (evt.originalEvent.code === "Slash") {
        //         console.log("processa a tag")

        //         console.log("validate", validate(evt.target.value))
        //         if (validate(evt.target.value)) {
        //             add(evt.target.value)
        //         }
        //     }
        // });
    });
}(window.jQuery));