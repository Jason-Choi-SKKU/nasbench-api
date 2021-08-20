sharpley_values = {
    "name": "sharpley_value",
    "children": [{
        "name": "INPUT to OUTPUT",
        "source": "input",
        "target": "output",
        "value": 0.02153817234095967,
        "include_accuracy": 0.9142298703231571,
        "exclude_accuracy": 0.8926916979821974
    }, {
        "name": "INPUT to 1X1 CONV",
        "source": "input",
        "target": "conv1x1-bn-relu",
        "value": 0.0011925026885490908,
        "include_accuracy": 0.8973735094242626,
        "exclude_accuracy": 0.8961810067357135
    }, {
        "name": "INPUT to 3X3 CONV",
        "source": "input",
        "target": "conv3x3-bn-relu",
        "value": 0.02184323446985814,
        "include_accuracy": 0.9071150718386907,
        "exclude_accuracy": 0.8852718373688325
    }, {
        "name": "INPUT to 3X3 MAXPOOL",
        "source": "input",
        "target": "maxpool3x3",
        "value": 0.0026510059387714335,
        "include_accuracy": 0.8980615286477047,
        "exclude_accuracy": 0.8954105227089333
    }, {
        "name": "1X1 CONV to OUTPUT",
        "source": "conv1x1-bn-relu",
        "target": "output",
        "value": 0.0063300123895806415,
        "include_accuracy": 0.899797025062223,
        "exclude_accuracy": 0.8934670126726424
    }, {
        "name": "1X1 CONV to 1X1 CONV",
        "source": "conv1x1-bn-relu",
        "target": "conv1x1-bn-relu",
        "value": -0.0037439419359760473,
        "include_accuracy": 0.894334125615385,
        "exclude_accuracy": 0.898078067551361
    }, {
        "name": "1X1 CONV to 3X3 CONV",
        "source": "conv1x1-bn-relu",
        "target": "conv3x3-bn-relu",
        "value": 0.017849878050388845,
        "include_accuracy": 0.9076284962164447,
        "exclude_accuracy": 0.8897786181660559
    }, {
        "name": "1X1 CONV to 3X3 MAXPOOL",
        "source": "conv1x1-bn-relu",
        "target": "maxpool3x3",
        "value": -0.016515184870416477,
        "include_accuracy": 0.8868023063085724,
        "exclude_accuracy": 0.9033174911789889
    }, {
        "name": "3X3 CONV to OUTPUT",
        "source": "conv3x3-bn-relu",
        "target": "output",
        "value": 0.02581374819870219,
        "include_accuracy": 0.9089880808785876,
        "exclude_accuracy": 0.8831743326798854
    }, {
        "name": "3X3 CONV to 1X1 CONV",
        "source": "conv3x3-bn-relu",
        "target": "conv1x1-bn-relu",
        "value": 0.0181818343849508,
        "include_accuracy": 0.9078296710456787,
        "exclude_accuracy": 0.8896478366607279
    }, {
        "name": "3X3 CONV to 3X3 CONV",
        "source": "conv3x3-bn-relu",
        "target": "conv3x3-bn-relu",
        "value": 0.01951500229952352,
        "include_accuracy": 0.9097213295954037,
        "exclude_accuracy": 0.8902063272958802
    }, {
        "name": "3X3 CONV to 3X3 MAXPOOL",
        "source": "conv3x3-bn-relu",
        "target": "maxpool3x3",
        "value": -0.0021680079013264297,
        "include_accuracy": 0.8954970970874719,
        "exclude_accuracy": 0.8976651049887984
    }, {
        "name": "3X3 MAXPOOL to OUTPUT",
        "source": "maxpool3x3",
        "target": "output",
        "value": -0.026816016542178245,
        "include_accuracy": 0.8841610605332847,
        "exclude_accuracy": 0.9109770770754629
    }, {
        "name": "3X3 MAXPOOL to 1X1 CONV",
        "source": "maxpool3x3",
        "target": "conv1x1-bn-relu",
        "value": -0.0006124496295345505,
        "include_accuracy": 0.8964398089357161,
        "exclude_accuracy": 0.8970522585652506
    }, {
        "name": "3X3 MAXPOOL to 3X3 CONV",
        "source": "maxpool3x3",
        "target": "conv3x3-bn-relu",
        "value": 0.01343488467184295,
        "include_accuracy": 0.9049528866662603,
        "exclude_accuracy": 0.8915180019944173
    }, {
        "name": "3X3 MAXPOOL to 3X3 MAXPOOL",
        "source": "maxpool3x3",
        "target": "maxpool3x3",
        "value": -0.029893923784442555,
        "include_accuracy": 0.8770343247000018,
        "exclude_accuracy": 0.9069282484844443
    }]
}