from .codegenerator import CodeGeneratorBackend
from .generators import CodeGenerator

class NeuralNetworkGenerator(CodeGenerator):
    def __init__(self, 
                inputs=3, outputs=2, hidden_layers=[2,4,8], type='regression', activation_str='sigmoid',
                loss_function='mean_squared_error',
                optimizer='SGD', learning_rate=0.01, optimizer_params={'decay': 0.001},
                regularizer='l2',
                kernel_initializer='glorot_uniform',
                bias_initializer='glorot_uniform',
                early_stopping=False,
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
        super().__init__(inputs, outputs)
        self.generate_init(inputs,outputs,hidden_layers,activation_str,optimizer)
        self.generate_parse_data()
        self.generate_get_optimizer(optimizer, learning_rate, kwargs=optimizer_params)
        self.generate_model(inputs,outputs,type,hidden_layers, loss_function, activation_str,regularizer,kernel_initializer,bias_initializer,dropout,dropout_rate)
        self.generate_training(verbosity,type,epochs,early_stopping,tensorboard)
        self.generate_testing(verbosity)

        self.generate_main()

    def generate_init(self,inputs,outputs,hidden_layers,activation_str,optimizer):
        self.c.write("from keras.models import Sequential")
        self.c.write("from keras.layers import Dense, Activation, Dropout")
        self.c.write("from keras.optimizers import {0}".format(optimizer))
        self.c.write("from keras.callbacks import TensorBoard, EarlyStopping")
        self.c.write("from keras import regularizers")
        self.c.write("")
        # In case, tensorflow needs to be replaced with something else
        # self.c.write("sess = tf.Session()")
        # self.c.write("K.set_session(sess)")

    def generate_get_optimizer(self,optimizer='SGD', learning_rate=0.01, kwargs={}):
        """
        TODO: Create a map of all the available optimizer functions and there parameters
        TODO: Add validation of kwargs from optimizer.json
        """
        self.c.write("def get_optimizer():")
        self.c.indent()
        function_params = "lr={0}".format(learning_rate)
        for key in kwargs:
            function_params += ", {0}={1}".format(key, kwargs[key])
        function_call = "{0}({1})".format(optimizer, function_params)
        self.c.write("return {0}".format(function_call))
        self.c.dedent()
        self.c.write("")


    def generate_model(self,inputs,outputs,type, hidden_layers, loss_function, activation_str, regularizer, kernel_initializer,bias_initializer,dropout=True,dropout_rate=0.1):
        self.c.write("def get_model():")
        self.c.indent()
        self.c.write("model = Sequential()\n")

        self.c.write("# Input layer")
        if len(hidden_layers) == 0:
            output_first_layer = outputs
        else:
            output_first_layer = hidden_layers[0]
        self.c.write("model.add(Dense({0},input_shape=({1},),kernel_initializer='{2}',bias_initializer='{3}',kernel_regularizer=regularizers.{4}()))".format(output_first_layer,inputs,kernel_initializer,bias_initializer,regularizer))
        self.c.write("model.add(Activation('{0}'))".format(activation_str))    
        if dropout and len(hidden_layers) > 0:
            self.c.write("model.add(Dropout({0}))".format(dropout_rate))
        self.c.write("")
        for i in range(1, len(hidden_layers)):
            self.c.write("model.add(Dense({0}, activation='{1}',kernel_initializer='{2}',bias_initializer='{3}',kernel_regularizer=regularizers.{4}()))".format(hidden_layers[i], activation_str,kernel_initializer,bias_initializer, regularizer))
            if dropout:
                self.c.write("model.add(Dropout({0}))".format(dropout_rate))
            self.c.write("")
        if len(hidden_layers) > 0:
            self.c.write("# Output layer")
            self.c.write("model.add(Dense({0},kernel_initializer='{1}',bias_initializer='{2}'))".format(outputs, kernel_initializer,bias_initializer))

        self.c.write("optim = get_optimizer()")
        self.c.write("model.compile(loss='{0}', optimizer=optim, metrics=['accuracy'])".format(loss_function))
        self.c.write("return model")
        self.c.dedent()
        self.c.write("")

    def generate_training(self,verbosity,type,epochs,early_stopping,tensorboard=False):
        self.c.write("def train_model(model, X_train, Y_train):")
        self.c.indent()
        callbacks = "[]"
        if early_stopping:
            self.c.write("early_stopping = EarlyStopping()")    
            callbacks = "[early_stopping]"
        if tensorboard:
            self.c.write("tb_callback = TensorBoard(log_dir='/tmp/tf-output', histogram_freq=10, write_grads=True, write_images=True)")
            callbacks = "[tb_callback]"
        if early_stopping and tensorboard:
            callbacks = "[early_stopping.tb_callback]"
        self.c.write("model.fit(X_train, Y_train, epochs={0}, verbose={1}, validation_split = 0.3, shuffle=True,callbacks={2})".format(epochs,verbosity,callbacks))
        self.c.dedent()
        self.c.write("")

    def generate_testing(self,verbosity):
        self.c.write("def test_model(model, X_test, Y_test):")
        self.c.indent()
        self.c.write("score = model.evaluate(X_test, Y_test, verbose={0})".format(verbosity))
        self.c.write("return score")
        self.c.write("")
        self.c.dedent()
