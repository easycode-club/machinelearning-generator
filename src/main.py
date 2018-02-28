from .neuralnetwork import NeuralNetworkGenerator
from .supportvector import SupportVectorMachine

def generate_code(method='neuralnetwork', *args, **kwargs):
    if method == 'neuralnetwork':
        return NeuralNetworkGenerator(*args, **kwargs)
    elif method == 'supportvector':
        return SupportVectorMachine(*args, **kwargs)
