$('#empresa_session').on('change', function () {
    //alert("Entro" ); // or $(this).val()
    var id = $("#empresa_session option:selected").val();
    var value = $("#empresa_session option:selected").text();
    //alert(id);
    $.ajax({
        url: "/config/modificarEmpresa/", // the endpoint
        type: "POST", // http method
        data: {id: id, 'csrfmiddlewaretoken': '{{ csrf_token }}', texto: value},
        success: function (data) {
            alert("Esta trabajando con la empresa " + data);

        },
        error: function () {
            alert("Escoja una empresa");
        },
    });
});


$('[data-click=panel-reload-message]').click(function (e) {
    e.preventDefault();
    var target = $(this).closest('.panel');
    if (!$(target).hasClass('panel-loading')) {
        var targetBody = $(target).find('.panel-body');
        var spinnerHtml = '<div class="panel-loader"><span class="spinner-small"></span></div>';
        $(target).addClass('panel-loading');
        $(targetBody).prepend(spinnerHtml);
        setTimeout(function () {
            $(target).removeClass('panel-loading');
            $(target).find('.panel-loader').remove();
        }, 2000);
    }

    $.ajax({
        url: "/login/getMessages/", // the endpoint
        type: "POST", // http method
        data: {'csrfmiddlewaretoken': '{{ csrf_token }}'},
        success: function (data) {

            var messages = jQuery.parseJSON(data);
            var html = '';
            $.each(messages, function(idx, obj) {
                msg=obj.fields;
                html += '<li class="media media-sm"> <div class="media-body">' +
                    '<h5 class="media-heading">'+msg.titulo+'</h5>' +
                    '<p>'+msg.mensaje+'</p></div>' +
                    '</li>';
            });
            $('#user-messages').html(html);

        },
        error: function (xhr, status, error) {
            var err = eval("(" + xhr.responseText + ")");
            alert(err.Message);
        },
    });


});

$( document ).ready(function() {
    $('[data-click=panel-reload-message]').click();
});