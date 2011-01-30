$(document).ready(function(){
    $(".feed").click(function(){
        var c = $(this).children('.feed_content').val();
        $("#conteudo").html(c);
    });
});