function map_capita_cartogram(){var legend_labels = ["0", "0-0.01", "0.11-0.02", "0.021-0.05", "0.51-0.1", "0.11-0.2","0.21-0.5","0.51-1","1.01-2","2.01-3",">3"];
var color_domain=[1,2,3,4,5,6,7,8,9,10];

var color = d3.scale.ordinal()
.domain([1,2,3,4,5,6,7,8,9,10])
.range(["#dddddd","#fff5eb","#fee6ce" , "#fdd0a2","#fdae6b","#fd8d3c","#f16913","#d94801" ,"#a63603" ,"#7f2704"]);

var width = 360,
height = 370,
centered;

var map = d3.select("#map_capita").append("svg")
.attr("width", width)
.attr("height", height);

var munics = map.append("g")
.attr("id", "counties")
.selectAll("path");


var proj = d3.geo.mercator()
.center([-120, 40])
.rotate([0, 0, 0])
.scale(1600)
.translate([0.5*width, 0.28*height]);

var topology,
geometries,
carto_features;

var vote_data = d3.map();

var carto = d3.cartogram()
.projection(proj)
.properties(function (d) {
            // this add the "properties" properties to the geometries
            return d.properties;
            });

// Load ca.csv
d3.csv("http://californiareportcard.org/v26/media/mobile/js/ca_capita_carto.csv", function (data) {
       data.forEach(function (d) {
                    vote_data.set(d.COUNTY, [d.POPULATION ,d.COLOR]);
                    })
       });

// This loads test the topojson file and creates the map.
d3.json("http://californiareportcard.org/v26/media/mobile/js/ca.topojson", function (data) {
        topology = data;
        geometries = topology.objects.counties.geometries;
        
        var neighbors = topojson.neighbors(topology.objects.counties.geometries);
        
        var features = carto.features(topology, geometries),
        path = d3.geo.path()
        .projection(proj);
        
        munics = munics.data(features)
        .enter()
        .append("path")
        .attr("class", "counties")
        .attr("id", function (d) {
              
              return d.properties.name;
              })
        .style("fill", function(d, i) {
               return color(vote_data.get(d.properties.name)[1]); })
        .attr("d", path)
        .style({"stroke-opacity":1,"stroke":"#000"});
        
        munics.append("title")
        .text(function (d) {
              return d.properties.name;
              });
        
        //d3.select("#click_to_run_capita").text("click here to run");
        });
    
    function do_update() {
        //d3.select("#click_to_run").text("thinking...");
        setTimeout(function () {
                   
                   // This sets the value to use for scaling, per district.
                   carto.value(function (d) {
                               return +vote_data.get(d.properties["name"])[0];
                               });
                   
                   
                   if (carto_features == undefined)
                   // this regenrates the topology features for the new map based on
                   carto_features = carto(topology, geometries).features;
                   
                   // update the map data
                   munics.data(carto_features)
                   .select("title")
                   .text(function (d) {
                         return d.properties.name + ", " + vote_data.get(d.properties["name"])[0];
                         });
                   
                   munics.transition()
                   .duration(750)
                   .each("end", function () {
                         d3.select("#click_to_run").text("")
                         })
                   .attr("d", carto.path);
                   }, 10);
    }
    

// add legend
var legend = map.selectAll("g.legend")
.data(color_domain)
.enter().append("g")
.attr("class", "legend");

var ls_w = 20, ls_h = 20;

legend.append("rect")
.attr("x", 10)
.attr("y", function(d, i){ return height - (i*ls_h) - 2*ls_h;})
.attr("width", ls_w)
.attr("height", ls_h)
.style("fill", function(d, i) { return color(d); })
.style("opacity", 0.8);

legend.append("text")
.attr("x", 40)
.attr("y", function(d, i){ return height - (i*ls_h) - ls_h - 4;})
.text(function(d, i){ return legend_labels[i]; });
    
    var map_capita_control = new Object();
    map_capita_control.do_update = do_update;
    return map_capita_control;
    
}

var map_capita_instance=map_capita_cartogram();

function map_capita_update(){
    map_capita_instance.do_update();
}
