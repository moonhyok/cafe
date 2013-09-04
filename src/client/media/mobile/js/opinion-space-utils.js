// opinion-space-utils.js
// Utility functions for Opinion Space
// Dependencies: jquery

var utils = (function($, d3, console) {
    // Enable strict javascript interpretation
    "use strict";

    // Arguments: two vectors, represented as arrays.
    // Return: the dot product of the two vectors if the vectors are composed of entirely
    //  numbers and are the same length, null otherwise.
    // Note: the type checking is done using the typeof function.
    // Running time: O(vector1.length)

    function dotProduct(vector1, vector2) {
        if (vector1.length !== vector2.length) {
            return null;
        }

        var sum = 0;
        for (var i = 0; i < vector1.length; i++) {
            if (typeof(vector1[i]) !== "number" || typeof(vector2[i]) !== "number") {
                return null;
            }
            sum += vector1[i] * vector2[i];
        }
        return sum;
    }

    // Arguments: listoflists, an array of arrays, index, the index to compile.
    // Return: the compiled list of elements at index index for all lists in listoflists.
    // Behavior: given a list of lists, this function will look at the specified index in every
    //  list, then compile those elements into a list, which will be returned. I.e., given
    //  ([[1,2,3],[4,5,6],[7,8,9]], 2), it will return [3,6,9].
    // Note: in python this would be simply [l[index] for l in listoflists].
    // Note: if index is out of bounds on any of the lists in listoflists, null will be added
    //  in place of the element at index index.
    // Running time: O(listoflists.length)

    function compileIndexedElementsToList(listoflists, index) {
        var result = [];

        for (var i = 0; i < listoflists.length; i++) {
            if (index < listoflists[i].length) {
                result.push(listoflists[i][index]);
            } else {
                result.push(null);
            }
        }
        return result;
    }

    // Arguments: eigenvectors, a list of lists in which the inner list at index ev_key_index
    //  is either zero or one, representing the x axis and y axis respectively, and which at
    //  index ev_value_index is a number value.
    //  ratings, a list of lists in which the inner list at key rating_uid_index is the uid of
    //  the user who submitted the rating (when they joined opinion space) and in which the index
    //  at rating_value_index is a number representing the user's response to one of the eight
    //  starting questions.
    // Return: list of object of type {uid: uid, x: computed x value, y: computed y value}
    // Note: x and y are computed by taking the dot products of the x and y eigenvectors with each rating.
    // Note: this does not garauntee output of the objects in any sorted order.
    // Note: all parameters except eigenvectors and ratings are optional.
    // Running time: O(ratings.length)

    function compileEigenvectorsAndRatings(eigenvectors, ratings, ev_value_index, rating_value_index, rating_uid_index) {
        //initialize optional parameters
        ev_value_index = typeof ev_value_index === 'undefined' ? 2 : ev_value_index;
        rating_uid_index = typeof rating_uid_index === 'undefined' ? 0 : rating_uid_index;
        rating_value_index = typeof rating_value_index === 'undefined' ? 2 : rating_value_index;

        // Note: the following code depends on the fact that we are measuring user data by 8 criteria.
        // If we change that, we have to change this code also.

        var ex = compileIndexedElementsToList(eigenvectors.slice(0, window.num_sliders), ev_value_index),
            ey = compileIndexedElementsToList(eigenvectors.slice(window.num_sliders), ev_value_index),
            result = [];
        var rating, x, y, uid;

        for (var i = 0; i < ratings.length; i += window.num_sliders) {
            rating = compileIndexedElementsToList(ratings.slice(i, i + window.num_sliders), rating_value_index);
            x = dotProduct(ex, rating);
            y = dotProduct(ey, rating);
            uid = ratings[i][rating_uid_index];
            result.push({
                'uid': uid,
                'x': x,
                'y': y
            });
        }
        return result;
    }

    function updateScoreHolders() {
        document.getElementById("score-holder").innerHTML = window.user_score.toString();
        document.getElementById("score-holder2").innerHTML = window.user_score.toString();
        document.getElementById("score-holder3").innerHTML = window.user_score.toString();
        document.getElementById("score-holder4").innerHTML = window.user_score.toString();
    }

    // Arguments: show_id, the id to pass to the show view (defaults to 1),
    //  neverseen_id, the id to pass to the neverseen view (also defaults to 1),
    //  func, the function to call on the calculated data. This function takes one paramerter,
    //  which is a list of objects of the form {uid:uid, x:x, y:y}
    // Return: the list of uid, x, y as returned by compileEigenvectorsAndRatings
    //  using the data pulled from the views.
    // Note: Returning data from this function is not plausible since because the ajax
    //  request will not finish until the function has returned. Instead a function parameter
    //  is included to process the data (e.g. add it do the DOM tree, etc).
    // Note: The function func will be called with teh ajax request returns, which is not
    //  gaurenteed to happen with any relationship to when this function returns. In most cases
    //  the results of calling func will not happen until half a second to a second after pullLivePoints
    //  is called.

    function pullLivePoints(showfunc, neverseenfunc, show_id, neverseen_id) {
        console.log("PULL LIVE POINTS WAS CALLED");
        neverseenfunc = neverseenfunc ? neverseenfunc : function() {};
        show_id = typeof show_id === 'undefined' ? 1 : show_id;
        neverseen_id = typeof neverseen_id === 'undefined' ? 1 : neverseen_id;

        var eigens, ratings, result; //these are undefined by default
        $.when(
            $.getJSON(window.url_root + '/os/show/' + show_id + '/'),
            $.getJSON(window.url_root + '/os/neverseencomments/' + neverseen_id + '/')
        ).done(function(data1, data2) {
            eigens = data1[0]['eigenvectors']; //data, success, jqxhr
            ratings = data2[0]['ratings'];


            // hack to allow own bloom - should be cleaned up later
            //var curr_user_id = data1[0]['cur_user_id'];
            var users_statements = data1[0]['statements'];
            var users_ratings = new Array();
            for (var i = 0; i < users_statements.length; i += 1) {
                users_ratings[i] = new Array(-1, users_statements[i][0], users_statements[i][3]);
            }
            //console.log(users_ratings);
            //console.log(ratings.concat(users_ratings));
            if (window.authenticated) {
                ratings = ratings.concat(users_ratings);
            }
            //end of hack


            if (window.authenticated) {
                //document.getElementById("landing").style.display = "none";
                console.log("im here at the hide landing code...");
                $('.landing').hide();
                $('.loading').hide();
                initMenubar();
                updateScoreHolders();
            } else {
                $('.loading').hide();
            }

            console.log("pulling the comments:");
            //console.log(data2);
            //console.log(data2.comments);
            result = compileEigenvectorsAndRatings(eigens, ratings);
            //console.log(result);
            showfunc({
                points: result,
                comments: data2[0].comments
            });
        });

    }

    function resetRatingSliders() {
        setTimeout(function() {
            $("#slider1").val(50).slider("refresh");
        }, 1500);
        setTimeout(function() {
            $("#slider2").val(50).slider("refresh");
        }, 1500);
    }

    function logScore() {
        if (window.user_score === undefined) {
            window.user_score = 1;
        } else {
            window.user_score += 1;
        }
        updateScoreHolders();

    }

    function bar() {
        var data = [{
            year: 2006,
            books: 54
        }, {
            year: 2007,
            books: 43
        }, {
            year: 2008,
            books: 41
        }, {
            year: 2009,
            books: 44
        }, {
            year: 2010,
            books: 35
        }];

        var barWidth = 40;
        var width = (barWidth + 10) * data.length;
        var height = 200;

        var x = d3.scale.linear().domain([0, data.length]).range([0, width]);
        var y = d3.scale.linear().domain([0, d3.max(data, function(datum) {
            return datum.books;
        })]).
        rangeRound([0, height]);

        // add the canvas to the DOM
        var barDemo = d3.select("#bargraph").
        append("svg:svg").
        attr("width", width).
        attr("height", height);

        barDemo.selectAll("rect").
        data(data).
        enter().
        append("svg:rect").
        attr("x", function(datum, index) {
            return x(index);
        }).
        attr("y", function(datum) {
            return height - y(datum.books);
        }).
        attr("height", function(datum) {
            return y(datum.books);
        }).
        attr("width", barWidth).
        attr("fill", "#2d578b");

        barDemo.selectAll("text").
        data(data).
        enter().
        append("svg:text").
        attr("x", function(datum, index) {
            return x(index) + barWidth;
        }).
        attr("y", function(datum) {
            return height - y(datum.books);
        }).
        attr("dx", -barWidth / 2).
        attr("dy", "1.2em").
        attr("text-anchor", "middle").
        text(function(datum) {
            return datum.books;
        }).
        attr("fill", "white");

        barDemo.selectAll("text.yAxis").
        data(data).
        enter().append("svg:text").
        attr("x", function(datum, index) {
            return x(index) + barWidth;
        }).
        attr("y", height).
        attr("dx", -barWidth / 2).
        attr("text-anchor", "middle").
        attr("style", "font-size: 12; font-family: Helvetica, sans-serif").
        text(function(datum) {
            return datum.year;
        }).
        attr("transform", "translate(0, 18)").
        attr("class", "yAxis");
    }

    function changeInstruction(text) {
        document.getElementById("inst_text").innerHTML = text;
    }

    function initScore() {
        document.getElementById("score").innerHTML = "[" + document.getElementById("score").innerHTML + "]";
        document.getElementById("score-label").innerHTML = "Score:";

    }

    function initMenubar() {
        document.getElementById("instructions").style.display = "none";
        document.getElementById("menubar").style.display = "inline";
    }

    function editComment() {
        document.getElementById("commentRegion").style.display = "none";
        document.getElementById("editComment").style.display = "inline";
    }

    function doneRating() {
        //note: this done-rating button is mapped twice, see below in populateBlooms #go-back.
        resetRatingSliders();
        logScore();

        if (!window.authenticated) {

            storeRating(document.getElementById("slider1").value, document.getElementById("slider2").value, window.current_cid);
            console.log('rated: ' + window.current_cid + " " + document.getElementById("slider2").value);

            switch (window.user_score) {
                case 1:
                    changeInstruction("You earned a point! Tap another bloom...");
                    $('.rate').slideUp();
                    initScore();
                    break;
                case 2:
                    $('.rate').slideUp('fast', function() {
                        $('.endsliders').slideDown();
                    });
                    // the endsliders button will cause register to come down
                    initMenubar();
                    break;
                    /*case 3:
            changeInstruction("Rate one more bloom and then you can add your own!");
            $('.rate').slideUp();
            break;
        case 4:
            $('.rate').slideUp('fast', function() {
                showRegister();
            });
            initMenubar();
            break;*/
                default:
                    $('.rate').slideUp();
                    break;
            }
        } else {
            sendAgreementRating({
                'r1': document.getElementById("slider1").value,
                'r2': document.getElementById("slider2").value,
                'cid': window.current_cid
            });
            sendInsightRating({
                'r1': document.getElementById("slider1").value,
                'r2': document.getElementById("slider2").value,
                'cid': window.current_cid
            });
            $('.rate').slideUp();
        }
    }

    // Side Effects: Populate the d3 graph with blooms according to the data from pullLivePoints.

    function populateBlooms() {
        // set up loading sign
        $('svg').remove();
        $('#d3 .loading').show();
        // remove an svg if there already is one

        // function for conviencence - given an array, returns a random element

        function choice(choices) {
            var index = Math.floor(Math.random() * choices.length);
            return choices[index];
        }

        // define the margins
        console.log("window height: " + $(window).height() + 'window width: ' + $(window).width());
        var margin = {
            top: 55,
            left: 55,
            right: 55,
            bottom: 55
        },
            //    width = $(window).width() - margin.right - margin.left-50,
            //  height = $(window).height() - margin.bottom - margin.top-50;
            width = $(window).width() - margin.right - margin.left,
            height = $(window).height() - margin.bottom - margin.top;

        console.log('resizing: width: ' + width + ' height: ' + height);

        pullLivePoints(function(object) {
            var data = object.points;
            var comments = object.comments;
            $('svg').remove();
            // clear anything that's in the div already (e.g. loading button)
            $('#d3 .loading').hide();
            var svg = d3.select('#d3')
                .append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
                .append('g')
            // .attr('class', 'main')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

            // create the scales - these will map actual data to pixels on the screen.
            var x = d3.scale.linear()
                .domain(d3.extent(data, function(d) {
                    return d.x;
                }))
                .range([0, width]);

            var y = d3.scale.linear()
                .domain(d3.extent(data, function(d) {
                    return d.y;
                }))
                .range([height, 0]);

            svg.selectAll('.bloom')
                .data(data)
                .enter()
                .append('g')
                .attr('class', 'bloom')
                .append('circle')
                .attr('class', 'bloom-circle')
                .attr('cx', function(d) {
                    return x(d.x);
                })
                .attr('cy', function(d) {
                    return y(d.y);
                })
                .attr('r', function() {
                    return choice([10, 20, 30, 40]);
                })
                .attr('data-r', function() {
                    return d3.select(this).attr('r');
                })
                .style('fill', function(d) {
                    if (d.uid == -1) { // its the users own bloom
                        return '#3E9ACA';
                    } else {
                        return choice(['purple', 'crimson', 'gold', 'mediumvioletred', 'green', 'teal', 'lime', 'orange']);

                    }
                })
            //.style('fill', 'url(#gradient)')
            .style('stroke', 'white')
                .style('stroke-width', '5px')
                .datum(function(d) {
                    return d;
                })
                .on('click', function(d) {
                    if (d.uid == -1) {
                        $('.myBloom').slideDown();
                        return;
                    }
                    if (readyToLogin() && !window.authenticated) {
                        showSliders();
                    } else {
                        var _this = d3.select(this);
                        $('.rate-loading').slideDown();
                        var commentData = pullComment(d.uid, 'uid', comments);
                        var content = commentData.comment;
                        var cid = commentData.cid;
                        window.current_cid = cid;

                        _this.transition()
                            .attr('r', function() {
                                return parseInt(_this.attr('data-r'), 10) + 20;
                            })
                            .duration(1000).each("end", function() {

                                updateDescriptions(document.getElementById('commentInput'), content);
                                $('.rate').slideDown(function() {
                                    $('.rate-loading').slideUp();
                                    $('.rate').data('cid', cid);
                                });
                                //$('.frame').show();
                                $('#go-back').click(function() {
                                    //$('.frame').hide();
                                    ///if(window.authenticated){
                                    // sendAgreementRating(window.currentRating[0]);
                                    //}
                                    _this.transition()
                                        .attr('r', 0)
                                        .duration(2000);
                                });
                            });


                    }


                })
                .append('circle')
                .attr('r', 2)
                .style('fill', 'white');

        });
    }

    // a function ot pull up the registration prompt

    function showRegister() {
        //$('#reg-question').prepend("<p>" + $('#question').html() + "</p>");
        $('.register').slideDown();
        //$('.frame').show();
        $('#finishRegistration').click(function() {
            //$('.register').slideUp();
            //$(this).hide();
        });
    }

    // a function ot pull up the registration prompt

    function showCommentInput() {
        //$('#reg-question').prepend("<p>" + $('#question').html() + "</p>");
        $('.comment-input').slideDown();
    }

    // a function to pull up the login prompt.

    function showLogin() {
        $('.landing').slideUp();
        $('.login').slideDown();
        $('.frame').show();
        $('.frame').click(function() {
            $('.login').slideUp();
            $(this).hide();
        });
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

    // update the questions element in the html

    function updateDescriptions(answer, content) {
        answer.innerHTML = content;
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

    //function that removes the landing page when the first time button is clicked.

    function firstTime() {
        console.log('clicked');
        $('.landing').slideUp();
    }

    // This function checks to see if the user has logged int
    // This is used to change the behavior of the site for users
    // that have logged in. (Mostly to send data to server immediately)

    function userIsAuthenticated() {

        var user_authenticated
        $.when(
            $.getJSON(window.url_root + '/os/show/1')
        ).done(function(data) {
            console.log("data is:");
            console.log(data);
            user_authenticated = data.is_user_authenticated;
            console.log(user_authenticated);
            return user_authenticated;
        });

    }


    //This function stores the values of the registration sliders to be used
    // after registration. After storing the values it will cause the register prompt
    // to slide up. 

    function storeSliders(num_sliders) {

        if (window.sliders === undefined) {
            window.sliders = [];
        }

        var slider_values = {}
        for (var i = 1; i <= num_sliders; i++) {
            slider_values['s' + i] = document.getElementById('s' + i).value;
            //alert(document.getElementById('s'+i).value);
        }

        window.sliders.push(slider_values);
        //$('.endsliders').slideUp();
        $('.endsliders').slideUp('fast', function() {
            showCommentInput();
        });
    }
    //This function just pulls up the registration sliders form, right before prompting the 
    //  user to register. Once sliders are filled, once done will only cause the registration prompt
    //  to frame will slide up.

    function showSliders() {
        if (!mustRegister()) {
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
                    // now we can take whatever means necessary.
                    console.log("successful login detected!!");
                    console.log(window.comment);
                    sendComment(window.comment);

                    for (var i = 1; i <= window.num_sliders; i++) {
                        sendSlider(window.sliders['s' + i], i);
                    }

                    for (var i = 0; i < window.ratings.length - 1; i++) {
                        sendAgreementRating(window.ratings[i]);
                        sendInsightRating(window.ratings[i], false);
                    }

                    sendAgreementRating(window.ratings[window.ratings.length - 1]);
                    sendInsightRating(window.ratings[window.ratings.length - 1], true);

                    //window.authenticated = true;
                    /*sendAgreementRating(window.ratings[0]);
                sendAgreementRating(window.ratings[1]);
                sendSlider(window.sliders.s1,1);
                sendSlider(window.sliders.s2,2);
                sendSlider(window.sliders.s3,3);
                sendSlider(window.sliders.s4,4);*/

                } else {
                    // we should rerender the form here.
                }
            },
            error: function() {
                console.log("ERROR posting login request. Abort!");
            }
        });
    }
    //@rating - the value of the slider 
    //@number - the number of which slider is being sent to the server
    //this function is used only right after registration to send the sliders
    //  that come up right before registration.

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

        })
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
                    console.log("data was sent!")
                    //sendInsightRating(rating);
                }
            },
            error: function() {
                console.log("Agreement didn't get sent!!");
            }
        })
    }

    // @rating - the values of the sliders and the cid to send the data to the server
    //           rating is of the form {r1: value, r2: value, cid: cid}, where r2 is for insight slider
    // Sends the value associated with the insight rating for the cid found on the rating

    function sendInsightRating(rating, reload_on_return) {
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: window.url_root + "/os/savecommentrating/1/" + rating.cid + "/",
            data: {
                "rating": rating.r2 / 100.0
            },
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    console.log("data was sent!");

                    
                    if (reload_on_return) {
                        location.reload();
                    }

                }
            },
            error: function() {
                console.log("Insight didn't get sent!!");
            }
        })

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
        })

    }


    return {
        'blooms': populateBlooms,
        'queryComment': pullComment,
        'showRegister': showRegister,
        'storeRating': storeRating,
        'readyToLogin': readyToLogin,
        'userIsAuthenticated': userIsAuthenticated,
        'showLogin': showLogin,
        'firstTime': firstTime,
        'storeSliders': storeSliders,
        'sendAgreementRating': sendAgreementRating,
        'sendInsightRating': sendInsightRating,
        'loginAfterRegister': loginAfterRegister,
        'sendSlider': sendSlider,
        'doneRating': doneRating, //the next three were added for quick login solution, remove them later
        'initScore': initScore,
        'initMenubar': initMenubar,
        'logScore': logScore,
        'editComment': editComment,
        'bar': bar
    };

})($, d3, console);

$.fn.serializeObject = function() {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};