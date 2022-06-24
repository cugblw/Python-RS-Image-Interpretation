import os
import sys

import uvicorn
from fastapi import FastAPI, Request, Response
from starlette import status
from fastapi.openapi.utils import get_openapi
from typing import Optional

import utils.tile_util as tu


app = FastAPI()

# @app.route('/{_:path}')
# async def https_redirect(request: Request):
#     return RedirectResponse(request.url.replace(scheme='https'))

@app.get("/")
@app.get("/homepage", status_code=status.HTTP_200_OK)
def homepage():
    return {"message": "This is the Image Tiler Homepage!"}

# 瓦片服务接口 
@app.get("/service/satellite/tile/{zoom}/{x}/{y}")
async def get_tile(zoom: int, x: int, y: int):
    data = tu.search_tile(zoom, x, y)
    res = Response(data)
    res.headers["Content-Type"] = "image/png"
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res

# http://10.168.1.105:8002/question?id=1
@app.get("/question")
async def get_question(id: int):
    return {"id": id, "question": "What's your name?"}


# Optional 可选参数
@app.get("/items/{item_id}")
async def read_item(item_id: int, question: Optional[str] = None):
    return {"item_id": item_id, "question": question}





if __name__ == "__main__":
    # uvicorn.run("tile_service:app",host='10.168.1.105', port=8002, reload=True,workers=3)
    uvicorn.run("tile_service:app",host='0.0.0.0', port=8002, reload=True,workers=3)