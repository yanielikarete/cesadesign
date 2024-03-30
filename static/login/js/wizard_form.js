$(function() {
  $(".bs-wizard").bs_wizard({
    nextText: "Siguiente",
    backText: "Volver",
    nextClasses: "btn btn-info",
    backClasses:" btn btn-default",
    beforeNext: before_next
  });
  $('#last-back').click($(".bs-wizard").bs_wizard('go_prev'));
  $('#configuracion').validate_popover({
    popoverPosition: 'top',
    onsubmit: false,
    rules: {
      'unidad_educativa': {
        required: true,
      },
      'nivel': {
        required: true,
      },
      'curso': {
        required: true,
      },
      'nombre': {
        required: true,
      },
    },
    messages: {
      unidad_educativa: "Por favor llene este campo",
      nivel: "Por favor llene este campo",
      curso: "Por favor llene este campo",
      nombre: "Por favor llene este campo",
    }
  });

  $(".submit-btn").click(function(ev) {
    ev.preventDefault();

    return false;
  });

  function validate_fields(fields, step) {
    var error_step, field, _i, _len;
    for (_i = 0, _len = fields.length; _i < _len; _i++) {
      field = fields[_i];
      if (!form_validator().element(field)) {
        error_step = step;
      }
    }
    return error_step != null ? error_step : true;
  }

  function form_validator() {
    return $('#configuracion').validate();
  }

  function current_step() {
    return $(".bs-wizard").bs_wizard('option', 'currentStep');
  }

  function before_next() {
    if (current_step() == 1){
      if (validate_fields($('#id_unidad_educativa,#id_nivel'), 1) === true){
        return  true;
      }else{
        return false;
      }
    }else{
        if (validate_fields($('#id_curso, #id_nombre'), 2) === true){
            ToolsCtr.setConfiguracion();
            return  true;
         }else{
            return false;
         }
    }
  }

  $(window).resize(function() {
      $.validator.reposition();
  });

});