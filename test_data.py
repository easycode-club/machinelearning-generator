import random
fl = open('data.csv','w+')
fl.write('0,1,2,3,4,5')
fl.write('\n')
for i in range(100):
    a = random.randint(0,10)
    b = random.randint(0,10)
    c = random.randint(0,10)
    fl.write('{0},{1},{2},{3},{4},{5}'.format(i,a,b,c,a+b+c,a-b+c))
    fl.write('\n')
fl.close()
