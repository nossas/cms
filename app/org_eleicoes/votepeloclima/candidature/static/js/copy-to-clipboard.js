const copyButton = document.querySelector("#copyButton");

function copyURL(url=null) {
  if (!url) {
    // Se a URL não for passada, use a URL atual da página
    url = window.location.href;
  }
  let modalString = "?modal=true";

  if (url.includes(modalString)) {
    url = url.replace(modalString, "");
  }

  navigator.clipboard.writeText(url).then(function() {
    const copyButton = document.querySelector("#copyButton");
    let tooltip = bootstrap.Tooltip.getInstance(copyButton) || new bootstrap.Tooltip(copyButton);
    tooltip.show();

    setTimeout(function() {
        tooltip.hide();
    }, 2000);

    console.log("URL copiada!");
  }).catch(function(err) {
      console.error("Algo deu errado: " + err);
  });
}

document.addEventListener("DOMContentLoaded", function() {
  if (copyButton) {
    new bootstrap.Tooltip(copyButton);
  }
});
