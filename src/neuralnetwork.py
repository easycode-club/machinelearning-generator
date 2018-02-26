from .codegenerator import CodeGeneratorBackend
from .generators import generate_comments, generate_parse_data, generate_main

c = CodeGeneratorBackend()

def generate_init(inputs,outputs,hidden_layers,activation_str,optimizer):
    c.begin()
    generate_comments(c, inputs, outputs)
    c.write("from keras.models import Sequential")
    c.write("from keras.layers import Dense, Activation, Dropout")
    c.write("from keras.optimizers import {0}".format(optimizer))
    c.write("from keras.callbacks import TensorBoard, EarlyStopping")
    c.write("")
    # In case, tensorflow needs to be replaced with something else
    # c.write("sess = tf.Session()")
    # c.write("K.set_session(sess)")

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


def generate_model(inputs,outputs,type, hidden_layers, loss_function, activation_str, kernel_initializer,bias_initializer,dropout=True,dropout_rate=0.1):
    c.write("def get_model():")
    c.indent()
    c.write("model = Sequential()\n")

    c.write("# Input layer")
    if len(hidden_layers) == 0:
        output_first_layer = outputs
    else:
        output_first_layer = hidden_layers[0]
    c.write("model.add(Dense({0},input_shape=({1},),kernel_initializer='{2}',bias_initializer='{3}'))".format(output_first_layer,inputs,kernel_initializer,bias_initializer))
    c.write("model.add(Activation('{0}'))".format(activation_str))    
    if dropout and len(hidden_layers) > 0:
        c.write("model.add(Dropout({0}))".format(dropout_rate))
    c.write("")
    for i in range(1, len(hidden_layers)):
        c.write("model.add(Dense({0}, activation='{1}',kernel_initializer='{2}',bias_initializer='{3}'))".format(hidden_layers[i], activation_str,kernel_initializer,bias_initializer))
        if dropout:
            c.write("model.add(Dropout({0}))".format(dropout_rate))
        c.write("")
    if len(hidden_layers) > 0:
        c.write("# Output layer")
        c.write("model.add(Dense({0},kernel_initializer='{1}',bias_initializer='{2}'))".format(outputs, kernel_initializer,bias_initializer))

    c.write("optim = get_optimizer()")
    c.write("model.compile(loss='{0}', optimizer=optim, metrics=['accuracy'])".format(loss_function))
    c.write("return model")
    c.dedent()
    c.write("")

def generate_training(verbosity,type,epochs,tensorboard=False):
    c.write("def train_model(model, X_train, Y_train):")
    c.indent()
    c.write("early_stopping = EarlyStopping()")    
    callbacks = "[early_stopping]"
    if tensorboard:
        c.write("tb_callback = TensorBoard(log_dir='/tmp/tf-output', histogram_freq=10, write_grads=True, write_images=True)")
        callbacks = "[early_stopping,tb_callback]"
    c.write("model.fit(X_train, Y_train, epochs={0}, verbose={1}, validation_split = 0.3, shuffle=True,callbacks={2})".format(epochs,verbosity,callbacks))
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
    inputs=3, outputs=2, hidden_layers=[2,4,8], type='regression', activation_str='sigmoid',
    loss_function='mean_squared_error',
    optimizer='SGD', learning_rate=0.01, optimizer_params={},
    kernel_initializer='glorot_uniform',
    bias_initializer='glorot_uniform',
    epochs=100,
    dropout=True, dropout_rate=0.1,
    verbosity=True, tensorboard=False, **kwargs):
    """Create a neural networks based on these parameters
    inputs: dimension of input shape
    outputs: no. of outputs
    hidden_layers: Array of hidden_layers required, empty if no hidden layers
    type: regression or classification
    activation_str: Name of Activation function

    optimizer: Name of optimizer
    learning_rate: Learning rate of the optimizer
    optimizer_params: Additional params for optimizer as defined in optimzer.json

    dropout_rate: Dropout rate

    tensorboard: To enable tensorboard output
    """
    generate_init(inputs,outputs,hidden_layers,activation_str,optimizer)
    generate_parse_data(c, inputs, outputs)
    generate_get_optimizer(optimizer, learning_rate, kwargs=optimizer_params)
    generate_model(inputs,outputs,type,hidden_layers, loss_function, activation_str,kernel_initializer,bias_initializer,dropout,dropout_rate)
    generate_training(verbosity,type,epochs,tensorboard)
    generate_testing(verbosity)

    generate_main(c)

    return c.end()
