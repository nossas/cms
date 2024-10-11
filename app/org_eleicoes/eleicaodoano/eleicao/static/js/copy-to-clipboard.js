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
      var successful = document.execCommand('copy');
      var msg = successful ? 'URL copiada!' : 'Falha ao copiar URL';
      console.log(msg);
  } catch (err) {
      console.error('Algo deu errado: ' + err);
  }
  document.body.removeChild(textArea);
}
