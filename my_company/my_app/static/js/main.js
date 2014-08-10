$('#hide_search_map').click(function() {
	if ( $("#div-search-map").is(":hidden") ) {
	    $("#div-search-map").show("slow");
	    $('#hide_search_map').html('Thu gọn');
	  } else {
	    $("#div-search-map").slideUp();
	    $('#hide_search_map').html('Tìm kiếm');
	  }
});

function searchHouses(params, is_remove_old) {
	search_params = params;
	$.ajax({
		type: "GET",
		url: "/json/get-house/",
		data: params,
		headers: {'X-CSRFToken': csrftoken}
	})
	.done(function(response) {
		if (response.HasError == true) {
			alert("Không có loại nhà trong khu vực bạn muốn tìm, bạn có thể mở rộng bán kính hoặc tìm địa điểm khác");
			return;
		}
		var data = response.data; 
		if (is_remove_old == true)
			$('#map').aviators_map('removeMarkers');
		
		$('#map').aviators_map('addMarkers', {
			locations: eval(data.locations),
			types    : eval(data.types),
			contents : eval(data.contents),
			images : eval(data.images)
		});
		var is_continue = response.data.is_continue;
		var details = data.details;
		loadHouseDetails(details, true);
		if (is_continue == true) {
			params.page = data.page;
			searchHouses(params, false);
		}
	});
}

function loadHouseDetails(houses, is_clear_old) {
	if (is_clear_old == true)
		$('#house_results').html('');
	if (houses) {
		$.each(houses, function(index, content) {
			var type = '';
			if (content.type == 0)
				type = 'Chung cư';
			else if (content.type == 1)
				type = 'Nguyên căn';
			else if (content.type == 2)
				type = 'Nhà trọ';
			
			var element_content = $('#result_template').html();
			element_content = element_content.replace(/{link}/g, content.link);
			element_content = element_content.replace(/{district}/g, content.district);
			element_content = element_content.replace(/{street}/g, content.street);
			element_content = element_content.replace(/{type}/g, type);
			element_content = element_content.replace(/{price}/g, content.price);
			element_content = element_content.replace(/{img}/g, content.img);
			element_content = element_content.replace(/{size}/g, content.size);
			element_content = element_content.replace(/{bedroom}/g, content.bedroom);
			element_content = element_content.replace(/{toalet}/g, content.toalet);
			element_content = $(element_content);
			element_content.show();
			$('#house_results').append(element_content);
		});
	}
}

$('.order_by').click(function() {
	$('.order_by').removeClass('selected');
	$(this).addClass('selected');
	search_params.order_by = $(this).attr('order_by');
	searchHouses(search_params);
});