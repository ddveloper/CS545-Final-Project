import numpy as np
from . import mlp

def get_train_data(train_set, train_size):
    length = int(np.shape(train_set[0])[0] * train_size)
    return (np.array(train_set[0][:length]), np.array(train_set[1][:length]))

def plotResults(trainResults, testResults):
    print(" results - train [{0}], test[{1}]".format(trainResults, testResults))

def shuffle_sets(data_set, cnt_out):
    combo = np.concatenate((data_set[0], data_set[1]), axis=1)
    np.random.shuffle(combo)
    length = np.shape(combo)[1] - cnt_out
    return (combo[:,:length], combo[:,length:])

def expand_labels(data_set, cnt_out):
    cnt_data = np.shape(data_set[1])[0]
    exp_labels = np.full((cnt_data, cnt_out), 0.1) # false = 0.1
    for i in range(cnt_data):
        exp_labels[i][int(data_set[1][i])] = 0.9 # true = 0.9
    return (data_set[0], exp_labels)

def train_test(train_set, valid_set, test_set, param, cnt_class):
    (eta, momentum, hidden_nodes, train_size, max_epoch, batch_size) = param
    train_data = get_train_data(train_set, train_size)

    cnt_out = cnt_class # output classes
    train_data = expand_labels(train_data, cnt_out)
    #valid_set = expand_labels(valid_set, cnt_out)
    test_set = expand_labels(test_set, cnt_out)

    model = mlp.mlp(np.shape(train_data[0])[1], hidden_nodes, cnt_out) # init model
    (a01, confu01) = model.test(train_data[0], train_data[1], cnt_out) # init result train
    (a02, confu02) = model.test(train_data[0], train_data[1], cnt_out) # init result test
    print(" initial accuracy: (train {0:.2f}, test {1:.2f})".format(a01, a02))
    for i in range(max_epoch):
        print(" --- --- epoch {0}: (mom-{1}, nH-{2}, tSize-{3})".format(i, momentum, hidden_nodes, train_size))
        train_data = shuffle_sets(train_data, cnt_out) # shuffle
        model.train(train_data[0], train_data[1], eta, momentum, batch_size) # train
        (a1, confu1) = model.test(train_data[0], train_data[1], cnt_out) # run train dataset
        (a2, confu2) = model.test(test_set[0], test_set[1], cnt_out) # run test set
        print(" accuracy: (train {0:.2f}, test {1:.2f})".format(a1, a2))

def sweep_test(train_set, valid_set, test_set, cnt_class):
    # parameters array: eta, momentum, hidden_nodes, train_size, max_epoch, batch_size
    params_arr = [
        # (0.1,   0.9,   1,    1.0,   50,   100), # hidden nodes 1, 5, 10
        # (0.1,   0.9,   5,    1.0,   50,   100),
        # (0.1,   0.9,   10,   1.0,   50,   100),
        # (0.1,   0,     10,   1.0,   50,   100), # momentum 0, 0.25, 0.5
        # (0.1,   0.25,  10,   1.0,   50,   100),
         (0.1,   0.5,   10,   1.0,   50,   100),
        # (0.1,   0.9,   10,   0.25,  50,   100), # train size 0.25, 0.5
        # (0.1,   0.9,   10,   0.5,   50,   100)
    ]

    for param in params_arr:
        train_test(train_set, valid_set, test_set, param, cnt_class)
