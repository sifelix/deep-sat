# ---
# jupyter:
#   jupytext:
#     formats: ipynb,python//py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# + pycharm={"is_executing": false}
import ee
import folium

# + pycharm={"name": "#%% Initialize ee connection\n", "is_executing": false}
ee.Initialize()


# + pycharm={"name": "#%% Download image\n", "is_executing": false}
sat_image = ee.Image('USGS/SRTMGL1_003')


# + pycharm={"name": "#%% Define a method for displaying Earth Engine image tiles to folium map.\n", "is_executing": false}
def add_ee_layer(self, ee_image_object, vis_params, name):
  map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
  folium.raster_layers.TileLayer(
    tiles = map_id_dict['tile_fetcher'].url_format,
    attr = "deep-sat",
    name = name,
    overlay = True,
    control = True
  ).add_to(self)

folium.Map.add_ee_layer = add_ee_layer

# + pycharm={"name": "#%% Set visualization parameters\n", "is_executing": true}
# %%capture # Do not display cell output
vis_params = {
  'min': 0,
  'max': 4000,
  'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}

my_map = folium.Map(location=[20, 0], zoom_start=3, height=500)
my_map.add_ee_layer(sat_image.updateMask(sat_image.gt(0)), vis_params, 'DEM')

# Add a layer control panel to the map
my_map.add_child(folium.LayerControl())

# + pycharm={"name": "#%% Display static image\n", "is_executing": false}
from IPython.display import Image
Image(url=sat_image.updateMask(sat_image.gt(0))
  .getThumbUrl({'min': 0, 'max': 4000, 'dimensions': 512,
                'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}))

# + pycharm={"name": "#%% Display map\n", "is_executing": false}
my_map

