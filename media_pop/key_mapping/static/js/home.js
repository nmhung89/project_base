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
		        $('#id_special_key').selectpicker('val', prefix);
		        $('#id_key').selectpicker('val', code);
		        $('#id_message').val('');
		        $('#id_message').focus();
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

$('#id_message').keydown(function(e) {
	if (e.keyCode == 13) {
		$('#id_enter_new_definition').click();
	}
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
		  		message: message,
		  		oper: 'edit'
		  	}
	})
	  .done(function(data) {
		  if (data.Code == 1) {
			  key_mapping[special_key + "_" + key] = {'Message': message, 
								                      'SpecialKey': special_key, 
								                      'Key': key, 
								                      'KeyText': key_text};
			  
			  repopulate_table(special_key + "_" + key);
			  
		      alertify.success(data.Message);
		  }
		  else {
			  alertify.error(data.Message);
		  }
	  });
});


$('#id_body_table').on('click', 'tr', function() {
	$('.active').removeClass('active');
	$(this).addClass('active');
	$('#id_special_key').selectpicker('val', $(this).find('.special_key').html());
    $('#id_key').selectpicker('val', $(this).find('.key').html());
    $('#id_message').val(htmlDecode($(this).find('.message').html()));
});

$('#id_body_table').on('click', '.remove', function() {
	var special_key = $(this).parent().find('.special_key').html();
	var key = $(this).parent().find('.key').html();
	$.ajax({
		  type: "POST",
		  url: "/json/input-definition/",
		  data: { 
			  		special_key: special_key, 
			  		key: key,
			  		oper: 'del'
			  	}
		})
		  .done(function(data) {
			  if (data.Code == 1) {
				  delete key_mapping[special_key + "_" + key];
				  
				  repopulate_table('');
				  
			      alertify.success(data.Message);
			  }
			  else {
				  alertify.error(data.Message);
			  }
		  });
});

function repopulate_table(selected) {
	$('#id_body_table').html('');
	$.each(key_mapping, function(key, value) {
		var tr_class = '';
		if (key == selected) {
			tr_class = 'active';
		}
		$('#id_body_table').append('<tr class="' + tr_class + '"><td class="special_key">' + value.SpecialKey + '</td>' + 
				'<td class="key_text">' + value.KeyText + '</td>' + 
				'<td class="message">' + htmlEncode(value.Message) + '</td>' + 
				'<td class="key">' + value.Key + '</td>' +
				'<td class="remove"><span class="glyphicon glyphicon-remove"></span></td></tr>');
	});
	
}

function htmlEncode(value){
	return $('<div/>').text(value).html();
}

function htmlDecode(value){
	return $('<div/>').html(value).text();
}
