import json
from main import generate_network

def machinelearning_generate(event, context):
    code = generate_network()
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "code": code,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
