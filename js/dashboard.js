/*!
 * Start Bootstrap - Grayscale Bootstrap Theme (http://startbootstrap.com)
 * Code licensed under the Apache License v2.0.
 * For details, see http://www.apache.org/licenses/LICENSE-2.0.
 */

// jQuery to collapse the navbar on scroll
$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "/dashboard",
        data:{"info":"","GETtype":"getstdev"}
    })
    .done(function(string) {
        console.log(string);
        $("#stdev").html(string);
        $('#slider').slider('value', string);
        //$("#slider").slider("value")=string;
    });
    $.ajax({
        type: "GET",
        url: "/dashboard",
        data:{"info":"","GETtype":"result"}
    })
    .done(function(string) {
        console.log(string);
        network();
        //if(string!="success"){
        //    $(".query-alert:first").fadeIn();
        //}
    });
    //network();
    //$(".query-alert:first").fadeIn();

    $(".navbar-fixed-top").addClass("top-nav-collapse");
    
    slider();

});
// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});

$(function(){
    $("#stdev_submit").click(function() {
        $.ajax({
            type: "GET",
            url: "/dashboard",
            data:{"info": $("#stdev").html(),"GETtype":"update"}
        })
        .done(function(string) {
            location.reload(true)

        });
    });
});

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
    $('.navbar-toggle:visible').click();
});

function network(){
    var width = 660,
    height = 450;

    var color = d3.scale.category20();

    var force = d3.layout.force()
        .charge(-120)
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
                "<p class='d3-paper'><strong>Abstract: </strong> <span>" + d.abstract + "</span></p>"+
                "<p class='d3-paper'><strong>Keywords: </strong> <span>" + d.keyword + "</span></p>"+
                "<p class='d3-paper'><strong>Author: </strong> <span>" + d.author + "</span></p>";
            }
            else{
                return "<p class='d3-p'><strong>Similarity: "+d.value+"<strong></p>";
            }
        })

    svg.call(tip);

    d3.json("/static/search/result.json", function(error, graph) {
        if (error) throw error;

        force
            .nodes(graph.nodes)
            .links(graph.links)
            .start();

        var link = svg.selectAll(".link")
            .data(graph.links)
            .enter().append("line")
            .attr("class", "link")
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide)
            .style("stroke-width", function(d) { 
                if(d.value>0){
                    return d.value*5; 
                }
            });

        var node = svg.selectAll(".node")
            .data(graph.nodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("r", function(d) {return 7;})
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide)
            .style("fill", function(d) { return color(d.group); })
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

function slider(){
    $( "#slider" ).slider({
        value:2,
        min: -3,
        max: 3,
        step: 0.5,
        slide: function( event, ui ) {
            $( "#stdev" ).html( ui.value );
        }
    });
    $( "#stdev" ).html($( "#slider" ).slider( "value" ));
}

