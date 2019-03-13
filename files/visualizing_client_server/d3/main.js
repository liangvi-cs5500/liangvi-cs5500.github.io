function drawChart(data){

    var margin = {top: 50, right: 50, bottom: 50, left: 50}; 
    var width = 800;
    var height = 500;
    
    var xScale = d3.scaleLinear()
    .domain([0,1])
    .range([0, width]);

    var yScale = d3.scaleLinear()
    .domain([0,1])
    .range([height, 0]);

    var roc = d3.line()
    .x(function(d) { return xScale(d.fpr)})
    .y(function(d) { return yScale(d.tpr)})
    .curve(d3.curveLinear); 

    var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("align","center")
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");       

    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xScale));

    svg.append("g")
    .attr("class", "y axis")
    .call(d3.axisLeft(yScale)); 

    
    svg.append("text")
    .attr("x", width/2)
    .attr("y", height+(margin.bottom/2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .text("False Positive Rate");

    svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x",0 - (height / 2))
    .attr("y", 0 - margin.left)
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .text("True Positive Rate");  

    svg.append("path")
    .datum(data) 
    .attr("class", "line")
    .attr("d", roc);

    svg.append("text")
    .attr("x", width-margin.right)
    .attr("y", height-margin.top)
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .datum(data) 
    .text("AUC Score: "  + data[0].score);

    svg.select(".path").transition()
        .duration(750)
        .attr("d", roc);

} 

function plot() {
    var url = "http://localhost:5000/roc/"
    var scaler = document.getElementById("scaler").value;
    var c = document.getElementById("c").value;

    url1 = url.concat(scaler).concat("/").concat(c);
    
    d3.json(url1).then(function(data) {
        document.getElementById('chart').innerHTML = "";
        drawChart(data);
    });
}