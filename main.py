from codegenerator import CodeGeneratorBackend

c = CodeGeneratorBackend()

def generate_init(inputs,outputs,hidden_layers,activation_str,optimizer):
    c.begin()
    c.write("# no. of inputs: {0}".format(inputs))
    c.write("# no. of outputs: {0}".format(outputs))
    c.write("")
    c.write("import pandas as pd")
    c.write("import tensorflow as tf")
    c.write("from keras import backend as K")
    c.write("from keras.models import Sequential")
    c.write("from keras.layers import Dense, Activation")
    c.write("from keras.optimizers import {0}".format(optimizer))
    c.write("from sklearn.model_selection import train_test_split")
    c.write("from keras.callbacks import TensorBoard")
    c.write("")
    # In case, tensorflow needs to be replaced with something else
    # c.write("sess = tf.Session()")
    # c.write("K.set_session(sess)")

def generate_end():
    return c.end()

def generate_parse_data(inputs, outputs):
    c.write("def parse_data(input_file):")
    c.indent()
    c.write("dataframe = pd.read_csv(input_file)") # Choose inputs, outputs columns
    c.write("data = dataframe.values")
    inputs_arr = []
    k = 1
    for i in range(inputs):
        inputs_arr.append(k)
        k+=1
    outputs_arr = []
    for i in range(outputs):
        outputs_arr.append(k)
        k+=1
    c.write("X = data[:,{0}]".format(inputs_arr))
    c.write("Y = data[:,{0}]".format(outputs_arr))
    c.write("return train_test_split(X,Y)")
    c.write("")
    c.dedent()

def generate_get_optimizer(optimizer='SGD', learning_rate=0.01, kwargs={}):
    # TODO: Create a map of all the available optimizer functions and there parameters
    # TODO: Add validation of kwargs from optimizer.json
    c.write("def get_optimizer():")
    c.indent()
    function_params = "lr={0}".format(learning_rate)
    for key in kwargs:
        function_params += ", {0}={1}".format(key, kwargs[key])
    function_call = "{0}({1})".format(optimizer, function_params)
    c.write("return {0}".format(function_call))
    c.dedent()
    c.write("")


def generate_model(inputs,outputs,hidden_layers,activation_str):
    c.write("def get_model():")
    c.indent()
    c.write("model = Sequential()\n")

    c.write("# Input layer")
    if len(hidden_layers) == 0:
        output_first_layer = outputs
    else:
        output_first_layer = hidden_layers[0]
    c.write("model.add(Dense({0},input_shape=({1},)))".format(output_first_layer,inputs))
    c.write("model.add(Activation('{0}'))".format(activation_str))
    c.write("")
    for i in range(0, len(hidden_layers)):
        c.write("model.add(Dense({0}))".format(hidden_layers[i]))
        c.write("model.add(Activation('{0}'))".format(activation_str))
        c.write("")
    c.write("# Output layer")
    c.write("model.add(Dense({0}))".format(outputs))
    c.write("optim = get_optimizer()")
    c.write("model.compile(loss='mean_squared_error', optimizer=optim, metrics=['accuracy'])")
    c.write("return model")
    c.dedent()
    c.write("")

def generate_training(verbosity,tensorboard=False):
    c.write("def train_model(model, X_train, Y_train):")
    c.indent()
    callbacks = "[]"
    if verbosity and tensorboard:
        c.write("tb_callback = TensorBoard(log_dir='/tmp/tf-output', histogram_freq=10, write_grads=True, write_images=True)")
        callbacks = "[tb_callback]"
    c.write("model.fit(X_train, Y_train, epochs=500, verbose={0}, validation_split = 0.3, shuffle=True,callbacks={1})".format(verbosity,callbacks))
    c.dedent()
    c.write("")

def generate_testing(verbosity):
    c.write("def test_model(model, X_test, Y_test):")
    c.indent()
    c.write("score = model.evaluate(X_test, Y_test, verbose={0})".format(verbosity))
    c.write("return score")
    c.write("")
    c.dedent()

def generate_network(
    inputs=3, outputs=2, hidden_layers=[2,4,8], activation_str='sigmoid',
    optimizer='SGD', learning_rate=0.01, optimizer_params={},
    verbosity=True, tensorboard=False):
    """Create a neural networks based on these parameters
    inputs: dimension of input shape
    outputs: no. of outputs
    hidden_layers: Array of hidden_layers required, empty if no hidden layers
    activation_str: Name of Activation function

    optimizer: Name of optimizer
    learning_rate: Learning rate of the optimizer
    optimizer_params: Additional params for optimizer as defined in optimzer.json

    tensorboard: To enable tensorboard output
    """
    generate_init(inputs,outputs,hidden_layers,activation_str,optimizer)
    generate_parse_data(inputs, outputs)
    generate_get_optimizer(optimizer, learning_rate, kwargs=optimizer_params)
    generate_model(inputs,outputs,hidden_layers,activation_str)
    generate_training(verbosity,tensorboard)
    generate_testing(verbosity)

    c.write("def main():")
    c.indent()
    c.write("# YOUR INPUT FILE GOES HERE")
    c.write("input_file = 'data.csv'")
    c.write("X_train, X_test, Y_train, Y_test = parse_data(input_file)")
    c.write("model = get_model()")
    c.write("train_model(model, X_train, Y_train)")
    c.write("score = test_model(model, X_test, Y_test)")
    c.write("Y_pred = model.predict(X_test)")
    c.write("for i in range(len(X_test)):")
    c.indent()
    c.write("print(Y_pred[i], Y_test[i])")
    c.dedent()
    c.write("print('Score: ',score)")
    c.dedent()
    c.write("")
    c.write("if __name__ == '__main__':")
    c.indent()
    c.write("main()")
    c.dedent()

    return generate_end()

if __name__ == '__main__':
    print(generate_network(hidden_layers=[10], tensorboard=False, optimizer_params={'momentum': 0.0}))
