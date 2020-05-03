import requests

f = open("Data.geojson","w")
url = "https://covid19-data.p.rapidapi.com/geojson-ww"

headers = {
    'x-rapidapi-host': "covid19-data.p.rapidapi.com",
    'x-rapidapi-key': "96c395c12bmsh7977f2a7f725335p156aa1jsn3256842e9bbc"
}

response = requests.request("GET", url, headers=headers)
f.write(response.text)

import json  # reading geojson files
import matplotlib.pyplot as plt  # plotting data
from shapely.geometry import asShape  # manipulating geometry
from descartes import PolygonPatch  # integrating geom object to matplot

#------------------------- LOAD THE DATA -----------------------------
data = json.load(open("Data.geojson"))  # from data folder.

plt.style.use('dark_background')
# initiate the plot axes
fig = plt.figure()  # create a figure to contain the plot elements
ax = fig.gca(xlabel="Longitude", ylabel="Latitude")

# loop through the features plotting polygon centroid
for feat in data["features"]:
    # convert the geometry to shapely
    geom = asShape(feat["geometry"])
    # obtain the coordinates of the feature's centroid
    x, y = geom.centroid.x, geom.centroid.y
    # plot the centroids
    ax.plot(x, y, 'ro',color="white")
    # label the features at the centroid location
    ax.text(x, y, feat["properties"]["confirmed"], fontsize=6, bbox=dict(fc='w',
                                                                    alpha=0.3))
    # plot the polygon features: type help(PolygonPatch) for more args
    ax.add_patch(PolygonPatch(feat["geometry"], fc='blue', ec='blue',
                              alpha=0.5, lw=0.5, ls='--', zorder=2))

ax.clear  # clear the axes memory

plt.title("Map of confirmed cases of CoVID-19 per country")
plt.show()
