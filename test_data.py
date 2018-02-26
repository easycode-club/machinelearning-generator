import random

def random_data():
    fl = open('data.csv','w+')
    fl.write('0,input1,input2,output1,output2')
    fl.write('\n')
    for i in range(100):
        a = random.randint(0,10)
        # b = a*a
        b = random.randint(0,10)
        c = a*b
        d = a*a
        # c = random.randint(0,10)
        # fl.write('{0},{1},{2},{3},{4},{5}'.format(i,a,b,c,a+b+c,a-b+c))
        fl.write('{0},{1},{2},{3},{4}'.format(i, a, b, c, d))
        fl.write('\n')
    fl.close()

random_data()
