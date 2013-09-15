// stats.js
// For the Stats and "My Comment" page
// Dependencies: jQuery

/* TODO: this uses the imagechart (depreciated) so it would be better if it used 
column chart: https://developers.google.com/chart/interactive/docs/gallery/barchart 
[I was getting errors when I tried this.]
There's some troubleshooting tips here: https://developers.google.com/chart/image/docs/debugging

I tried to make a generic showGraph function but I was getting type error when I passed
the getElementbyId a variable instead of a literal. */

google.load('visualization', '1', {packages: ['imagechart']});

var show_id = 1; // hard coded
var insufficient_ratings = null;

var stats_conf = { 'AGREEMENT_HISTOGRAM_TEXT' : null,
'LEGEND_AGREEMENT_LEFT' : null,
'LEGEND_AGREEMENT_RIGHT' : null,
'INSIGHT_HISTOGRAM_TEXT' : null,
'LEGEND_INSIGHT_LEFT' : null,
'LEGEND_INSIGHT_RIGHT' : null
};

var stats = (function() {

  function setConf(a, b, c, d, e, f) {
    stats_conf['AGREEMENT_HISTOGRAM_TEXT'] = a;
    stats_conf['LEGEND_AGREEMENT_LEFT'] = b;
    stats_conf['LEGEND_AGREEMENT_RIGHT'] = c;
    stats_conf['INSIGHT_HISTOGRAM_TEXT'] = d;
    stats_conf['LEGEND_INSIGHT_LEFT'] = e;
    stats_conf['LEGEND_INSIGHT_RIGHT'] = f;
  }

  /** Returns true iff all elements of BUCKETS are 0. */
  function all_zeros(buckets) {
    for (var j = 0; j < buckets.length; j++) {
      if (buckets[j] !== 0) {
        return false;
      }
    }
    return true;
  }

  function showGraph1() {
  var source = 'user_agreement_buckets';
  var result = null;
  $.when($.getJSON(window.url_root + '/os/stats/' + show_id + '/')).done(function(data1) {
    var buckets = data1[source].reverse();
    result = new Array(buckets.length);


    var t = all_zeros(buckets);
    if (t) {
      insufficient_ratings = true;
      return;
    } else {
      insufficient_ratings = false;
    }

    for (var i = 0; i < buckets.length; i++) {
      var str = "";

      if (i === 0) { str = stats_conf['LEGEND_AGREEMENT_LEFT']; }
      if (i == buckets.length - 1) { str = stats_conf['LEGEND_AGREEMENT_RIGHT']; }

      result[i] = new Array(str, buckets[i]);
    }

    var data = google.visualization.arrayToDataTable(result, true);

    var options = { cht: 'bvs',
    color: '#E48701',
    max: 10,
    backgroundColor: '#E7E1D8',
    valueLabelsInterval: 1,
    title: stats_conf['AGREEMENT_HISTOGRAM_TEXT']
  };

  new google.visualization.ImageChart(document.getElementById("graph-1")).
  draw(data, options);
});
  
}

function showGraph2() {
  var source = 'user_insight_buckets';
  var result = null;

  $.when($.getJSON(window.url_root + '/os/stats/' + show_id + '/')).done(function(data1) {
    var buckets = data1[source].reverse();
    result = new Array(buckets.length);

    for (var i = 0; i < buckets.length; i++) {
      var str = "";

      if (i === 0) { str = stats_conf['LEGEND_INSIGHT_LEFT']; }
      if (i == buckets.length - 1) { str = stats_conf['LEGEND_INSIGHT_RIGHT']; }

      result[i] = new Array(str, buckets[i]);
    }

    var data = google.visualization.arrayToDataTable(result, true);

    var options = { cht: 'bvs',
    color: '#E48701',
    max: 10,
    backgroundColor: '#E7E1D8',
    valueLabelsInterval: 1,
    title: stats_conf['INSIGHT_HISTOGRAM_TEXT']
  };

  new google.visualization.ImageChart(document.getElementById("graph-2")).
  draw(data, options);
});
  
}

/** Shows the graphs. If JUSTREGISTERED, then short-curcuits and shows the insufficient message. */
/*  TODO note: justRegistered was added because it seemed like os/show/1/ hadn't set 'authenticated'
    when it should, which would cause this code to error because 'buckets' is undefined. Should be figured out. */
function showGraphs(justRegistered) {
    justRegistered = typeof justRegistered !== 'undefined' ? justRegistered : false;

    if (justRegistered) {
      $('.graphs-insufficient').show();
      //console.log("There were insufficient ratings");
      $('.graphs').hide();
      return;
    }


    showGraph1();

    if (!insufficient_ratings) {
      //console.log("There were enough ratings");
      $('.graphs-insufficient').hide();
      $('.graphs').show();
      showGraph2();

    } else {
      $('.graphs-insufficient').show();
      //console.log("There were insufficient ratings");
      $('.graphs').hide();
    }

}

return {
  'setConf' : setConf,
  'showGraphs' : showGraphs
};

})();


$(document).ready(function() {

  $('.stats-btn').click(function() {
    $('.stats').slideDown();
    $('.menubar').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');
  });

  $('.stats-done-btn').click(function() {
    $('.stats').slideUp();
    $('.menubar').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');
  });

});


