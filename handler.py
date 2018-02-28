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
    code = generate_code(inputs=2,outputs=2,method="neuralnetwork", type="regression", activation_str='hard_sigmoid', loss_function='mean_squared_error', regularizer='l1', kernel_initializer='random_uniform',bias_initializer='random_uniform',optimizer='SGD', learning_rate=0.01, optimizer_params={'decay':0.0001}, verbosity=True, epochs=10000, hidden_layers=[100],dropout=False, tensorboard=False)
    print(code)
