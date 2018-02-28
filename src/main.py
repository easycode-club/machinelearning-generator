from .neuralnetwork import NeuralNetworkGenerator
from .supportvector import SupportVectorMachine

def generate_code(method='neuralnetwork', *args, **kwargs):
    if method == 'neuralnetwork':
        Code = NeuralNetworkGenerator(*args, **kwargs)
    elif method == 'supportvector':
        Code = SupportVectorMachine(*args, **kwargs)
    return Code.end()
