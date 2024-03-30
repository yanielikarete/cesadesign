;(function( ToolsCtr, $, undefined ){

	/*****************************************************************************************************
	 */
	ToolsCtr.getDetalleUE = function (id) {
	    if( id == "" || id == undefined){ id = 0}
		$.ajax({
			url: '/docente/configuracion/unidad-educativa/'+id+'/detalle/',
			success:function( data ){
				$('#ue-nombre').text( data.nombre );
				$('#ue-logo').attr('src', data.logo);
				$('#detalle-ue').removeClass('hide');
			},
			error: function(){
			    $('#detalle-ue').addClass('hide');
				alert( "Oh No!\nAlgo extraño sucedió, por favor vuelva a intentarlo.");
			},
		});

	};

	/*****************************************************************************************************
	 */
	ToolsCtr.getNivelUE = function (id) {
	    if( id == "" || id == undefined){ id = 0}
		$.ajax({
			url: '/docente/configuracion/nivel/'+id+'/detalle/',
			success:function( data ){
                $('#form-grado').html( data );
			},
			error: function(){
				alert( "Oh No!\nAlgo extraño sucedió, por favor vuelva a intentarlo.");
			},
		});
	};

	/*****************************************************************************************************
	 */
	ToolsCtr.setConfiguracion = function () {
	    var id_curso = $('#id_curso').val();
	    var nombre_paralelo = $('#id_nombre').val();
		$.ajax({
			url: '/docente/configuracion-inicial/'+id_curso+'/'+nombre_paralelo+'/',
			success:function( data ){
                $('#configuracion-inicial').html( data );
			},
			error: function(){
				alert( "Oh No!\nAlgo extraño sucedió, por favor vuelva a intentarlo.");
			},
		});
	};

	/*****************************************************************************************************
	 */
	ToolsCtr.guardarParalelo = function(){
        $(".ajax-form-paralelo").submit(function(e){
            e.preventDefault();
            var postData = $(this).serializeArray();
            var formURL = $(this).attr("action");
            $('.btn-ajax-form').attr("disabled",true);
            $.ajax({
                url : formURL,
                type: "POST",
                data : postData,
                success:function(data, textStatus, jqXHR){
                    $('.btn-ajax-form').attr("disabled",false);
                    $('#form-paralelo').modal('hide');
                    var nombre_paralelo = $("#form-paralelo #id_nombre").val();
                    $("#lista-paralelos tbody").append('<tr><td>'+nombre_paralelo+'<a class="pull-right btn btn-danger" title="Eliminar paralelo"><i class="fa fa-trash-o"></i> Borrar</a></td></tr>');
                    alert("Paralelo agregado!");
                },
                error: function(jqXHR, textStatus, errorThrown){
                    alert("Oh No!\nAlgo extraño sucedió, por favor vuelva a intentarlo.");
                    $('.btn-ajax-form').attr("disabled",false);
                }
            });
        });
    };

}( window.ToolsCtr = window.ToolsCtr || {}, jQuery ));