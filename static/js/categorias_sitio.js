$( document ).ready(function() {
 
 
  $("#aside-ctrl").click(function () {
    if ($('#aside-ctrl').is(':checked')) {
    cargar_aside_tags()
    }
});
 

});








function cargar_aside_tags() {
  $.ajax({
    type: 'GET',
    url: '/aside_categorias',
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    cache: false,
    success: function (result) {
      console.log(result)
      $('#aside-contenido').html('');
      $('#aside-contenido').append(result.htmlresponse);
      
    },
  });

}

function buscar_tag(tag) {
  $('#search').val(tag.toLowerCase().trim().replace('{"', ''));
   $('#aside-ctrl').click()
  buscar()
}