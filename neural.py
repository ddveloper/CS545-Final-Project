'''
Our neural net implementation on the credit-card data.
Details: 1 Hidden layer (due to UAT), Dimensionality reduction.
Authors: Dalton, Ebele, Dawei, Daniel Lee, Daniel Connelly
Class: CS545 - Fall 2019 | Professor Anthony Rhodes
'''
import numpy as np

def normalize_data(data):
  ''' normalize data for training
      method: ( data - mean ) / std
      in: np array of training inputs
      out: np array of normalized inputs 
  '''
  means = np.mean(data, axis=0) # mean, col-wise
  stds = np.std(data, axis=0) # std
  dim = np.shape(means)[0]
  ret = data - np.transpose(means).reshape(1, dim)
  ret = ret / np.transpose(stds).reshape(1, dim)
  return ret

def alter_labels(data, idx_label):
  ''' in-place rearrange data so labels altering evenly
      in: np array with all raw dataset
      out: none
  '''
  labels = data[:, [idx_label]]
  unique, counts = np.unique(labels, return_counts=True)
  cnt_labels = dict(zip(unique, counts))
  # labels 0:1 = 23364:6636 = 3.52:1 ~= 3.5:1 = 7:2
  p1, p2 = 0, 0
  length = np.shape(data)[0]
  while p1 < length and p2 < length:
    target = 1 if p1%9 == 3 or p1%9 == 8 else 0
    if data[p1, idx_label] != target:
      p2 = p1 + 1
      while p2 < length and data[p2, idx_label] != target:
        p2 += 1
      if p2 < length and data[p2, idx_label] == target:
        data[[p1, p2]] = data[[p2, p1]] # swap them
    p1 += 1
  labels = data[:, [idx_label]]
  # move dirty distrubution top, so training set will use them
  np.flip(data, axis=0)

def prepare_data(data, idx_label):
  ''' preprocess data for training
      in: np array with all raw dataset
      out: inputs, labels as np arrays
  '''
  alter_labels(data, idx_label) # rearrange data for later splitting
  labels = data[:, [idx_label]]
  raw_examples = np.delete(data, idx_label, axis=1)
  examples = normalize_data(raw_examples)
  return (labels, examples)

def split_indexes(n_train, n_validate, n_test, row_total):
  ''' calculate where to split
  '''
  i0 = n_train / (n_train + n_validate + n_test) * row_total
  i1 = (n_train + n_validate) / (n_train + n_validate + n_test) * row_total
  return (int(i0), int(i1))


def main():
  # read in data
  raw_data = np.genfromtxt('data\data.csv', delimiter=',')
  # preprocessing, normalization, etc.
  (labels, examples) = prepare_data(raw_data, np.shape(raw_data)[1] - 1)
  # split
  (i0, i1) = split_indexes(3, 1, 1, np.shape(examples)[0])
  train_set = (examples[:i0], labels[0:i0])
  valid_set = (examples[i0:i1], labels[i0:i1])
  test_set = (examples[i1:], labels[i1:])

  # train the model

  pass



  
if __name__=="__main__":
  main()
