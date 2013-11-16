// rate.js
// Handles ratings and scoring
// Dependencies: jQuery

var rate = (function($, d3, console) {
    // Enable strict javascript interpretation
    "use strict";

    // update the questions element in the html
    function updateDescriptions(answer, content) {
        answer.value = content;
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
            $(".flip-1").val('no').trigger('create'); //.slider("refresh");
            $(".flip-1").trigger('slidestop');
        }, 1500);
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
        $('.inst_text').text(t);
    }

    function initScore() {
        $('.inst-score').prepend('[');
        $('.inst-score').append(']');
        $('.inst-score').show();
    }

    function initMenubar() {
        $('.instructions').hide();
        $('.menubar').show();
    }
    
    function hideMenubar() {
        $('.instructions').hide();
        $('.menubar').hide();
    }


    function doneRating() {
        //note: this done-rating button is mapped twice, see below in populateBlooms #go-back.
        resetRatingSliders();
        logScore();

            sendAgreementRating({
                'r1': $("#slider1").val(),
                'r2': $("#slider2").val(),
                'cid': window.current_cid
            });
            sendInsightRating({
                'r1': $("#slider1").val(),
                'r2': $("#slider2").val(),
                'cid': window.current_cid
            });
            
            
            //TODO FIX!!!
            if (window.user_score == 2) {
                $('.rate').slideUp();
                $('.comment-input').slideDown();
            }
            else if (window.user_score == 1)
            {
                $('.rate').slideUp();
                hideMenubar();
                $('.dialog-score').slideDown();
            }
            else{
                $('.rate').slideUp();
            }
            
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
        cid = comments[index]['cid'];
        return {
            comment: comment,
            uid: uid,
            cid: cid
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
        if(!accounts.setAuthenticated()){// if user enter with valid entry code, no need to show Register
        accounts.showRegister();
        }
        $('.endsliders').slideUp();
    }
    //This function just pulls up the registration sliders form, right before prompting the 
    //  user to register. Once sliders are filled, once done will only cause the registration prompt
    //  to frame will slide up.

    function showSliders() {
        if (!accounts.mustRegister()) {
            $('.endsliders').slideDown();
            $('.frame').show();
            $('.frame').click(function() {
                $('.endsliders').slideUp();
                $(this).hide();
            });
        } else {
            showRegister();
        }
    }

    
    function sendSlider(rating, number) {
        $.ajax({
            type: "POST",
            url: window.url_root + "/os/saverating/1/",
            data: {
                'id': number,
                'rating': rating / 100
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
        $.ajax({
            type: "POST",
            url: window.url_root + "/os/savecommentagreement/1/" + rating.cid + "/",
            data: {
                "agreement": rating.r1 / 100.0
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
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: window.url_root + "/os/savecommentrating/1/" + rating.cid + "/",
            data: {
                "rating": rating.r2 / 100.0
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

    function sendComment(comment) {
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: window.url_root + "/os/savecomment/1/",
            data: {
                "comment": comment
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
        'doneRating' : doneRating,
        'pullComment' : pullComment,
        'getComment' : getComment,
        'getCommentByUID' : getCommentByUID,
        'storeRating' : storeRating,
        'saveRating' : saveRating,
        'storeSliders' : storeSliders,
        'sendSlider' : sendSlider,
        'sendAgreementRating' : sendAgreementRating,
        'sendInsightRating' : sendInsightRating,
        'sendComment' : sendComment
    };

})($, d3, console);

$(document).ready(function() {
    $('.score-label').text(utils.toTitleCase(window.conf['YOUR_SCORE_LANGUAGE']).trim().replace(':', '') + ': ');

    $('.done-endsliders-btn').click(function() {
        rate.storeSliders(num_sliders);
    });

    $('.comment-submit-btn').click(function() {
        window.comment = $('#entered-comment').val();
        $('.comment-input').slideUp();
        rate.sendComment($('#entered-comment').val());
        //accounts.showRegister();
    });


    // 'comment-submit-btn'
    //onClick='window.comment = document.getElementById('entered-comment').value;$('.comment-input').slideUp();accounts.showRegister();'
});
