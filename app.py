from __future__ import division, print_function, absolute_import

from starlette.responses import RedirectResponse


from module.sharpley_values import sharpley_values
from module.querying import querying, recommend_cell
import json, os, requests


from absl import app as absl_app
from nasbench import api as nasbench_api


from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import Optional


if not os.path.isfile('./nasbench_only108.tfrecord'):
    print('There is no tfrecord file. Downloading...')
    req = requests.get('https: // storage.googleapis.com/nasbench/nasbench_only108.tfrecord', allow_redirects=True)
    open('nasbench_only108.tfrecord', 'wb').write(req.content)


NASBENCH_TFRECORD = './nasbench_only108.tfrecord'
nasbench = nasbench_api.NASBench(NASBENCH_TFRECORD)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/querying')
async def get_querying(request: Request):
    body = request.body()
    input_matrix = body.get('matrix')
    ops = body.get('ops')
    return querying(nasbench_api, nasbench, input_matrix, ops)


@app.post('/recommendation')
async def get_recommend_cell(request: Request):
    body = request.body()
    edge_data = body.get('edge_data')
    node_data = body.get('node_data')
    return recommend_cell(nasbench, edge_data, node_data)

@app.get('/overview/edge-sharpley-value')
async def get_edge_sharpley_value():
    return sharpley_values

@app.get('/')
async def index():
    return RedirectResponse('/static/index.html', 307)
