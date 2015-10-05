function map_capita(){	

		var map = L.map('map_capita').setView([37.9, -118.8], 5.5);
                map.scrollWheelZoom.disable();


		// control that shows state info on hover
		var info = L.control();

		info.onAdd = function (map) {
			this._div = L.DomUtil.create('div', 'info');
			this.update();
			return this._div;
		};
        
        if (!L.Browser.touch){
			info.update = function (props) {
				this._div.innerHTML = (props ?
					'<b>' + props.NAME + '</b>'+'  ' + parseFloat(props.ratio).toFixed(2)
				
					: 'Hover over a county');
				};
		}
		else{
			info.update = function (props) {
				this._div.innerHTML = (props ?
					'<b>' + props.NAME + '</b>'+'  ' + parseFloat(props.ratio).toFixed(2)
				
					: 'Click a county');
			};
		}

		info.addTo(map);


		// get color depending on grade
        function getColor(d) {
			
			
		return	   d > 3 ? "#7f2704" :
		           d > 2   ? "#a63603" :
		           d > 1   ? "#d94801" :
		           d > 0.5   ? "#f16913" :
		           d > 0.2   ? "#fd8d3c" :
 			       d > 0.1   ? "#fdae6b" :
			       d > 0.05   ? "#fdd0a2" :
			       d > 0.02   ? "#fee6ce" :
			       d > 0      ? "#fff5eb" :
			                    "#dddddd" ;
		}

		function style(feature) {
			return {
				weight: 1,
				opacity: 1,
				color: '#170e03',
				dashArray: '',
				fillOpacity: 0.7,
				fillColor: getColor(feature.properties.ratio)
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
	    geojson = L.geoJson(geostat_population, {
			style: style,
			onEachFeature: onEachFeature
		}).addTo(map);	
		
		map.attributionControl.addAttribution('Report card data &copy; <a href="http://citris-uc.org/">UC Berkeley CITRIS</a>');


		var legend = L.control({position: 'topright'});

		legend.onAdd = function (map) {

			var div = L.DomUtil.create('div', 'info legend'),
				grades = ['>3','2.01-3','1.01-2','0.51-1','0.21-0.5','0.11-0.2','0.051-0.1','0.021-0.05','0.01-0.02','0'],
				legend_color=[3.1,2.5,1.5,0.7,0.3,0.15,0.07,0.03,0.015,0],
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


}
map_capita()
