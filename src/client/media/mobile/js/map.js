	

		var map = L.map('map').setView([37.9, -117.8], 5);
        
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
			
		return	   score > 99.9 ? "#bc3160" :
		           score > 92   ? "#e05e75" :
		           score > 86   ? "#ff8ba1" :
		           score > 81   ? "#fbbd88" :
		           score > 69   ? "#fef391" :
 			       score > 63   ? "#c1e9a3" :
			       score > 56   ? "#61b392" :
			       score > 44   ? "#5890a8" :
			       score > 38   ? "#5e7dbc" :
			       score > 32   ? "#59569e" :
			       score > 19   ? "#8c75a9" :
			       score > 1    ? "#c3c3c3" :
			       score >-1    ? "#7d625f" :
			                      "#3d3333";
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
