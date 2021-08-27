from __future__ import division, print_function, absolute_import
from numpy.core.records import array

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
from typing import Dict, List, Optional


class Query(BaseModel):
    matrix : List[int]
    ops : List[str]

class PartialGraph(BaseModel):
    node_data : List[Dict]
    edge_data : List[Dict]


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
async def get_querying(item : Query):
    item = item.dict()
    return querying(nasbench_api, nasbench, item['matirix'], item['ops'])


@app.post('/recommendation')
async def get_recommend_cell(item : PartialGraph):
    item = item.dict()
    return recommend_cell(nasbench, item['edge_data'], item['node_data'])

@app.get('/overview/edge-sharpley-value')
async def get_edge_sharpley_value():
    return sharpley_values

@app.get('/')
async def index():
    return RedirectResponse('/static/index.html', 307)
