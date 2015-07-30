// rate.js
// Handles ratings and scoring
// Dependencies: jQuery

var rate = (function($, d3, console) {
    // Enable strict javascript interpretation
    "use strict";

    // update the questions element in the html
    function updateDescriptions(answer, content) {
        $('#commentInput').html(content);
    }

    function updateDescriptionsSpanish(answer, content) {
        $('#commentInputSpanish').html(content);
    }
    
    function logUserEvent(logtype,buttonType) {
        $.ajax({
            type: "POST",
            url: window.url_root + "/log/userevent/",
            data: {
                'log_type': logtype,
                'details': buttonType
            },
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    console.log("Event logged");
                }
            },
            error: function() {
                console.log("Log save failed");
            }
        });
    }

    function updateScoreHolders() {
        $('.score-value').html((~~(window.user_score * window.conf.SCORE_SCALE_FACTOR)).toString());
    }
    
    function resetRatingSliders() {
        setTimeout(function() {
            $("#slider1").val(50); //.slider("refresh");
        }, 1500);
        setTimeout(function() {
            $("#slider2").val(50); //.slider("refresh");
        }, 1500);
        setTimeout(function() {
            document.getElementById('flag').innerHTML='';
        }, 500);
        // setTimeout(function() {
        //     $("#studentTag").val('Select Appropriate Tag').selectmenu('refresh'); //.slider("refresh");
        // }, 500);
    }

    function resetEndSliders() {
        for (var i = 1; i <= window.num_sliders; i++) {
            $("#s" + i.toString()).val(50).slider("refresh");
        }
    }

    function logScore() {
        if (window.user_score === undefined) {
            window.user_score = 1;
        } else {
            window.user_score += 1;
        }
        updateScoreHolders();

    }

    function changeInstruction(t) {
        //$('.inst_text').text(t);
    }

    function initScore() {
        //$('.inst-score').prepend('[');
        //$('.inst-score').append(']');
        //$('.inst-score').show();
    }

    function initMenubar() {
        //$('.instructions').hide();
        $('.menubar').show();
        //$('.top-bar').trigger('height');

        //if (window.user_score >= 1) {
        //    $('.scorebox').show();
        //}
    }
    
    function hideMenubar() {
        //$('.instructions').hide();
        $('.scorebox').hide();
        $('.menubar').hide();

        $('.top-bar').trigger('height');
    }
    
    function doneRating() {
        //note: this done-rating button is mapped twice, see below in populateBlooms #go-back.
        resetRatingSliders();
        logScore();
        logUserEvent(4,'rated');
        window.cur_state = 'map';
        var myDiv = document.getElementById('rate');
        myDiv.scrollTop = 0;

        $("#slider-importance").children().children().children(".slider-grade-bubble").each( function(i){
        $(this).css("background-image",$(this).css("background-image").replace("keypad-down","keypad"));
        });

        // var studentTag = document.getElementById('studentTag').value;
        // console.log(studentTag+" jinjihae");

        //$("#slider-importance").children().children().children(".slider-grade-bubble").css("background-color","transparent"); 

            sendAgreementRating({
                'r1': window.current_rating,
                'r2': window.current_rating,
                'cid': window.current_uid
            });
            window.current_rating = 0.5;
            sendInsightRating({
                'r1': window.current_rating,
                'r2': window.current_rating,
                'cid': window.current_uid
            });
            
            //TODO FIX!!!
            if (window.user_score == 2) {
                $('.rate').hide();
                $('.instructions-light').show();


                if(window.lang == 'en'){
                    $('.instructions-light').html("Please join the conversation by clicking your sphere to add your own suggestion for the next report card.")
                }
                else{
                    $('.instructions-light').html("Ahora es su turno. Presione sobre su esfera para introducir su sugerencia.")
                }
                    
                //$('.instructions2').hide();
                //$('.instructions3').show();
                try{
                            blooms.addYourMug();
                            window.your_mug.transition().duration(1500).style("opacity", "1");
                   }catch(err){
                            console.log(err);
                   }
                //hideMenubar();
                //$('.dialog-yourmug').show();
                //$('.comment-input').slideDown();
            }
            else if (window.user_score == 1)
            {
                $('.rate').hide();
                // ui has changed!
                $('.top-bar').trigger('height');
                //$('.instructions-light').hide();
		    if(window.lang == 'en'){
                    $('.instructions-light').show();
                    $('.instructions-light').html("You're halfway done!")
                }
                else{
                    $('.instructions-light').hide();
                }
                //$('.instructions2').show();
                //$('.dialog-score').show();
            }
            else{
                $('.rate').hide();

            }
            //utils.hideLoading();
            //utils.hideLoading();
    }
    
    function doneRatingNoSave() {
        //note: this done-rating button is mapped twice, see below in populateBlooms #go-back.
        resetRatingSliders();
        logUserEvent(4,'rated');
        try {
               window.cur_clicked_mug.transition().duration(2000).style("opacity", "0").remove();
               var index = window.blooms_list.indexOf(window.current_uid);
               console.log(index);
               if (index >= 0) {
                   window.blooms_list.splice(index, 1);
               }

               if (window.blooms_list.length <= 2) {
               utils.showLoading("Loading More Spheres...");
               window.blooms_list = undefined; //needed to avoid infinite recursing
               setTimeout(blooms.populateBlooms, 500);
               }

            } catch (err) {
                    console.log(err);
            }

                $('.rate').hide();
                $('.menubar').show();
    }

    // pulls a live comment text from the database. id is either the cid or the uid,
    // and type is "cid" if you want to search through the comments by comment id or
    // "uid" if you want to search via uid.

    function pullComment(id, type, comments, neverseen_id) {
        neverseen_id = neverseen_id === undefined ? 1 : neverseen_id;
        type = type === undefined || (type !== 'cid' && type !== 'uid') ? 'cid' : type;

        var commentAndUID;
        if (type === 'cid') {
            commentAndUID = getComment(id, comments);
        } else {
            commentAndUID = getCommentByUID(id, comments);
        }
        return commentAndUID;
    }

    // helper function - simply gets the comment from the list using the specified cid

    function getComment(cid, comments) {
        var comment, uid, index = 0;
        while (comments[index]['cid'] !== cid) {
            index++;
        }

        comment = comments[index]['comment'];
        uid = comments[index]['uid'];
        return {
            comment: comment,
            uid: uid,
            cid: cid
        };
    }

    // does the same thing as getComment but with uid instead of cid.
    // IMPORTANT!! this only works because every user is only allowed to make one comment.
    // so if we change that invariat, we will have to change how this function works as well.

    function getCommentByUID(uid, comments) {
        var comment, cid, index = 0;
        while (comments[index]['uid'] !== uid) {
            index++;
        }

        comment = comments[index]['comment'];
        var spanish_comment = comments[index]['spanish_comment'];
        cid = comments[index]['cid'];
        return {
            'comment': comment,
            'spanish_comment': spanish_comment,
            'uid': uid,
            'cid': cid
        };
    }

    // takes two values and stores them in the window for later use.
    // also takes the cid for reference

    function storeRating(value1, value2, cid) {
        if (window.ratings === undefined) {
            window.ratings = [];
        }
        window.ratings.push({
            r1: value1,
            r2: value2,
            cid: cid
        });
    }

    // This function saves the rating of the slider until the user moves
    // back to the main OS page. This function is used so that that the values
    // are not constantly sent every time a slider is moved and will only be sent
    // once once the user is ocmpletely finished.

    function saveRating(value1, value2, cid) {
        if (window.currentRating === undefined) {
            window.currentRating = [];
            window.currentRating[0] = {
                r1: value1,
                r2: value2,
                cid: cid
            };
        } else {
            window.currentRating[0] = {
                r1: value1,
                r2: value2,
                cid: cid
            };
        }

    }

    //This function stores the values of the registration sliders to be used
    // after registration. After storing the values it will cause the register prompt
    // to slide up. 

    function storeSliders(num_sliders) {
        /*if (window.sliders === undefined) {
            window.sliders = [];
        }

        var slider_values = {};
        for (var i = 1; i <= num_sliders; i++) {
            slider_values['s' + i] = $('#s' + i).val();
        }

        window.sliders.push(slider_values);*/
        //$('.endsliders').slideUp();
        if(!window.entry_code){// if user enter with valid entry code, no need to show Register
        accounts.showRegister();
        }
        else
        {
            if(window.user_score <= 2)
            {
               $('.dialog').show();
            }
        }
        $('.endsliders').hide();


    }
    //This function just pulls up the registration sliders form, right before prompting the 
    //  user to register. Once sliders are filled, once done will only cause the registration prompt
    //  to frame will slide up.

    function showSliders() {
        if (!accounts.mustRegister()) {
            $('.endsliders').show();
            $('.frame').show();
            $('.frame').click(function() {
                $('.endsliders').hide();
                $(this).hide();
            });
        } else {
            showRegister();
        }
    }

    
    function sendSlider(rating, number) {
        // console.log(number + " number");
        // console.log(rating + " rating");
        $.ajax({
            type: "POST",
            url: window.url_root + "/os/saverating/1/",
            data: {
                'id': number,
                'rating': rating / 10,
            },
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    console.log("slider successfully sent");
                }
            },
            error: function() {
                console.log("ERROR slider didn't get sent");
            }
        });
    }
    
    //@rating - the values of the sliders and the cid to send the data to the server 
    //          rating is of the form {r1: value, r2: value, cid: cid}, where r1 is for agreement slider
    // sends the value assoicated with the agreement rating for the cid found in the rating. 
    // The function also calls the the sendInsightRating to completly send the entire rating

    function sendAgreementRating(rating) {

        var language = 'english'
        if(window.lang == 'es')
            language = 'spanish'

        $.ajax({
            type: "POST",
            url: window.url_root + "/os/savecommentagreement/1/" + rating.cid + "/",
            data: {
                "agreement": rating.r1 / 10.0,
                "raterViewingLanguage": language
            },
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    console.log("data was sent!");
                    //sendInsightRating(rating);
                }
            },
            error: function() {
                console.log("Agreement didn't get sent!!");
            }
        });
    }

    // @rating - the values of the sliders and the cid to send the data to the server
    //           rating is of the form {r1: value, r2: value, cid: cid}, where r2 is for insight slider
    // Sends the value associated with the insight rating for the cid found on the rating


    function sendInsightRating(rating) {

        var language = 'english'
        if(window.lang == 'es')
            language = 'spanish'

        $.ajax({
            type: "POST",
            dataType: 'json',
            url: window.url_root + "/os/savecommentrating/1/" + rating.cid + "/",
            data: {
                "rating": rating.r2 / 10.0,
                "raterViewingLanguage": language
            },
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    
                }
            },
            error: function() {
                console.log("Insight didn't get sent!!");
            }
        });
    }

    function sendComment(comment,tag) {
        var language = 'english'
        if(window.lang == 'es')
            language = 'spanish'

        $.ajax({
            type: "POST",
            dataType: 'json',
            url: window.url_root + "/os/savecomment/1/",
            data: {
                "comment": comment,
                "commentLanguage" : language,
                "tag":tag
            },
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    //console.log("data was sent!")
                }
            },
            error: function() {
                console.log("Comment didn't get sent!");
            }
        });
    }


    return {
        'updateDescriptions' : updateDescriptions,
        'updateScoreHolders' : updateScoreHolders,
        'resetRatingSliders' : resetRatingSliders,
        'resetEndSliders' : resetEndSliders,
        'logScore' : logScore,
        'changeInstruction' : changeInstruction,
        'initScore' : initScore,
        'initMenubar' : initMenubar,
        'logUserEvent' : logUserEvent,
        'doneRating' : doneRating,
        'doneRatingNoSave' : doneRatingNoSave,
        'pullComment' : pullComment,
        'getComment' : getComment,
        'getCommentByUID' : getCommentByUID,
        'storeRating' : storeRating,
        'updateDescriptionsSpanish': updateDescriptionsSpanish,
        'saveRating' : saveRating,
        'storeSliders' : storeSliders,
        'sendSlider' : sendSlider,
        'sendAgreementRating' : sendAgreementRating,
        'sendInsightRating' : sendInsightRating,
        'sendComment' : sendComment
    };

})($, d3, console);

$(document).ready(function() {
    //$('.score-label').text(utils.toTitleCase(window.conf['YOUR_SCORE_LANGUAGE']).trim().replace(':', '') + ' is ');

    $('.endsliders-next-btn').click(function(event){         
        $('.first-dialog-nav').hide();
        $('.slider-nav-box').show();

        window.skipped[window.current_slider-1] = true;

        if(window.current_slider +1 > window.num_sliders){
            window.prev_state = 'grade';
            window.cur_state = 'register';
            rate.logUserEvent(5,'sliders finished');
            rate.storeSliders(window.num_sliders);
            if (window.authenticated) {
                for (var i = 0; i < window.num_sliders; i++) {
                    rate.sendSlider(window.sliders[i], i+1);
                }

            }
        } else {
            window.current_slider = window.current_slider  + 1;
            var ua = navigator.userAgent.toLowerCase();
            var isAndroid = ua.indexOf("android") > -1; //&& ua.indexOf("mobile");
            if(isAndroid || screen.width >= 700) {
                $("#slide-"+window.current_slider).fadeIn(1000);
            } else 
                $("#slide-"+window.current_slider).show("slide", { direction: "right" }, 500);
            
            $("#slide-"+(window.current_slider-1)).hide();
            /*$(".slider-progress-dot-"+(parseInt(event.target.id.substring(5),10)+1)).css("background","#FFFFFF");*/

        }
    });

    $('.skip-btn').click(function(event){ 
        
        $('.first-dialog-nav').hide();
        $('.slider-nav-box').show();

        if(parseInt(event.target.id.substring(5),10)+1 > window.num_sliders)
        {
            window.prev_state = 'grade';
        window.cur_state = 'register';
        rate.logUserEvent(5,'sliders finished');
        rate.storeSliders(window.num_sliders);
        alert("skip-btn");
        if (window.authenticated) {
            for (var i = 0; i < window.num_sliders; i++) {
                rate.sendSlider(window.sliders[i], i+1);
            }

        }
        }
        else
            {
                $("#slide-"+event.target.id.substring(5)).hide();
                $("#slide-"+(parseInt(event.target.id.substring(5),10)+1)).show("slide", { direction: "right" }, 500);
                /*$(".slider-progress-dot-"+(parseInt(event.target.id.substring(5),10)+1)).css("background","#FFFFFF");*/

            }
    });

    $('.comment-submit-btn').click(function() {
        window.comment = $('#entered-comment').val();
        window.tag = $('#studentTag').val();
        if ($('#studentTag').val() == "Other"){
            window.tag = $('#otherTag').val();
        }
        $('.comment-input').hide();
        $('.dialog-continue').show();
        $('.scorebox').hide();
        $('.menubar').hide();
        $('.instructions-light').hide();
        window.your_mug.transition().duration(2000).style("opacity", "0.4");
        window.prev_state = 'comment';
        //todo fix
        window.cur_state = 'continue';
        utils.showLoading('');
        rate.logUserEvent(6,'comment submitted');
        rate.sendComment($('#entered-comment').val(),window.tag);

        if ($('#regemail').val()){
                accounts.sendEmail($('#regemail').val());
            }
            
        utils.hideLoading('');
        //if ($('#regemail').val()){
	//		accounts.sendEmail($('#regemail').val());
	//	}
        //accounts.showRegister();
    });
    
    $('.comment-cancel-btn').click(function() {
          $('.comment-input').hide();
          $('.dialog-continue').show();
          $('.scorebox').hide();
          $('.menubar').hide();
          window.prev_state = 'comment';
          window.cur_state = 'map';
        //$('.scorebox').show();
    });

    $('.button-div').on("touchstart",function(e){  
    $(this).css("border","2px solid #FFFF99");
    });

    $('.button-div').on("touchend",function(e){  
    $(this).css("border","1px solid #FFFFFF");
    });

    $('.button-div').on("mousedown",function(e){  
    $(this).css("border","2px solid #FFFF99");
    });

    $('.button-div').on("mouseup",function(e){  
    $(this).css("border","1px solid #FFFFFF");
    });


    // 'comment-submit-btn'
    //onClick='window.comment = document.getElementById('entered-comment').value;$('.comment-input').slideUp();accounts.showRegister();'
});
