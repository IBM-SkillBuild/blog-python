$( document ).ready(function() {
 
 
  $("#aside-ctrl").click(function () {
    window.scrollTo(0, 0);
    if ($('#aside-ctrl').is(':checked')) {
        $('html, body').css({
          overflow: 'hidden',
          height: '100%',
        });
      cargar_aside_tags();
      $('html, body').css({
        overflow: 'auto',
        height: 'auto',
      });
 
           
    
       
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
       $('#aside-ctrl').prop('readonly', false);
       $('#search').prop('readonly', false);
      
    },
  });

}

function buscar_tag(tag) {
  $('#search').val(tag.toLowerCase().trim().replace('{"', '').replace('}"', '').replace('"', ''));
  $('#aside-ctrl').prop('readonly', true);
  $('#search').prop('readonly', true);
  buscar()
 
}