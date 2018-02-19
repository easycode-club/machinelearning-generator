from .neuralnetwork import generate_network
from .supportvector import generate_svm

def generate_code(method='neuralnetwork', *args, **kwargs):
    if method == 'neuralnetwork':
        return generate_network(*args, **kwargs)
    elif method == 'supportvector':
        return generate_svm(*args, **kwargs)
