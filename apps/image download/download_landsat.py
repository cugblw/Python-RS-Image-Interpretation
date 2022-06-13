
import json
from landsatxplore.api import API

# Initialize a new API instance and get an access key
api = API('Weil_Lee', 'WeilLee|2021')

# Search for Landsat TM scenes
scenes = api.search(
    dataset='landsat_tm_c1',
    latitude=50.85,
    longitude=-4.35,
    start_date='1995-01-01',
    end_date='1995-10-01',
    max_cloud_cover=10
)

print(f"{len(scenes)} scenes found.")

# Process the result
for scene in scenes:
    print(scene['acquisition_date'])
    # Write scene footprints to disk
    fname = f"{scene['landsat_product_id']}.geojson"
    with open(fname, "w") as f:
        json.dump(scene['spatialCoverage'], f)

api.logout()