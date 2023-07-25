(function ($) {
  "use strict";

  $(function () {
    function successCallback(position) {
      $("#id_geolocation").val(JSON.stringify({
        "latitude": position.coords.latitude,
        "longitude": position.coords.longitude
      }));
    }
    function errorCallback(error) {
      console.error(error);
    }

    navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
  });
}(window.jQuery));