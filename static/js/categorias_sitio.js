// javascript para el comportamiento del aside
$(document).ready(function () {
 
 // en el caso de pusar el boton flecha para abrir aside
  $("#aside-ctrl").click(function () {
    window.scrollTo(0, 0);
    if ($('#aside-ctrl').is(':checked')) {
        $('html, body').css({
          overflow: 'hidden',
          height: '100%',
        });
      // aqui se quita el ancho del aside para cuando esté oculto
      // es para evitar gestos del movil que puden enseñarlo
      // a pesar de estar oculto
        $('.aside-ctrl--reset').css({
          witdh: '0%',
        });
      // se llamar a funcion ajax (python) peticion de datos
      // e inyeccion de codigo para motrar contenido del aside
      cargar_aside_tags();
      $('html, body').css({
        overflow: 'auto',
        height: 'auto',
      });
        
    
      // este caso es para eliminar temporalmente el tamaño del aside
      // ya que al estar oculto no precisa ancho alguno en css
      // esto mejora la experiencia en el comportamiento de moviles
      // ya que estos hacen gestos y podrian mostralo vacio.
    } else {
        $('.aside-ctrl--reset').css({
          witdh: '0%',
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
      // inyectamos pieza codigo en aside
      $('#aside-contenido').html('');
      $('#aside-contenido').append(result.htmlresponse);
      // nos aseguramos del ancho del aside para ver resultados
       $('aside-ctrl--reset').css({
         overflow: 'hidden',
         witdh: '100%',
       });
       
      
    },
  });

}

function buscar_tag(tag) {
  $('#search').val(tag.toLowerCase().trim().replace('{"', '').replace('}"', '').replace('"', ''));
  
  buscar()
 
}