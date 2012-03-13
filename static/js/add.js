$(document).ready(function(){

iminit.map_init();
iminit.add_listeners();

$("#clearbtn").fadeOut('fast');
      $("#findbtn").fadeOut('fast',function() {
      $("#mapcontainer").slideUp('fast');
      });
$( "#date_end").datepicker({
                    dateFormat:"yy-m-d"
                    });
$("#mark_location").change(function(){ 
  if ($("#mark_location").prop('checked')) { 
      iminit.mark=true;
      iminit.draggable=true;
      $("#mapcontainer").slideDown('fast',function() {
      $("#clearbtn").fadeIn('fast');
      $("#findbtn").fadeIn('fast');
      iminit.check_resize();
      });
  }
  else {
      iminit.mark=false;
      $("#clearbtn").fadeOut('fast');
      $("#findbtn").fadeOut('fast',function() {
      $("#mapcontainer").slideUp('fast');
      });
  }
});
$("#clearbtn").click(function(){ 
iminit.deleteOverlays();
$('#loc').val("");
});
$("#findbtn").click(function(){ 
    if ($('#loc').val()) {
        iminit.codeAddress(); 
    }
    else {
        iminit.adressCode();
    }
});


/*$("#findbtn").submit(function(){ 
  iminit.codeAddress(); 
  return false; 
});*/
 
});
