$(function(){




    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(getCoords, getError);
    }else{
        initialize(13.20272, -87.194107);
    }

    function getCoords(position){
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;

        initialize(lat,lng);
    }
    function getError(err){
        initialize(13.20272, -87.194107);
    }

    function initialize(lat,lng){
        var latlng = new google.maps.LatLng(lat,lng);
        var mapSettings = {
            center: latlng,
            zoom:15,
            mapTypeId:'roadmap'
        }
        var map = new google.maps.Map($('#mapa').get(0),mapSettings);

        new google.maps.Marker({
            position: latlng,
            map: map,
            draggable: true,
            title: 'Arrastrame!'
        });

          // Define the LatLng coordinates for the polygon's path.

          /* var barrio = [
          {lng: -74.184212, lat: 4.625376}, {lng: -74.183394, lat: 4.624414},
          {lng: -74.183236, lat: 4.624228}, {lng: -74.182293, lat: 4.623081},
          {lng: -74.181552, lat: 4.622185}, {lng: -74.181539, lat: 4.622197},
          {lng: -74.181495, lat: 4.622239}, {lng: -74.181249, lat: 4.622461},
          {lng: -74.180967, lat: 4.622715}, {lng: -74.180735, lat: 4.622925},
          {lng: -74.180492, lat: 4.623144}, {lng: -74.180473, lat: 4.623124},
          {lng: -74.180463, lat: 4.623112}, {lng: -74.180399, lat: 4.623032},
          {lng: -74.180389, lat: 4.623018}, {lng: -74.180346, lat: 4.622964},
          {lng: -74.180302, lat: 4.622977}, {lng: -74.179944, lat: 4.623084},
          {lng: -74.179822, lat: 4.623133}, {lng: -74.179276, lat: 4.623467},
          {lng: -74.178875, lat: 4.623129}, {lng: -74.178685, lat: 4.623607},
          {lng: -74.178606, lat: 4.623705}, {lng: -74.178412, lat: 4.623556},
          {lng: -74.178259, lat: 4.623461}, {lng: -74.178101, lat: 4.623383},
          {lng: -74.177994, lat: 4.623309}, {lng: -74.177972, lat: 4.623334},
          {lng: -74.177713, lat: 4.623215}, {lng: -74.17748, lat: 4.623391},
          {lng: -74.177158, lat: 4.623626}, {lng: -74.17746, lat: 4.623894},
          {lng: -74.177569, lat: 4.623987}, {lng: -74.177699, lat: 4.624104},
          {lng: -74.177808, lat: 4.624195}, {lng: -74.177878, lat: 4.624258},
          {lng: -74.177914, lat: 4.62429}, {lng: -74.17808, lat: 4.624434},
          {lng: -74.178282, lat: 4.624612}, {lng: -74.178407, lat: 4.624731},
          {lng: -74.178504, lat: 4.624815}, {lng: -74.178575, lat: 4.624878},
          {lng: -74.179118, lat: 4.624426}, {lng: -74.179602, lat: 4.625005},
          {lng: -74.180354, lat: 4.625922}, {lng: -74.179636, lat: 4.626529},
          {lng: -74.180236, lat: 4.62729}, {lng: -74.180996, lat: 4.626691},
          {lng: -74.181421, lat: 4.627233}, {lng: -74.181604, lat: 4.627098},
          {lng: -74.182138, lat: 4.626743}, {lng: -74.182584, lat: 4.626443},
          {lng: -74.183071, lat: 4.626118}, {lng: -74.183391, lat: 4.625922},
          {lng: -74.184014, lat: 4.62548}, {lng: -74.18407, lat: 4.62556},
          {lng: -74.184259, lat: 4.625432}, {lng: -74.184212, lat: 4.625376},
          {lng: -74.184212, lat: 4.625376}
          ]; */



        var addListenersOnPolygon = function(polygon) {
            google.maps.event.addListener(polygon, 'click', function (event) {
              /*alert(polygon.indexID);*/
              var tam = denuncias[0]
              var areaPoligono = google.maps.geometry.spherical.computeArea(polygon.getPath());
              for (let i = 1; i <= tam; i++){
                if(polygon.indexID==denuncias[i][0]){
                  //alert(denuncias[1][2]);
                  //alert("Denuncias "+denuncias[i][2]);
                  alert("Barrio: "+denuncias[i][1]+"\nNúmero de hurtos: "+denuncias[i][2]+"\nÍndice del barrio: "+denuncias[i][3]);
                  break;
                }
              }
            });
          }
        var cantidadBarrios=barrios[0];
        for (let i =1; i <=cantidadBarrios; i++) {
            var zona=[];
            var tam=barrios[i][0];
            for (let index =2; index <=tam+1; index++) {
                zona[index-2]={lat:barrios[i][index][0],lng:barrios[i][index][1]};
            }
            var z = new google.maps.Polygon({
                paths: zona,
                strokeColor: '#9c9c9c',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#9c9c9c',
                fillOpacity: 0.35,
                indexID: barrios[i][1]
              });

            z.setMap(map);
            addListenersOnPolygon(z);
        }
          // Construct the polygon.



    }
});
