/*
 Project Name: CENSEA PROJECT
 Version: 1
 Author: Gabriel Paladines
 Website: http://www.gaphit.com
 /var/cesadesign/static/color_admin/assets/js/censea.js
 */

/* BEGIN RRHH BLOCK */



/* END RRHH BLOCK */

/*
 Function: tipo_solicitud_new
 Created at: 2016-08-17
 */
var delay = 1000; //1 second


$().ajaxSend(function (r, s) {
    $("#page-loader").show();
});

$().ajaxStop(function (r, s) {
    $("#page-loader").fadeOut("slow");
});

//TIMEPICKER
$(function () {
    "use strict";
    $('#id_hora_desde').timepicker(
        {
            "showMeridian":false,
            "minuteStep":30,
        }
    );
});

$(function () {

    "use strict";
    $('#id_hora_hasta').timepicker(
        {
            "showMeridian":false,
            "minuteStep":30,
        }
    );
});







$(function () {
    $('#fecha_desde_hasta').daterangepicker({
        locale: {
            "format": "YYYY-MM-DD",
            "separator": " - ",
            "applyLabel": "Aplicar",
            "cancelLabel": "Cancelar",
            "fromLabel": "Desde",
            "toLabel": "Para",
        },
    });
});


$(document).ready(function () {

    var hora_desde;
    var minuto_desde;
    var hora_hasta;
    var minuto_hasta;
    var h_desde;
    var h_hasta;

    clearFormSolicitud();

    $('#id_tipo_solicitud').change(function () {

        tipo_id = $('#id_tipo_solicitud').val();

        if (tipo_id == '1') {
            $('#create-title').html('SOLICITUD DE PERMISO');
            clearFormSolicitud();
            $('.permiso').css("display","block");
        }
        else if (tipo_id == '2') {
            $('#create-title').html('SOLICITUD DE VACACIONES');
            clearFormSolicitud();
            $('.vacaciones').css("display","block");
        }
        else if (tipo_id == '3') {
            $('#create-title').html('SOLICITUD DE AUTORIZACION');
            clearFormSolicitud();
            $('.autorizaciones').css("display","block");
        } else {
            $('#create-title').html();
            clearFormSolicitud();
        }

    });


//DATERANGEPICKER

    $('#fecha_desde_hasta').on('apply.daterangepicker', function (ev, picker) {
        fecha_desde = picker.startDate.format('YYYY-MM-DD');
        fecha_hasta = picker.endDate.format('YYYY-MM-DD');
        var dias = diferenciaFechas(fecha_desde, fecha_hasta,"dias");

        $("#id_total_dias_ausencia").val(dias);
        $("#total_dias_gozados").val(dias);
    });

    //TIMEPICKER VALIDATION
    $('#id_hora_desde').timepicker().on('hide.timepicker', function(e) {

                h_desde= e.time.value;
                hora_desde = e.time.hours;
                minuto_desde = e.time.minutes;
                document.getElementById('id_hora_hasta').value = "";

    });

    $('#id_hora_hasta').timepicker().on('hide.timepicker', function(e) {

                h_hasta= e.time.value;
                hora_hasta = e.time.hours;
                minuto_hasta = e.time.minutes;

                if (hora_desde < hora_hasta || (hora_desde == hora_hasta && minuto_desde < minuto_hasta)) {

                    var horas = diferenciaFechas("1986-04-07 "+h_desde, "1986-04-07 "+h_hasta,"horas");
                    $("#id_total_horas_ausencia").val(horas);
                    $("#id_total_horas_laboradas").val(horas);

                }else{
                    document.getElementById('id_hora_hasta').value = "";
                    document.getElementById('id_total_horas_ausencia').value = "";
                    $.gritter.add({
                        title: 'Ingreso de horas',
                        text: 'Por favor ingrese una hora menor a la anterior.'
                    });
                }



    });



});

//SUBMIT BUTTONS
$('#post-create').on('submit', function (event) {
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    $('#ts-create').modal('hide');
    create_tipo_solicitud();
});

$('#solicitud-create-form').on('submit', function (event) {
    event.preventDefault();
    create_solicitud();
});


$('#update-solicitud-form').on('submit', function (event) {
    event.preventDefault();
    console.log("form update submitted!")  // sanity check
    $('#update-solicitud').modal('hide');
    update_solicitud();
});




//FUNCTIONS
function create_tipo_solicitud() {
    console.log("create post is working!"); // sanity check
    $.ajax({
        url: "/recursos_humanos/create-tipo-solicitud/", // the endpoint
        type: "POST", // http method
        data: {codigo: $('#codigo').val(), descripcion: $('#descripcion').val()}, // data sent with the post request

        // handle a successful response
        success: function (json) {
            //$('#post-text').val(''); // remove the value from the input

            $.gritter.add({
                title: 'Ingreso exitoso!',
                text: 'Ud. ha agregado un nuevo tipo de solicitud.'
            });

            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            $('#post-create').trigger("reset");
            setTimeout(function () {
                location.reload();
            }, delay);

        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

};


function create_solicitud() {
    console.log("create solicitud is working!"); // sanity check
    var fecha_desde_hasta= $('#fecha_desde_hasta').val();
    var arr = fecha_desde_hasta.split('-');
    var fecha_desde=null;
    var fecha_hasta=null;
    if (fecha_desde_hasta.length == 0) {
fecha_desde=null;
        fecha_hasta=null;

    }else{
    fecha_desde1=arr[0].split('/');
    fecha_hasta1=arr[1].split('/');
   fecha_desde=$.trim(fecha_desde1[2])+'-'+$.trim(+fecha_desde1[0])+'-'+$.trim(fecha_desde1[1])+' 00:00:00';
   fecha_hasta=$.trim(fecha_hasta1[2])+'-'+$.trim(fecha_hasta1[0])+'-'+$.trim(fecha_hasta1[1])+' 00:00:00';
        }
    var optradio = $('input:radio[name=motivoradio]:checked').val();
    var tipo_permiso = $('input:radio[name=optradio]:checked').val();
    var vacaciones_radio = $('input:radio[name=vacacionesradio]:checked').val();





    $.ajax({
        url: "/recursos_humanos/create-solicitud/", // the endpoint
        type: "POST", // http method
        data: {
            tipo: $('#id_tipo_solicitud').val(),
            fecha: $('#id_fecha_solicitud').val(),
            empleado: $('#id_empleados_empleado').val(),
            fecha_desde: fecha_desde,
            fecha_hasta: fecha_hasta,
            total_dias_ausencia: $('#id_total_dias_ausencia').val(),

            hora_desde: $('#id_hora_desde').val(),
        hora_hasta: $('#id_hora_hasta').val(),
        total_horas_ausencia: $('#id_total_horas_ausencia').val(),
            total_horas_laboradas: $('#id_total_horas_laboradas').val(),
            vacaciones_radio:vacaciones_radio,
            total_dias_gozados:$('#total_dias_gozados').val(),
            total_dias_pendientes:$('#id_total_dias_pendientes').val(),
            periodo_dias_pendiente:$('#id_periodo_dias_pendiente').val(),

        optradio : optradio,
        tipo_permiso: tipo_permiso,

        cargo_vacaciones : $('#id_cargo_vacaciones').val(),
        observacion: $('#id_observacion').val()

        }, // data sent with the post request

        // handle a successful response
        success: function (json) {

            $.gritter.add({
                title: 'Ingreso exitoso!',
                text: 'Ud. ha agregado una nueva solicitud.'
            });

            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            alert(json['result']);
            $('#solicitud-create-form').trigger("reset");
            setTimeout(function () {
                location.reload();
            }, delay);

        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

};



function update_solicitud() {

    console.log("update solicitud is working!"); // sanity check
    $("#update-solicitud").modal();
    $.ajax({
        url: "/recursos_humanos/update-solicitud/", // the endpoint
        type: "POST", // http method
        data: {id: $('#field-id').val(), estado: $('#id_activo').val()}, // data sent with the post request

        // handle a successful response
        success: function (json) {

            $.gritter.add({
                title: 'Notificación del Sistema',
                text: 'Ud. ha modificado el estado de una  solicitud.'
            });

            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            alert(json['result']);
            setTimeout(function () {
                location.reload();
            }, delay);

        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

};

function clearFormSolicitud(){

    $('.permiso').css("display","none");
    $('.vacaciones').css("display","none");
    $('.autorizaciones').css("display","none");

}


$(function () {
    "use strict";
    $('.hora_inicio').timepicker(
        {
            "showMeridian":false,
            "minuteStep":30,
        }
    );
});

$(function () {
    "use strict";
    $('.hora_fin').timepicker(
        {
            "showMeridian":false,
            "minuteStep":30,
        }
    );
});