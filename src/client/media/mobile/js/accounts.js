// accounts.js
// Handles authentication, registration, login
// Dependencies: jQuery

var accounts = (function($, d3, console) {
    // Enable strict javascript interpretation
    "use strict";
    // a function to pull up the registration prompt

    function showRegister() {
        $('.register').slideDown();
        $('#finishRegistration').click(function() {});
    }

    function showCommentInput() {
        $('.comment-input').slideDown();
    }

    // a function to pull up the login prompt.

    function showLogin() {
        $('.landing').slideUp();
        $('.login').slideDown();
    }

    //function that determines if the user has already rated 2 comments
    // and should now login/ register to move forward.

    function readyToLogin() {
        return window.ratings && window.ratings.length >= 2;
    }

    // function that determines if the user should register to continue
    // it returns true when both the registration sliders have been saved.

    function mustRegister() {
        return window.sliders && window.sliders.length >= 1;
    }

    //function that removes the landing page and populates the map when the first time button is clicked.

    function firstTime() {
        utils.showLoading("Loading the garden...", function() {
            utils.ajaxTempOff(blooms.populateBlooms);

            setTimeout(function() { // d3 needs a little extra time to load
                $('.landing').slideUp('fast', function() {
                    utils.hideLoading(1000);
                });
            }, 1500);
        });
    }
    // Checks to see if the user has logged in and sets window.authentiated.
    // This is used to change the behavior of the site for users
    // that have logged in. (Mostly to send data to server immediately)

    function setAuthenticated() {
        utils.ajaxTempOff(function() {
            $.getJSON(window.url_root + '/os/show/1/', function(data) {
                window.authenticated = data['is_user_authenticated'];
            });
        });

        return window.authenticated;
    }

    //@logindata - data is in a serialized form
    //This function is used specifically to login right after registration. This function also
    //  sends the data that has been stored in the window to the server after a successful the login.

    function loginAfterRegister(loginData) {
        $.ajax({
            url: window.url_root + '/accountsjson/login/',
            type: 'POST',
            dataType: 'json',
            data: loginData,
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    console.log("successful login detected!!");
                    //rate.sendComment(window.comment);
                    rate.logUserEvent(0,'login');
                    for (var i = 1; i <= window.num_sliders; i++) {
                        rate.sendSlider(window.sliders[i], i);
                        //blooms will be populated at the end of this! see callback
                        //there are two calls!!
                    }
                    accounts.initLoggedInFeatures(true);
                    
                    //for (i = 0; i < window.ratings.length - 1; i++) {
                    //    rate.sendAgreementRating(window.ratings[i]);
                    //    rate.sendInsightRating(window.ratings[i]);
                    //}

                    //rate.sendAgreementRating(window.ratings[window.ratings.length - 1]);
                    //rate.sendInsightRating(window.ratings[window.ratings.length - 1]);
                    //window.authenticated = true;
                } else {
                    // we should rerender the form here.
                }
            },
            error: function() {
                console.log("ERROR posting login request. Abort!");
            }
        });
    }


    function loadMyCommentDiv() {
        utils.ajaxTempOff(function() {
            $.getJSON(window.url_root + '/os/show/1/', function(data) {
                try {
                    var comment = data['cur_user_comment'][0][0];
                    $('.comment-text').html(comment);
                    $('.edit-comment-box').html(comment);
                } catch (err) {
                    // probably an admin user or something. they didn't have a comment
                }
            });
        });

        $('.my-comment').slideDown();
        $('.menubar').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');

    }

    /** Sets the field ".num-rated-by" to the number of people who've rated the 
     *  users comment. */

    function setNumRatedBy() {
        utils.ajaxTempOff(function() {
            $.getJSON(window.url_root + '/os/ratedby/1/', function(data) {
                $('.num-rated-by').text(data['sorted_comments_ids'].length);
            });

        });
    }

    /** Sets up all the stuff that loggedIn users expect and need. 
     *  JUSTREGISTERED is a boolean and optional. Used to shortcircuit showGraphs.
     */

    function initLoggedInFeatures(justRegistered) {
        $('.top-bar').show();
        justRegistered = typeof justRegistered !== 'undefined' ? justRegistered : false;

        utils.ajaxTempOff(function() {
            stats.showGraphs(justRegistered);

            //var data = $.getJSON(window.url_root + '/os/show/1/');
            $.getJSON(window.url_root + '/os/show/1/', function(data) {
                $('.score-value').text("" + ~~(data['cur_user_rater_score'] * window.conf.SCORE_SCALE_FACTOR));
                window.user_score = data['cur_user_rater_score'];
                $('.username').text(' ' + data['cur_username']);
            });

        });
        
        if (window.user_score == 0) {
            $('.dialog').show();
        } else {
            rate.initMenubar();
        }
        setNumRatedBy();
    }
    
    function sendEmail(mail){
		
		$.ajax({
            type: "POST",
            dataType: 'json',
            url: window.url_root + "/confirmationmail/",
            data: {'mail':mail},
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    //console.log("data was sent!")
                }
            },
            error: function() {
				
                console.log("email didn't get sent!");
            }
        });
	}
    return {
        'showCommentInput': showCommentInput,
        'showRegister': showRegister,
        'showLogin': showLogin,
        'readyToLogin': readyToLogin,
        'mustRegister': mustRegister,
        'firstTime': firstTime,
        'setAuthenticated': setAuthenticated,
        'loginAfterRegister': loginAfterRegister,
        'loadMyCommentDiv': loadMyCommentDiv,
        'initLoggedInFeatures': initLoggedInFeatures,
        'sendEmail': sendEmail
    };

})($, d3, console);

$(document).ready(function() {
    $('#reg_form').submit(function(e) {
        $('#register').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');
        e.preventDefault();
        e.stopPropagation();
        rate.logUserEvent(9,'register');
        
        if (window.registration_in_progress) {
            return;
        }
        else{
            window.registration_in_progress = true;
        }

        $("#username-error").hide();
        $("#password-error").hide();
        $("#zipcode-error").hide();

        /*Let us leave this to the server to handle
        // Handle bad length zipcodes client-side
        if ($('#regzip').val().length != 5) {
            $("#zipcode-error").html("Please enter a 5 digit zipcode.");
            $("#zipcode-error").show();
            $('#registerpanel').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');
            return;
        }*/
        
        var registrationData = {
            "username": $('#regusername').val(),
            "password": $('#regpassword1').val(),
            "password1": $('#regpassword1').val(),
            "password2": $('#regpassword1').val(),
            "email": $('#regemail').val(),
            "zipcode" : ($('#regzip').val() == '')?'-1':$('#regzip').val()
        };

        var loginData = {
            "username": registrationData.username.toLowerCase(),
            "password": registrationData.password,
        };

        utils.ajaxTempOff(function() {
            $.ajax({
                url: window.url_root + '/accountsjson/register/',
                type: 'POST',
                dataType: 'json',
                data: registrationData,
                success: function(data) {
                    $("#username-error").hide();
                    //$("#email-error").hide();
                    $("#password-error").hide();

                    window.foo = data;
                    window.registration_in_progress = false;

                    if (data.hasOwnProperty('success')) {
                        accounts.setAuthenticated();
                        utils.showLoading("Loading...", function() {
                            accounts.loginAfterRegister(loginData);
                            blooms.populateBlooms();
                            $('.register').slideUp();
                            utils.hideLoading();
                            /*setTimeout(function() { //give d3 some extra time
                                $('.register').slideUp('fast', function() {
                                    utils.hideLoading(500);
                                });
                            }, 500);*/
                        });
                        //accounts.setAuthenticated();
                    } else {
                        accounts.showRegister();
                        if (data.hasOwnProperty('form_errors')) {

                            var errors = data['form_errors'];

                            if ('username' in errors) {
                                $("#username-error").html(errors['username']);
                                $("#username-error").show();
                            }

                            /* if ('email' in errors) {
                                $("#email-error").html(errors['email']);
                                $("#email-error").show();
                            }*/

                            if ('password1' in errors) {
                                $("#password-error").html(errors['password1']);
                                $("#password-error").show();
                            }

                            try {
                            //TODO: why doesn't this come up under form_errors[zip_code]
                                if (data['form_errors']['__all__'][0]) {
                                    $("#zipcode-error").html(data['form_errors']['__all__'][0]);
                                    $("#zipcode-error").show();
                                }
                            } catch(err) { }

                        }
                    }
                },
                error: function() {
                    console.log("ERROR posting registration request. Abort!");
                },
            });
        });
    });

    $('#login_form').submit(function(e) {
        e.preventDefault();
        e.stopPropagation();

        var serializedFormData = $(this).serialize();

        utils.ajaxTempOff(function() {
            $.ajax({
                url: window.url_root + '/accountsjson/login/',
                type: 'POST',
                dataType: 'json',
                data: serializedFormData,
                success: function(data) {
                    $("#login-error").hide();

                    if (data.hasOwnProperty('success')) {
                        accounts.setAuthenticated();
                        utils.showLoading("Loading...", function() {
                            blooms.populateBlooms();
                            accounts.initLoggedInFeatures();
                            $('.top-bar').show();

                            setTimeout(function() { // d3 needs a little extra time to load
                                $('.login').slideUp('fast', function() {
                                    utils.hideLoading(1000);
                                });
                            }, 1000);
                        });
                    } else {
                        console.log("Failed login attempt");
                        $('#login-error').text(data['form_errors'].__all__[0]);
                        $("#login-error").show();
                        $('#login').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');

                    }
                },
                error: function() {
                    console.log("ERROR posting login request. Abort!");
                }
            });
        });

    });

    $('.first-time-btn').click(function() {
        //accounts.firstTime();
        $('.landing').slideUp();
        $('.endsliders').slideDown();
        rate.logUserEvent(7,'first time');
        //$('.top-bar').show();
        //rate.initScore();
    });

    $('.login-btn').click(function() {
        accounts.showLogin();
    });

    $('.login-form-go-back').click(function() {
        $('.landing').slideDown();
        $('.login').slideUp();
    });

    $('.my-comment-btn').click(function() {
        accounts.loadMyCommentDiv();
    });

    $('.edit-comment-btn').click(function() {
        $('.comment-region').hide();
        $('.edit-comment').show();
    });
    
    $('#flag').click(function() {
        document.getElementById('flag').innerHTML='<strong>Flagged for Review</strong>';
            $.ajax({
            type: "POST",
            url: window.url_root + "/os/flagcomment/1/"+window.current_cid+"/",
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    console.log("flag successfully sent");
                }
            },
            error: function() {
                console.log("ERROR flag didn't get sent");
            }
        });
    });

    $('.dialog-ready').click(function() {
        rate.logUserEvent(8,'dialog 1');
        //rate.initMenubar();
        $('.instructions').show();
        $('.dialog').slideUp();
    });
    
    $('.dialog-score-ready').click(function() {
        rate.logUserEvent(8,'dialog 2');
        $('.dialog-score').slideUp();
        $('.scorebox').show();
        //rate.initMenubar();
    });
    
    $('.dialog-continue-ready').click(function() {
        rate.logUserEvent(8,'dialog 3');
        $('.dialog-continue').hide();
        rate.initMenubar();
        $('.scorebox').show();
    });
    
    $('.dialog-yourmug-ready').click(function() {
        rate.logUserEvent(8,'dialog 4');
        $('.dialog-yourmug').slideUp();
        rate.initMenubar();
        $('.scorebox').show();
        try{
            window.your_mug.transition().duration(1000).style("opacity", "1");
        }catch(err){
            console.log(err);
        }
    });


    $('.edit-comment-save-btn').click(function() {
        rate.sendComment($('.edit-comment-box').val());
        $('.menubar').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');

        $('.my-comment').slideUp('slow', function() {
            $('.edit-comment').hide();
            $('.comment-region').show();
        });
    });

    $('.edit-comment-cancel-btn').click(function() {
        $('.comment-region').show();
        $('.edit-comment').hide();
    });

    $('.edit-comment-done-btn').click(function() {
        $('.menubar').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');
        $('.my-comment').slideUp();
    });

    $('.logout-btn').click(function(e) {
        rate.logUserEvent(1,'logout');
        $('.logout').show();
        e.preventDefault();
        e.stopPropagation();
        window.history.pushState("", "", '/mobile');

        $.ajax({
            url: window.url_root + '/accountsjson/logout/',
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    // TODO: this needs to be cleaned up into some sort of function
                    // and this logic is shitty and it's not resetting the score labels well
                    //$('.landing').show();
                    window.user_score = undefined;
                    window.authenticated = false;
                    $('.menubar').hide();
                    rate.resetEndSliders();
                } else {}
            },
            error: function() {
                console.log("ERROR posting login request. Abort!");
            }
        });

    });

    $('.logout-start-over').click(function() {
        location.reload();
    });

    $('.logout-login-again').click(function() {
        $('.logout').slideUp();
        $('.login').slideDown();
    });
    
    $('#regrade-btn').click(function(){
		$('.welcome-back').hide();
		$('.endsliders').show();
	});
	
	$('#garden-btn').click(function(){
		$('.welcome-back').slideUp();
                $('.menubar').show();
	});
});
