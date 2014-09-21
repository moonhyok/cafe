$.get(window.userhist1_url) // check if the histogram exists
    .done(function() { 
        var img = $('<img/>');
        img.attr('src', window.userhist1_url);
        img.appendTo('#userhist1');

    }).fail(function() { 
		if (window.show_hist1){
           $( "#userhist1" ).html( "<span style=' font-size:14px;color: #f5ebde;'>The statistics are calculated on a daily basis. Please revisit tomorrow</span><br/>" );
           document.getElementById( "userhist1" ).style.height="20px";
	    }
	    else{
			$( "#userhist1" ).html( "<span style=' font-size:14px;'>You haven't received any grades</span><br/>" );
			document.getElementById( "userhist1" ).style.height="20px";
		}
    })
    
$.get(window.userhist2_url) // check if the histogram exists
    .done(function() { 
        var img = $('<img/>');
        img.attr('src', window.userhist2_url);
        img.appendTo('#userhist2');

    }).fail(function() { 
		if (window.show_hist2){
           $( "#userhist2" ).html( "<span style=' font-size:14px;'>The statistics are calculated on a daily basis. Please revisit tomorrow</span><br/>" );
           document.getElementById( "userhist2" ).style.height="20px";
	    }
	    else{
			$( "#userhist2" ).html( "<span style=' font-size:14px;'>You haven't received any grades</span><br/>" );
			document.getElementById( "userhist2" ).style.height="20px";
		}
    })
