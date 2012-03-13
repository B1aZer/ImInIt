var iminit = {
    //geocoder: null,
    //map:null,
    markersArray : [],
    geocode:null,
    draggable:false,
    marker:null,

    map_init : function () {
        geocoder = new google.maps.Geocoder();
        var myOptions = {
            center: new google.maps.LatLng(55.75, 37.616666699999996),
            zoom: 8,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            scrollwheel: false,
            zoom: 10
        };
        map = new google.maps.Map(document.getElementById("mapcanvas"),
        myOptions);
    },

    add_listeners : function() {
        google.maps.event.addListener(map, 'click', function(event) {
            iminit.deleteOverlays();
            iminit.placeMarker(event.latLng);
        });

    },

    check_resize : function() {
        google.maps.event.trigger(map, 'resize');
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
        var image = 'static/img/icons/ios/regroup.png';
        //if (iminit.markersArray.length == 0) {
            iminit.marker = new google.maps.Marker({
                position: location,
                map: map,
                draggable: iminit.draggable,
                icon:image
            })
            google.maps.event.addListener(iminit.marker, "dragend", function() {
                iminit.geocode = iminit.marker.getPosition();
                iminit.addCoord(iminit.geocode);
            });
            google.maps.event.addListener(iminit.marker, 'dblclick', function() {
                map.setZoom(15);
                map.setCenter(iminit.marker.getPosition());
            });
            iminit.markersArray.push(iminit.marker);
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
                iminit.deleteOverlays();
                iminit.placeMarker(iminit.geocode);
                iminit.addCoord(iminit.geocode);
            } else {
                var reason="<a class=\"close\" data-dismiss=\"alert\">×</a> <strong>Warning!</strong>" + status;
                $("#loc_error").html(reason).addClass("alert").fadeIn();
            }
        });
    },

    adressCode : function() {

        if (iminit.marker) {
            geocoder.geocode({'latLng': iminit.marker.getPosition()}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    if (results[1]) {
                        $('#loc').val(results[1].formatted_address);
                        iminit.addCoord(iminit.marker.getPosition());
                    }
                } else {
                    var reason="<a class=\"close\" data-dismiss=\"alert\">×</a> <strong>Warning!</strong>" + status;
                    $("#loc_error").html(reason).addClass("alert").fadeIn();

                }
            });
        }

    },

    addCoord : function(geocode) {
        $("#add-point #lat").val(geocode.lat());
        $("#add-point #lng").val(geocode.lng());

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












