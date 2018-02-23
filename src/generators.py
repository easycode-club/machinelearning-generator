from .codegenerator import CodeGeneratorBackend

def generate_comments(c, inputs,outputs):
    c.write("# no. of inputs: {0}".format(inputs))
    c.write("# no. of outputs: {0}".format(outputs))
    c.write("")
    c.write("import pandas as pd")
    c.write("from sklearn.model_selection import train_test_split")
    c.write("")

def generate_parse_data(c, inputs, outputs):
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

def generate_main(c):
    c.write("def main():")
    c.indent()
    c.write("# YOUR INPUT FILE GOES HERE")
    c.write("input_file = 'data.csv'")
    c.write("X_train, X_test, Y_train, Y_test = parse_data(input_file)")
    c.write("model = get_model()")
    c.write("train_model(model, X_train, Y_train)")
    c.write("score = test_model(model, X_test, Y_test)")
    c.write("model.save('model.hdf5')")
    c.write("Y_pred = model.predict(X_test)")
    c.write("for i in range(len(X_test)):")
    c.indent()
    c.write("print(Y_pred[i], Y_test[i])")
    c.dedent()
    c.write("print('Score: ',score)")
    c.write("return score")
    c.dedent()
    c.write("")
    c.write("if __name__ == '__main__':")
    c.indent()
    c.write("main()")
    c.dedent()
