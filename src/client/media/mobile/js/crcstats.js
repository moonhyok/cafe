function tick_num(data_object)
{
	  switch (d3.max(data_object, function(d) { return d.y; }))
	  {
		  case 1:
		     return 1;
		     break;
		  case 2:
		     return 2;
		     break;
		  case 3:
		     return 3;
		     break;
		  case 4:
		     return 4;
		     break;
		  default:
		     return 5;
	  }
	  		  
}

function generate_s1_hist()
{
   var formatCount = d3.format(",.0f");
   var s1_rating = window.conf.S1_RATING;
   
   
   
    var margin = {top: 10, right: 10, bottom: 10, left: 10},
    width = 320 - margin.left - margin.right,
    height = 200 - margin.top - margin.bottom,
    textheight=30;
    var x = d3.scale.linear()
    .domain([0, 1])
    .range([0, width]);
    var data = d3.layout.histogram()
    .bins(x.ticks(20))
    (s1_rating);
    var s1_median=d3.median(s1_rating);
    var y = d3.scale.linear()
    .domain([0, d3.max(data, function(d) { return d.y; })])
    .range([height-textheight, 0]);
    var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");
    
    var yAxis = d3.svg.axis()
                  .scale(y)
                  .orient("left")
                  .ticks(tick_num(data))
                  .tickFormat(d3.format(",.0f"));
                  
    var svg = d3.select("#s1hist").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    var bar = svg.selectAll(".bar")
    .data(data)
    .enter().append("g")
    .attr("class", "bar")
    .attr("transform", function(d) { return "translate(" + (x(d.x)+margin.left) + "," + y(d.y) + ")"; });
    
    bar.append("rect")
    .attr("x", 0)
    .attr("width", x(data[0].dx) - 1)
    .attr("height", function(d) { return height - y(d.y)-textheight; })
    .attr("fill",
    function(d){if (d.x<=s1_median && d.x+d.dx>s1_median)
                {return "brown"} 
                else{return "white"}});
    
    /*bar.append("text")
    .attr("y", 10)
    .attr("x", x(data[0].dx) / 2)
    .attr("text-anchor", "middle")
    .attr("font-size","10px")
    .text(function(d) { if (d!=0)
                          {return formatCount(d.y); }
                        else
                          {return ""}
                          });*/
    
    svg.append("line")
       .attr("x1",margin.left)
       .attr("x2",(width+margin.left).toString())
       .attr("y1",(height-textheight).toString())
       .attr("y2",(height-textheight).toString())
       .attr("stroke-width", 2)
       .attr("stroke","#594027");
       
    svg.append("text")
       .attr("y", height-textheight+15)
       .attr("x", margin.left)
       .text("Not Important")
       .attr("font-size","12px");
    
    svg.append("text")
       .attr("y", height-textheight+15)
       .attr("x", width+margin.left-82)
       .text("Very Important")
       .attr("font-size","12px");
    
    svg.append("g")
                .attr("class", "axis")
                .attr("transform", "translate(" +margin.left	+ ",0)")
                .call(yAxis);
}   

function generate_s2_hist()
{
	var formatCount = d3.format(",.0f");
   var s2_rating = window.conf.S2_RATING;  
   
   
    var margin = {top: 10, right: 10, bottom: 10, left: 10},
    width = 320 - margin.left - margin.right,
    height = 200 - margin.top - margin.bottom,
    textheight=30;
    var x = d3.scale.linear()
    .domain([0, 1])
    .range([0, width]);
    var data = d3.layout.histogram()
    .bins(x.ticks(20))
    (s2_rating);
    var s2_median=d3.median(s2_rating);
    var y = d3.scale.linear()
    .domain([0, d3.max(data, function(d) { return d.y; })])
    .range([height-textheight, 0]);
    var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");
    
    var yAxis = d3.svg.axis()
                  .scale(y)
                  .orient("left")
                  .ticks(tick_num(data))
                  .tickFormat(d3.format(",.0f"));
                  
    var svg = d3.select("#s2hist").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    var bar = svg.selectAll(".bar")
    .data(data)
    .enter().append("g")
    .attr("class", "bar")
    .attr("transform", function(d) { return "translate(" + (x(d.x)+margin.left) + "," + y(d.y) + ")"; });
    
    bar.append("rect")
    .attr("x", 0)
    .attr("width", x(data[0].dx) - 1)
    .attr("height", function(d) { return height - y(d.y)-textheight; })
    .attr("fill",
    function(d){if (d.x<=s2_median && d.x+d.dx>s2_median)
                {return "brown"} 
                else{return "white"}});
    
    /*bar.append("text")
    .attr("y", 10)
    .attr("x", x(data[0].dx) / 2)
    .attr("text-anchor", "middle")
    .attr("font-size","10px")
    .text(function(d) { if (d!=0)
                          {return formatCount(d.y); }
                        else
                          {return ""}
                          });*/
    
    svg.append("line")
       .attr("x1",margin.left)
       .attr("x2",(width+margin.left).toString())
       .attr("y1",(height-textheight).toString())
       .attr("y2",(height-textheight).toString())
       .attr("stroke-width", 2)
       .attr("stroke","#594027");
       
    svg.append("text")
       .attr("y", height-textheight+15)
       .attr("x", margin.left)
       .text("Not Interested")
       .attr("font-size","12px");
    
    svg.append("text")
       .attr("y", height-textheight+15)
       .attr("x", width+margin.left-84)
       .text("Very Interested")
       .attr("font-size","12px");
    
    svg.append("g")
                .attr("class", "axis")
                .attr("transform", "translate(" +margin.left	+ ",0)")
                .call(yAxis);
}
generate_s1_hist();
generate_s2_hist(); 
