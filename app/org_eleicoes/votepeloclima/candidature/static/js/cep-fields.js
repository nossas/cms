(function ($) {
  "use strict";

  $(function () {
    $("[data-address-name]").each((i, item) => {
      // console.log("Loop: ", item);
      const $field = $(item);
      
      const name = $field.data("addressName");
      const url = $field.data("addressUrl");
      const placeholder = $field.data("addressPlaceholder") || "Select";
      const value = $field.find(":selected").val();

      const parentName = $field.data("addressParent");
      const $parent = $(`[data-address-name="${parentName}"]`);

      if (!value) {
        // Add empty value only not selected value
        $field.prepend(`<option value="">${placeholder}</option>`).val("");
      }

      // Use if to not repeat apply select2, fix when used in Layout django crispy
      if (!$field.data('select2-id')) {
        // console.log("If: ", $field);

        $field.select2({
          allowClear: true,
          dropdownAutoWidth: true,
          width: "100%",
          placeholder: placeholder
        });
  
        if ($parent) {
          const changeEvent = (evt) => {
            const value = evt.target.value;
  
            $field.empty();
            $field.append(`<option value="">${placeholder}</option>`);
    
            if (value) {
              $.get(url + "?" + parentName + "=" + value, (data) => {
                $.each(data, (index, value) => {
                  $field.append(
                    '<option value="' + value.code + '">' + value.name + '</option>'
                  );
                });
              });
            }
          }
  
          $parent.on("change", changeEvent);
        }
      }
    });
  });
}(jQuery));
