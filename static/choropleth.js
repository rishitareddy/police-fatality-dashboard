var width = 400;
    height = 300;

var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-5, 0])
  .html(function(d) {
    var dataRow = countryById.get(d.properties.name);
       if (dataRow) {
           console.log(dataRow);
           return dataRow.state + ": " + dataRow.value;
       } else {
           console.log("no dataRow", d);
           return d.properties.name + ": No data.";
       }
  })


var svg1 = d3.select('#vis').append('svg')
    .attr('width', width)
    .attr('height', height);

svg1.call(tip);

var projection = d3.geoAlbersUsa()
    .scale(500) // mess with this if you want
    .translate([width / 2, height / 2]);

var path = d3.geoPath()
    .projection(projection);

var colorScale = d3.scaleLinear().range(["#D4EEFF", "#0099FF"]).interpolate(d3.interpolateLab);

var countryById = d3.map();

// we use queue because we have 2 data files to load.
queue()
    .defer(d3.json, "static/us-states.json")
    .defer(d3.csv, "static/statesdata.csv", typeAndSet) // process
    .await(loaded);

function typeAndSet(d) {
    d.value = +d.value;
    countryById.set(d.state, d);
    return d;
}

function getColor(d) {
    var dataRow = countryById.get(d.properties.name);
    if (dataRow) {
        console.log(dataRow);
        return colorScale(dataRow.value);
    } else {
        console.log("no dataRow", d);
        return "#ccc";
    }
}


function loaded(error, usa, value) {

    console.log(usa);
    console.log(value);

    colorScale.domain(d3.extent(value, function(d) {return d.value;}));

    var states = topojson.feature(usa, usa.objects.units).features;

    svg1.selectAll('path.state')
        .data(states)
        .enter()
        .append('path')
        .attr('class', 'states')
        .attr('d', path)
		.on('mouseover',function(d){
			tip.show(d);
			d3.select(this)
			  .style('opacity', 1)
			  .style('stroke-width', 3);
		  })
		  .on('mouseout', function(d){
			tip.hide(d);
			d3.select(this)
			  .style('opacity', 0.8)
			  .style('stroke-width',0.3);
		  })
          .on("click",function(d, i) {

            console.log("In on click ", d.properties.name);

            json_dictionary = {state : d.properties.name, race: 'Black'}

            // resp = ""
            var jqxhr = $.ajax({
                     type: "POST",
                     contentType: "text/html;charset=utf-8",
                     url: "/get_top_pd",
                     traditional: "true",
                     data : JSON.stringify(json_dictionary),
                     dataType: "application/json",
                     async : false
                    //  success: function (response) {
                    //         dat = response.multi;
                    //         ext += response.extent
                    //         variable = response.variable
                    //         console.log("Data ", response);
                    //         resp = response
                    //     }  ,error: function(error){
                    //                 console.log("Multiline chart error ",error);
                    //               }

                    }) ;
                    var response = {valid: jqxhr.statusText,  data: jqxhr.responseText};

                    var obj = JSON.parse(response.data)
                    console.log(obj.multi)
                    drawMultiLineChart(obj)         
        })
        .attr('fill', function(d,i) {
            return getColor(d);
        })
        .append("title");

    var linear = colorScale;

    svg1.append("g")
      .attr("class", "legendLinear")
      .attr("transform", "translate(-5,-5)");

    var legendLinear = d3.legendColor()
      .shapeWidth(30)
      .orient('horizontal')
      .scale(linear);

    svg1.select(".legendLinear")
      .call(legendLinear);

}


