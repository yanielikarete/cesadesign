$(document).ready(function(){

  $(window).scroll(function() {
    if($(this).scrollTop() !== 0) {
      $('#toTop').fadeIn();
      //$('#navbar').removeClass('bg-blue-light');
    } else {
      $('#toTop').fadeOut();
      //$('#navbar').addClass('bg-blue-light');
    }
  });

  $(document).on('click', '#toTop', function() {
    $('body,html').animate({scrollTop:0},800);
  });

  $(".perfiles .btn").tooltip();

  // Contact Form
  $("#form-contact").submit(function(e){
    e.preventDefault();
    var name = $("#inputNombre").val();
    var email = $("#inputEmail").val();
    var mensaje = "";

    var dataString = 'name=' + name + '&email=' + email;

    if( name === "" ){
      mensaje += "Ingrese un nombre en el formulario.<br />";
    }
    if( isValidEmail(email) ){
      mensaje += "E-mail debe ser válido.<br />";
    }

    if ( mensaje === "" ){
      var img_ajax = $('.ajax-loader');
      var btn_ajax = $('.ajax-btn');

      img_ajax.css('visibility','visible');
      btn_ajax.addClass('disabled');
      $.ajax({
        type: "POST",
        url: "mail.php",
        data: dataString,
        success: function(){
          msj("Tu mensaje ha sido enviado con éxito.","alert-danger","alert-success");
          limpiarForm();
        },
        complete: function(){
          img_ajax.css('visibility','hidden');
          btn_ajax.removeClass('disabled');
        }
      });
    }
    else{
      msj(mensaje,"alert-success","alert-danger");
    }

    return false;
  });

  // Contact Form
  $("#id_provincia").change(function(e){
    var id_provincia = $(this).val();
    $.ajax({
        type: "GET",
        url: "/registro/ajax/ciudad/?provincia_id="+id_provincia,
        success: function(data){
          $('#ciudad-content').html(data);
        },
        error: function(data){
          alert("Ocurrio un error, vuelva a intentarlo.");
        },
    });

    return false;
  });

});

function msj(data,ocultar,mostrar){
  $('#msj span').html(data);
  $('#msj')
    .removeClass(ocultar)
    .addClass(mostrar)
    .removeClass('hide');
}
function isValidEmail(emailAddress) {
  var pattern = new RegExp(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3,4})+$/);
  return pattern.test(emailAddress);
}
function limpiarForm(){
  $("#inputNombre").val("");
  $("#inputEmail").val("");
}