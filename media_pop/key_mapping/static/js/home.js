$(document).keydown(function(e) {
	var prefix = '';
	var code = '';
	if (e.ctrlKey) {
		prefix = "CTRL";
		e.preventDefault();
	}
	else if (e.altKey) {
		prefix = "ALT";
		e.preventDefault();
	}
	else 
		return;
	
	if (e.keyCode < 65 || e.keyCode > 122)
		return;
	if (e.keyCode >= 97)
		code = e.keyCode - 32;
	else
		code = e.keyCode;
	var key = prefix + "_" + code;
	var message = key_mapping[key];
	if (message == undefined)
		message = 'This combination was not defined!';
	alert(message);
});

$('#id_enter_new_definition').click(function() {
	var special_key = $('#id_special_key').val();
	var key = $('#id_key').val();
	var key_text = $('#id_key option:selected').text();
	var message = $('#id_message').val();
	$.ajax({
	  type: "POST",
	  url: "/json/input-definition/",
	  data: { 
		  		special_key: special_key, 
		  		key: key,
		  		message: message
		  	}
	})
	  .done(function(data) {
		  if (data.Code == 1) {
			  $('#id_body_table').append('<tr><td>' + special_key + '</td><td>' + key_text + '</td><td>' + message + '</td></tr>');
			  key_mapping[special_key + "_" + key] = message;
		  }
		  else {
			  alert(data.Message);
		  }
	  });
});
