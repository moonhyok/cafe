var slider_utils = (function($, d3, console) {
	
    return {
    };

})($, d3, console);

jQuery(document).ready(function(){

for (var i=1;i<=window.num_sliders;i++)
{
	/*$(".slider-progress").append("<div class=\"slider-progress-dot slider-progress-dot-"+i+"\"></div>")*/
}

//$( ".slider" ).append( "<span class=\"manual-slide manual-slide-left\"><</span>" );
$( ".slider" ).append( "<div class=\"crc-div-wrapper\"><div class=\"grade-container\"></div></div>" );

grades = ['A-','A','A+','B-','B','B+','C-','C','C+','D+']
grades.forEach(function(grade) { 

	if(grade.indexOf('+') >= 0)
		$(".grade-container").append("<div class=\"slider-grade-bubble slider-grade-p bubble-" +grade.replace("+","p")+"\">"+""+"</div>");
	else if (grade.indexOf('-') >= 0 ) 
		$(".grade-container").append("<div class=\"slider-grade-bubble slider-grade-m bubble-" +grade+"\">"+""+"</div>");
	else	
		$(".grade-container").append("<div class=\"slider-grade-bubble slider-grade-main bubble-" +grade.replace("+","p")+"\">"+""+"</div>");

});
$(".slider-grade-bubble").on("click",function(e){ 
	//$(this).parent().children(".slider-grade-bubble").css("opacity","1.0"); 
	//$(this).parent().children(".slider-grade-bubble").css("background-image","url()"); 
    
    $(this).parent().children(".slider-grade-bubble").each( function(i){
    	$(this).css("background-image",$(this).css("background-image").replace("keypad-down-0","keypad-0"));
	});

	//$(this).css("opacity","1.0"); 
	$(this).css("background-image",$(this).css("background-image").replace("keypad-0","keypad-down-0"));
	
	if($(this).parent().parent().parent().attr("id").substring(7).indexOf("importance") > -1)
	{
		var classList = $(this).attr('class').split(/\s+/);
		window.current_rating = grade_to_score(classList[2].substring(7).replace("p","+"));
		        $('.menubar').show();
        rate.doneRating();

        try {
            window.cur_clicked_mug.transition().duration(2000).style("opacity", "0").remove();
        } catch (err) {
            console.log(err);
        }
        //_this.transition().duration(500).style("opacity", "0");
        /* Remove this bloom from our bookkeeping array. */
        var index = jQuery.inArray(window.current_uid, window.blooms_list);
        if (index >= 0) {
            window.blooms_list.splice(index, 1);
        }
        /* Load more blooms if none left */
        try {
            if (window.blooms_list.length <= 2) {
                console.log("here");
                utils.showLoading("Loading More Mugs...");
                window.blooms_list = undefined; //needed to avoid infinite recursing
                setTimeout(blooms.populateBlooms, 500);
                //utils.hideLoading();
                // utils.showLoading("Loading More Ideas...", function() {
                //     populateBlooms();
                //});
                //utils.hideLoading(5000);
            }
        } catch (err) {
         /* undefined variable blooms. */
         console.log(err);
        }
		return;
	}
	else
	{
		//TODO cleanup
		$('.first-dialog-nav').hide();
        $('.slider-nav-box').show();

        if(window.current_slider +1 > window.num_sliders)
        {
            window.prev_state = 'grade';
        window.cur_state = 'register';
        rate.logUserEvent(5,'sliders finished');
        rate.storeSliders(window.num_sliders);
        
        if (window.authenticated) {
            for (var i = 1; i <= window.num_sliders; i++) {
                rate.sendSlider(window.sliders[i], i);
            }

        }

        }
        else
            {
                setTimeout(function(){
                window.current_slider = window.current_slider  + 1;
                var ua = navigator.userAgent.toLowerCase();
                var isAndroid = ua.indexOf("android") > -1; //&& ua.indexOf("mobile");
                if(isAndroid) {
                    $("#slide-"+window.current_slider).fadeIn(500);
                }   
                else
                    $("#slide-"+window.current_slider).show("slide", { direction: "right" }, 500);

                $("#slide-"+(window.current_slider-1)).hide();
                window.scrollTo(0,0); 
            },50);
                /*$(".slider-progress-dot-"+(parseInt(event.target.id.substring(5),10)+1)).css("background","#FFFFFF");*/

            }
	}

	try {
	statement_id = parseInt($(this).parent().parent().parent().attr("id").substring(7));
	var classList =$(this).attr('class').split(/\s+/);
	window.sliders[statement_id-1] = grade_to_score(classList[2].substring(7).replace("p","+"));
	median = score_to_grade(100*medians[statement_id]);
	rate.logUserEvent(11,'slider_set ' + statement_id + ' ' + window.sliders[statement_id-1]/10);

	/*$(this).parent().children(".bubble-"+median.replace("+","p")).css("border","4px solid #66FFFF");
	if (window.rate_count == 0){
	$(".median-grade-"+statement_id).html("The median grade so far is highlighted in blue.");
	$(".median-grade-"+statement_id).fadeIn(500);
	$(".median-grade-"+statement_id).fadeOut(6000);
	}*/
	
	//$(".skip-button-"+statement_id).hide();
	}
	catch(exception){}

	window.rate_count = window.rate_count + 1
	
	//$(this).parent().children(".bubble-"+median.replace("+","p")).innerHTML = "<div style=\"font-size: 10px;\">Median</font>";
});

$(".slider-grade-bubble").on("touchstart",function(e){ 

	$(this).css("background-image",$(this).css("background-image").replace("keypad-0","keypad-down-0"));
	
	if($(this).parent().parent().parent().attr("id").substring(7).indexOf("importance") > -1)
	{
		var classList = $(this).attr('class').split(/\s+/);
		window.current_rating = grade_to_score(classList[2].substring(7).replace("p","+"));
		return;
	}

	try {
	statement_id = parseInt($(this).parent().parent().parent().attr("id").substring(7));
	var classList =$(this).attr('class').split(/\s+/);
	window.sliders[statement_id-1] = grade_to_score(classList[2].substring(7).replace("p","+"));
	median = score_to_grade(100*medians[statement_id]);
	rate.logUserEvent(11,'slider_set ' + statement_id + ' ' + window.sliders[statement_id-1]/10);

	/*$(this).parent().children(".bubble-"+median.replace("+","p")).css("border","4px solid #66FFFF");
	if (window.rate_count == 0){
	$(".median-grade-"+statement_id).html("The median grade so far is highlighted in blue.");
	$(".median-grade-"+statement_id).fadeIn(500);
	$(".median-grade-"+statement_id).fadeOut(6000);
	}*/
	
	//$(".skip-button-"+statement_id).hide();
	}
	catch(exception){}

	window.rate_count = window.rate_count + 1

	//median = score_to_grade(100*medians[parseInt($(this).parent().parent().parent().attr("id").substring(7))]);
	
	//$(this).parent().children(".bubble-"+median.replace("+","p")).css("opacity","1.0");
	//$(this).parent().children(".bubble-"+median.replace("+","p")).css("border","1px solid #000000");
	//$(this).parent().children(".bubble-"+median.replace("+","p")).innerHTML = "<div style=\"font-size: 10px;\">Median</font>";
});
//$(".slider-grade-bubble").on("mouseover",function(e){ $(this).css("opacity","0.5"); });


});