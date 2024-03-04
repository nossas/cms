(function ($) {
    "use strict";
  
    $(function () {
        $('[data-bs-toggle="dropdown"]').on('show.bs.dropdown', (evt) => {
            const limitHeight = 125.966;
            let height = $(evt.target).next().children('ul').height();
            if (height > limitHeight && (height - limitHeight) < limitHeight) {
                height = 125.966;
            } else if (height > limitHeight) {
                height = height - 125.966;
            }
            $(evt.target).next().css("height", height + 20);
        });

        $('[data-bs-toggle="dropdown"]').on('hide.bs.dropdown', (evt) => {
            $(evt.target).next().removeAttr("style");
        });

        // Open Dropdown on Navbar with hover
        $('.d-none .navbar-nav > .child').hover(function() {
            const dropdownBtn = $(this).find('.dropdown-toggle');
            const dropdownEl = new bootstrap.Dropdown(dropdownBtn);
            dropdownEl.show();
            
          }, function() {
            const dropdownBtn = $(this).find('.dropdown-toggle');
            const dropdownEl = new bootstrap.Dropdown(dropdownBtn);
            dropdownEl.hide();
        });

        // Enable click on Dropdown
        $('.d-none a.dropdown-toggle').on("click", function() {
            // $(this).attr.href
            
            console.log("clicked", $(this).attr('href'));
            window.location.href = $(this).attr('href')
        });
    });
}(window.jQuery));