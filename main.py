import io
import json
import zipfile

import ndc_parser
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, ORJSONResponse

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'])

with zipfile.ZipFile('zips/ndc8.zip') as zfile, zfile.open('ndc8.ttl') as readfile:
    ndc8_items_source = ndc_parser.parse('8', io.TextIOWrapper(readfile, 'utf-8'))
    ndc8_items = {}
    for key, item in ndc8_items_source.items():
        i = item.copy()
        del i['source']
        ndc8_items[key] = i

with zipfile.ZipFile('zips/ndc9.zip') as zfile, zfile.open('ndc9.ttl') as readfile:
    ndc9_items_source = ndc_parser.parse('9', io.TextIOWrapper(readfile, 'utf-8'))
    ndc9_items = {}
    for key, item in ndc9_items_source.items():
        i = item.copy()
        del i['source']
        ndc9_items[key] = i

with open('./templates/index.html', encoding='utf-8') as file:
    index_html = file.read()

with open('jsonschema.json', encoding='utf-8') as file:
    json_schema = json.load(file)


@app.get(
    '/',
    tags=['index'],
    summary='トップページ',
    description='トップページの表示',
    response_description='トップページのHTMLを返す',
    response_class=HTMLResponse,
)
async def index():
    return index_html


@app.get(
    '/schema',
    tags=['schema'],
    summary='JSONスキーマ',
    description='JSONスキーマの取得',
    response_description='JSONスキーマを返す',
)
async def schema():
    return ORJSONResponse(json_schema, headers={'Access-Control-Allow-Origin': '*'})


@app.get(
    '/ndc8.json',
    tags=['ndc8'],
    summary='NDC8',
    description='NDC8の全データの取得',
    response_description='NDC8の全データを返す',
)
async def ndc8_json():
    return ORJSONResponse(ndc8_items, headers={'Access-Control-Allow-Origin': '*'})


@app.get(
    '/ndc8/',
    tags=['ndc8'],
    summary='NDC8トップ',
    description='NDC8のトップの取得',
    response_description='NDC8のトップを返す',
)
async def ndc8_top():
    return ORJSONResponse(ndc8_items_source[''], headers={'Access-Control-Allow-Origin': '*'})


@app.get(
    '/ndc8/{ndc}',
    tags=['ndc8'],
    summary='NDC8分類項目',
    description='NDC8の分類項目の取得',
    response_description='NDC8の分類項目を返す',
)
async def ndc8(ndc: str):
    return ORJSONResponse(ndc8_items_source[ndc], headers={'Access-Control-Allow-Origin': '*'})


@app.get(
    '/ndc9.json',
    tags=['ndc9'],
    summary='NDC9',
    description='NDC9の全データの取得',
    response_description='NDC9の全データを返す',
)
async def ndc9_json():
    return ORJSONResponse(ndc9_items, headers={'Access-Control-Allow-Origin': '*'})


@app.get(
    '/ndc9/',
    tags=['ndc9'],
    summary='NDC9トップ',
    description='NDC9のトップの取得',
    response_description='NDC9のトップを返す',
)
async def ndc9_top():
    return ORJSONResponse(ndc9_items_source[''], headers={'Access-Control-Allow-Origin': '*'})


@app.get(
    '/ndc9/{ndc}',
    tags=['ndc9'],
    summary='NDC9分類項目',
    description='NDC9の分類項目の取得',
    response_description='NDC9の分類項目を返す',
)
async def ndc9(ndc: str):
    return ORJSONResponse(ndc9_items_source[ndc], headers={'Access-Control-Allow-Origin': '*'})
