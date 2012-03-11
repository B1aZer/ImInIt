$(document).ready(function(){

//$('.formin').hide();
    /*$(".span8").slideUp('fast');*/
    /**/
    /*$("#clearbtn").hide();*/
    /*$("#findbtn").hide();*/
    /*iminit.map_init();*/


$("#clearbtn").click(function(){ 
iminit.deleteOverlays()
});

$("#findbtn").click(function(){ 
  iminit.codeAddress(); 
  //return false; 
});

$("#mark_location").change(function(){ 
  if ($("#mark_location").prop('checked')) { 
      iminit.mark=true;
      /*$("#clearbtn").fadeIn('fast');*/
      /*$("#findbtn").fadeIn('fast');*/
      /*$(".span8").slideDown('slow');*/

  }
  else {
      iminit.mark=false;
      /*$("#clearbtn").fadeOut('fast');*/
      /*$("#findbtn").fadeOut('fast');*/
      /*$(".span8").slideUp('fast');*/

  }
  //return false; 
});


/*$("#findbtn").submit(function(){ 
  iminit.codeAddress(); 
  return false; 
});*/
 
});
