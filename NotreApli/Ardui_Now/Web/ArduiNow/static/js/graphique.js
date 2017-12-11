
let getData = function (callback) {
	$.getJSON(
		"http://"+server+"/graph/json/1",
        callback
	);
};
$.displayHighChart = function(data){
    document.graph = new Highcharts.chart('graph-container', data);
};
let server = "localhost:5000";

id=-1;
function reload() {
  getData(function (data) {
      $.displayHighChart( data);
      id = data.id;
  });
};

$(reload());

function load(data){
    // insert dans la page le graph passé en paramètre
    $.displayHighChart( data);
      id = data.id;
};

function tracer(source){
  let agregat = source.value;
  let captIds = $("#itemList li input:checked");
  let graphique =[];
  for (let i=0; i<captIds.length; i++){
      captId = captIds[i].value;
      getData(function (data){
      for (let i= 0 ;i< data.series.length;i++ ){
          let graph = data.series[i];
          let condition = false;
          switch (agregat) {
              case "max" :
                   condition = graph.name.includes("Capteur "+captId+" : Maximum");
                  break;
              case "min" :
                   condition = graph.name.includes("Capteur "+captId+" : Minimum");
                  break;
              case "moy" :
                   condition = graph.name.includes("Capteur "+captId+" : Moyenne");
                  break;
              case "sum" :
                  condition = graph.name.includes("Capteur "+captId+" : Somme");
                  break;
              case "" :
                   condition = graph.name.includes("Capteur "+captId)&&(!graph.name.includes("Maximum")&&
                                   !graph.name.includes("Minimum")&&
                                   !graph.name.includes("Moyenne")&&
                                   !graph.name.includes("Somme"));

                  console.log(  "max");
                  break;
          };
          if(condition){
              graphique.push(graph);
              data.series = graphique ;
              $(load(data));
            return graph;
          }}
      //Le graphique n'éxiste pas on le trace
      fetch("http://"+server+"/graph/add/"+id+"/"+captId+"/"+agregat).then(tracer(source));
      });
  }
};
