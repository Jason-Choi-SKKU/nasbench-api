
INPUT = 'input'
OUTPUT = 'output'
CONV1X1 = 'conv1x1-bn-relu'
CONV3X3 = 'conv3x3-bn-relu'
MAXPOOL3X3 = 'maxpool3x3'

def querying(nasbench_api, nasbench, input_matrix, ops):
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


def recommend_cell(nasbench, node_data, edge_data):
    ops_type = [node['type'] for node in node_data]
    ops_id = [node['id'] for node in node_data]
    result = []

    for fixed_statistics in nasbench.fixed_statistics.items():
        cnt = 0
        skip = 0
        computed_statistics = nasbench.computed_statistics[fixed_statistics[0]]
        module_operations = fixed_statistics[1]['module_operations']
        module_adjacency = fixed_statistics[1]['module_adjacency'].tolist()
        if sorted(ops_type) != sorted(module_operations):
            continue
        node_mapper = [None for _ in node_data]

        node_mapper[0] = 0
        node_mapper[len(node_mapper)-1] = 1

        conv33_id = [i for i, x in enumerate(module_operations) if x == CONV3X3]
        conv11_id = [i for i, x in enumerate(module_operations) if x == CONV1X1]
        pool33_id = [i for i, x in enumerate(module_operations) if x == MAXPOOL3X3]

        for edge in edge_data:
            source_id = edge['sourceNode']
            target_id = edge['targetNode']
            source_type = ops_type[ops_id.index(edge['sourceNode'])]
            target_type = ops_type[ops_id.index(edge['targetNode'])]

            if source_id not in node_mapper:
                if source_type == CONV3X3:
                    idx = conv33_id.pop(0)
                    node_mapper[idx] = source_id
                elif source_type == CONV1X1:
                    idx = conv11_id.pop(0)
                    node_mapper[idx] = source_id
                elif source_type == MAXPOOL3X3:
                    idx = pool33_id.pop(0)
                    node_mapper[idx] = source_id
                cnt += 1

            if target_id not in node_mapper:
                if target_type == CONV3X3:
                    idx = conv33_id.pop(0)
                    node_mapper[idx] = target_id
                elif target_type == CONV1X1:
                    idx = conv11_id.pop(0)
                    node_mapper[idx] = target_id

                elif target_type == MAXPOOL3X3:
                    idx = pool33_id.pop(0)
                    node_mapper[idx] = target_id
                cnt += 1

            mapped_source_id = node_mapper.index(source_id)
            mapped_target_id = node_mapper.index(target_id)
            if module_adjacency[mapped_source_id][mapped_target_id] != 1:
                if cnt == len(node_data):
                    print(mapped_source_id, mapped_target_id,
                          node_mapper, module_adjacency)
                skip = 1
                break

        if skip == 0:
            result.append(
                [
                    computed_statistics[108][0]['final_test_accuracy'],
                    module_operations,
                    module_adjacency,
                ]
            )

    result = sorted(result, key=lambda x: x[0], reverse=True)
    return result[0:5]
