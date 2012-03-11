var iminit = {
    //geocoder: null,
    //map:null,

    mark:false,
    markersArray : [],
    geocode:null,


    map_init : function () {
        
        geocoder = new google.maps.Geocoder();

        var myOptions = {
            center: new google.maps.LatLng(55.75, 37.616666699999996),
            zoom: 8,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById("mapcanvas"),
        myOptions);
        google.maps.event.addListener(map, 'click', function(event) {
            //iminit.mark = true || iminit.placeMarker(event.latLng);
            if (iminit.mark && iminit.markersArray.length == 0) {
                iminit.placeMarker(event.latLng);
                iminit.mark=false;
            }
            
        });
                
        
        

    },
    getMarkers : function () {
         $.getJSON("/ajax", function(json) { 
            //console.log('ajax',json.result);
            if (json.result.length>0) { 
                for (j in json.result) { 
                    //var location = json.Locations[i]; 
                    //console.log();
                    if (json.result[j].lat && json.result[j].lng) {
                        var myLatlng = new google.maps.LatLng(json.result[j].lat,json.result[j].lng);
                        iminit.placeMarker(myLatlng);
                    }
                  } 
            }
        });
    },

    placeMarker : function (location) {
        //if (iminit.markersArray.length == 0) {
        var marker = new google.maps.Marker({
        position: location,
        map: map,
        draggable: true
        })
        google.maps.event.addListener(marker, "dragend", function() {
                    iminit.geocode = marker.getPosition();
                    iminit.addCoord(iminit.geocode);
                });
        iminit.markersArray.push(marker);
        //console.log(location);
        //}
        
    },
    // Deletes all markers in the array by removing references to them
    deleteOverlays : function() {
      if (iminit.markersArray) {
        for (i in iminit.markersArray) {
          iminit.markersArray[i].setMap(null);
        }
        iminit.markersArray.length = 0;
      }
    },
    
    codeAddress : function() {
        var address =$("#add-point input[name=loc]").val();
        geocoder.geocode( { 'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
                iminit.geocode = results[0].geometry.location;
                //console.log(iminit.geocode);
                //iminit.savePoint(iminit.geocode);
                iminit.addCoord(iminit.geocode);
                iminit.placeMarker(iminit.geocode);
                
            } else {
                var reason="Code "+status;
		        $("#add-point .error").html(reason).fadeIn();
		        iminit.geocode = null;  
            }
        });
    },

        addCoord : function(geocode) {
					$("#add-point input[name=lat]").val(geocode.lat());
					$("#add-point input[name=lng]").val(geocode.lng());
                    
},


   /* savePoint : function(geocode) {
					var data = $("#add-point :input").serializeArray();
                    console.log('here we go',data);
					data[data.length] = { name: "lng", value: geocode.lat() };
					data[data.length] = { name: "lat", value: geocode.lng() };
                    console.log('fishy:',data);
					$.post($("#add-point").attr('action'), data, function(json){
						$("#add-point .error").fadeOut();
						if (json.status == "fail") {
							$("#add-point .error").html(json.message).fadeIn();
						}
						if (json.status == "success") {
							$("#add-point :input[name!=action]").val("");
							var location = json.data;
                            
                            iminit.placeMarker(geocode);
                            console.log('success:',iminit.mark);
							//addLocation(location);
							//zoomToBounds();
						}
					}, "json");
}*/
}






  





