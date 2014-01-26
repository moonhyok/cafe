/* 
ga('send', 'event', 'category', 'action', 'label', value); 

category - object interacted with
action - type of interaction (e.g. click)
label - useful for categorizing events
value - non-negative number
*/

$(document).ready(function() {

	$('.first-time-btn').on('click', function() {
		ga('send', 'event', 'Begin Button', 'click');
	});

	$('.help-btn-dialog').on('click', function() {
		ga('send', 'event', 'About Link Clicked', 'click');
	});


	$('.done-endsliders-btn').on('click', function() {
		ga('send', 'event', 'Finished Report Card', 'click');		
	});

	$('.skip-img-btn').click(function() {
		var num = $(this).attr('id').replace("skip-img", "");
		ga('send', 'event', 'Skipped Subject', 'click', '# ' + num);
	});

	$('#registerb').click(function() {
		ga('send', 'event', 'Submit Zip Code', 'click');
	});

	$('.dialog-ready').click(function() {
		ga('send', 'event', 'Join the Discussion Dialog', 'click');
	});

	$('#go-back').click(function() {
		ga('send', 'event', 'Rated Comment', 'click');		
	});

	$('.comment-submit-btn').click(function() {
		ga('send', 'event', 'Submit Comment', 'click');
	});

	$('.comment-cancel-btn').click(function() {
		ga('send', 'event', 'Post Comment Later', 'click');		
	});

	$('.dialog-continue-ready').click(function() {
		ga('send', 'event', 'Email Submit', 'click');	
	});

	$('.dialog-email-ready ').click(function() {
		ga('send', 'event', 'Continue Grading After Email', 'click');		
	});

	$(".home-btn-dialog").click(function() {
		var parent = $(this).parent().parent().attr("class").split(/\s+/)[0];
		ga('send', 'event', 'Go Home', 'click',  'from ' + parent);
	});

	$(".help-btn-dialog").click(function() {
		var parent = $(this).parent().parent().attr("class").split(/\s+/)[0];
		ga('send', 'event', 'View Help', 'click', 'from ' + parent);
	});

	$(".back-btn-dialog").click(function() {
		var parent = $(this).parent().parent().attr("class").split(/\s+/)[0];
		ga('send', 'event', 'Go Back', 'click', 'from ' + parent);
	});

	$(".logout-btn").click(function() {
		var parent = $(this).parent().parent().attr("class").split(/\s+/)[0];
		ga('send', 'event', 'Logout', 'click', 'from ' + parent);
	});

	$("#flag1").click(function() {
		var parent = $(this).parent().parent().attr("class").split(/\s+/)[0];
		ga('send', 'event', 'Flagged Idea', 'click');
	});

});