/*!
 * Start Bootstrap - Grayscale Bootstrap Theme (http://startbootstrap.com)
 * Code licensed under the Apache License v2.0.
 * For details, see http://www.apache.org/licenses/LICENSE-2.0.
 */

// jQuery to collapse the navbar on scroll
$(window).scroll(function() {
    if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
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

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
    $('.navbar-toggle:visible').click();
});

$('.dropdown-menu li a').click(function() {
    $('#query-btn-type').html($(this).html());
});

$('#search-btn').click(function(e){
    if($('#query').val()==""){
        $(".query-alert:eq(1)").fadeIn();
        setTimeout("$('.query-alert:eq(1)').fadeOut();",5000);
    }
    else{
        $.ajax({
            type: "PUT",
            url: "/dashboard",
            data: {"querystring": $("#query").val() , "qtype": "title"}
        })
        .done(function() {
            window.location.href = "/static/dashboard.html";
        });
        e.preventDefault();
    }
        
});

$('#analysis-btn').click(function(e){
    console.log($("#analysis_input").val());
    $.ajax({
        type: "PUT",
        url: "/LDA",
        data: {"querystring": $("#analysis_input").val() , "qtype": "title"}
    })
    .done(function() {
        window.location.href = "/static/LDA.html";
    });
    e.preventDefault();
});
