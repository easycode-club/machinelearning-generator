from main import generate_network

def machinelearning_name(event, context):
    code = generate_network()
    message = 'Hello {} {}!'.format(event['first_name'],
                                    event['last_name'])
    return {
        'message' : message,
        'code': code
    }
