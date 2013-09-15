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
                textonly: true,
                theme: 'a',
                html: ""
            });
        } else {
            $.mobile.loading('show', {
                text: msg,
                textVisible: true,
                textonly: true,
                theme: 'a',
                html: ""
            });
            setTimeout(f, TIMEOUT_AFTER_LOADING);
        }
    }

    /** Hides the loader with an artifical delay of DELAY milliseconds. */

    function hideLoading(delay) {
        if (delay !== undefined) {
            setTimeout(function() {
                $.mobile.loading('hide', {
                    textVisible: true,
                    theme: 'a',
                    html: ""
                });
            }, delay);
        } else {
            $.mobile.loading('hide', {
                textVisible: true,
                theme: 'a',
                html: ""
            });

        }
        // $('.spinner').fadeOut('fast');
    }

    function ajaxTempOff(f) {
        // if (!ajaxStatus) {
        //     f();
        // } else {

        $.ajaxSetup({
            async: false
        });

        // ajaxStatus = false;

        f();

        //     $.ajaxSetup({
        //         async: true
        //     });

        //     ajaxStatus = true;
        // }
    }

    function toTitleCase(str) {
        return str.replace(/\w\S*/g, function(txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
    }

    return {
        'showLoading': showLoading,
        'hideLoading': hideLoading,
        'ajaxTempOff': ajaxTempOff,
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