var files;
$(document).ready(function() {
    $(document).on({
        ajaxStart: function() { $('body').addClass("loading");    },
        ajaxStop: function() { $('body').removeClass("loading"); }
    });

    $('#id_asignatura').multiSelect({
      selectableHeader: "<div class='custom-header'>Materias disponibles</div>",
      selectionHeader: "<div class='custom-header'>Materias del paralelo</div>",
    });

    $(document).on('click', '.btn-ajax-form', function() {
      $('body').addClass("loading");
    });
    
 
    //========= List table Print2 =========
    $(document).on('click', 'a.print-data', function() {
      printTableData();
      return false;
    });

    //========= Tooltip, Chosen, Datepicker =========
    $("a, abbr, button").tooltip();
    //$("select").chosen({allow_single_deselect: true, width: "100%"});

    $("#id_fecha_nacimiento").mask("99/99/9999",{placeholder:"dd/mm/yyyy"});
    $("#id_movil").mask("0999999999");
    $("#id_cedula").mask("9999999999");
    $('#id_telefono').mask('(09) 999-9999');

    /*$("input[name*='fecha']").datetimepicker({
      language: "es",
      pickTime: false,
    });*/
    $("input[name*='date'], input[name*='_at']").datetimepicker({
      language: "es",
    });

    $(document).on('change', '#id_unidad_educativa', function() {
        ToolsCtr.getDetalleUE( $(this).val() );
        return false;
    });
    $(document).on('change', '#id_nivel', function() {
        ToolsCtr.getNivelUE( $(this).val() );
        return false;
    });
    ToolsCtr.guardarParalelo();

    $(document).on('click', '#btn-editar', function() {
        $('.editar').addClass('hide');
        $('.editar-form').removeClass('hide');
        return false;
    });

});
function printTableData(){
  var data  = "<head>" + $('head').html() + "</head>" + $('.col-main').html();
	var winPrint = window.open("");
	winPrint.document.write(data);
	winPrint.print();
	winPrint.close();
}
function toggleArrow(obj,add,remove){
   $(obj).find('.arrow-collapse').removeClass(remove)
                                  .addClass(add);
}
function actionCheckbox(){
  var num_selected = $( ".table tr td.action-checkbox input:checked" ).length;

  $('.table tr td.action-checkbox input').on('change', function () {
    checkRow(this);
  });

  $('.table #action-toggle input').on('click', function () {
    var check_row = $(this).is(':checked');
    $('.table tr td.action-checkbox input').each(function() {
      if(check_row){
        this.checked = true;
        checkRow(this);
      }else{
        this.checked = false;
        checkRow(this);
      }
    });
  });
}
function checkRow(obj){
  if($(obj).is(':checked')){
    $(obj).closest('tr').addClass('warning');
  }else{
    $(obj).closest('tr').removeClass('warning');
  }
  num_selected = $( ".table tr td.action-checkbox input:checked" ).length;
  if(num_selected <= 0){
    num_selected = "";
    $(".form-actions .btn").addClass("disabled");
  }else{
    $(".form-actions .btn").removeClass("disabled");
  }
  $(".num_select").text(num_selected);
}
function actionFormList(url_action,target){
  if(target){
    $("#form-list").attr("target", "_black");
  }
  $("#form-list").attr("action", url_action);
  $("#form-list").submit();
}
function eliminarFila(obj) {
  var url = $(obj).attr("href");
  var id_row = $(obj).data("id");
  $.ajax({
    url:url,
    success:function(){
      $("#row-"+id_row).hide('slow');
      $("#row-"+id_row).remove();
    },
    error: function(){
      alert("Ocurrio un Error Vuelva a Intentarlo");
    }
  });
  return false;
}
function activarDesactivarFila(obj,flag) {
  var $obj = $(obj);
  var url = $obj.attr("href");
  var id_row = $obj.data("id");
  var src_img = "/static/admin/img/icon-yes.gif";
  $.ajax({
    url:url,
    success:function(){
      var $row = $("#row-"+id_row);
      $row.find("#activar-user").toggleClass("hidden");
      $row.find("#desactivar-user").toggleClass("hidden");

      if(flag){
        alert("Usuario Activado");
      }else{
        alert("Usuario Desactivado"); src_img = "/static/admin/img/icon-no.gif";
      }

      $row.find(".is_active img").attr("src",src_img);

    },
    error: function(){
      alert("Ocurrio un Error Vuelva a Intentarlo");
    }
  });
  return false;
}
function today(){
  var d = new Date();

  var month = d.getMonth()+1;
  var day = d.getDate();

  var output =  ((''+day).length<2 ? '0' : '') + day + '/' +
    ((''+month).length<2 ? '0' : '') + month + '/' +
    d.getFullYear();
  return output;
}
