//Width and height
	var w = 700;
	var h = 300;
	
	//Data
	var coords = [ [100, 50], [200, 75], [300, 100], [400, 125], [500,150] ];
	
	//Create SVG element
	var svg = d3.select("body")
				.append("svg")
				.attr("width", w)
				.attr("height", h);

	var circles = svg.selectAll("circle")
		.data(coords) // changed from xCoords
		.enter()
		.append("circle");

	circles.attr("cx", function(d) {
				return d[0]; // TODO need to make this dynamic
				//return d[i]
			})
		   .attr("cy", function(d, i){
				return d[1];   
		   })
		   .attr("r", function(d) {
				return d[0]/10;
		   })
		   .attr("fill", function(d) {
				return "rgb(150, 50, " + (d[0]/2) + ")";   
		   })
		   .attr("stroke", "white")
		   .attr("stroke-width", function(d) {
				/*if (d <= 10)
					return d/3;
				else if (d <= 30)
					return d/4.5;
				else*/
					return d[0]/100 + 2;
		   });

/*var vis = d3.select("body");

xRange = d3.scale.linear().range ([20, 180]).domain([0, 300]);
yRange = d3.scale.linear().range ([20, 180]).domain([0, 300]);

function update() {
	var circles = vis.selectAll("circle").data(randomData(), function (d) { return d.id; } );
	
	circles.enter()
		.append("svg:circle")
		.attr("cx", function (d) {return d.value1;})
		.attr("cx", function (d) {return d.value2;})
		.style("fill", "blue");
		
	circles.transition().duration(1000)
		.attr("cx", function (d) { return d.value1; })
		.attr("cy", function (d) { return d.value2; })
		.attr("r", function (d) { return d.value3; });
		
	circles.exit ()
		.transition().duration(1000)
			.attr("r", 0)
				.remove ();
				
	setTimeout(update, 2000);
}

update();*/

/*xCoords = [5, 10, 30];
yCoords = [10, 20, 60];
width = 500;
height = 300;

max = d3.max(data);

x  = d3.scale.linear().domain([0, xCoords.length - 1]).range [0, w]
y  = d3.scale.linear().domain([0, yCoords.length - 1]).range [h, 0]


// base vis layer
var vis = d3.select("#chart")
			.append("svg:svg")
			.attr("width", width)
			.attr("height", height)*/

/*var r = 960,
    format = d3.format(",d"),
    fill = d3.scale.category20c();

var bubble = d3.layout.pack()
    .sort(null)
    .size([r, r])
    .padding(1.5);

var vis = d3.select("#chart").append("svg")
    .attr("width", r)
    .attr("height", r)
    .attr("class", "bubble");

d3.json("../data/flare.json", function(json) {
  var node = vis.selectAll("g.node")
      .data(bubble.nodes(classes(json))
      .filter(function(d) { return !d.children; }))
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

  node.append("title")
      .text(function(d) { return d.className + ": " + format(d.value); });

  node.append("circle")
      .attr("r", function(d) { return d.r; })
      .style("fill", function(d) { return fill(d.packageName); });

  node.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", ".3em")
      .text(function(d) { return d.className.substring(0, d.r / 3); });
});

// Returns a flattened hierarchy containing all leaf nodes under the root.
function classes(root) {
  var classes = [];

  function recurse(name, node) {
    if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
    else classes.push({packageName: name, className: node.name, value: node.size});
  }

  recurse(null, root);
  return {children: classes};
}
*/