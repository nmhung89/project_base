function htmlEncode(value){
	return $('<div/>').text(value).html();
}

function htmlDecode(value){
	return $('<div/>').html(value).text();
}

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
	if (message == undefined) {
		alertify.confirm("<b>Opps!</b> It seems that you have not defined a message for your keys.<br/>" +
				"Do you want to define them now?", function (e) {
		    if (e) {
		    	if ($('#id_special_key').html() != undefined) {
		    		//in case of bootstrap table
			        $('#id_special_key').selectpicker('val', prefix);
			        $('#id_key').selectpicker('val', code);
			        $('#id_message').val('');
			        $('#id_message').focus();
		    	} else {
			        //in case of jqgrid
			        $('#add_list').click();
			        $('#SpecialKey').val(prefix);
			        $('#Key').val(code);
			        $('#Message').focus();
		    	}
		    } else {
		        // user clicked "cancel"
		    }
		});
		return;
	}
	else {
		message = message.Message;
	}
	
	alertify.success(htmlEncode(message));
});