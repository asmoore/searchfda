function makeBarChart(results) {

var term = [];
var count = [];
for (i = 0; i < results.length; i++) {
    term.push(results[i].term.toLowerCase());
    count.push(results[i].count+i*0.001);
    //added 0.001 as a hack because non-unique values are ignored
}

var chart,
    width = 400,
    bar_height = 20,
    height = bar_height * term.length,
    left_width = 210,
    x, 
    yScore, 
    yName,
    gap = 2,
    tickNumber=5;

x = d3.scale.linear()
   .domain([0, d3.max(count)])
   .range([0, width-50]);

yScore = d3.scale.ordinal()
    .domain(count)
    .range([0, width])
    .rangeRoundBands([0, (bar_height + 2 * gap) * count.length]);

yName = d3.scale.ordinal()
    .domain(term)
    .rangeBands([0, (bar_height + 2 * gap) * term.length]);

chart = d3.select(".chart")
    .attr('class', 'chart')
    .attr('width', left_width + width)
    .attr('height', (bar_height + 2 * gap) * term.length);

chart.selectAll("line")
    .data(x.ticks(tickNumber))
    .enter().append("line")
    .attr("x1", function(d) { return x(d) + left_width; })
    .attr("x2", function(d) { return x(d) + left_width; })
    .attr("y1", 0)
    .attr("y2", (bar_height + gap * 2) * term.length);

chart.selectAll("rect")
    .data(count)
    .enter().append("rect")
    .attr("x", left_width)
    .attr("y", yScore)
    .attr("width", x)
    .attr("height", yScore.rangeBand());

chart.selectAll("text.score")
    .data(count)
    .enter().append("text")
    .attr("x", function(d) { return x(d) + left_width + 10; })
    .attr("y", function(d){ return yScore(d) + yScore.rangeBand()/2; } )
    .attr("dx", -5)
    .attr("dy", ".36em")
    .attr("text-anchor", "left")
    .attr('class', 'score')
.text(function(d) { return String(d3.round(d)); } );

chart.selectAll('text.name')
    .data(term)
    .enter().append('text')
    .attr('x', left_width - 10)
    .attr('y', function(d) { return yName(d) + yName.rangeBand() / 2; })
    .attr('dy', '.36em')
    .attr('text-anchor', 'end')
    .attr('class', 'name')
    .text(String);

chart.selectAll(".rule")
    .data(x.ticks(tickNumber))
    .enter().append("text")
    .attr("class", "rule")
    .attr("x", function(d) { return x(d) + left_width; })
    .attr("y", 3)
    .attr("dy", -6)
    .attr("text-anchor", "middle")
    .text(String);
 
}

