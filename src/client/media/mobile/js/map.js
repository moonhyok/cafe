	

		var map = L.map('map').setView([37.9, -117.8], 5);
                map.scrollWheelZoom.disable();
		/*var cloudmade = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
			attribution: 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade',
			key: 'BC9A493B41014CAABB98F0471D759707',
			styleId: 22677
		}).addTo(map);*/


		// control that shows state info on hover
		var info = L.control();

		info.onAdd = function (map) {
			this._div = L.DomUtil.create('div', 'info');
			this.update();
			return this._div;
		};
        
        if (!L.Browser.touch){
			info.update = function (props) {
				this._div.innerHTML = '<h4>California Report Card Grade</h4>' +  (props ?
					'<b>' + props.NAME + '</b><br>'+'Number of Participants  ' + props.PARTICIPANTS
				
					: 'Hover over a county');
				};
		}
		else{
			info.update = function (props) {
				this._div.innerHTML = '<h4>California Report Card Grade</h4>' +  (props ?
					'<b>' + props.NAME + '</b><br>'+'Number of Participants  ' + props.PARTICIPANTS
				
					: 'Click a county');
			};
		}

		info.addTo(map);


		// get color depending on grade
		function getColor(d) {
			score=100 - d*100;
			
		return	   score > 99.9 ? "#fff7ec" :
		           score > 92   ? "#fee8c8" :
		           score > 86   ? "#fdd49e" :
		           score > 81   ? "#fdbb84" :
		           score > 69   ? "#FDA766" :
 			       score > 63   ? "#fc8d59" :
			       score > 56   ? "#ef6548" :
			       score > 44   ? "#EF5430" :
			       score > 38   ? "#d7301f" :
			       score > 32   ? "#b30000" :
			       score > 19   ? "#7f0000" :
			       score > 1    ? "#590000" :
			       score >-1    ? "#390000" :
			                      "#dddddd";
		}
		function style(feature) {
			return {
				weight: 1,
				opacity: 1,
				color: '#170e03',
				dashArray: '',
				fillOpacity: 0.7,
				fillColor: getColor(feature.properties.s1)
			};
		}
        
					   
					   
		function highlightFeature(e) {
			var layer = e.target;

			layer.setStyle({
				weight: 2,
				color: 'white',
				dashArray: '',
				fillOpacity: 0.7
			});

			if (!L.Browser.ie && !L.Browser.opera) {
				layer.bringToFront();
			}
            if (!L.Browser.touch)
            {
			info.update(layer.feature.properties);
		    }
		}

	    

		function resetHighlight(e) {
			geojson.resetStyle(e.target);
			info.update();
		}

		function zoomToFeature(e) {
			map.fitBounds(e.target.getBounds());
			
		    if (L.Browser.touch) {
            info.update(e.target.feature.properties);
            }

		}
		
		function onEachFeature(feature, layer) {
			layer.on({
                mouseover: highlightFeature,
                mouseout: resetHighlight,
				click: zoomToFeature,

			});
		}

		
        var geojson;
	    geojson = L.geoJson(geostat, {
			style: style,
			onEachFeature: onEachFeature
		}).addTo(map);	
		
		map.attributionControl.addAttribution('Report card data &copy; <a href="http://citris-uc.org/">UC Berkeley CITRIS</a>');


		var legend = L.control({position: 'bottomright'});

		legend.onAdd = function (map) {

			var div = L.DomUtil.create('div', 'info legend'),
				grades = ['A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F','NA'],
				legend_color=[0,0.05,0.1,0.17,0.25,0.35,0.4,0.5,0.6,0.65,0.8,0.9,0.99,1.01],
				labels = [],
				from;// to;
                for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(legend_color[i]) + '"></i> ' +
            grades[i] + '<br>';
    }

			return div;
		};

		legend.addTo(map); 

//for label
    L.LabelOverlay = L.Class.extend({
        initialize: function(/*LatLng*/ latLng, /*String*/ label, options) {
            this._latlng = latLng;
            this._label = label;
            L.Util.setOptions(this, options);
        },
        options: {
            offset: new L.Point(0, 2)
        },
        onAdd: function(map) {
            this._map = map;
            if (!this._container) {
                this._initLayout();
            }
            map.getPanes().overlayPane.appendChild(this._container);
            this._container.innerHTML = this._label;
            map.on('viewreset', this._reset, this);
            this._reset();
        },
        onRemove: function(map) {
            map.getPanes().overlayPane.removeChild(this._container);
            map.off('viewreset', this._reset, this);
        },
        _reset: function() {
            var pos = this._map.latLngToLayerPoint(this._latlng);
            var op = new L.Point(pos.x + this.options.offset.x, pos.y - this.options.offset.y);
            L.DomUtil.setPosition(this._container, op);
        },
        _initLayout: function() {
            this._container = L.DomUtil.create('div', 'leaflet-label-overlay');
        }
    });   

var labelLocation1 = new L.LatLng(40.5, -119.2);
var labelLocation2 = new L.LatLng(40.2, -119.2);
var labelLocation3 = new L.LatLng(39.9, -119.2);
var labelTitle1 = new L.LabelOverlay(labelLocation1, 'Participants');
    map.addLayer(labelTitle1);
var labelTitle2 = new L.LabelOverlay(labelLocation2, 'Outside');
    map.addLayer(labelTitle2);
    
var labelTitle3 = new L.LabelOverlay(labelLocation3, 'California');
    map.addLayer(labelTitle3);
    
    map.on('movestart', function () {
        map.removeLayer(labelTitle1);
        map.removeLayer(labelTitle2);
        map.removeLayer(labelTitle3);
    });
    map.on('moveend', function () {
        map.addLayer(labelTitle1);
        map.addLayer(labelTitle2);
        map.addLayer(labelTitle3);
    });


function changeData(sel)
{
	var value = "s"+sel.value;
	map.removeLayer( geojson );
	function Style(feature) {
	    return {
				weight: 1,
				opacity: 1,
				color: '#170e03',
				dashArray: '',
				fillOpacity: 0.7,
				fillColor: getColor(feature.properties[value])
			};
		}
    geojson = L.geoJson(geostat, {
			style: Style,
			onEachFeature: onEachFeature
		}).addTo(map);
    
    
}
