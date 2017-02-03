/*!
 * Start Bootstrap - Grayscale Bootstrap Theme (http://startbootstrap.com)
 * Code licensed under the Apache License v2.0.
 * For details, see http://www.apache.org/licenses/LICENSE-2.0.
 */

// jQuery to collapse the navbar on scroll
var level=0
$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "/LDA",
        data:{"info":"","GETtype":"top"}
    })
    .done(function(string) {
        network()
        network2()
    });
    /*$.ajax({
        type: "GET",
        url: "/dashboard",
        data:{"info":"","GETtype":"result"}
    })
    .done(function(string) {
        if(string!="success"){
            $(".query-alert:first").fadeIn();
        }
    });*/

    $(".navbar-fixed-top").addClass("top-nav-collapse");
});

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
    $('.navbar-toggle:visible').click();
});

function network(){
    var width = 1200;
    var height = 400;

    var force = d3.layout.force()
        .charge(-1000)
        .linkDistance(30)
        .size([width, height]);

    var svg = d3.select("#graph").append("svg")
        .attr("width", width)
        .attr("height", height);

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d) {
            if(d.name){
                return "<p class='d3-p'><strong>Title: "+d.title+"</strong></p>"+
                //"<p class='d3-paper'><strong>Abstract: </strong> <span style='color:white'>" + d.abstract + "</span></p>"+
                //"<p class='d3-paper'><strong>Keywords: </strong> <span style='color:white'>" + d.keyword + "</span></p>"+
                "<p class='d3-paper'><strong>Author: </strong> <span>" + d.author + "</span></p>";
            }
            else{
                return "<p class='d3-p'><strong>Similarity: "+d.value+"<strong></p>";
            }
        })

    svg.call(tip);
    filename="/static/search/LDA.json";
    d3.json(filename, function(error, graph) {
        if (error) throw error;

        force
            .nodes(graph.nodes)
            .links(graph.links)
            //.on("tick", tick)
            .start();

        var link = svg.selectAll(".link")
            .data(graph.links)
            .enter().append("line")
            .attr("class", "link")
            .on('mouseover', tip.show)
            //.on('mouseout', tip.hide)
            .style("stroke-width", function(d) { 
                if(d.value>0){
                    return d.value*10; 
                }
                else{
                    return 0.01
                }
            });
        var node = svg.selectAll(".node")
            .data(graph.nodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("r", function(d) {if(d.group==0){return 15;}else{return 7;}})
            .on('mouseover', tip.show)
            //.on('mouseout', tip.hide)
            .style("fill", function(d) { return color60(parseInt(d.group)); })
            .call(force.drag);

        node.append("title")
            .text(function(d) { return d.name; });

        force.on("tick", function() {
            link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node.attr("cx", function(d) { return d.x=Math.max(0,Math.min(width, d.x)); })
                .attr("cy", function(d) { return d.y=Math.max(0,Math.min(height, d.y)); });
        });
    });  
}

function network2(){
    var width = 1200;
    var height = 400;

    var force = d3.layout.force()
        .charge(-1000)
        .linkDistance(30)
        .size([width, height]);

    var svg = d3.select("#graph2").append("svg")
        .attr("width", width)
        .attr("height", height);

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d) {
            if(d.name){
                return "<p class='d3-p'><strong>Title: "+d.title+"</strong></p>"+
                //"<p class='d3-paper'><strong>Abstract: </strong> <span style='color:white'>" + d.abstract + "</span></p>"+
                //"<p class='d3-paper'><strong>Keywords: </strong> <span style='color:white'>" + d.keyword + "</span></p>"+
                "<p class='d3-paper'><strong>Author: </strong> <span>" + d.author + "</span></p>";
            }
            else{
                return "<p class='d3-p'><strong>Similarity: "+d.value+"<strong></p>";
            }
        })

    svg.call(tip);
    filename="/static/search/LDA_refresh.json";
    d3.json(filename, function(error, graph) {
        if (error) throw error;

        force
            .nodes(graph.nodes)
            .links(graph.links)
            //.on("tick", tick)
            .start();

        var link = svg.selectAll(".link")
            .data(graph.links)
            .enter().append("line")
            .attr("class", "link")
            .on('mouseover', tip.show)
            //.on('mouseout', tip.hide)
            .style("stroke-width", function(d) { 
                if(d.value>0){
                    return d.value*7; 
                }
                else{
                    return 0.01
                }
            });
        var node = svg.selectAll(".node")
            .data(graph.nodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("r", function(d) {if(d.group==0){return 15;}else{return 7;}})
            .on('mouseover', tip.show)
            //.on('mouseout', tip.hide)
            .style("fill", function(d) { return color60(parseInt(d.group)); })
            .call(force.drag);

        node.append("title")
            .text(function(d) { return d.name; });

        force.on("tick", function() {
            link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node.attr("cx", function(d) { return d.x=Math.max(0,Math.min(width, d.x)); })
                .attr("cy", function(d) { return d.y=Math.max(0,Math.min(height, d.y)); });
        });
    });  
}

function color60(n){
    var list=["#1f77b4","#aec7e8","#ff7f0e","#ffbb78","#2ca02c","#98df8a","#d62728","#ff9896","#9467bd","#c5b0d5","#8c564b",
                "#c49c94","#e377c2","#f7b6d2","#7f7f7f","#c7c7c7","#bcbd22","#dbdb8d","#17becf","#9edae5","#393b79","#5254a3",
                "#6b6ecf","#9c9ede","#637939","#8ca252","#b5cf6b","#cedb9c","#8c6d31","#bd9e39","#e7ba52","#e7cb94","#843c39",
                "#ad494a","#d6616b","#e7969c","#7b4173","#a55194","#ce6dbd","#9edae5","#de9ed6","#3182bd","#6baed6","#9ecae1",
                "#c6dbef","#e6550d","#fd8d3c","#fdae6b","#fdd0a2","#31a354","#74c476","#a1d99b","#c7e9c0","#756bb1","#9e9ac8",
                "#bcbddc","#dadaeb","#636363","#969696","#bdbdbd","#d9d9d9"]
    return list[n % list.length];
}