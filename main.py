from codegenerator import CodeGeneratorBackend

c = CodeGeneratorBackend()

def generate_init():
    c.begin()
    c.write("import pandas as pd")
    c.write("from keras.models import Sequential")
    c.write("from keras.layers import Dense, Activation")
    c.write("from keras.optimizers import SGD")
    c.write("from sklearn.model_selection import train_test_split")
    c.write("")

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
    c.dedent()

def generate_model(inputs,outputs,hidden_layers):
    c.write("def get_model():")
    c.indent()
    c.write("model = Sequential()")

    c.write("model.add(Dense({0},input_shape=({1},)))".format(hidden_layers[0],inputs))
    c.write("model.add(Dense({0}))".format(outputs))

    c.write("optim = SGD(lr=0.001, momentum=0.9, nesterov=True)")
    c.write("model.compile(loss='mean_squared_error', optimizer=optim, metrics=['accuracy'])")
    c.write("return model")
    c.dedent()
    c.write("")

def generate_training():
    c.write("def train_model(model, X_train, X_test):")
    c.indent()
    c.write("model.fit(X_train, Y_train, epochs=500, verbose=False, validation_split = 0.3, shuffle=True)")
    c.dedent()
    c.write("")

def generate_testing():
    c.write("def test_model(model, X_test, Y_test):")
    c.indent()
    c.write("score = model.evaluate(X_test, Y_test, verbose=0)")
    c.write("return score")
    c.dedent()
    c.write("")

def generate_network(inputs=24, outputs=2, hidden_layers=[2]):
    generate_init()
    generate_parse_data(inputs, outputs)
    generate_model(inputs,outputs,hidden_layers)
    generate_training()
    generate_testing()

    c.write("if __name__ == '__main__':")
    c.indent()
    c.write("# YOUR INPUT FILE GOES HERE")
    c.write("input_file = 'data.csv'")
    c.write("X_train, X_test, Y_train, Y_test = parse_data(input_file)")
    c.write("model = get_model()")
    c.write("train_model(model, X_train, X_test)")
    c.write("score = test_model(model, X_test, Y_test)")
    c.write("print(score)")
    c.dedent()

    return generate_end()

print(generate_network())
