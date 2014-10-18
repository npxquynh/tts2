import time

if __name__ == '__main__':
    t = time.time()
    with open('./test', 'w') as output:
        for i in range(10000):
            output.write('%d\n' % i)

    print "Write 1 time: %f" % (time.time() - t)
    
    t = time.time()
    for i in range(10000):
        with open('./test', 'a') as output:
            output.write('%d\n' % i)

    print "Write file 10000 times: %f" % (time.time() - t)

