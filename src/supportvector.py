from .codegenerator import CodeGeneratorBackend
from .generators import generate_comments, generate_parse_data, generate_main

c = CodeGeneratorBackend()

def get_model_function(type):
    if(type == 'classification'):
        return "SVC"
    else:
        return "SVR"

def generate_init(inputs, type):
    c.begin()
    generate_comments(c, inputs, outputs=1)
    c.write("from sklearn.svm import {0}".format(get_model_function(type)))
    c.write("")

def generate_model(inputs, type, kernel):
    c.write("def get_model():")
    c.indent()
    c.write("clf = {0}(kernel='{1}')".format(get_model_function(type), kernel))
    c.write("return clf")
    c.dedent()
    c.write("")

def generate_training():
    c.write("def train_model(model, X_train, Y_train):")
    c.indent()
    c.write("model.fit(X_train, Y_train)")
    c.dedent()
    c.write("")

def generate_testing():
    c.write("def test_model(model, X_test, Y_test):")
    c.indent()
    c.write("score = model.score(X_test, Y_test)")
    c.write("return score")
    c.write("")
    c.dedent()

def generate_svm(inputs=3, type='regression', kernel='rbf', *args, **kwargs):
    generate_init(inputs, type)
    generate_parse_data(c, inputs, outputs=1)
    generate_model(inputs, type, kernel)
    generate_training()
    generate_testing()

    generate_main(c)

    return c.end()
