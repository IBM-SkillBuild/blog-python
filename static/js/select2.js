

$(document).ready(function () {
 
  $('.categorias').select2({
    placeholder: 'Selecciona categoria',
    allowClear: true,
    tags: true,
   
  });
 
 



  $('#update-form').on('submit', function () {
   
    var text = $('#categorias option:selected')
      .toArray()
      .map((item) => item.text)
      .join();
   
    $('#tags').val(text);
    return true
  });





 
  function mostrar_opciones() {
    $('#categorias').select2('open');
  }

})