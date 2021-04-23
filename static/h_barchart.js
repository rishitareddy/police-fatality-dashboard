function hbarchart(data){
 

  
  //I like to use the golden rectangle ratio if they work for my charts.
  
  // var svg = d3.select('#chartArea').append('svg');
  //We add our svg to the div area
  
  
  //We will build a basic function to handle window resizing.
  // function resize() {
  //     width = document.getElementById('chartArea').clientWidth;
  //     height = width / 3.236;
  //     d3.select('#chartArea')
  //       .attr('width', width)
  //       .attr('height', height);
  // }
  
  // window.onresize = resize;
  //Call our resize function if the window size is changed.
  
  
  // set the dimensions and margins of the graph
  var margin = {top: 20, right: 30, bottom: 40, left: 90},
      width = 460 - margin.left - margin.right,
      height = 400 - margin.top - margin.bottom;
  
      // const bar = d3.select('svg')
      // .attr("width", "100%")
      // .attr("height", "100%");
      
      // const svgContainer = d3.select('#container');
  
  // append the svg object to the body of the page
  var svg = d3.select("#hdata")
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");
  
  
    // Add X axis
    var x = d3.scaleLinear()
      .domain([0, d3.max(data, function(d){return d.killingcount;})])
      .range([ 0, width]);
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))
      .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");
  
    // Y axis
    var y = d3.scaleBand()
      .range([ 0, height ])
      .domain(data.map(function(d) { return d.state; }))
      .padding(.1);
    svg.append("g")
      .call(d3.axisLeft(y))
  
    //Bars
    svg.selectAll("myRect")
      .data(data)
      .enter()
      .append("rect")
      .attr("x", x(0) )
      .attr("y", function(d) { return y(d.state); })
      .attr("width", function(d) { return x(d.killingcount); })
      .attr("height", y.bandwidth() )
      .attr("fill", "#69b3a2")
  
  
      // .attr("x", function(d) { return x(d.Country); })
      // .attr("y", function(d) { return y(d.Value); })
      // .attr("width", x.bandwidth())
      // .attr("height", function(d) { return height - y(d.Value); })
      // .attr("fill", "#69b3a2")
  
  }