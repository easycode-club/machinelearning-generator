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
    code = generate_code(method="neuralnetwork", type="regression", activation_str='linear', loss_function='mean_squared_error', kernel_initializer='random_uniform',bias_initializer='random_uniform',optimizer='Adam',verbosity=False, hidden_layers=[10],dropout=False, tensorboard=False)
    print(code)
