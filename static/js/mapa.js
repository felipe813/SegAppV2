
function IngresarComentario() {
  jQuery.noConflict();
  var nombreBarrio= $('#nombreBarrio').text().trim();
  var comentario= $('#textoComentario').val();
  if(nombreBarrio == 'NOMBRE BARRIO'){
    document.getElementById("respuestaComentarioNuevo").innerHTML = "Seleccione un barrio para comentar.";
    $("#modalComentarioNuevo").modal("show");
  }else{
    $.ajax({
      url : '/mapa/',
      type : "POST",
      data : {'operacion': 'ingresarComentario',
      'comentario': comentario,
      'barrio': nombreBarrio,
      csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),},
  }).done(function(returned_data){
      //alert(returned_data);
      document.getElementById("respuestaComentarioNuevo").innerHTML = "Comentario agregado correctamente.";
      document.getElementById("textoComentario").value="";
      $("#modalComentarioNuevo").modal("show");
  });
  }

}

function SeleccionarBarrio() {
  var nombreBarrio= $('#nombreBarrio').text();
  $.ajax({
      url : '/mapa/',
      type : "POST",
      data : {'operacion': 'obtenerComentarios',
      'barrio': nombreBarrio,
      csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),},
  }).done(function(returned_data){
      //alert(returned_data["1"]);
      //alert(returned_data["0"]);
      //alert(returned_data["2"]["Fecha"]);
      llenarComentarios(returned_data);
  });
}

function llenarComentarios(comentarios){
  cantidad = comentarios["cantidad"];
  //alert(cantidad);
  if(cantidad>0){
    textoHTML = '';
    for (let index = 0; index < cantidad; index++) {
      c = comentarios[index];
      textoHTML = textoHTML + obtenerItemComentario(index,c["Comentario"],c["Fecha"],c["Usuario"]);
      //alert(textoHTML);
    }
  }else{
    textoHTML = 'No hay comentarios para este sector.'
  }
  document.getElementById("listaComentarios").innerHTML = textoHTML;
}

function obtenerItemComentario(indexComentario,comentario,fecha,autor){
  if(indexComentario==0){
    cabezera = '<div class="carousel-item col-md-12 active">';
  }else{
    cabezera = '<div class="carousel-item col-md-12">';
  }
  retorno =
  cabezera
  +'<div class="card">'
  +'<div class="card-header bg-dark text-white">'
  +fecha +' , '+ autor+ ' dice :  '
  +'</div>'
  +'<div id="textoComentario" class="card-body">'
  +comentario
  +'</div>'
  +'</div>'
  +'</div>';
  return retorno;
}

$(function () {
// FUNCIONES PARA CALCULAR COLOR
  function numberToColorHsl(i, min, max) {
    var ratio = i;
    if (min > 0 || max < 1) {
      if (i < min) {
        ratio = 0;
      } else if (i > max) {
        ratio = 1;
      } else {
        var range = max - min;
        ratio = (i - min) / range;
      }
    }
    // as the function expects a value between 0 and 1, and red = 0° and green = 120°
    // we convert the input to the appropriate hue value
    var hue = ratio * 1.2 / 3.60;
    //if (minMaxFactor!=1) hue /= minMaxFactor;
    //console.log(hue);
    // we convert hsl to rgb (saturation 100%, lightness 50%)
    var rgb = hslToRgb(hue, 1, .5);
    // we format to css value and return
    return 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')';
  }
  function hslToRgb(h, s, l) {
    var r, g, b;
    if (s == 0) {
      r = g = b = l; // achromatic
    } else {
      function hue2rgb(p, q, t) {
        if (t < 0) t += 1;
        if (t > 1) t -= 1;
        if (t < 1 / 6) return p + (q - p) * 6 * t;
        if (t < 1 / 2) return q;
        if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
        return p;
      }
      var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      var p = 2 * l - q;
      r = hue2rgb(p, q, h + 1 / 3);
      g = hue2rgb(p, q, h);
      b = hue2rgb(p, q, h - 1 / 3);
    }
    return [Math.floor(r * 255), Math.floor(g * 255), Math.floor(b * 255)];
  }
  function obtenerRGB(indice){
    if(indice<=0.1) indice = 0.1;
    else if(indice<=0.35) indice = 0.35;
    else if(indice<=0.6) indice = 0.6;
    else if(indice<=0.85) indice = 0.85;
    else indice = 1;
    return numberToColorHsl(1-indice, 0, 1);
  }
// FUNCIONES PARA LLENAR INFORMACIÓN DEL BARRIO
  function llenarInformacion(nombreBarrio, numeroDelitos, indice, denuncias_delitos) {
    document.getElementById('nombreBarrio').innerHTML = nombreBarrio;
    document.getElementById('cantidadHurtos').innerHTML = denuncias_delitos["cantidadHurtos"];
    document.getElementById('cantidadDelitosSexuales').innerHTML = denuncias_delitos["cantidadDelitosSexuales"];
    document.getElementById('cantidadHurtoAutomotores').innerHTML = denuncias_delitos["cantidadHurtoAutomotores"];
    document.getElementById('cantidadHomicidios').innerHTML = denuncias_delitos["cantidadHomicidios"];

    element = document.getElementById("barraPeligrosidad");
    var valor = indice * 100;
    element.style.width = valor + '%';
    var color = obtenerRGB(indice);
    element.style.background = color;
    //alert("Barrio: " + nombreBarrio + "\nNúmero de hurtos: " + numeroHurtos + "\nÍndice del barrio: " + indice);
  }

// FUNCIONES DEL MAPA
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(getCoords, getError);
  } else {
    initializeDefault();
  }
  function getCoords(position) {
    var lat = position.coords.latitude;
    var lng = position.coords.longitude;

    initialize(lat, lng);
  }
  function getError(err) {
    initializeDefault();
  }
  function initializeDefault(){
    initialize(4.627958878621314, -74.06539470584593);
  }
  function initialize(lat, lng) {
    var latlng = new google.maps.LatLng(lat, lng);
    var mapSettings = {
      center: latlng,
      zoom: 15,
      mapTypeId: 'roadmap'
    }
    var map = new google.maps.Map($('#mapa')[0], mapSettings);
    // new google.maps.Marker({
    //   position: latlng,
    //   map: map,
    //   draggable: true,
    //   title: 'Arrastrame!'
    // });
    var addListenersOnPolygon = function (polygon) {
      google.maps.event.addListener(polygon, 'click', function (event) {
        var tam = denuncias[0]
        for (let i = 1; i <= tam; i++) {
          if (polygon.indexID == denuncias[i][0]) {
            var denuncias_delitos = {cantidadDelitosSexuales : denuncias[i][5], cantidadHomicidios : denuncias[i][6], cantidadHurtos : denuncias[i][7], cantidadHurtoAutomotores : denuncias[i][8]}
            llenarInformacion(denuncias[i][1], denuncias[i][2], denuncias[i][4], denuncias_delitos);
            SeleccionarBarrio();
            break;
          }
        }
      });
    }
    var cantidadBarrios = barrios[0];
    for (let i = 1; i <= cantidadBarrios; i++) {
      var zona = [];
      var tam = barrios[i][0];
      for (let index = 2; index <= tam + 1; index++) {
        zona[index - 2] = { lat: barrios[i][index][0], lng: barrios[i][index][1] };
      }
      var color = obtenerRGB(denuncias[i][4]);
      var z = new google.maps.Polygon({
        paths: zona,
        strokeColor: color,
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: color,
        fillOpacity: 0.35,
        indexID: barrios[i][1]
      });

      z.setMap(map);
      addListenersOnPolygon(z);
    }
  }
});
