$(document).ready(function(){
    $(".feed_content").toggle();
    $(".feed").click(function(){
        $(this).children(".feed_content").slideToggle();
    });

    $(".feed").children(".feed_header").children("img").click(function(){
        feed = $(this).parent(".feed_header").parent(".feed");
        _id = feed.attr("id");
        feed.hide();
        $.get("/remove_feed/" + _id + "/", {}, 'html');
        //return false;
    }); // .feed... .click
});
