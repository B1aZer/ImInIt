$(document).ready(function(){

    var starty = 0;
    var startyof = 0;
    var starthero = 0;
    var startpane =  0;
    //log = function(data) {console.log(data)};
    log = console.log;
    log('height:',$('.hero-unit').height());

    $( ".slider" ).draggable({
        axis:'y',
        
        start: function(e, ui) {
            starty = ui.position.top;
            log('starty=',starty);
            startyof = ui.offset.top;
            log('startofy=',startyof);
            starthero = $('.hero-unit').offset().top+$('.hero-unit').height()
            startpane =  $('.slider').offset().top
            log('starthero',starthero);
            log('startpane',startpane);
        },
        stop: function(e, ui) {
                
                var a=e.type;
                var endy=ui.position.top;
                log('endy',endy)
                var endyof=ui.offset.top;
                log('endyof',endyof)
                    
            $('.hero-unit').animate({

                //test = function(){console.log( 'dsa',$(this).height)},
                height: $('.hero-unit').height()+endyof-startyof+startpane-starthero,
              }, 1500,
              function() { console.log('',$(this).height());}),
                
            
            ui.helper.stop(true).animate({
                top: '+=10',
                opacity: 1,
            }, 200);
            },
    });

});

