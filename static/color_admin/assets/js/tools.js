

/*
* Calcula la diferencia entre fechas con formato YYYY-MM-DD
* Tipos= "dias", "horas"
 */
function diferenciaFechas(fecha_desde,fecha_hasta, tipo){

        f1 = Number(new Date(fecha_desde));
        f2 = Number(new Date(fecha_hasta));

        // Convert both dates to milliseconds
        // var date1_ms = fecha_desde.getTime();
        //var date2_ms = fecha_desde.getTime();
        t1 = +f1;
        t2 = +f2;

        //Get 1 day in milliseconds
        var one_day = 1000 * 60 * 60 * 24;

        // Calculate the difference in milliseconds
        var difference_ms = t2 - t1;

        //take out milliseconds
        difference_ms = difference_ms / 1000;
        var seconds = Math.floor(difference_ms % 60);
        difference_ms = difference_ms / 60;
        var minutes = Math.floor(difference_ms % 60);
        difference_ms = difference_ms / 60;
        var hours =difference_ms % 24;
        var days = Math.floor(difference_ms / 24);

        if(tipo=="dias"){
            return days;
        }else if(tipo=="horas"){
            return hours;
        }
        return 0;
}