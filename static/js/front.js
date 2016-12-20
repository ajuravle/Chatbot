/*jslint browser: true*/
/*global $, jQuery, alert*/
$( document ).ready(function() {
    $(document).mouseup(function(e){
        var container = $("#placeholder");
        if(!container.is(e.target)){
            $( "#placeholder" ).addClass("chat__input__placeholder");
            $( "#placeholder" ).empty();
        }
        else
            $("#placeholder").removeClass("chat__input__placeholder");
    });
    window.setTimeout(function(){$(".chat__bubble--bot").addClass("chat__bubble--slideIn");}, 100);
    window.setTimeout(function(){$(".chat__bubble--bot").addClass("chat__bubble--fade");}, 500);
});