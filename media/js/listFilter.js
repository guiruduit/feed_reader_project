// "http://kilianvalkhof.com/uploads/listfilter/" based
$(document).ready(function(){
    // custom css expression for a case-insensitive contains()
    jQuery.expr[':'].Contains = function(a,i,m) {
        return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase())>=0;
    }; // Contains

    $("#search").change(function(){
        var filter = $(this).val();
        if (filter) {
            $("#lista_feeds").find(".feed_title:not(:Contains(" + filter + "))").parent().slideUp();
            $("#lista_feeds").find(".feed_title:Contains(" + filter + ")").parent().slideDown();
        } else {
            $("#lista_feeds").find(".feed_header").slideDown();
        }
        return false;
    }).keyup(function(){
        $(this).change();
    });
}); // document.ready
