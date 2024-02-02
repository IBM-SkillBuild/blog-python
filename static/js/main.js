  


const search = document.querySelector('.search-bar-container');
const magnifier = document.querySelector('.magnifier');
   window.onload = function() {
    $('.aside-ctrl--reset').css({
      witdh: '0%',
    });
       
     
      document.body.addEventListener('click', (e) => {
        if (!search.contains(e.target)) {
          search.classList.remove('active');
        }
      });
   
   
   
     // $('.device-menu').css('display', 'none');
   
    
    
      
    
    const micIcon = document.querySelector('.mic-icon');
    const input = document.querySelector('.input');
    const listItem = document.querySelector('.voice-text');
     const recognition = new webkitSpeechRecognition() || SpeechRecognition();
     const openMobileMenuBtn = document.querySelector('.device-menu'); 
     const headerMenu = document.querySelector('.header-nav');



     openMobileMenuBtn.addEventListener('click', () => {
         
     $('html, body').animate({ scrollTop: scroll + 'px' }, 50);
     if (openMobileMenuBtn.classList.contains('open')) {
       openMobileMenuBtn.classList.remove('open');
       headerMenu.classList.remove('active');
       $('#barra-busqueda').attr('style', 'display: none !important');
     } else {
       headerMenu.classList.add('active');
       openMobileMenuBtn.classList.add('open');
       $('#barra-busqueda').attr('style', 'display: block !important');
     }
   });
  
    
   
  
    micIcon.addEventListener('click', () => {
      recognition.start();

      recognition.onresult = (e) => {
        const result = event.results[0][0].transcript;
        input.value = result;
        buscar();
      };
      input.value = '';

      recognition.onerror = (event) => {
        alert('Speech recognition error: ' + event.error);
      };
    });

 $(input).keypress(function (ev) {
   var keycode = ev.keyCode ? ev.keyCode : ev.which;
   if (keycode == '13') {
     buscar();
   }
 });
  
  

    }

    function portapapeles(id) {
      navigator.clipboard
        .writeText(id)
        .then(() => {
          console.log('Texto copiado al portapapeles');
          console.log(id);
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
      //$('#publicacion').css('margin-top', 200);
      let reducir = 10;
      $('html, body').animate(
        {
          scrollTop: $('#publicacion').offset().top - reducir,
        },
        1000,
      );
    }

   

  

$(window).scroll(function () {
     
      scroll = window.scrollY;
      if ($(this).scrollTop() > 100) {
        $('a.scroll-top').fadeIn('slow');
        $('.device-menu').css('display', 'block');
        $('.info').css('display', 'none');
      } else {
        $('a.scroll-top').fadeOut('slow');
        $('.info').css('display', 'block');
        $('.device-menu').css('display', 'none');
      }
    });
    $('a.scroll-top').click(function (event) {
      event.preventDefault();
      $('html, body').animate({ scrollTop: 0 }, 600);
    });

    document.querySelectorAll('.my-lightbox-toggle').forEach((el) =>
      el.addEventListener('click', (e) => {
        e.preventDefault();
        const lightbox = new Lightbox(el, options);
        if (window.screen.width > 1100) {
          lightbox.show();
        }
    
      }),
    );

  

    $(window).resize(function () {
      if (screen.width < 758) {
        $('.device-menu').css('display', 'block');
      }
      else {
        $('.device-menu').css('display', 'none');
      }
    });



    function buscar() {

      $.ajax({
        type: 'GET',
        url: '/consulta-categorias',
        data: {
          mibusqueda: $('#search').val(),
        },
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        cache: false,
        success: function (result) {
       
          $('#contenido').html('');
          $('#contenido').append(result.htmlresponse);
          $('#search').val("");
          $('html, body').css({
            overflow: 'auto',
            height: 'auto',
          });
          var el = document.getElementById('search');
          if (typeof el.selectionStart == 'number') {
            el.selectionStart = el.selectionEnd = el.value.length;
          } else if (typeof el.createTextRange != 'undefined') {
            var range = el.createTextRange();
            range.collapse(false);
            range.select();
          }
     
    

        },
      });
    }




    document.body.addEventListener('click', (e) => {
      if (!search.contains(e.target)) {
        search.classList.remove('active');

      }
    });


function mostrar_menu() {
  openMobileMenuBtn = document.getElementById('device-menu');
  headerMenu = document.querySelector('.header-nav');
       $('html, body').animate({ scrollTop: scroll + 'px' }, 50);
       if (openMobileMenuBtn.classList.contains('open')) {
         openMobileMenuBtn.classList.remove('open');
         headerMenu.classList.remove('active');
         $('#barra-busqueda').attr('style', 'display: inline-flex !important');
       } else {
         headerMenu.classList.add('active');
         openMobileMenuBtn.classList.add('open');
         $('#barra-busqueda').attr('style', 'display: none !important');
       }
}
     
  magnifier.addEventListener('click', (e) => {
    search.classList.toggle('active');
    e.stopPropagation();
    $(input).focus();
    if (!$(search).hasClass('active')) {
      buscar();
    }
  });