import random

def random_data():
    fl = open('data.csv','w+')
    fl.write('0,input1,input2,output1,output2')
    fl.write('\n')
    for i in range(10000):
        a = round(random.random()*10, 2)
        # b = a*a
        b = round(random.random()*10, 2)
        c = round(a*b, 2)
        d = round(a*a, 2)
        # c = random.randint(0,10)
        # fl.write('{0},{1},{2},{3},{4},{5}'.format(i,a,b,c,a+b+c,a-b+c))
        fl.write('{0},{1},{2},{3},{4}'.format(i, a, b, c, d))
        fl.write('\n')
    fl.close()

random_data()
