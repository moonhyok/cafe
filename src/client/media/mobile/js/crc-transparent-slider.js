var slider_utils = (function($, d3, console) {
	
	var grade_to_offset = {'Ap': -100, 'A': -49, 'A-': 2, 'Bp': 53,'B': 104,'B-':155,'Cp':206,'C':257,'C-':308,'Dp':359,'D':410,'D-':461,'F':512};

	function focusSlider(slider){
		current_pos = slider.children(".grade-container").css("right");
		current_pos = current_pos.substring(0,current_pos.length - 2);
		current_pos = parseInt(current_pos,10);
		for (var grade in grade_to_offset)
		{
			if(grade_to_offset[grade] == current_pos)
			{
				slider.children(".grade-container").children(".bubble-"+grade).css("border","1px solid #3f8b44");
				slider.children(".grade-container").children(".bubble-"+grade).css("backgroundColor","rgba(255, 255, 255, 0.3)");
			}
			else
			{
				slider.children(".grade-container").children(".bubble-"+grade).css("border","1px solid #FFFFFF");
				slider.children(".grade-container").children(".bubble-"+grade).css("backgroundColor","transparent");
			}
		}
	}

	function setOpacity(slider){
		current_pos = slider.children(".grade-container").css("right");
		current_pos = current_pos.substring(0,current_pos.length - 2);
		current_pos = parseInt(current_pos,10);
		for (var grade in grade_to_offset)
		{
			opacity_slider = (1-Math.abs(grade_to_offset[grade] - current_pos)/612.0);
			slider.children(".grade-container").children(".bubble-"+grade).css("opacity",Math.pow(opacity_slider,4));
		}
	}

    return {
    	'grade_to_offset':grade_to_offset,
    	'focusSlider': focusSlider,
    	'setOpacity': setOpacity
    };

})($, d3, console);

jQuery(document).ready(function(){

$( ".slider" ).append( "<span class=\"manual-slide manual-slide-left\"><</span>" );
$( ".slider" ).append( "<div class=\"crc-div-wrapper\"><div class=\"grade-container\"></div></div>" );

grades = ['A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F']
grades.forEach(function(grade) { $(".grade-container").append("<div class=\"slider-grade-bubble bubble-" +grade.replace("+","p")+"\">"+grade+"</div>");});
$( ".slider" ).append( "<span class=\"manual-slide manual-slide-right\">></span>" );
slider_utils.focusSlider($( ".slider" ).children(".crc-div-wrapper"));
slider_utils.setOpacity($( ".slider" ).children(".crc-div-wrapper"));

//$('.slider').click(function() {alert(this.children[1].children[0]);});

$('.manual-slide-left').click(function() {
									var current_pos = $(this).parent().children(".crc-div-wrapper").children(".grade-container").css("right");
									current_pos = current_pos.substring(0,current_pos.length - 2);
									current_pos = current_pos - 51;
									current_pos = Math.min(Math.max(current_pos,-100),512);
									$(this).parent().children(".crc-div-wrapper").children(".grade-container").css("right",current_pos+"px");
									slider_utils.focusSlider($(this).parent().children(".crc-div-wrapper"));
									slider_utils.setOpacity($(this).parent().children(".crc-div-wrapper"));

								});

$('.manual-slide-right').click(function() {
									var current_pos = $(this).parent().children(".crc-div-wrapper").children(".grade-container").css("right");
									current_pos = current_pos.substring(0,current_pos.length - 2);
									current_pos = parseInt(current_pos,10) + 51;
									current_pos = Math.min(Math.max(current_pos,-100),512);
									$(this).parent().children(".crc-div-wrapper").children(".grade-container").css("right",current_pos+"px");
									slider_utils.focusSlider($(this).parent().children(".crc-div-wrapper"));
									slider_utils.setOpacity($(this).parent().children(".crc-div-wrapper"));

								});

/*$(".crc-div-wrapper").on("swipeleft",function(){
        var current_pos = $(this).children(".grade-container").css("right");
		current_pos = current_pos.substring(0,current_pos.length - 2);
		current_pos = parseInt(current_pos,10) + 51;
		$(this).parent().children(".crc-div-wrapper").children(".grade-container").css("right",current_pos+"px");
        });

$(".crc-div-wrapper").on("swiperight",function(){
        var current_pos = $(this).children(".grade-container").css("right");
		current_pos = current_pos.substring(0,current_pos.length - 2);
		current_pos = current_pos - 51;
		$(this).parent().children(".crc-div-wrapper").children(".grade-container").css("right",current_pos+"px");
        });*/

$(".crc-div-wrapper").on("vmousedown",function(e){
        x=e.pageX;
        y=e.pageY;
        window.mousedown  =x;
        });

$(".crc-div-wrapper").on('vmousemove',function(e){
  
  if(window.mousedown != 0)
  {x=e.pageX;
  y=e.pageY;
  var current_pos = $(this).children(".grade-container").css("right");
  current_pos = current_pos.substring(0,current_pos.length - 2);
  current_pos = parseInt(current_pos,10) - (x - window.mousedown)/20;

  current_pos = Math.min(Math.max(current_pos,-100),512);
  slider_utils.setOpacity($(this));
  $(this).parent().children(".crc-div-wrapper").children(".grade-container").css("right",current_pos+"px");
	}

});


$(".crc-div-wrapper").on("vmouseup",function(e){
        x=e.pageX;
        y=e.pageY;
        var current_pos = $(this).children(".grade-container").css("right");
									current_pos = current_pos.substring(0,current_pos.length - 2);
									current_pos = parseInt(current_pos,10) - 257;
									current_pos = Math.round(current_pos/51.0)*51.0 + 257;
									current_pos = Math.min(Math.max(current_pos,-100),512);
									$(this).parent().children(".crc-div-wrapper").children(".grade-container").css("right",current_pos+"px");
        					window.mousedown  =0;
        					slider_utils.focusSlider($(this));
        					slider_utils.setOpacity($(this));
        });

$(".crc-div-wrapper").on("touchstart",function(e){
        x=e.pageX;
        y=e.pageY;
        window.mousedown  =x;
        });

$(".crc-div-wrapper").on('touchmove',function(e){
  
  if(window.mousedown != 0)
  {x=e.pageX;
  y=e.pageY;
  var current_pos = $(this).children(".grade-container").css("right");
  current_pos = current_pos.substring(0,current_pos.length - 2);
  current_pos = parseInt(current_pos,10) - (x - window.mousedown)/20;

  current_pos = Math.min(Math.max(current_pos,-100),512);
  slider_utils.setOpacity($(this));
  $(this).parent().children(".crc-div-wrapper").children(".grade-container").css("right",current_pos+"px");
	}

});


$(".crc-div-wrapper").on("touchend",function(e){
        x=e.pageX;
        y=e.pageY;
        var current_pos = $(this).children(".grade-container").css("right");
									current_pos = current_pos.substring(0,current_pos.length - 2);
									current_pos = parseInt(current_pos,10) - 257;
									current_pos = Math.round(current_pos/51.0)*51.0 + 257;
									current_pos = Math.min(Math.max(current_pos,-100),512);
									$(this).parent().children(".crc-div-wrapper").children(".grade-container").css("right",current_pos+"px");
        					window.mousedown  =0;
        					slider_utils.focusSlider($(this));
        					slider_utils.setOpacity($(this));
        });


});