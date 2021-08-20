from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from flask import Flask, request
from flask_restx import Resource, Api, reqparse
from flask_cors import CORS

from absl import app as absl_app
from nasbench import api as nasbench_api


NASBENCH_TFRECORD = './nasbench_only108.tfrecord'
nasbench = nasbench_api.NASBench(NASBENCH_TFRECORD)

from numpy.matrixlib.defmatrix import matrix
from itertools import combinations


INPUT = 'input'
OUTPUT = 'output'
CONV1X1 = 'conv1x1-bn-relu'
CONV3X3 = 'conv3x3-bn-relu'
MAXPOOL3X3 = 'maxpool3x3'

def get_data_from_nasbench(nasbench_api, nasbench, input_matrix, ops):
    model_spec = nasbench_api.ModelSpec(
        matrix=input_matrix,
        ops=ops
    )
   
    data = nasbench.query(model_spec)
    dic = {
        "trainable_parameters" : data['trainable_parameters'],
        "training_time" : data['training_time'],
        "train_accuracy" : data['train_accuracy'],
        "validation_accuracy" : data["validation_accuracy"],
        "test_accuracy" : data["test_accuracy"]
    }
    
    return dic


def get_candidate_cell(nasbench_api, nasbench, edge_data, node_data):
    # edge_data를 돌면서 only sourcenode 인 목록 찾아서 topological sort
    # 만들어진 topological sort 목록들을 depth 대로 정렬
    ops = [node['id'] for node in node_data]
    only_source_node = ops[2:]
    for edge in edge_data:
        try:
            only_source_node.remove(edge['targetNode'])
        except:
            pass
    
    topological_sort_list = []
    
    for start_node in only_source_node:
        visited = [start_node]
        frontier = [start_node]
        topological_sort = []
        
        while frontier:
            has_children = 0
            top = frontier[-1]
            
            for edge in edge_data:
                if edge['sourceNode'] == top and edge['targetNode'] not in visited:
                    visited.append(edge['targetNode'])
                    frontier.append(edge['targetNode'])
                    has_children = 1
                    break
            
            if not has_children:
                topological_sort.append(frontier.pop())
        
        topological_sort.sort(reverse=True)
        topological_sort_list.append(topological_sort)
        
    
    topological_sort_list = sorted(topological_sort_list, key= lambda x : len(x), reverse=True)
    
    ops_id_mapped = [0]
    
    for i in range(len(topological_sort_list[0])):
        for topo in topological_sort_list:
            if topo[i] not in ops_id_mapped:
                ops_id_mapped.append(topo[i])
                
    ops_id_mapped.append(1)
    ops_type_mapped = []
    for op in ops_id_mapped:
        for node in node_data:
            if node['id'] == op:
                ops_type_mapped.append(node['type'])
    
    
    edge_candidate = []
    for i in range(1, len(node_data)):
        for j in range(i, len(node_data)):
            edge_candidate.append([i,j])
    
    
    # matrix 생성
    
    matrix = [[0] * len(node_data) for _ in node_data]
    for edge in edge_data:
        source_node = ops_id_mapped.index(edge['sourceNode'])
        target_node = ops_id_mapped.index(edge['targetNode'])
        matrix[source_node][target_node] = 1
        edge_candidate.remove([source_node, target_node])
        
    result = []
    for num_edge in range(len(edge_data), 10):
        for edges in edge_candidate:
            new_matrix = matrix[:]
            for edge in edges:
                new_matrix[edge[0]][edge[1]] = 1
                
            acc = get_data_from_nasbench(nasbench_api, nasbench, new_matrix, ops_type_mapped)['test_accuracy']
            result.append(acc, new_matrix, ops_type_mapped)
            
    return result[0:5]
                
        
dummy_node_data = [
    {
        'id' : 0,
        'type' : 'input'
    },
    {
        'id': 1,
        'type': 'output'
    },
    {
        'id': 2,
        'type': CONV1X1
    },
    {
        'id': 3,
        'type': CONV3X3
    },
    {
        'id': 4,
        'type': CONV3X3
    },
    {
        'id': 5,
        'type': CONV3X3
    },
    {
        'id': 6,
        'type': CONV3X3
    }, 
]
dummy_edge_data = [
    {
        'sourceNode' : 1,
        'targetNode' : 2,
    },
    {
        'sourceNode' : 2,
        'targetNode' : 4,
    },
    {
        'sourceNode': 3,
        'targetNode': 4,
    },
] 


print(get_candidate_cell(nasbench_api, nasbench, dummy_edge_data, dummy_node_data))
        
        
