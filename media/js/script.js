$(document).ready(function(){
    $(".feed_content").toggle();
    $(".feed").click(function(){
        $(this).children(".feed_content").slideToggle();
    });
});
