# FILE = './brute.top'
FILE = './index.top'
METRIC_FILE = './pairs.ref'

if __name__ == '__main__':
    metric = [0 for i in range(1001)]
    predicted = [0 for i in range(1001)]

    with open(METRIC_FILE) as f:
        for line in f:
            temp = line.strip().split()
            id_1 = int(temp[0])
            id_2 = int(temp[1])

            metric[id_1] = id_2
    
    with open(FILE) as f:
        for line in f:
            temp = line.strip().split()
            id_1 = int(temp[0])
            id_2 = int(temp[1])

            predicted[id_1] = id_2

    # compare
    error_count = 0
    for i in range(100):
        if metric[i] != predicted[i]:
            error_count += 1
            print '%d - %d - %d' % (i, metric[i], predicted[i])

    print "Error_count %d" % error_count


