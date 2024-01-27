$(document).ready(function () {
 
  $('.categorias').select2({
    placeholder: 'Selecciona categoria',
    allowClear: true,
    tags: true,
   
  });

 
});

 $('#categorias').on('select2:select', function (e) {
  
   let text = $(this).val().toString();
     
   $('#tags').val(text);
 });


