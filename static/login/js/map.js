/***************************************
JavaScript para Mapas
Version: 1.0 - 2012
author: @jbravot (jonathan Bravo)
email: info@jonathanbravo.com
web: jonathanbravo.com
****************************************/
/*
  VARIABLES GLOBALES
*/
var map;
var marker;
var selectedmarker;
var geocoder = new google.maps.Geocoder();
var resize_icon = "/static/crm/img/control/resize.png";
var flag_fullscreen = 0;
var mapdiv;
var infowindow = new google.maps.InfoWindow({
    content: ''
});

/***************************************
Funcion para crear el mapa
****************************************/
function cargar_gmap(lati,longi,texto,flag_create){
    var myOptions = {
      zoom: 15,
      center: new google.maps.LatLng("-2.14682994994","-79.8824501038"),
      mapTypeControl: true,
      streetViewControl: false,
      mapTypeControlOptions: {
        style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
      },
      mapTypeId: google.maps.MapTypeId.ROADMAP,
    };
    mapdiv = document.getElementById("map_canvas");
    map = new google.maps.Map(mapdiv, myOptions);

    if(flag_create){
      var fullscreenControlDiv = document.createElement('div');
      var fullscreenControl = new FullscreenControl(fullscreenControlDiv, map);

      fullscreenControlDiv.index = 4;
      map.controls[google.maps.ControlPosition.TOP_RIGHT].push(fullscreenControlDiv);

      if( latlogValid(lati,longi) ){
        createPointToEdit(lati,longi);
      }else{
        createPointToEdit("-2.14682994994","-79.8824501038");
      }

    }else{
      crearPuntoInfowindows(texto,lati,longi);
    }

}
function latlogValid(latitud,longitud){
  if( (latitud != "" && latitud !== "None") && (longitud != "" && longitud !== "None") ){
    return true;
  }else{ return false;}
}
/**************************
Funcion Para crear un punto con una ventana de informacion
***************************/
function crearPuntoInfowindows(descripcion,latitud,longitud){

  if( latlogValid(latitud,longitud) ){
    latitud = latitud.replace(',', '.');
    longitud = longitud.replace(',', '.');
    marker = crearPunto(parseFloat(latitud),parseFloat(longitud));
  }

  if(descripcion != "" && marker){
    (function(marker, descripcion){
      google.maps.event.addListener(marker, 'click', function() {
          infowindow.setContent("<strong>"+descripcion+"</strong>");
                                  infowindow.open(map, marker);
          });
    })(marker,descripcion);
  }
  return marker;
}
/**************************
Funcion Para crear un punto
***************************/
function crearPunto(latitud,longitud){
  var point = new google.maps.LatLng(latitud, longitud);
  marker = new google.maps.Marker({
    animation: google.maps.Animation.DROP,
    map: map,
    position: point
  });
  return marker;
}
/***************************************
Funcion que detecta el geocode
****************************************/
function geocodePosition() {
  var direccio = "";
  var ciudad = "";
  var pais = "";

  var element_direccion = document.getElementById("id_direccion");
  var element_ciudad = document.getElementById("id_ciudad");
  var element_pais = document.getElementById("id_pais");

  if(element_direccion){
    direccion = element_direccion.value;
  }else{
    direccion = document.getElementById("id_direccion_factura").value;
  }

  if(element_ciudad){
    ciudad = element_ciudad.value;
  }else{
    ciudad = document.getElementById("id_ciudad_factura").value;
  }

  if(element_pais){
    pais = element_pais.value;
  }else{
    pais = document.getElementById("id_pais_factura").value;
  }

  var address = direccion;
  if(ciudad != ""){
    address += ", " + ciudad;
  }
  if(pais != ""){
    address += ", " + pais;
  }else{ address += ", Ecuador"; }

  geocoder.geocode( { 'address': address}, function(results, status) {

    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      marker.setPosition(results[0].geometry.location);
      fill_id_coords();
    } else {
      alert("No podemos encontrar la direcci&oacute;n, error: " + status);
    }
  });
}
/***************************************
Funcion para crear un punto editable
****************************************/
function createPointToEdit(latitud, longitud)
{
  latitud = latitud.replace(',', '.');
  longitud = longitud.replace(',', '.');
  marker = markerdraggable(latitud, longitud);
  marker.setMap(map);
  selectedmarker = marker;
  map.setCenter(marker.getPosition());
}
/***************************************
Creates a draggable marker and updates the needed fields
Used in post, but it doesn't work
****************************************/
function markerdraggable(lat,lon) {
    var thismarker;
    var myLatLng = new google.maps.LatLng(lat, lon);
    var marker = new google.maps.Marker({
          draggable: true,
          animation: google.maps.Animation.DROP,
          position: myLatLng,
          map: map,
        });

    var options = {};

    thismarker = marker;

    google.maps.event.addListener(thismarker, "dragstart", function() {
                   selectedmarker = thismarker;
                });
    google.maps.event.addListener(thismarker, "dragend", function() {
                   fill_id_coords();
                });
    markerdraggable_listener = google.maps.event.addListener(map, "click", function(){
                   fill_id_coords();
                });
  return thismarker;
}
/**************************
Fills the needed field in the form, when posting
***************************/
function fill_id_coords() {
// this is the function who fill the coords in POST process
        lon = selectedmarker.getPosition().lng();
        lat = selectedmarker.getPosition().lat();

        var element_lat = document.getElementById("id_lat_dir");
        var element_lon = document.getElementById("id_lon_dir");

        if(!element_lat){
          element_lat = document.getElementById("id_lat_dir_factura");
        }
        if(!element_lon){
          element_lon = document.getElementById("id_lon_dir_factura");
        }

        element_lat.value = lat;
        element_lon.value = lon;
}
/***************************************
funcion para el control de fullscreen
****************************************/
function FullscreenControl(controlDiv, map) {
  controlDiv.style.padding = '5px';

  // Set CSS for the control border
  var controlUI = document.createElement('div');
  controlUI.style.height = '24px';
  controlUI.style.width = '24px';
  controlUI.style.backgroundColor = 'white';
  controlUI.style.borderStyle = 'solid';
  controlUI.style.borderWidth = '1px';
  controlUI.style.borderColor = '#717B87';
  controlUI.style.textAlign = 'center';
  controlUI.style.cursor = 'pointer';
  controlUI.title = 'Expander Mapa';
  controlDiv.appendChild(controlUI);

  // Set CSS for the control interior
  var controlText = document.createElement('div');
  controlText.style.paddingTop = '2px';
  controlText.style.paddingLeft = '3px';
  controlText.style.paddingRight = '3px';
  controlText.innerHTML = '<img src="'+resize_icon+'"  />';
  controlUI.appendChild(controlText);

  // Setup the click event listeners
  google.maps.event.addDomListener(controlUI, 'click', function() {
      fullscreenMap();
  });
}
/***************************************
funcion para el fullscreen
****************************************/
function fullscreenMap() {
  if(flag_fullscreen === 0){
      mapdiv.style.position = 'fixed';
      mapdiv.style.top = '0';
      mapdiv.style.left = '0';
      mapdiv.style.width = '100%';
      mapdiv.style.height = '100%';
      mapdiv.style.zIndex = '999';
      flag_fullscreen = 1;
  }else{
      mapdiv.style.position = 'relative';
      mapdiv.style.top = '0';
      mapdiv.style.left = '0';
      mapdiv.style.width = '100%';
      mapdiv.style.height = '178px';
      mapdiv.style.zIndex = '0';
      flag_fullscreen = 0;
  }
  google.maps.event.trigger(map, 'resize');

}