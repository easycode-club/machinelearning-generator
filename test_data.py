import random

def random_data():
    fl = open('data.csv','w+')
    fl.write('0,input1,input2,input3,output1,output2')
    fl.write('\n')
    for i in range(1000):
        a = random.randint(0,10)
        b = random.randint(0,10)
        c = random.randint(0,10)
        fl.write('{0},{1},{2},{3},{4},{5}'.format(i,a,b,c,a+b+c,a-b+c))
        fl.write('\n')
    fl.close()

random_data()
