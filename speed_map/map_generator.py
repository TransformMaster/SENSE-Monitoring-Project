import gpxpy.gpx
import folium
import csv
import branca.colormap as cm

gpx_file = open('route.gpx', 'r')
with open('CO2_and_Time.csv', 'r') as file:
    reader = csv.reader(file)
    all_lines = list(reader)
    index = 1
    length = len(all_lines)

    gpx = gpxpy.parse(gpx_file)
    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append(tuple([point.latitude, point.longitude]))
    ave_lat = sum(p[0] for p in points)/len(points)
    ave_lon = sum(p[1] for p in points)/len(points)

    # Load map centred on average coordinates
    my_map = folium.Map(location=[ave_lat, ave_lon], zoom_start=14)
    colormap = cm.LinearColormap(colors=['green', 'red'], index=[540, 940], vmin=540, vmax=940)

    previous = points[0]
    pre_line = all_lines[index]
    for p in points:
        row = all_lines[index]
        if(index<length-1):
            index += 1
        # change color here
        folium.ColorLine([previous,p], colors=[int(float(pre_line[1])),int(float(row[1]))], colormap=colormap, weight=2.5, opacity=1).add_to(my_map)
        pre_line = row
        previous = p
    my_map.add_child(colormap)
    # Save map
    my_map.save("./gpx_washington.html")
