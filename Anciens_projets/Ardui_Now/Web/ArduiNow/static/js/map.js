markers=[]

function myMap() {
  var myLatLng = {lat: 47.9028900, lng: 1.9038900};
  var mapCanvas = document.getElementById("imageMap");
  var mapOptions = {
    center: myLatLng,
    zoom: 10,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  }
  var map = new google.maps.Map(mapCanvas, mapOptions);
  var styles = [
      {
        stylers: [
          { hue: "#00ffe6" },
          { saturation: -20 }
        ]
      },{
        featureType: "road",
        elementType: "geometry",
        stylers: [
          { lightness: 100 },
          { visibility: "simplified" }
        ]
      },{
        featureType: "road",
        elementType: "labels",
        stylers: [
          { visibility: "off" }
        ]
      }
    ];

    map.setOptions({styles: styles});


    // on créer les markers
    fetch("http://localhost:5000/api/capteurs").then(logCapteurs);
    function logCapteurs(json){
      json.json().then(loadCapteurs);
    }
    function loadCapteurs(reponse){
      var image = {
        url: 'images/beachflag.png',
        // This marker is 20 pixels wide by 32 pixels high.
        size: new google.maps.Size(20, 32),
        // The origin for this image is (0, 0).
        origin: new google.maps.Point(0, 0),
        // The anchor for this image is the base of the flagpole at (0, 32).
        anchor: new google.maps.Point(0, 32)
      };
      var shape = {
        coords: [1, 1, 1, 20, 18, 20, 18, 1],
        type: 'poly'
      };
      for (let i=0; i<reponse.length; i++){
        var myLatLng = {lat: reponse[i]['pos_x'], lng: reponse[i]['pos_y']};
        var marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            title: reponse[i]['cName']
        });
        markers.push(marker);
      }
    }
}

function bounce(source){
  for(let i=0;i<markers.length;i++){
    if(source.name==markers[i].title){
      if(source.checked){
      markers[i].setAnimation(google.maps.Animation.BOUNCE);
    }
    else{
      markers[i].setAnimation(null);
    }
  }
  }
}
