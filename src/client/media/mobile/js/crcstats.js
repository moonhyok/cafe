
function drawlines(){

  var canvas = document.getElementById('seperate-lines1');
  var context = canvas.getContext('2d');
  context.beginPath();
  context.moveTo(0, 0);
  context.lineTo(260, 0);
  context.strokeStyle = '#ffffff';
  context.lineWidth = 1;
  context.stroke();
  context.beginPath();
  context.moveTo(0, 4);
  context.lineTo(260, 4);
  context.strokeStyle = '#ffffff';
  context.lineWidth = 1;
  context.stroke();
  
   var canvas = document.getElementById('seperate-lines2');
      var context = canvas.getContext('2d');
      context.beginPath();
      context.moveTo(0, 0);
      context.lineTo(260, 0);
      context.strokeStyle = '#ffffff';
      context.lineWidth = 1;
      context.stroke();
      context.beginPath();
      context.moveTo(0, 4);
      context.lineTo(260, 4);
      context.strokeStyle = '#ffffff';
      context.lineWidth = 1;
      context.stroke();
      
            var canvas = document.getElementById('seperate-lines3');
      var context = canvas.getContext('2d');
      context.beginPath();
      context.moveTo(0, 0);
      context.lineTo(260, 0);
      context.strokeStyle = '#ffffff';
      context.lineWidth = 1;
      context.stroke();
      context.beginPath();
      context.moveTo(0, 4);
      context.lineTo(260, 4);
      context.strokeStyle = '#ffffff';
      context.lineWidth = 1;
      context.stroke();
      
            var canvas = document.getElementById('seperate-lines4');
      var context = canvas.getContext('2d');
      context.beginPath();
      context.moveTo(0, 0);
      context.lineTo(260, 0);
      context.strokeStyle = '#ffffff';
      context.lineWidth = 1;
      context.stroke();
      context.beginPath();
      context.moveTo(0, 4);
      context.lineTo(260, 4);
      context.strokeStyle = '#ffffff';
      context.lineWidth = 1;
      context.stroke();

}

drawlines()
$.get(window.userhist1_url) // check if the histogram exists
    .done(function() { 
        var img = $('<img width="310">');
        img.attr('src', window.userhist1_url);
        img.appendTo('#userhist1');

    }).fail(function() { 
		if (window.show_hist1){
           $( "#userhist1" ).html( "<span style='left:23px; position:relative; font-size:14px;color: #f5ebde;'>The statistics are calculated on a daily basis. Please revisit tomorrow</span><br/>" );
	    }
	    else{
			$( "#userhist1" ).html( "<span style='left:23px; position:relative; font-size:14px;color: #f5ebde;'>You haven't received any grade</span><br/>" );
		}
    })
    
$.get(window.userhist2_url) // check if the histogram exists
    .done(function() { 
        var img = $('<img width="310">');
        img.attr('src', window.userhist2_url);
        img.appendTo('#userhist2');

    }).fail(function() { 
		if (window.show_hist2){
           $( "#userhist2" ).html( "<span style='left:23px; position:relative; font-size:14px;color: #f5ebde;'>The statistics are calculated on a daily basis. Please revisit tomorrow</span><br/>" );
	    }
	    else{
			$( "#userhist2" ).html( "<span style='left:23px; position:relative; font-size:14px;color: #f5ebde;'>You haven't received any grade</span><br/>" );
		}
    })
