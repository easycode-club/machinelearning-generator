import json
from src.main import generate_code

def machinelearning_generate(event, context):
    input_body = event["body"]
    input_body = json.loads(input_body)
    code = generate_code(**input_body)
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "code": code,
        "input": event
    }

    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
            "Access-Control-Allow-Credentials" : True  #// Required for cookies, authorization headers with HTTPS
        },
        "body": json.dumps(body)
    }

    return response

if __name__ == '__main__':
    # Score:  [2.166258760070801, 0.98199999999999998]
    params = {
        "inputs":2,
        "outputs":2,
        "method":"neuralnetwork",
        "type":"regression",
        "activation_str":'hard_sigmoid',
        "loss_function":'mean_squared_error',
        "regularizer":'l1',
        "kernel_initializer":'random_uniform',
        "bias_initializer":'random_uniform',
        "optimizer":'SGD',
        "learning_rate":0.01,
        "optimizer_params":{
            'decay':0.0001, 
            'momentum': 0.01,
            'nesterov': True
        },
        "verbosity":True,
        "epochs":400,
        "hidden_layers":[1000],
        "dropout":False,
        "tensorboard":False
    }

    # Score:  0.999988786778
    params = {
        "inputs": 2,
        "outputs": 1,
        "type": "regression",
        "method": "supportvector",
        "verbosity": True,
        "kernel": "poly",
        "degree": 2
    }
    code = generate_code(**params)
    print(code)
