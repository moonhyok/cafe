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
			this._div.innerHTML = '<h4>Citizen Report Card Transportation Grade</h4>' +  (props ?
				'<b>' + props.NAME + '</b><br>'+'Number of Participants  ' + props.PARTICIPANTS+
				'<br>'+ "A:  " +props.A+"    "+"B:  "+props.B+"    "+"C:  "+props.C+"    "+"D:  "+props.D+"    "+"F:  "+props.F
				: 'Hover over a county');
		};

		info.addTo(map);


		// get color depending on population density value
		function getColor(d) {
		return	   d > 0.8 ?  "#006837" :
			       d > 0.6  ? "#66bd63" :
			       d > 0.4  ? "#f46d43" :
			       d > 0.2  ? "#d73027" :
			                  "#a50026";
		}
		function style(feature) {
			return {
				weight: 1,
				opacity: 1,
				color: 'white',
				dashArray: '3',
				fillOpacity: 0.7,
				fillColor: getColor(feature.properties.AVERAGE)
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

		var geojson;

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

		geojson = L.geoJson(map_data0, {
			style: style,
			onEachFeature: onEachFeature
		}).addTo(map);

		map.attributionControl.addAttribution('Report card data &copy; <a href="http://citris-uc.org/">UC Berkeley CITRIS</a>');


		var legend = L.control({position: 'bottomright'});

		legend.onAdd = function (map) {

			var div = L.DomUtil.create('div', 'info legend'),
				grades = ['A','B','C','D','F'],
				labels = [],
				from;// to;

			for (var i = 0; i < grades.length; i++) {
				from = grades[i];
				//to = grades[i + 1];

				labels.push(
					'<i style="background:' + getColor((9-i*2)/10) + '"></i> ' +
					from) ;//+ (to ? '&ndash;' + to : '+'));
			}

			div.innerHTML = labels.join('<br>');
			return div;
		};

		legend.addTo(map); 

function update(index){
	switch(index)
	{
		case '0':
		map.removeLayer( geojson );
	    geojson = L.geoJson(map_data0, {
			style: style,
			onEachFeature: onEachFeature
		}).addTo(map);
		break;
		case '1':
		map.removeLayer( geojson );
		geojson = L.geoJson(map_data1, {
			style: style,
			onEachFeature: onEachFeature
		}).addTo(map);
		break;
	}
			
}
