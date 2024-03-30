;(function( CategoriaProductoCtr, $, undefined ){

	/*****************************************************************************************************
	 */
	CategoriaProductoCtr.crearHandsontable = function(){
	    var
          container = document.getElementById('categorias'),
          lista_categorias;

        var nota_validator_fn = function (value, callback) {
        	if(isNaN(value)){
        		alert("Error de Ingreso: el campo codigo acepta solo numeros.");
        		callback(false);
        	}
        };

        lista_categorias = new Handsontable(container, {
          data: [],
          dataSchema: {codigo_categoria: null, descripcion_categoria: null, predeterminado: null},
          startRows: 15,
          startCols: 2,
          colHeaders: ['CODIGO','DESCRIPCION', 'PREDETERMINADO'],
          columns: [
            {data: 'codigo'},
            {data: 'descripcion'},
            {data: 'predeterminado'},

          ],
          columnSorting: true,
          minSpareRows: 1,
          colWidths: [100, 600, 100],
          rowHeaders: true,
          currentRowClassName: 'currentRow',
          currentColClassName: 'currentCol',
          autoWrapRow: true,
          contextMenu: true,
        });

        return lista_categorias;
	};

	/*****************************************************************************************************
	 */
	CategoriaProductoCtr.guardarDatos = function( datos, url ){
	    if(confirm("Esta seguro de guardar esta lista de categorias?")){
    	  $.ajax({
    		url: url,
    		data: 'data='+JSON.stringify(datos),
    		type: 'POST',
    		success: function (res) {
    		  if (res.exito == 1) {
    			alert('Categoria agregada correctamente.');
    			window.location.assign("http://ec2-54-183-111-26.us-west-1.compute.amazonaws.com:8000/inventario/categoria-producto/")
    		  }
    		  else {
    		   console.log(res);
    		   alert('Ocurrio un error, por favor vuelva a intentarlo');
    		  }
    		},
    		error: function (res) {
    			console.log(res);
    			alert('Ocurrio un error, por favor vuelva a intentarlo');
    		}
    	  });
    	}
	};

}( window.CategoriaProductoCtr = window.CategoriaProductoCtr || {}, jQuery ));