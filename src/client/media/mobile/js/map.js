	
		var map = L.map('map').setView([37.47, -122.2], 5);
        
		var cloudmade = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
			attribution: 'Map data &copy; 2011 OpenStreetMap contributors, Imagery &copy; 2011 CloudMade',
			key: 'BC9A493B41014CAABB98F0471D759707',
			styleId: 22677
		}).addTo(map);


		// control that shows state info on hover
		var info = L.control();

		info.onAdd = function (map) {
			this._div = L.DomUtil.create('div', 'info');
			this.update();
			return this._div;
		};

		info.update = function (props) {
			this._div.innerHTML = '<h4>California Report Card Grade</h4>' +  (props ?
				'<b>' + props.NAME + '</b><br>'+'Number of Participants  ' + props.PARTICIPANTS
				
				: 'Hover over a county');
		};

		info.addTo(map);


		// get color depending on grade
		function getColor(d) {
			score=100 - d*100;
			
		return	   score > 86 ?  "#1a9641" :
			       score > 63  ? "#a6d96a" :
			       score > 38  ? "#ffffbf" :
			       score > 1   ? "#fdae61" :
			       score >-1   ? "#d7191c" :
			                     "#aaaaaa";
		}
		function style(feature) {
			return {
				weight: 1,
				opacity: 1,
				color: 'white',
				dashArray: '3',
				fillOpacity: 0.7,
				fillColor: getColor(feature.properties.s1)
			};
		}

		function highlightFeature(e) {
			var layer = e.target;

			layer.setStyle({
				weight: 3,
				color: '#666',
				dashArray: '',
				fillOpacity: 0.7
			});

			if (!L.Browser.ie && !L.Browser.opera) {
				layer.bringToFront();
			}

			info.update(layer.feature.properties);
		}

	    

		function resetHighlight(e) {
			geojson.resetStyle(e.target);
			info.update();
		}

		function zoomToFeature(e) {
			map.fitBounds(e.target.getBounds());
		}

		function onEachFeature(feature, layer) {
			layer.on({
				mouseover: highlightFeature,
				mouseout: resetHighlight,
				click: zoomToFeature
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
				grades = ['A','B','C','D','F','NA'],
				legend_color=[0,0.3,0.5,0.8,0.99,1.01],
				labels = [],
				from;// to;

			for (var i = 0; i < grades.length; i++) {
				from = grades[i];
				//to = grades[i + 1];

				labels.push(
					'<i style="background:' + getColor(legend_color[i]) + '"></i> ' +
					from) ;//+ (to ? '&ndash;' + to : '+'));
			}

			div.innerHTML = labels.join('<br>');
			return div;
		};

		legend.addTo(map); 



function changeData(sel)
{
	var value = "s"+sel.value;
	map.removeLayer( geojson );
	function Style(feature) {
	    return {
				weight: 1,
				opacity: 1,
				color: 'white',
				dashArray: '3',
				fillOpacity: 0.7,
				fillColor: getColor(feature.properties[value])
			};
		}
    geojson = L.geoJson(geostat, {
			style: Style,
			onEachFeature: onEachFeature
		}).addTo(map);
    
    
}
