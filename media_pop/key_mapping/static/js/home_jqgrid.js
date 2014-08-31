jQuery("#list").jqGrid({
   	url:'json/load-grid-data/',
   	editurl:'json/edit-grid-data/',
	datatype: "json",
   	colNames:['Special key', 'Key', 'Message'],
   	colModel:[
   		{name:'SpecialKey',index:'SpecialKey', width:100, editable: true, edittype: 'select', editoptions: {value: special_keys}},
   		{name:'Key',index:'Key', width:100, editable: true, edittype: 'select', editoptions: {value: keys}},
   		{name:'Message',index:'Message', width:400, editable: true, sortable:false}
   	],
   	rowNum:10,
   	rowList:[10,20,30],
   	pager: '#pager',
    viewrecords: true,
    height: 'auto',
    caption:"Key Mapping"
});

jQuery("#list").jqGrid('navGrid','#pager',{
	edit:true, add:true, del:true, search:false}, {
		//edit
		beforeShowForm : function() { 
			$('#SpecialKey').attr('disabled', true);
			$('#SpecialKey').css('background', 'rgb(241, 241, 241)');
			$('#Key').css('background', 'rgb(241, 241, 241)');
			$('#Key').attr('disabled', true);
		},
		closeAfterEdit: true,
		afterSubmit: function(response, postdata){
			response = response.responseJSON;
            if(response.Code == 1) {
                 success = true;
                 alertify.success(response.Message);
                 key_mapping[response.Key] = response.Data;
            }
             else 
            	 success = false;

             return [success, response.Message]
         }
	}, {
		//add
		closeAfterAdd: true,
		afterSubmit: function(response, postdata){
			response = response.responseJSON;
            if(response.Code == 1) {
                 success = true;
                 alertify.success(response.Message);
                 key_mapping[response.Key] = response.Data;
            }
             else 
            	 success = false;
            
             return [success, response.Message]
         }
	}, {
		//del
		afterSubmit: function(response, postdata){
			response = response.responseJSON;
			delete key_mapping[response.Key];
			alertify.success(response.Message);
			return [true, ''];
         }
	}

);