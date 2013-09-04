$(document).ready(function() {
	
	utils.blooms();

	$(window).resize(function() {
		console.log('hello');
		utils.blooms();
	});

	$('#reg_form').submit(function(e) {
		e.preventDefault();
		e.stopPropagation();

		//The following set of code is needed to format the data for the login which occurs after the registration
		var serializedData = $(this).serializeArray();
		var names = serializedData.map(function(r) {
			return r.name;
		});
		var index_user = names.indexOf("regusername");
		var index_pass = names.indexOf("regpassword1");
		var index_email = names.indexOf("regemail");

		var data2 = {};
		data2["username"] = serializedData[index_user].value;
		data2["password1"] = serializedData[index_pass].value;
		data2["password"] = serializedData[index_pass].value;
		data2["password2"] = serializedData[index_pass].value;
		data2["email"] = serializedData[index_email].value;

		console.log(data2);

		var serializedFormData = $(this).serialize();

		$.ajax({
			url: window.url_root + '/accountsjson/register/',
			type: 'POST',
			dataType: 'json',
			data: data2,
			success: function(data) {
				console.log(data); //remove
				if (data.hasOwnProperty('success')) {
					// now we can take whatever means necessary.
					console.log("successful registration detected!!");

					// $.mobile.loading( 'show', {
					// 	text: 'foo',
					// 	textVisible: true,
					// 	theme: 'z',
					// 	html: ""
					// });
					utils.loginAfterRegister(data2);
					$('.register').slideUp();
					//$('.comment-input').slideDown();
					$('.frame').hide();
				} else {
					utils.showRegister();
					if (data.hasOwnProperty('form_errors')) {
						document.getElementById("username-error").style.display = "none";
						document.getElementById("password-error").style.display = "none";
						document.getElementById("email-error").style.display = "none";

						var errors = data['form_errors'];

						if ('username' in errors) {
							document.getElementById("username-error").innerHTML = errors['username'];
							document.getElementById("username-error").style.display = "";
						}

						if ('email' in errors) {
							document.getElementById("email-error").innerHTML = errors['email'];
							document.getElementById("email-error").style.display = "";
						}

						if ('password1' in errors) {
							document.getElementById("password-error").innerHTML = errors['password1'];
							document.getElementById("password-error").style.display = "";
						}

						$('#register').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');


					}
				}
			},
			error: function() {
				console.log("ERROR posting registration request. Abort!");
			},
		});


		//$.post('http://opinion.berkeley.edu', function (data) {
		//if (data.hasOwnPropertry('success')) {
		//	$.post('http://opinion.berkeley.edu/learning/acountsjson/login',{'username':params.username, 'password':'params.password'});
		//}
		//});
	});

	$('#login_form').submit(function(e) {
		e.preventDefault();
		e.stopPropagation();

		// make the form data into a request string that can be passed to POST


		var serializedFormData = $(this).serialize();


		// ajax POST to url, pass the serialized form data and interpret the response as a JSON object
		// call the success function if the request succeeds, otherwise log an error
		$.ajax({
			url: window.url_root + '/accountsjson/login/',
			type: 'POST',
			dataType: 'json',
			data: serializedFormData,
			success: function(data) {
				if (data.hasOwnProperty('success')) {
					// now we can take whatever means necessary.
					console.log("successful login detected!!");
					console.log(data); //remove
					location.reload();
				} else {
					console.log("this was a failed attempt")
					document.getElementById("login-error").style.display = "";
					// this "unpresses" the button if the login was in correct
					$('#login').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');

				}
			},
			error: function() {
				console.log("ERROR posting login request. Abort!");
			}
		});
	});
});