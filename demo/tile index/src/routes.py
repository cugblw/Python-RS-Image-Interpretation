from flask import Flask
from flask import render_template, make_response

from tile_index_parser import get_tile_data

app = Flask(__name__)
BASE = "http://127.0.0.1:8005"
INDEX_DIR = "https://bluedata-dom.minedata.cn/satellite/index"
TILE_DIR = "https://bluedata-dom.minedata.cn/satellite"


@app.route('/')
def index():
    return ('<h1>Hello World!</h1>')



@app.route('/satellite/service', methods=['GET'])
def result():
    projection = 'MECATOR'
    if projection == 'wmts':
        projection = 'LATLON'
    else:
        projection = "MECATOR"

    center = [116.397428, 39.90923]
    zoom = 14

    style = {
        "sources": {
            "satellite": {
                "type": "raster",
                "tileSize": 512,
                # "tiles": ["/service/map/satellite/" + id + "?z={z}&x={x}&y={y}"]
                "tiles": ["/service/map/satellite/{z}/{x}/{y}"]
            }
        },
        # "sprite": "minemap://sprite/sprite",
        "layers": [
            {
                "layout": {
                    "visibility": "visible"
                },
                "maxzoom": 22,
                "paint": {
                    "background-color": "#f5f5f5"
                },
                "source": "",
                "source-layer": "",
                "id": "9a2f44ef549240b88e0b1cea15d750c3",
                "type": "background",
                "minzoom": 0
            },
            {
                "id": "satellite",
                "type": "raster",
                "source": "satellite",
                "minzoom": 0,
                "maxzoom": 22,
                "layout": {
                    "visibility": "visible"
                }
            }

        ],
        "glyphs": "minemap://fonts/{fontstack}/{range}",
        "version": 8
    }

    return render_template("resultservice.html", zoom=zoom, center=center, style=style, projection=projection), 200

@app.route('/satellite/map/satellite/<int:zoom>/<int:x>/<int:y>', methods=['GET'])
def tile_service(zoom, x, y):
    data = get_tile_data(zoom, x, y, TILE_DIR, INDEX_DIR)
    res = make_response(data)
    res.headers['Content-Type'] = 'image/jpeg'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res