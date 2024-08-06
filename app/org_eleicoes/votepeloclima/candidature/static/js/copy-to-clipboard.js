function copyURL() {
  var url = window.location.href;
  var modalString = "?modal=true";

  if (url.includes(modalString)) {
    url = url.replace(modalString, "");
  }

  navigator.clipboard.writeText(url).then(function() {
    var copyButton = document.querySelector("#copyButton");
    var tooltip = bootstrap.Tooltip.getInstance(copyButton) || new bootstrap.Tooltip(copyButton);
    tooltip.show();

    setTimeout(function() {
        tooltip.hide();
    }, 2000);

    console.log("URL copiada!");
  }).catch(function(err) {
      console.error("Algo deu errado: " + err);
  });
}

document.addEventListener('DOMContentLoaded', function() {
  var copyButton = document.querySelector("#copyButton");
  new bootstrap.Tooltip(copyButton);
});
