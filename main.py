import json
import codecs

from fastapi import FastAPI, Body
from starlette.responses import HTMLResponse, UJSONResponse
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'])


import io
import zipfile
from NDCParser import parse_ndc_ttl

with zipfile.ZipFile("zips/ndc8.zip") as zfile:
    with zfile.open("ndc8.ttl") as readfile:
        ndc8_items_source = parse_ndc_ttl("8", io.TextIOWrapper(readfile, "utf-8"))
        ndc8_items = {}
        for key, item in ndc8_items_source.items():
            i = item.copy()
            del i["source"]
            ndc8_items[key] = i

with zipfile.ZipFile("zips/ndc9.zip") as zfile:
    with zfile.open("ndc9.ttl") as readfile:
        ndc9_items_source = parse_ndc_ttl("9", io.TextIOWrapper(readfile, "utf-8"))
        ndc9_items = {}
        for key, item in ndc9_items_source.items():
            i = item.copy()
            del i["source"]
            ndc9_items[key] = i



@app.get("/",
    tags=["index"],
    summary="トップページ",
    description="トップページの表示",
    response_description="トップページのHTMLを返す",
    content_type=HTMLResponse
)
async def index():
    with codecs.open("./templates/index.html", "r", "utf-8") as file:
        return file.read()


@app.get("/schema",
    tags=["schema"],
    summary="JSONスキーマ",
    description="JSONスキーマの取得",
    response_description="JSONスキーマを返す"
)
async def schema():
    with codecs.open("jsonschema.json", "r", "utf-8") as file:
        json_schema = json.load(file)
    return UJSONResponse(json_schema, headers={'Access-Control-Allow-Origin': '*'})


@app.get("/ndc8.json",
    tags=["ndc8"],
    summary="NDC8",
    description="NDC8の全データの取得",
    response_description="NDC8の全データを返す"
)
async def ndc8_json():
    return UJSONResponse(ndc8_items, headers={'Access-Control-Allow-Origin': '*'})

@app.get("/ndc8/",
    tags=["ndc8"],
    summary="NDC8トップ",
    description="NDC8のトップの取得",
    response_description="NDC8のトップを返す"
)
async def ndc8_top():
    return UJSONResponse(ndc8_items_source[""], headers={'Access-Control-Allow-Origin': '*'})

@app.get("/ndc8/{ndc}",
    tags=["ndc8"],
    summary="NDC8分類項目",
    description="NDC8の分類項目の取得",
    response_description="NDC8の分類項目を返す"
)
async def ndc8(ndc: str):
    return UJSONResponse(ndc8_items_source[ndc], headers={'Access-Control-Allow-Origin': '*'})

@app.get("/ndc9.json",
    tags=["ndc9"],
    summary="NDC9",
    description="NDC9の全データの取得",
    response_description="NDC9の全データを返す"
)
async def ndc8_json():
    return UJSONResponse(ndc9_items, headers={'Access-Control-Allow-Origin': '*'})

@app.get("/ndc9/",
    tags=["ndc9"],
    summary="NDC9トップ",
    description="NDC9のトップの取得",
    response_description="NDC9のトップを返す"
)
async def ndc9_top():
    return UJSONResponse(ndc9_items_source[""], headers={'Access-Control-Allow-Origin': '*'})

@app.get("/ndc9/{ndc}",
    tags=["ndc9"],
    summary="NDC9分類項目",
    description="NDC9の分類項目の取得",
    response_description="NDC9の分類項目を返す"
)
async def ndc9(ndc: str):
    return UJSONResponse(ndc9_items_source[ndc], headers={'Access-Control-Allow-Origin': '*'})



# Fast API Sample
# class Item(BaseModel):
#     name: str
#     description: str = None
#     price: float
#     tax: float = None

# @app.post("/items/{item_id}", tags=["FastAPI example"])
# async def create_item(
#     *,
#     item_id: int,
#     item: Item = Body(
#         ...,
#         example={
#             "name": "Foo",
#             "description": "A very nice Item",
#             "price": 35.4,
#             "tax": 3.2,
#         },
#     )
# ):
#     """
#     Create an item with all the information:

#     * name: each item must have a name
#     * description: a long description
#     * price: required
#     * tax: if the item doesn't have tax, you can omit this
#     * tags: a set of unique tag strings for this item
#     """
#     results = {"item_id": item_id, "item": item}
#     return results

# @app.get("/elements/", tags=["FastAPI example"], deprecated=True)
# async def read_elements():
#     return [{"item_id": "Foo"}]

