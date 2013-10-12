// blooms.js
// Crunches numbers & generates the ``garden" of blooms.
// Dependencies: jQuery

var blooms = (function($, d3, console) {
    // Enable strict javascript interpretation
    "use strict";


    /** Creates global variable window.visuals to determine blooms colors and sizes.
     *  Copied from the flash version. */

    function generateBloomSizesAndColors(data) {
        window.visuals = {
            userIdToCommentScoreBucket: {},
            userIdToAvgAgreementBucket: {},
            POINT_SIZES: null,
            POINT_COLORS: null,
        };

        if (window.conf.FUN_COLORS) {
            window.visuals.POINT_SIZES = [20, 25, 30, 36, 42];
            window.visuals.POINT_COLORS = ['#000099', '#FF7519', '#66FF33', '#FFCC00', '#FF1975', '#FF0000', '#470047'];
        } else {
            window.visuals.POINT_SIZES = [9, 12.5, 20, 27.5, 35];
            window.visuals.POINT_COLORS = ['#ffda10', '#ffaa10', '#ff5b11', '#ef3a47', '#c22f3a', '#c22faf', '#9e2fc2'];
        }

        var sorted_comments_ids;
        var sorted_avg_agreement;
        
        sorted_comments_ids = data['sorted_comments_ids'];
        sorted_avg_agreement = data['sorted_avg_agreement'];

        // utils.ajaxTempOff(function() {
        //     $.getJSON(window.url_root + '/os/all/1/', function(data) {
        //         sorted_comments_ids = data['sorted_comments_ids'];
        //         sorted_avg_agreement = data['sorted_avg_agreement'];
        //     });

        // });

        storeSortedIDsToBuckets(sorted_comments_ids, window.visuals.userIdToCommentScoreBucket, window.visuals.POINT_SIZES.length);
        storeSortedIDsToBuckets(sorted_avg_agreement, window.visuals.userIdToAvgAgreementBucket, window.visuals.POINT_COLORS.length);
    }

    /** Data: array; Bucket: object, NumBuckets: int 
     *  Again, copied from the flash version. */

    function storeSortedIDsToBuckets(data, bucket, numBuckets) {

        if (data.length == 1) {
            if (Math.random() < 5)
                bucket[data[0][0]] = numBuckets;
            else
                bucket[data[0][0]] = numBuckets - 2;
            return;
        }

        var intervalSize = data.length / numBuckets;
        var remainder = data.length % numBuckets;
        var intervalNum = 1;
        var commentsSoFar = 0;

        // default to having the larger points first
        if (intervalSize === 0)
            intervalNum = numBuckets - data.length + 1;

        for (var k = 0; k < data.length; k++) {
            // Corner case: if the number of points displayed < NUM_SIZE_INTERVALS and 
            // intervalSize is 0
            if (intervalSize === 0) {
                bucket[data[k][0]] = intervalNum;
                intervalNum += 1;
                continue;
            }

            // Standard case: intervalSize > 0, remainder >= 0
            if (commentsSoFar >= intervalSize) { // Two cases: 1) maybe use a remainder, 2) remainder has been used

                if (remainder > 0 && commentsSoFar == intervalSize) { // use remainder
                    remainder -= 1;
                } else { // remainder has been used or no remainder left 
                    intervalNum += 1;
                    commentsSoFar = 0;
                }
            }

            // Set the corresponding interval number for the user_id
            bucket[data[k][0]] = intervalNum;
            commentsSoFar += 1;
        }
    }

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
        neverseenfunc = neverseenfunc ? neverseenfunc : function() {};
        show_id = typeof show_id === 'undefined' ? 1 : show_id;
        neverseen_id = typeof neverseen_id === 'undefined' ? 1 : neverseen_id;

        var eigens, ratings, result; //these are undefined by default

        var data1, data2;

        $.ajax({
            async: false,
            dataType: "json",
            url: window.url_root + '/os/show/' + show_id + '/',
            success: function(d1) {
                data1 = d1;
                eigens = data1['eigenvectors'];
                data2 = data1['never_seen_comments'];
                ratings = data2['ratings'];
                generateBloomSizesAndColors(data2);
                //console.log(eigens);

            }
        });

        // $.when(
        //     $.getJSON(window.url_root + '/os/show/' + show_id + '/'),
        //     $.getJSON(window.url_root + '/os/neverseencomments/' + neverseen_id + '/')
        // ).done(function(data1, data2) {
        //     eigens = data1[0]['eigenvectors']; //data, success, jqxhr
        //     ratings = data2[0]['ratings'];


        //make this it's own function
        // hack to allow own bloom - should be cleaned up later
        //var curr_user_id = data1[0]['cur_user_id'];
        var users_statements = data1['statements'];
        var users_ratings = [];
        for (var i = 0; i < users_statements.length; i += 1) {
            users_ratings[i] = new Array("curUser", users_statements[i][0], users_statements[i][3]);
        }

        if (window.authenticated) {
            ratings = ratings.concat(users_ratings);
        }
        //end of hack

        result = compileEigenvectorsAndRatings(eigens, ratings);
        showfunc({
            points: result,
            comments: data2.comments
        });
        // });

    }

    // function for conviencence - given an array, returns a random element

    function choice(choices) {
        var index = Math.floor(Math.random() * choices.length);
        return choices[index];
    }

    /** Self explanatory
     *  Again, copied from the flash version. */

    function mapScoreToRadius(uid, comments) {
        if (uid == 'curUser') {
            return window.visuals.POINT_SIZES[window.visuals.POINT_SIZES.length - 1];
        }

        return window.visuals.POINT_SIZES[window.visuals.userIdToCommentScoreBucket[uid] - 1];
    }

    /** Self explanatory
     *  Again, copied from the flash version. */

    function mapUidToColor(uid, comments) {
        if (uid == "curUser") {
            return '#3E9ACA';
        }

        return window.visuals.POINT_COLORS[window.visuals.userIdToAvgAgreementBucket[uid] - 1];
    }

    // Side Effects: Populate the d3 graph with blooms according to the data from pullLivePoints.

    function populateBlooms() {
//        generateBloomSizesAndColors();

        // set up loading sign
        $('svg').remove();
        $('#d3 .loading').show();
        // remove an svg if there already is one

        // define the margins
        //console.log("window height: " + $(window).height() + 'window width: ' + $(window).width());
        var margin = {
            top: 55,
            left: 55,
            right: 55,
            bottom: 55
        },

            width = $(window).width() - margin.right - margin.left,
            height = $(window).height() - margin.bottom - margin.top; // - $('.top-bar').height();

        //console.log('resizing: width: ' + width + ' height: ' + height);

         pullLivePoints(function(object) {
            var data = object.points;
            var comments = object.comments;

            console.log(data);
            console.log(comments);

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

            //var rescale = generateRescalingFactor();

            svg.selectAll(".bloom")
            .data(data)
            .enter()
            .append("svg:image")
            .attr("xlink:href", function() {
                return window.url_root + "/media/mobile/img/cafe/cafe" + Math.floor((Math.random()*6)).toString() + ".png";

            })
            .attr('x', function(d) {
                return x(d.x);
            })
            .attr('y', function(d) {
                return y(d.y);
            })
            .attr("width", "140")
            .attr("height", "140")
            .attr("transform", function(d) {
                    //var rotations = ['-65', '-20', '45', '80'];
                    //return "rotate(" + choice(rotations).toString() + ")";
                    return choice(["rotate(-65)", "rotate(-45)", "rotate(20)"]);
                })
            .datum(function(d) {
                return d;
            })
            .on('click', function(d) {
                var commentData = rate.pullComment(d.uid, 'uid', comments);
                var content = commentData.comment;
                var cid = commentData.cid;
                window.current_cid = cid;
                $('.rate').slideDown();
                $('.rate-loading').slideDown();
                rate.updateDescriptions(document.getElementById('commentInput'), content);
                $('.rate').slideDown(function() {
                    $('.rate-loading').slideUp();
                    $('.rate').data('cid', cid);
                });
                $('#go-back').click(function() {
                    _this.transition()
                    .attr('r', 0)
                    .duration(2000);
                });
            });
        });
    }

    /** Handles a users entrance into the garden if they are already authenticated. */

    function alreadyAuthenticated() {
        //TOFIX utils.showLoading("Loading...");

        //utils.ajaxTempOff(function() {
        populateBlooms();
        //});
        accounts.initLoggedInFeatures();
        //TOFIX utils.hideLoading();
        $('.landing').hide();
    }

    return {
        'populateBlooms': populateBlooms,
        'alreadyAuthenticated': alreadyAuthenticated
    };
})($, d3, console);

$(document).ready(function() {
    if (accounts.setAuthenticated()) {
        blooms.alreadyAuthenticated();
    }

    $(window).resize(function() {
        // TODO: this needs to occur iff substantial resize
        // and not if in middle of AJAX call.
        // utils.blooms();
    });
});
