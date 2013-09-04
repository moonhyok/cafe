// JavaScript Document
$(document).ready(function() {
    "use strict";
        //slider 1 How much do you agree with this idea?
        $( ".slider" )
        .slider({
            animate: true,
            value: 50,
            min: 0,
            max: 100,
            change: function (e) {
                if (!e.originalEvent) {
                    return;
                }

                // if ($(this).slider('option', 'disabled') === true) {
                //     return;
                // }
                console.log('slider changed!');
                var value = $('#slider1').slider('value');
                var otherValue = $('#slider2').slider('value');

                if(utils.userIsAuthenticated()){
                    utils.saveRatings(value,otherValue,cid);
                } else {
                    if (window.ratings && window.ratings.length > 2) {
                        //we screwed up
                        return;
                    } else {
                        var cid = $(this).parents('.rate').data('cid');
                        utils.storeRating(value, otherValue, cid);
                    }
                }
                if (otherValue === 50 || value === 50) {
                    $('.rated-thanks').hide();
                    $('.rated-thanks').show();
                    $('.rated-thanks').fadeOut(2000);
                } else {
                    $('.rated').hide();
                    $('.rated').show();
                    $('.rated').fadeOut(2000);
                }

            }
        });
});

// function SaveFunction(){
//     var rating1 = slider1.value();
//     var rating2 = slider2.value();
// }