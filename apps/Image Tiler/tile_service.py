import os
import sys

import uvicorn
from fastapi import FastAPI
from starlette import status
from fastapi.openapi.utils import get_openapi
from fastapi_restful import Resource, Api, set_responses


app = FastAPI()
api = Api(app)

@app.get("/")
@app.get("/homepage", status_code=status.HTTP_200_OK)
async def homepage():
    return {"message": "This is the Image Tiler Homepage!"}


# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="Custom title",
#         version="2.5.0",
#         description="This is a very custom OpenAPI schema",
#         routes=app.routes,
#     )
#     openapi_schema["paths"]["/api/auth"] = {
#         "post": {
#             "requestBody": {"content": {"application/json": {}}, "required": True}, "tags": ["Auth"]
#         }
#     }
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


# app.openapi = custom_openapi

class TileService(Resource):
    @set_responses(response={"message": "This is the Image Tiler Tile Service!"})
    def get(self):
        return {"message": "This is the Image Tiler Service!"}

api.add_resource(TileService, "/service/satellite/tile")


if __name__ == "__main__":
    uvicorn.run("image_tiler:app",host='192.168.21.146', port=8002, reload=True,workers=3)