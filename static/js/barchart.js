
data = [
  {
    key: "Mylan drugs",
    values: [
      { 
        "term": "ASPIRIN",
        "count": 88729
      },
      {
        "term": "METHOTREXATE SODIUM",
        "count": 81382
      },
      {
        "term": "METHOTREXATE",
        "count": 79644
      },
      {
        "term": "LISINOPRIL",
        "count": 71716
      },
      {
        "term": "FUROSEMIDE",
        "count": 68537
      },
      {
        "term": "LEVOTHYROXINE SODIUM",
        "count": 59454
      },
      {
        "term": "HYDROCHLOROTHIAZIDE",
        "count": 56509
      },
      {
        "term": "SIMVASTATIN",
        "count": 56426
      },
      {
        "term": "OMEPRAZOLE",
        "count": 55349
      },
      {
        "term": "ACETAMINOPHEN",
        "count": 50715
      }
    ]
  }
];

nv.addGraph(function() {
  var chart = nv.models.discreteBarChart()
    .x(function(d) { return d.term })
    .y(function(d) { return d.count })
    .staggerLabels(true)
    .tooltips(false)
    .showValues(true)

  d3.select('#chart svg')
    .datum(data)
    .transition().duration(500)
    .call(chart)
    ;

  nv.utils.windowResize(chart.update);

  return chart;
});