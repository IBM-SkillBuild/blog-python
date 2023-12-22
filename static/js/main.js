
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

function publicacion(source) {
  $('#publicacion').attr('src', source);
  $('#publicacion').css('overflow', 'hidden');
  $('#publicacion').show();
  $('#publicacion').css('width', '100%');
  $('#publicacion').css('height', '2000');
  $('#publicacion').css('margin-top', 200);
  let reducir = 200;
  $('html, body').animate(
    {
      scrollTop: $('#publicacion').offset().top - reducir,
    },
    1000,
  );
}
