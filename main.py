from brute import *
from index import *
import time
import os

if __name__ == '__main__':
    for n in [100,200,500,1000,2000,5000,10000]:
        print 'Brute N = %d' % n
        t = time.time()
        brute = Brute(n)
        os.remove('./brute.top')
        print '------------------------ %f' % (time.time() - t)

    for n in [100,200,500,1000,2000,5000,10000]:
        print 'Index N = %d' % n
        t = time.time()
        index =  Index(n)
        os.remove('./index.top')
        print '------------------------ %f' % (time.time() - t)

    

