var slider_utils = (function($, d3, console) {
	
    return {
    };

})($, d3, console);

jQuery(document).ready(function(){

for (var i=1;i<=window.num_sliders;i++)
{
	$(".slider-progress").append("<div class=\"slider-progress-dot slider-progress-dot-"+i+"\"></div>")
}

//$( ".slider" ).append( "<span class=\"manual-slide manual-slide-left\"><</span>" );
$( ".slider" ).append( "<div class=\"crc-div-wrapper\"><div class=\"grade-container\"></div></div>" );

grades = ['A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F']
grades.forEach(function(grade) { 

	if(grade.indexOf('+') >= 0)
		$(".grade-container").append("<div class=\"slider-grade-bubble slider-grade-p bubble-" +grade.replace("+","p")+"\">"+grade+"</div>");
	else if (grade.indexOf('-') >= 0 ) 
		$(".grade-container").append("<div class=\"slider-grade-bubble slider-grade-m bubble-" +grade+"\">"+grade+"</div>");
	else	
		$(".grade-container").append("<div class=\"slider-grade-bubble slider-grade-main bubble-" +grade.replace("+","p")+"\">"+grade+"</div>");

});
$(".slider-grade-bubble").on("click",function(e){ 
	$(this).parent().children(".slider-grade-bubble").css("opacity","1.0"); 
	$(this).parent().children(".slider-grade-bubble").css("border","2px solid #FFFFFF");
	$(this).parent().children(".slider-grade-bubble").css("color","#FFFFFF");

	$(this).css("opacity","1.0"); 
	$(this).css("border","4px solid #00CCFF");
	$(this).css("color","#FFFFFF");
	//median = score_to_grade(100*medians[parseInt($(this).parent().parent().parent().attr("id").substring(7))]);
	
	//$(this).parent().children(".bubble-"+median.replace("+","p")).css("opacity","1.0");
	//$(this).parent().children(".bubble-"+median.replace("+","p")).css("border","1px solid #000000");
	//$(this).parent().children(".bubble-"+median.replace("+","p")).innerHTML = "<div style=\"font-size: 10px;\">Median</font>";
});

$(".slider-grade-bubble").on("touchstart",function(e){ 
	$(this).parent().children(".slider-grade-bubble").css("opacity","1.0"); 
	$(this).parent().children(".slider-grade-bubble").css("border","2px solid #FFFFFF");
	$(this).parent().children(".slider-grade-bubble").css("color","#FFFFFF");

	$(this).css("opacity","1.0"); 
	$(this).css("border","4px solid #00CCFF");
	$(this).css("color","#FFFFFF");
	//median = score_to_grade(100*medians[parseInt($(this).parent().parent().parent().attr("id").substring(7))]);
	
	//$(this).parent().children(".bubble-"+median.replace("+","p")).css("opacity","1.0");
	//$(this).parent().children(".bubble-"+median.replace("+","p")).css("border","1px solid #000000");
	//$(this).parent().children(".bubble-"+median.replace("+","p")).innerHTML = "<div style=\"font-size: 10px;\">Median</font>";
});
//$(".slider-grade-bubble").on("mouseover",function(e){ $(this).css("opacity","0.5"); });


});