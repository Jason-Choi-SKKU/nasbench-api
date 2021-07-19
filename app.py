from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from flask import Flask, request
from flask_restx import Resource, Api, reqparse

from absl import app as absl_app
from nasbench import api as nasbench_api

NASBENCH_TFRECORD = './nasbench_only108.tfrecord'

INPUT = 'input'
OUTPUT = 'output'
CONV1X1 = 'conv1x1-bn-relu'
CONV3X3 = 'conv3x3-bn-relu'
MAXPOOL3X3 = 'maxpool3x3'


def get_data_from_nasbench(input_matrix):

    nasbench = nasbench_api.NASBench(NASBENCH_TFRECORD)

    model_spec = nasbench_api.ModelSpec(
        matrix=input_matrix,
        ops=[INPUT, CONV1X1, CONV3X3, CONV3X3, CONV3X3, MAXPOOL3X3, OUTPUT]
    )

    print('Querying an Inception-like model.')
    data = nasbench.query(model_spec)
    print(data)
    dic = {
        "trainable_parameters" : data['trainable_parameters'],
        "training_time" : data['training_time'],
        "train_accuracy" : data['train_accuracy'],
        "validation_accuracy" : data["validation_accuracy"],
        "test_accuracy" : data["test_accuracy"]
    }
    print(dic)
    return dic


app = Flask(__name__)
api = Api(app)


@api.route('/nasbench')
class Nasbench(Resource):
    def get(self):
        input_matrix = request.json.get('matrix')
        print(input_matrix)
        return get_data_from_nasbench(input_matrix)


if __name__ == '__main__':
    app.run(debug=True, host=0.0.0.0, port=8080)


