from .codegenerator import CodeGeneratorBackend
from .generators import CodeGenerator

class SupportVectorMachine(CodeGenerator):
    def __init__(self,inputs=3, type='regression', kernel='rbf',degree=2,verbosity=True, *args, **kwargs):
        super().__init__(inputs)
        self.generate_init(inputs, type)
        self.generate_parse_data()
        self.generate_model(inputs, type, kernel,degree,verbosity)
        self.generate_training()
        self.generate_testing()

        self.generate_main()

    def get_model_function(self, type):
        if(type == 'classification'):
            return "SVC"
        else:
            return "SVR"

    def generate_init(self, inputs, type):
        self.c.write("from sklearn.svm import {0}".format(self.get_model_function(type)))
        self.c.write("")

    def generate_model(self, inputs, type, kernel,degree,verbosity):
        self.c.write("def get_model():")
        self.c.indent()
        self.c.write("clf = {0}(kernel='{1}',degree={2},verbose={3})".format(self.get_model_function(type), kernel,degree,verbosity))
        self.c.write("return clf")
        self.c.dedent()
        self.c.write("")

    def generate_training(self):
        self.c.write("def train_model(model, X_train, Y_train):")
        self.c.indent()
        self.c.write("model.fit(X_train, Y_train)")
        self.c.dedent()
        self.c.write("")

    def generate_testing(self):
        self.c.write("def test_model(model, X_test, Y_test):")
        self.c.indent()
        self.c.write("score = model.score(X_test, Y_test)")
        self.c.write("return score")
        self.c.write("")
        self.c.dedent()
