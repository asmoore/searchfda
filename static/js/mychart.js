function makeBarChart(jsonData) {

results = [
    {
      "term": "PRODUCT USED FOR UNKNOWN INDICATION",
      "count": 243900
    },
    {
      "term": "DRUG USE FOR UNKNOWN INDICATION",
      "count": 195340
    },
    {
      "term": "RHEUMATOID ARTHRITIS",
      "count": 180838
    },
    {
      "term": "MULTIPLE SCLEROSIS",
      "count": 180035
    },
    {
      "term": "HYPERTENSION",
      "count": 135399
    },
    {
      "term": "DEPRESSION",
      "count": 98884
    },
    {
      "term": "PAIN",
      "count": 75702
    },
    {
      "term": "CONTRACEPTION",
      "count": 71176
    },
    {
      "term": "DIABETES MELLITUS",
      "count": 71097
    },
    {
      "term": "OSTEOPOROSIS",
      "count": 64590
    },
    {
      "term": "PSORIASIS",
      "count": 58556
    },
    {
      "term": "BLOOD CHOLESTEROL INCREASED",
      "count": 48840
    },
    {
      "term": "TYPE 2 DIABETES MELLITUS",
      "count": 47878
    },
    {
      "term": "CROHN'S DISEASE",
      "count": 43773
    },
    {
      "term": "ASTHMA",
      "count": 43530
    },
    {
      "term": "SMOKING CESSATION THERAPY",
      "count": 42489
    },
    {
      "term": "ANXIETY",
      "count": 38408
    },
    {
      "term": "MULTIPLE MYELOMA",
      "count": 38151
    },
    {
      "term": "HEPATITIS C",
      "count": 37370
    },
    {
      "term": "ATRIAL FIBRILLATION",
      "count": 37185
    },
    {
      "term": "PSORIATIC ARTHROPATHY",
      "count": 36137
    },
    {
      "term": "PROPHYLAXIS",
      "count": 35573
    },
    {
      "term": "PERITONEAL DIALYSIS",
      "count": 32003
    },
    {
      "term": "BIPOLAR DISORDER",
      "count": 30625
    },
    {
      "term": "INSOMNIA",
      "count": 30417
    },
    {
      "term": "BREAST CANCER",
      "count": 30204
    },
    {
      "term": "GASTROOESOPHAGEAL REFLUX DISEASE",
      "count": 30094
    },
    {
      "term": "CHRONIC OBSTRUCTIVE PULMONARY DISEASE",
      "count": 29200
    },
    {
      "term": "ARTHRITIS",
      "count": 27646
    },
    {
      "term": "SCHIZOPHRENIA",
      "count": 26938
    },
    {
      "term": "BACK PAIN",
      "count": 24773
    },
    {
      "term": "HIV INFECTION",
      "count": 24635
    },
    {
      "term": "HORMONE REPLACEMENT THERAPY",
      "count": 24006
    },
    {
      "term": "PULMONARY ARTERIAL HYPERTENSION",
      "count": 23367
    },
    {
      "term": "HYPOTHYROIDISM",
      "count": 21846
    },
    {
      "term": "ILL-DEFINED DISORDER",
      "count": 21827
    },
    {
      "term": "EPILEPSY",
      "count": 21481
    },
    {
      "term": "ATTENTION DEFICIT/HYPERACTIVITY DISORDER",
      "count": 21194
    },
    {
      "term": "DIABETES MELLITUS NON-INSULIN-DEPENDENT",
      "count": 21138
    },
    {
      "term": "MIGRAINE",
      "count": 18268
    },
    {
      "term": "ANKYLOSING SPONDYLITIS",
      "count": 17470
    },
    {
      "term": "HYPERCHOLESTEROLAEMIA",
      "count": 17341
    },
    {
      "term": "ACNE",
      "count": 16215
    }
]

results = jsonData;
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
    left_width = 200,
    x, 
    yScore, 
    yName,
    gap = 2,
    tickNumber=5;

x = d3.scale.linear()
   .domain([0, d3.max(count)])
   .range([0, width]);

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

