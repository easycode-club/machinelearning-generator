from .neuralnetwork import generate_network

def generate_code(method='neuralnetwork', *args, **kwargs):
    if method == 'neuralnetwork':
        return generate_network(*args, **kwargs)
    elif method == 'supportvector':
        return None
