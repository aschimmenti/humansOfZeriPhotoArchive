
var svg = d3.select("#cities_graph"),
        width = +svg.attr("width"),
        height = +svg.attr("height");

svg.attr("viewBox", [-width / 2, -height / 2, width, height]);

var color = d3.scaleOrdinal(d3.schemeCategory20);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody().strength(-55))
    .force("x", d3.forceX())
    .force("y", d3.forceY());

d3.json("./json/graph.json", function(error, graph) {
    if (error) throw error;

    var link = svg.append("g")
        .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
        .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

    var node = svg.append("g")
        .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter().append("g")
    
    var circles = node.append("circle")
        .attr("r", 7)
        .attr("fill", function(d) { return color(d.group); })
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    var lables = node.append("text")
        .text(function(d) {
        return d.id;
        })
        .attr('x', 6)
        .attr('y', 3);

    node.append("title")
        .text(function(d) { return d.id; });

    simulation
        .nodes(graph.nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(graph.links);

    function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        })
    }
});

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}


/*-----------------------------------------------------------------------------------*/ 
am4core.ready(function() {
    
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    // Create map instance
    var chart = am4core.create("mapdiv", am4maps.MapChart);
    var interfaceColors = new am4core.InterfaceColorSet();
    
    try {
        chart.geodata = am4geodata_worldLow;
    }
    catch (e) {
        chart.raiseCriticalError(new Error("Map geodata could not be loaded. Please download the latest <a href=\"https://www.amcharts.com/download/download-v4/\">amcharts geodata</a> and extract its contents into the same directory as your amCharts files."));
    }
    
    
    var label = chart.createChild(am4core.Label)
    label.text = "CITIZENSHIP OF PHOTOGRAPHERS PER COUNTRY. \n Bullet size uses logarithmic scale.";
    label.fontSize = 12;
    label.align = "left";
    label.valign = "bottom"
    label.fill = am4core.color("#354E6E");
    label.background = new am4core.RoundedRectangle()
    label.background.cornerRadius(10,10,10,10);
    label.padding(10,10,10,10);
    label.marginLeft = 30;
    label.marginBottom = 30;
    label.background.strokeOpacity = 0.3;
    label.background.stroke =am4core.color("#496B97");
    label.background.fill = am4core.color("white");
    label.background.fillOpacity = 0.6;
    
    // Set projection
    chart.projection = new am4maps.projections.Orthographic();
    chart.panBehavior = "rotateLongLat";
    chart.padding(20,20,20,20);
    
    // Add zoom control
    chart.zoomControl = new am4maps.ZoomControl();
    
    var homeButton = new am4core.Button();
    homeButton.events.on("hit", function(){
      chart.goHome();
    });
    
    homeButton.icon = new am4core.Sprite();
    homeButton.padding(7, 5, 7, 5);
    homeButton.width = 30;
    homeButton.icon.path = "M16,8 L14,8 L14,16 L10,16 L10,10 L6,10 L6,16 L2,16 L2,8 L0,8 L8,0 L16,8 Z M16,8";
    homeButton.marginBottom = 10;
    homeButton.parent = chart.zoomControl;
    homeButton.insertBefore(chart.zoomControl.plusButton);
    
    chart.backgroundSeries.mapPolygons.template.polygon.fill = am4core.color("#F0F6F9"); //mare
    chart.backgroundSeries.mapPolygons.template.polygon.fillOpacity = 1;
    chart.deltaLongitude = 20;
    chart.deltaLatitude = -20;
    
    // limits vertical rotation
    chart.adapter.add("deltaLatitude", function(delatLatitude){
        return am4core.math.fitToRange(delatLatitude, -90, 90);
    })
    
    // Create map polygon series
    
    var shadowPolygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
    shadowPolygonSeries.geodata = am4geodata_continentsLow;
    
    try {
        shadowPolygonSeries.geodata = am4geodata_continentsLow;
    }
    catch (e) {
        shadowPolygonSeries.raiseCriticalError(new Error("Map geodata could not be loaded. Please download the latest <a href=\"https://www.amcharts.com/download/download-v4/\">amcharts geodata</a> and extract its contents into the same directory as your amCharts files."));
    }
    
    shadowPolygonSeries.useGeodata = true;
    shadowPolygonSeries.dx = 2;
    shadowPolygonSeries.dy = 2;
    shadowPolygonSeries.mapPolygons.template.fill = am4core.color("#000");
    shadowPolygonSeries.mapPolygons.template.fillOpacity = 0.2;
    shadowPolygonSeries.mapPolygons.template.strokeOpacity = 0;
    shadowPolygonSeries.fillOpacity = 0.1;
    shadowPolygonSeries.fill = am4core.color("#000");
    
    
    // Create map polygon series
    var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
    polygonSeries.useGeodata = true;
    
    polygonSeries.calculateVisualCenter = true;
    polygonSeries.tooltip.background.fillOpacity = 0.2;
    polygonSeries.tooltip.background.cornerRadius = 20;
    
    var template = polygonSeries.mapPolygons.template;
    template.nonScalingStroke = true;
    template.fill = am4core.color("#F0F6F9"); //paesi
    template.stroke = am4core.color("#98C1D9"); //selezione
    
    polygonSeries.calculateVisualCenter = true;
    template.propertyFields.id = "id";
    template.tooltipPosition = "fixed";
    template.fillOpacity = 1;
    
    template.events.on("over", function (event) {
      if (event.target.dummyData) {
        event.target.dummyData.isHover = true;
      }
    })
    template.events.on("out", function (event) {
      if (event.target.dummyData) {
        event.target.dummyData.isHover = false;
      }
    })
    
    var hs = polygonSeries.mapPolygons.template.states.create("hover");
    hs.properties.fillOpacity = 1;
    hs.properties.fill = am4core.color("#98C1D9");
    
    
    var graticuleSeries = chart.series.push(new am4maps.GraticuleSeries());
    graticuleSeries.mapLines.template.stroke = am4core.color("#F0F6F9");
    graticuleSeries.fitExtent = false;
    graticuleSeries.mapLines.template.strokeOpacity = 0.2;
    graticuleSeries.mapLines.template.stroke = am4core.color("#F0F6F9");
    
    
    var measelsSeries = chart.series.push(new am4maps.MapPolygonSeries())
    measelsSeries.tooltip.background.fillOpacity = 0;
    measelsSeries.tooltip.background.cornerRadius = 20;
    measelsSeries.tooltip.autoTextColor = false;
    measelsSeries.tooltip.label.fill = am4core.color("#000");
    measelsSeries.tooltip.dy = -5;
    
    var measelTemplate = measelsSeries.mapPolygons.template;
    measelTemplate.fill = am4core.color("#496B97");
    measelTemplate.strokeOpacity = 0;
    measelTemplate.fillOpacity = 0.75;
    measelTemplate.tooltipPosition = "fixed";
    
    
    
    var hs2 = measelsSeries.mapPolygons.template.states.create("hover");
    hs2.properties.fillOpacity = 1;
    hs2.properties.fill = am4core.color("#354E6E");
    
    polygonSeries.events.on("inited", function () {
      polygonSeries.mapPolygons.each(function (mapPolygon) {
        var count = data[mapPolygon.id];
    
        if (count > 0) {
          var polygon = measelsSeries.mapPolygons.create();
          polygon.multiPolygon = am4maps.getCircle(mapPolygon.visualLongitude, mapPolygon.visualLatitude, Math.max(0.2, Math.log(count) * Math.LN10 / 10));
          polygon.tooltipText = mapPolygon.dataItem.dataContext.name + ": " + count;
          mapPolygon.dummyData = polygon;
          polygon.events.on("over", function () {
            mapPolygon.isHover = true;
          })
          polygon.events.on("out", function () {
            mapPolygon.isHover = false;
          })
        }
      })
    })
    
    
    var data = {
      "AT": 2,
      "BE": 2,
      "CH": 1,
      "CZ": 2,
      "DE": 10,
      "DK": 1,
      "FR": 7,
      "GB": 3,
      "HU": 1,
      "IT": 48,
      "JP": 1,
      "NL": 4,
      "NZ": 1,
      "SE": 1,
      "SI": 1,
      "US": 9
    }
/*----------------------------------------------------------------------------------*/
     // Themes begin
     am4core.useTheme(am4themes_material);
     am4core.useTheme(am4themes_animated);
     // Themes end
     
     var chart = am4core.create("barchartdiv", am4charts.XYChart);
     chart.hiddenState.properties.opacity = 0; // this creates initial fade-in
     
     chart.data = [{
   "name": "Anonimo",
   "number of contributions": 13355
 }, {
   "name": "Brogi, Giacomo",
   "number of contributions": 2213
 }, {
   "name": "ICCD",
   "number of contributions": 1539
 }, {
   "name": "Alinari, Fratelli",
   "number of contributions": 1532
 }, {
   "name": "Anderson, James",
   "number of contributions": 1192
 }, {
   "name": "SSPSAE",
   "number of contributions": 929
 }, {
   "name": "A. Villani e Figli",
   "number of contributions": 512
 }, {
   "name": "A. C. Cooper",
   "number of contributions": 397
 }, {
   "name": "Sotheby's",
   "number of contributions": 284
 }, {
   "name": "National Gallery, London",
   "number of contributions": 221
 }, {
   "name": "Perotti, Mario",
   "number of contributions": 184
 }];
     
     var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
     categoryAxis.renderer.grid.template.location = 0;
     categoryAxis.dataFields.category = "name";
     categoryAxis.renderer.minGridDistance = 40;
     categoryAxis.fontSize = 7;
     
     var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
     valueAxis.min = 0;
     valueAxis.max = 14000;
     valueAxis.strictMinMax = true;
     valueAxis.renderer.minGridDistance = 30;
     // axis break
     var axisBreak = valueAxis.axisBreaks.create();
     axisBreak.startValue = 2500;
     axisBreak.endValue = 12800;
     //axisBreak.breakSize = 0.005;
     
     // fixed axis break
     var d = (axisBreak.endValue - axisBreak.startValue) / (valueAxis.max - valueAxis.min);
     axisBreak.breakSize = 0.05 * (1 - d) / d; // 0.05 means that the break will take 5% of the total value axis height
     
     // make break expand on hover
     var hoverState = axisBreak.states.create("hover");
     hoverState.properties.breakSize = 1;
     hoverState.properties.opacity = 0.1;
     hoverState.transitionDuration = 1500;
     
     axisBreak.defaultState.transitionDuration = 1000;
     /*
     // this is exactly the same, but with events
     axisBreak.events.on("over", function() {
       axisBreak.animate(
         [{ property: "breakSize", to: 1 }, { property: "opacity", to: 0.1 }],
         1500,
         am4core.ease.sinOut
       );
     });
     axisBreak.events.on("out", function() {
       axisBreak.animate(
         [{ property: "breakSize", to: 0.005 }, { property: "opacity", to: 1 }],
         1000,
         am4core.ease.quadOut
       );
     });*/
     
     var series = chart.series.push(new am4charts.ColumnSeries());
     series.dataFields.categoryX = "name";
     series.dataFields.valueY = "number of contributions";
     series.columns.template.tooltipText = "{valueY.value}";
     series.columns.template.tooltipY = 0;
     series.columns.template.strokeOpacity = 0;
     
     // as by default columns of the same series are of the same color, we add adapter which takes colors from chart.colors color set
     series.columns.template.adapter.add("fill", function(fill, target) {
       return chart.colors.getIndex(target.dataItem.index);
     });
     
     /*--------------------------------------------------------------*/
     /*PIECHART */
      // Themes begin
    am4core.useTheme(am4themes_material);
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    // Create chart instance
    var chart = am4core.create("piediv", am4charts.PieChart);
    
    // Add data
    chart.data = [ {
    "photographer": "Anonimo",
    "count": 13355
}, {
   "photographer": "People (and/or Photo Studies)",
   "count": 8850
}, {
   "photographer": "Institutions",
    "count": 9254
    } ];
    
    // Add and configure Series
    var pieSeries = chart.series.push(new am4charts.PieSeries());
    pieSeries.dataFields.value = "count";
    pieSeries.dataFields.category = "photographer";
    pieSeries.slices.template.stroke = am4core.color("#fff");
    pieSeries.slices.template.strokeWidth = 2;
    pieSeries.slices.template.strokeOpacity = 1;
    
    // This creates initial animation
    pieSeries.hiddenState.properties.opacity = 1;
    pieSeries.hiddenState.properties.endAngle = -90;
    pieSeries.hiddenState.properties.startAngle = -90;
    
}); // end am4core.ready()
