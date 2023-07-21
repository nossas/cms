(function ($) {
    "use strict";
  
    $(function () {

        function successCallback(position){
            console.log(position);
            
            
        }
        function errorCallback(error){
            console.log(error);
        }
        navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
      
    });
  }(window.jQuery));