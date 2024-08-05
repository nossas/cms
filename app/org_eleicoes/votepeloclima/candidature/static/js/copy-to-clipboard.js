function copyURL() {
  var url = window.location.href;
  var modalString = "?modal=true";

  // Verifica se a URL contém "?modal=true" e remove, se necessário
  if (url.includes(modalString)) {
      url = url.replace(modalString, "");
  }

  // Criando um elemento fantasma na DOM pra copiar a URL a partir dele. A API Clipboard só funciona quando tem HTTPS ou localhost.
  var textArea = document.createElement("textarea");

  textArea.value = url;
  document.body.appendChild(textArea);
  textArea.select();
  try {
      var copyButton = document.querySelector("#copyButton");
      var tooltip = bootstrap.Tooltip.getInstance(copyButton) || new bootstrap.Tooltip(copyButton);
      tooltip.show();
      setTimeout(function() {
        tooltip.hide();
      }, 2000);

      console.log("URL copiada!");
  } catch (err) {
      console.error("Algo deu errado: " + err);
  }
  document.body.removeChild(textArea);
}
