import pandas as pd

# Load the CSV data from files into DataFrames
df_hotspots = pd.read_csv("hotspots.csv")
df_details = pd.read_csv("hotspot_notes.csv")

# Join the two dataframes on the 'name' column
df = pd.merge(df_hotspots, df_details, on="name")

# Change the way we create markers for direct embedding as JS objects.
markers = []
for index, row in df.iterrows():
    marker = {
        "name": row['name'],
        "locatienaam": row['locatienaam'],
        "height": row['height'],
        "eigenaar": row['eigenaar'],
        "kosten": row['kosten'],
        "latitude": row['latitude'],
        "longitude": row['longitude']
    }
    markers.append(marker)

markers_string = ",".join([str(marker) for marker in markers])


# HTML template for Mapbox GL JS
html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hotspots Map</title>
    <script src="https://api.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.js"></script>
    <link href="https://api.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.css" rel="stylesheet">
    <style>
        body, html {{ height: 100%; margin: 0; font-family: Arial, sans-serif; }}
        #map {{ position: absolute; top: 0; bottom: 0; left: 500px; width: calc(100% - 500px); background-color: #191A1A;}}
        #sidebar {{ width: 500px; background-color: #2C2C2C; position: absolute; top: 0; bottom: 0; left: 0; overflow: auto; z-index: 2; box-shadow: 2px 0px 10px rgba(0,0,0,0.5);}}
        #sidebar h4 {{ padding: 20px; background-color: #4CAF50; color: #FFF; margin: 0; }}
        #sidebar .counter {{ padding: 10px 20px; background-color: #3C3C3C; border-bottom: 1px solid #444; font-size: 14px; color: #ddd; }}
        #sidebar a {{ color: #4CAF50; text-decoration: none; }}  /* Style for the links in sidebar */
        #sidebar a:hover {{ text-decoration: underline; }}  /* Hover effect for the links in sidebar */
        #sidebar table, #sidebar th, #sidebar td {{ border-color: #444; color: #ddd; }}
    </style>

</head>
<body>
    <div id="sidebar">
        <h4>Hotspots</h4>
        <div class="counter">Total Hotspots: {len(df)}</div>
        <table border="1" cellspacing="0" cellpadding="5" width="100%">
            <thead>
                <tr><th>Name</th><th>Location Name</th><th>Height</th><th>Cost</th></tr>
            </thead>
            <tbody>
"""

# Append table rows to the HTML
for index, row in df.iterrows():
    html += f"""
    <tr>
        <td><a href="javascript:void(0);" onclick="flyTo({row['latitude']}, {row['longitude']}, 15); return false;">{row['name']}</a></td>
        <td>{row['locatienaam']}</td>
        <td>{row['height']}</td>
        <td>{row['kosten']}</td>
    </tr>"""

html += """
            </tbody>
        </table>
    </div>

    <div id="map"></div>

    <script>
        mapboxgl.accessToken = 'pk.eyJ1IjoiaGV4YXNwb3QiLCJhIjoiY2xnbnN5cWk1MGl5MjNyb2VudWZpeXF1bSJ9.6TkZlxe23xYmU3bxyYsLvg';

        var map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/dark-v10',
            center: [5, 52],  // Change to the average of your latitudes and longitudes if needed
            zoom: 5,
            antialias: true
        });

        map.on('load', function() {
            var markers = [""" + markers_string + """];
    
    markers.forEach(function(marker) {
    new mapboxgl.Marker()
        .setLngLat([marker.longitude, marker.latitude])
        .setPopup(new mapboxgl.Popup({offset: 25})
        .setHTML(`<strong>${marker.name}</strong><br>Location Name: ${marker.locatienaam}<br>Height: ${marker.height}<br>Owner: ${marker.eigenaar}<br>Cost/month: ${marker.kosten}`))
        .addTo(map);
});


            map.addLayer({
    'id': '3d-buildings',
    'source': 'composite',
    'source-layer': 'building',
    'filter': ['==', 'extrude', 'true'],
    'type': 'fill-extrusion',
    'minzoom': 15,
    'paint': {
        'fill-extrusion-color': '#aaa',
        'fill-extrusion-height': [
            'interpolate',
            ['linear'],
            ['zoom'],
            15,
            0,
            15.05,
            ['get', 'height']
        ],
        'fill-extrusion-base': [
            'interpolate',
            ['linear'],
            ['zoom'],
            15,
            0,
            15.05,
            ['get', 'min_height']
        ],
        'fill-extrusion-opacity': 0.6
    }
});
        });

        function flyTo(lat, lng, zoom) {
            map.flyTo({
                center: [lng, lat],
                zoom: zoom
            });
        }
    </script>
</body>
</html>
"""

# Save the HTML to a file
with open("index.html", "w") as file:
    file.write(html)

print("Map with sidebar saved as index_with_sidebar.html!")

