from .codegenerator import CodeGeneratorBackend

class CodeGenerator(object):
    def __init__(self, inputs, outputs=1):
        self.c = CodeGeneratorBackend()
        self.c.begin()
        self.inputs = inputs
        self.outputs = outputs
        self.generate_comments()
        
    def end(self):
        return self.c.end()
        
    def generate_comments(self):
        self.c.write("# no. of inputs: {0}".format(self.inputs))
        self.c.write("# no. of outputs: {0}".format(self.outputs))
        self.c.write("")
        self.c.write("import pandas as pd")
        self.c.write("from sklearn.model_selection import train_test_split")
        self.c.write("")

    def generate_parse_data(self):
        self.c.write("def parse_data(input_file):")
        self.c.indent()
        self.c.write("dataframe = pd.read_csv(input_file)") # Choose inputs, outputs columns
        self.c.write("data = dataframe.values")
        inputs_arr = []
        k = 1
        for i in range(self.inputs):
            inputs_arr.append(k)
            k+=1
        outputs_arr = []
        for i in range(self.outputs):
            outputs_arr.append(k)
            k+=1
        self.c.write("X = data[:,{0}]".format(inputs_arr))
        self.c.write("Y = data[:,{0}]".format(outputs_arr))
        self.c.write("return train_test_split(X,Y)")
        self.c.write("")
        self.c.dedent()

    def generate_main(self):
        self.c.write("def main():")
        self.c.indent()
        self.c.write("# YOUR INPUT FILE GOES HERE")
        self.c.write("input_file = 'data.csv'")
        self.c.write("X_train, X_test, Y_train, Y_test = parse_data(input_file)")
        self.c.write("model = get_model()")
        self.c.write("train_model(model, X_train, Y_train)")
        self.c.write("score = test_model(model, X_test, Y_test)")
        self.c.write("model.save('model.hdf5')")
        self.c.write("Y_pred = model.predict(X_test)")
        self.c.write("for i in range(len(X_test)):")
        self.c.indent()
        self.c.write("print(Y_pred[i], Y_test[i])")
        self.c.dedent()
        self.c.write("print('Score: ',score)")
        self.c.write("return score")
        self.c.dedent()
        self.c.write("")
        self.c.write("if __name__ == '__main__':")
        self.c.indent()
        self.c.write("main()")
        self.c.dedent()
