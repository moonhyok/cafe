// utils.js
// All purpose utility functions
// Dependencies: jQuery

/** True if ajax is on */
var ajaxStatus = true;

var utils = (function($, d3, console) {
    // Enable strict javascript interpretation
    "use strict";

    /** The time to wait (in milliseconds) after showing a loading 
        message before proceeding. I noticed that if you do a fat JSON request 
        right after a loading message, the message doesn't show. */
    var TIMEOUT_AFTER_LOADING = 500;

    /** Shows a loading screen with MSG, delay, and then calls f() */

    function showLoading(msg, f) {
        if (f === undefined) {

        $.mobile.loading('show', {
                        text: msg,
                        textVisible: true,
                        textonly: false,
                        theme: 'b',
                        html: ""
                    });

        } else {
            $.mobile.loading('show', {
                text: msg,
                textVisible: true,
                textonly: false,
                theme: 'b',
                html: ""
            });
            setTimeout(f, TIMEOUT_AFTER_LOADING);
        }
    }

     function showLoadingNewPts(msg, f) {
                $.mobile.loading('show', {
                    text: msg,
                    textVisible: true,
                    textonly: true,
                    theme: 'b',
                    html: ""
                });
                setTimeout(f, TIMEOUT_AFTER_LOADING);
            }
    

    /** Hides the loader with an artifical delay of DELAY milliseconds. */

    function hideLoading(delay) {
        setTimeout(function(){$.mobile.loading( 'hide' );}, delay);
        // $('.spinner').fadeOut('fast');
    }


    function toTitleCase(str) {
        return str.replace(/\w\S*/g, function(txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
    }

    return {
        'showLoading': showLoading,
        'showLoadingNewPts': showLoadingNewPts,
        'hideLoading': hideLoading,
        'toTitleCase': toTitleCase
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


jQuery(function($) {
    $(document).on('click', '.ui-btn', function() {
        $('.ui-btn-active').removeClass('ui-btn-active ui-focus');
    });
});


//function to unpress a button