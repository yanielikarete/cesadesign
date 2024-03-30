/***************************************
JavaScript para Dashboard
Version: 1.0 - 2014
author: @jbravot (jonathan Bravo)
email: info@jonathanbravo.com
web: jonathanbravo.com
****************************************/
var monthNames = ['Enero', 'Febrero', 'Marzo', 'Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
var monthNamesShort = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];
var dayNames = ['Domingo','Lunes','Martes','Mi\u00E9rcoles','Jueves','Viernes','S\u00e1bado'];
var dayNamesWeek = ['Lunes','Martes','Mi\u00E9rcoles','Jueves','Viernes'];
var dayNamesShort = ['Dom','Lun','Mar','Mi\u00E9','Jue','Vie','S\u00e1b'];

$(document).ready(function() {
    
    if(!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
        $(".dashboard .scroll").scroll(function () {
            scrollMovil(this,$(this).parent().data('id'));
        });
    }
    
});

function createRangeDate(){
    $('#dashboard-range').daterangepicker(
    {
      format: 'DD/MM/YYYY',
      locale: {
        applyLabel: 'Aplicar',
        cancelLabel: 'Cancelar',
        fromLabel: 'Desde',
        toLabel: 'Hasta',
        weekLabel: 'S',
        customRangeLabel: 'Seleccionar Fecha',
        firstDay: 0
      },
      ranges: {
         'Hoy': [moment(), moment()],
         'Ayer': [moment().subtract('days', 1), moment().subtract('days', 1)],
         'Últimos 7 Días': [moment().subtract('days', 6), moment()],
         'Últimos 30 Días': [moment().subtract('days', 29), moment()],
         'Mes Actual': [moment().startOf('month'), moment().endOf('month')],
         'Mes Anterior': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
      },
      startDate: moment().subtract('days', 29),
      endDate: moment()
    },
    function(start, end) {
        //console.log("prueba");
    }
  );
}
function createCalendar(url){
    $('#calendario').fullCalendar({
        monthNames: monthNames,
        monthNamesShort: monthNamesShort,
        dayNames: dayNames,
        dayNamesShort: dayNamesShort,
        firstDay: 1,
        buttonText: {
                prev: '&nbsp;&#9668;&nbsp;',
                next: '&nbsp;&#9658;&nbsp;',
                prevYear: '&nbsp;&lt;&lt;&nbsp;',
                nextYear: '&nbsp;&gt;&gt;&nbsp;',
                today: 'hoy',
                month: 'mes',
                week: 'semana',
                day: 'd\u00eda'
        },
        titleFormat: {
                month: 'MMMM yyyy',
                week: "d [ yyyy]{ '&#8212;'[ MMM] d MMM yyyy}",
                day: 'dddd, d MMM, yyyy'
        },
        columnFormat: {
                month: 'ddd',
                week: 'ddd d/M',
                day: 'dddd d/M'
        },
        allDayText: 'todo el dia',
        axisFormat: 'H:mm',
        timeFormat: {
            '': 'H(:mm)',
            agenda: 'H:mm{ - H:m'
        },
        events: url,
        eventClick: function(event) {
                var element = this;
                $(element).popover('destroy');
                $(element).popover({
                    animation: true,
                    html: true,
                    placement: 'top',
                    trigger: 'manual',
                    content:'<i class="close-popover pull-right fa fa-times"></i><h5><b>'+ event.title +'</b></h5><i class="flg fa fa-calendar-o"></i> '+ moment(event.start).format('dddd, D MMMM') + '<br><span class="fsm fcg"><i class="flg fa fa-user"></i> '+ event.user +'</span><br><hr><a href="'+ event.urlView +'" target="_black" class="pull-left btn btn-link">Ver Detalle</a><a href="'+ event.urlEdit +'" target="_black" class="pull-right btn btn-link">Editar '+ event.tipo +'</a>',
                });
                $(element).popover('show');
                $(document).on('click', function(e) {
                    $(element).popover('destroy');
                });
                $(".close-popover").on('click', function(e) {
                    $(element).popover('destroy');
                });

                return false;
        },
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        editable: false,
        loading: function(bool) {
            if (bool){
                $('#calendar-refresh i').addClass('fa-spin');
            }
            else{
                $('#calendar-refresh i').removeClass('fa-spin');
            }
        }
    });
}
function getCalendar(url){
    $('#calendario').fullCalendar('removeEvents');
    $('#calendario').fullCalendar('addEventSource', url);
}
function getHtmlTareas(obj){
    var html =  '<li class="clearfix">'+
                '<a target="_black" class="clearfix" href="'+ obj.urlView +'" >'+
                    '<div class="text-dash-list pull-left">'+
                        obj.title +
                        '<div class="fsm fcg"><span><i class="flg fa fa-user"></i> '+ obj.user +'</span></div>'+
                    '</div>'+
                    '<div class="text-2-dash-list pull-right">'+
                        moment(obj.end).format('DD MMM') +
                    '</div>'+
                '</a>'+
            '</li>';
    return html;
}
function getHtmlOportunidad(obj){
    var html =  '<li class="clearfix">'+
                '<a target="_black" class="clearfix" href="'+ obj.urlView +'" >'+
                    '<div class="text-dash-list pull-left">'+
                        obj.name +
                        '<div class="fsm fcg"><span><i class="flg fa fa-user"></i> '+ obj.user +'</span></div>'+
                    '</div>'+
                    '<div class="text-2-dash-list pull-right">'+
                        obj.data +
                    '</div>'+
                '</a>'+
            '</li>';
    return html;
}
function getHtmlObject(obj){
    var html =  '<li class="clearfix">'+
                    '<div class="text-dash-list pull-left">'+
                        obj.name +
                    '</div>'+
                    '<div class="text-2-dash-list pull-right">'+
                        obj.data +
                    '</div>'+
            '</li>';
    return html;
}
function getObjectList(url,id,object){
    $('#'+id+'-refresh i').addClass('fa-spin');
    $('#'+id+' .obj-list').html("");
    $.getJSON(url, function(data) {
        $('#'+id+' .badge').text(data.length);
        $.each(data, function(){
            var html_item = "";
            if(object == "tarea"){
                html_item = getHtmlTareas(this);
            }else if(object == "oportunidad"){
                html_item = getHtmlOportunidad(this);
            }else{
                html_item = getHtmlObject(this);
            }

            $('#'+id+' .obj-list').append(html_item);
        });
    })
    .error(function() { alert("Error al Cargar los Datos"); })
    .complete(function() { $('#'+id+'-refresh i').removeClass('fa-spin'); });
}
function drawChart(jsonData, id) {
    var chart = new Highcharts.Chart({
            chart: {
                renderTo: id,
                type: "column"
            },
            title: {
                text: null
            },
            subtitle: {
                text: null
            },
            xAxis: {
                categories: ['Oportunidades'],

            },
            yAxis: {
                allowDecimals: false,
                min: 0,
                gridLineWidth: 1,
                title: {
                    text: 'Suma de Valores [$]'
                }
            },
            tooltip: {
                formatter: function() {
                    return this.series.name +': $'+ this.y +'<br/>'+
                        'Total: $'+ this.point.stackTotal;
                }
            },
            plotOptions: {
                column: {
                    stacking: 'normal'
                }
            },
            legend: {
                borderWidth: 0,
                backgroundColor: "#FFFFFF",
                shadow: false
            },
            credits: {
                enabled: false
            },
            series: jsonData
    });
}
function drawChartMonth(jsonData, id, jsonCategories) {
    Highcharts.setOptions({
        lang: {
            months: monthNames,
            weekdays: dayNames,
            shortMonths: monthNamesShort,
            resetZoom: "Reiniciar Zoom"
        }
    });
    var chart = new Highcharts.Chart({
            chart: {
                renderTo: id,
                zoomType: 'x',
                spacingRight: 20
            },
            title: {
                text: null
            },
            subtitle: {
                text: document.ontouchstart === undefined ?
                    'Haz click y arrastra sobre la gráfica para hacer zoom' :
                    'Click en la gráfica para hacer zoom'
            },
            xAxis: {
                type: 'datetime',
                maxZoom: 14 * 24 * 3600000, // fourteen days
                title: {
                    text: null
                }
            },
            yAxis: {
                allowDecimals: false,
                min: 0,
                gridLineWidth: 1,
                title: {
                    text: 'Suma de Valores [$]'
                }
            },
            tooltip: {
                formatter: function() {
                    return Highcharts.dateFormat("%e. %b",this.x)+"<br/><b>$ "+this.y+"</b>";
                }
            },
            plotOptions: {
                area: {
                    stacking: 'normal',
                }
            },
            legend: {
                borderWidth: 0,
                backgroundColor: "#FFFFFF",
                shadow: false
            },
            credits: {
                enabled: false,
                text:"gizcloud.com",
                href:"http://www.gizcloud.com"
            },
            series: jsonData,
    });
}
function getOportunidadesBy(url,id,id_2,flag){
    $('#'+id+' i').addClass('fa-spin');
    $.getJSON(url, function(data) {
        if(flag == 1){
            drawChartMonth(data.data, id_2, data.categories);
        }else{drawChart(data, id_2);}
    })
    .error(function() { alert("Error al Cargar los Datos"); })
    .complete(function() { $('#'+id+' i').removeClass('fa-spin'); });
}
function drawChartActiviades(jsonData) {
    var chart = new Highcharts.Chart({
            chart: {
                renderTo: 'activi-chart',
                type: "column"
            },
            title: {
                text: null
            },
            subtitle: {
                text: null
            },
            xAxis: {
                categories: dayNamesWeek,

            },
            yAxis: {
                allowDecimals: false,
                min: 0,
                gridLineWidth: 1,
                title: {
                    text: null
                }
            },
            tooltip: {
                formatter: function() {
                    return this.y;
                }
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            legend: {
                borderWidth: 0,
                backgroundColor: "#FFFFFF",
                shadow: false
            },
            credits: {
                enabled: false
            },
            series: jsonData
    });
}
function getActividades(url){
    $('#activi-refresh i').addClass('fa-spin');
    $.getJSON(url, function(data) {
        drawChartActiviades(data);
    })
    .error(function() { alert("Error al Cargar los Datos"); })
    .complete(function() { $('#activi-refresh i').removeClass('fa-spin'); });
}
function scrollMovil(obj,id){
    var tamanio_scroll = $(obj).find('.dash-list').height();
    /***    sonbra    ***/
    if($(obj).scrollTop() !== 0){
         $("#"+id+" .panel-heading").addClass('box-sombra');
    }else{
        $("#"+id+" .panel-heading").removeClass('box-sombra');
    }
    /***    efecto rebote    ***/
    if($(obj).scrollTop() + $(obj).height() < tamanio_scroll){flag_scroll = 0;}
    if( ($(obj).scrollTop() + $(obj).height() == tamanio_scroll) && flag_scroll != 1){
        flag_scroll = 1;
        $(obj).find('.dash-list').animate({marginBottom: '+=10px'},{
            duration: 200,
            step: function(now, fx) {
                $(this).parent().scrollTop(now + tamanio_scroll);
            },
            complete: function(){
                $(this).animate({marginBottom: '-=10px'},
                    {duration: 200}
                );
            }
        });
    }
}