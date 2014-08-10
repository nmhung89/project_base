var geocoder = new google.maps.Geocoder();

$('.house-search').click(function() {
	var parent = $(this).parent().parent().parent();
	var ward = '';
	var district = '';
	
	if (parent.find('.ward').val() != "")
		ward = parent.find('.ward').find(':selected').text();
	if (parent.find('.district').val() != "")
		district = parent.find('.district').find(':selected').text();
	
	var address = parent.find('.address').val() + ', ' + ward + ', ' + district + ', Ho Chi Minh, Vietnam';
	var geocode_request = {'address': address};
	
	var house_type = parent.find('.house-type').val();
	var min_price = parent.find('.min-price').val();
	var max_price = parent.find('.max-price').val();
	var radius = parent.find('.radius').val();
	
	geocoder.geocode(geocode_request, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			map.setCenter(results[0].geometry.location);
	        map.fitBounds(results[0].geometry.viewport);
	        
	        var lat = results[0].geometry.location.k;
	        var long =  results[0].geometry.location.A;
	        
	      } else {
	    	  alert("Geocode was not successful for the following reason: " + status);
	      }
	});
});
