from fastapi import FastAPI
from starlette.responses import UJSONResponse
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


@app.get("/")
def read_root():
    return UJSONResponse({"Hello": "FastAPI"}, headers={'Access-Control-Allow-Origin': '*'})

@app.get("/ndc8.json")
async def ndc8_index():
    return UJSONResponse(ndc8_items, headers={'Access-Control-Allow-Origin': '*'})

@app.get("/ndc8/")
def ndc8():
    return UJSONResponse(ndc8_items_source[""], headers={'Access-Control-Allow-Origin': '*'})

@app.get("/ndc8/{ndc}")
def ndc8(ndc):
    return UJSONResponse(ndc8_items_source[ndc], headers={'Access-Control-Allow-Origin': '*'})

@app.get("/ndc9.json")
def ndc8_index():
    return UJSONResponse(ndc9_items, headers={'Access-Control-Allow-Origin': '*'})

@app.get("/ndc9/")
def ndc9():
    return UJSONResponse(ndc9_items_source[""], headers={'Access-Control-Allow-Origin': '*'})

@app.get("/ndc9/{ndc}")
def ndc9(ndc):
    return UJSONResponse(ndc9_items_source[ndc], headers={'Access-Control-Allow-Origin': '*'})


