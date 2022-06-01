from datetime import datetime

from shapely.geometry import Point
from pylandsat import Catalog, Product

catalog = Catalog()

begin = datetime(2020, 1, 1)
end = datetime(2020, 2, 1)
geom = Point(4.34, 50.85)

# Results are returned as a list
scenes = catalog.search(
    begin=begin,
    end=end,
    geom=geom,
    sensors=['LE07', 'LC08']
)
print(scenes)

# Get the product ID of the first scene
product_id = scenes[0].get("product_id")

# Download the scene
product = Product(product_id)
product.download(out_dir='data')

# The output of catalog.search() can be converted to a DataFrame
# for further processing. For instance:
# Get the product ID of the scene with the lowest cloud cover
import pandas as pd

df = pd.DataFrame.from_dict(scenes)
df.set_index(["product_id"], inplace=True)
df = df.sort_values(by='cloud_cover', ascending=True)
product_id = df.index[0]