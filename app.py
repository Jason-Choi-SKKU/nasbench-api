from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from flask import Flask, request
from flask_restx import Resource, Api, reqparse
from flask_cors import CORS

from absl import app as absl_app
from nasbench import api as nasbench_api

from module.querying import get_data_from_nasbench
from module.sharpley_values import sharpley_values

NASBENCH_TFRECORD = './nasbench_only108.tfrecord'
nasbench = nasbench_api.NASBench(NASBENCH_TFRECORD)
app = Flask(__name__)
CORS(app)
api = Api(app)


@api.route('/querying')
class Querying(Resource):
    def post(self):
        input_matrix = request.json.get('matrix')
        ops = request.json.get('ops')
        return get_data_from_nasbench(nasbench_api, nasbench, input_matrix, ops)

@api.route('/overview/edge-sharpley-value')
class EdgeSharpleyValue(Resource):
    def get(self):
        return sharpley_values
       

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


