'''
Our neural net implementation on the credit-card data.
Details: 1 Hidden layer (due to UAT), Dimensionality reduction.
Authors: Dalton, Ebele, Dawei, Daniel Lee, Daniel Connelly
Class: CS545 - Fall 2019 | Professor Anthony Rhodes
'''
import numpy as np
from prepare import prepare_data
from MLP import mlp_test as mt

def main():
  # read in data
  data = np.genfromtxt('data\mnist_test.csv', delimiter=',')
  #idx_label = np.shape(data)[1] - 1 # last column
  idx_label = 0
  (train_set, valid_set, test_set) = prepare_data(data, idx_label, 3, 1, 1)
  mt.sweep_test(train_set, valid_set, test_set, 10)

if __name__=="__main__":
  main()
