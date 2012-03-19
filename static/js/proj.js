$(function() {
    /*$("#add").click(function () {
    if ($('#add > i').hasClass('icon-ok-sign')) {
        $('#add > i').attr("class", "icon-remove-sign");
        }
    else {
        $('#add > i').attr("class", "icon-ok-sign");
        }
    });*/
    
    $("#add").click(function () {
     // $('#add > i').switchClass("icon-ok-sign", "icon-remove-sign");

    //$('.icon-remove-sign').css({width:"0%"});

    $("#add > i")
    .fadeOut(500, function() {
        if ($(this).hasClass('icon-ok-sign')) {

        $(this).removeClass("icon-ok-sign").addClass("icon-remove-sign");
        }
        else {
        $(this).removeClass("icon-remove-sign").addClass("icon-ok-sign");
        }
        
    }).fadeIn(500, function() {
    })


    /*        $("#add > i").animate({
    width: "0%",
    },{
    duration:1000,
    complete: function() {
      $(this).animate({ width: "100%",
        },1000);
    }
    });
    */

    });

    /*$('#add > i').cycle({
		fx: 'fade' // choose your transition type, ex: fade, scrollUp, shuffle, etc...
	});*/
        
    
    
});
