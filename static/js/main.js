
$(document).ready(function() {
  $("p").click(function(event) {
    let text = document.getElementById('url-clip').innerHTML;
    const copyContent = async () => {
      try {
        await navigator.clipboard.writeText(text);
        console.log('Content copied to clipboard');
      } catch (err) {
        console.error('Failed to copy: ', err);
      }
    }
     
  });
});

function portapapeles(id) {
  navigator.clipboard
    .writeText(id)
    .then(() => {
      console.log('Texto copiado al portapapeles');
    })
    .catch((err) => {
      console.error('Error al copiar al portapapeles:', err);
    });
}

function publicacion(source) {
  $('#publicacion').attr('src', source);
  $('#publicacion').css('overflow', 'hidden');
  $('#publicacion').show();
  $('#publicacion').css('width', '100%');
  $('#publicacion').css('height', '6000');
  $('#publicacion').css('margin-top', 200);
  let reducir = 200;
  $('html, body').animate(
    {
      scrollTop: $('#publicacion').offset().top - reducir,
    },
    1000,
  );
  
}


function datos() {
  url="/publicaciones"
    $.ajax({
      type: 'GET',
      url: url,
      data: { modo: reset },
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      cache: false,
      success: function (result) {
       if (reset == 'reset') $('#contenido').html(result);
       $('#contenido').append(result.htmlresponse);
      },
    });
}

