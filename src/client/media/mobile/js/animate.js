var intervalID = setInterval(function(){
	$("[shake='1']").each(function(index) {
		if (Math.random() < 0.3) {
      		//$(this).effect( "shake" ) ; //"shake", {"direction": this_dir} );
			$(this).attr('class', 'animated pulse infinite');
}
})

}, 1500);