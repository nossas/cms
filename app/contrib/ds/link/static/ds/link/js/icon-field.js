$(function(){
  // Custom Label on Icon Select
  function formatState (state) {
    if (!state.id) {
      return state.text;
    }

    var $state = $(
      '<span><i class="bi bi-' + state.element.value.toLowerCase() + '"></i> ' + state.text + '</span>'
    );
    return $state;
  };
  
  $("[name='icon']").select2({
    templateResult: formatState
  });
});