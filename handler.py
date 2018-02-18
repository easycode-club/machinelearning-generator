import json
from main import generate_network

def machinelearning_generate(event, context):
    input_body = event["body"]
    input_body = json.loads(input_body)
    code = generate_network(**input_body)
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