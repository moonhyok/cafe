$(document).ready(function()
{
	$("#osTable:has(tbody tr)").tablesorter({headers: { 0:{sorter: false}}, widgets: ['zebra']});
	
	$('#checkAll').live('click',function() 
	{
        var checked = $(this).attr('checked');
        $('input').attr('checked', checked);
    });
});

	function processComment(urlData)
	{
		try 
		{
			var table = dojo.byId('osTable');
			var rowCount = table.rows.length;
			var rowId = "";
			var report = "0";
			for(var i=0; i<rowCount; i++) 
			{
				var row = table.rows[i];
				var chkbox = row.cells[0].childNodes[0];
				if(null != chkbox && true == chkbox.checked) 
				{
					if(row != table.rows[0])
					{
						rowId = row.id.split("-")[1];
						var passingUrl = urlData + rowId + "/";
						dojo.xhrGet({
							url: passingUrl,
							handleAs: "json",
							load:function(response, ioArgs)
							{
								if (response.success)
								{
									if(report == "0")
									{
										if(table.rows.length == 1)
										{
											$("#osTable").hide();
											$("button").hide();
											$("#message").show();
										}										
										alert("Operation successful!");									
									}
									report = "1";
								}	
							},
							error:function(data)
							{ // This happens on a 500 error or alikes.
								alert('Error: failed sending data');
							}
						});				
						
					}
				}
			}
			deleteRow(table);
		}
		catch(e) 
		{
			alert(e);
		}		
	}
	
	function deleteRow(table) 
	{
			try 
			{
				var rowCount = table.rows.length;
				for(var i=0; i<rowCount; i++) 
				{
					var row = table.rows[i];
					var chkbox = row.cells[0].childNodes[0];
					if(chkbox != null && chkbox.checked == true) 
					{
						table.deleteRow(i);
						rowCount--;
						i--;
					}

				}
			}
			catch(e) 
			{
				alert(e);
			}
	}
