const openMobileMenuBtn = document.querySelector('.device-menu');
const headerMenu = document.querySelector('.header-nav');
 
$(document).ready(function () {
   $('.device-menu').css('display', 'none');
  $('p').click(function (event) {
    let text = document.getElementById('url-clip').innerHTML;
    const copyContent = async () => {
      try {
        await navigator.clipboard.writeText(text);
        console.log('Content copied to clipboard');
      } catch (err) {
        console.error('Failed to copy: ', err);
      }
    };
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
  $('#publicacion').css('margin-top', 200);
  let reducir =10;
  $('html, body').animate(
    {
      scrollTop: $('#publicacion').offset().top - reducir,
    },
    1000,
  );
}

openMobileMenuBtn.addEventListener('click', () => {
  if (openMobileMenuBtn.classList.contains('open')) {
    openMobileMenuBtn.classList.remove('open');
    headerMenu.classList.remove('active');
  } else {
    headerMenu.classList.add('active');
    openMobileMenuBtn.classList.add('open');
  }
});

function mostrar_menu() {
  
  if (openMobileMenuBtn.classList.contains('open')) {
    openMobileMenuBtn.classList.remove('open');
    headerMenu.classList.remove('active');
  } else {
    headerMenu.classList.add('active');
    openMobileMenuBtn.classList.add('open');
  }
}

$(window).scroll(function () {
  if ($(this).scrollTop() > 300) {
    $('a.scroll-top').fadeIn('slow');
     $('.device-menu').css('display', 'block');
  } else {
    $('a.scroll-top').fadeOut('slow');
   
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
    lightbox.show();
  }),
);

function resizeIframe(obj) {
  obj.style.height =
    obj.contentWindow.document.documentElement.scrollHeight + 155 + 'px';
}

$(window).resize(function () {
  if (screen.width < 758) {
    $('.device-menu').css('display', 'block');
  } 
  else {
    $('.device-menu').css('display', 'none');
  }
});