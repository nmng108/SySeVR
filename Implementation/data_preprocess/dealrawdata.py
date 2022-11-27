## coding: utf-8
'''
This python file is used to train data in CNN model
'''

from __future__ import absolute_import
from __future__ import print_function
import pickle
# import _Pickle as cPickle
import numpy as np
import random
import time
import math
import os
from collections import Counter
# from imblearn.ensemble import BalanceCascade
from imblearn.over_sampling import ADASYN
from imblearn.over_sampling import SMOTE


np.random.seed(1337)  # for reproducibility

'''
dealrawdata function
-----------------------------
This function is used to cut the dataset, do shuffle and save into pkl file.

# Arguments
    raw_traindataSet_path: String type, the raw data path of train set
    raw_testdataSet_path: String type, the raw data path of test set
    traindataSet_path: String type, the data path to save train set
    testdataSet_path: String type, the data path to save test set
    batch_size: Int type, the mini-batch size
    maxlen: Int type, the max length of data
    vector_dim: Int type, the number of data vector's dim

'''
def dealrawdata(raw_traindataSet_path, raw_testdataSet_path, traindataSet_path, testdataSet_path, 
                batch_size, maxlen, vector_dim):
    print("Loading data...")
    
    for root_folder in os.listdir(raw_traindataSet_path):
        abs_folder_name = os.path.join(raw_traindataSet_path, root_folder)
        
        for filename in os.listdir(abs_folder_name):
            if not (filename.endswith(".pkl")):
                print(filename)
                continue
            print(filename)
            X_train, train_labels, funcs, filenames, testcases = load_data_binary(os.path.join(abs_folder_name, filename), 
                                                                                batch_size, maxlen=maxlen, vector_dim=vector_dim)

            target_folder_path = os.path.join(traindataSet_path, root_folder)
            if not os.path.exists(target_folder_path):
                os.mkdir(target_folder_path)
                
            f_train = open(os.path.join(target_folder_path, filename), 'wb')
            pickle.dump([X_train, train_labels, funcs, filenames, testcases], f_train)
            f_train.close()


    for root_folder in os.listdir(raw_testdataSet_path):
        abs_folder_name = os.path.join(raw_testdataSet_path, root_folder)
        
        for filename in os.listdir(abs_folder_name):
            if not ("api" in filename):
                continue
            if not (filename.endswith(".pkl")):
                print(filename)
                continue
            print(filename)
            X_test, test_labels, funcs, filenames, testcases = load_data_binary(os.path.join(abs_folder_name, filename), 
                                                                                batch_size, maxlen=maxlen, vector_dim=vector_dim)

            target_folder_path = os.path.join(testdataSet_path, root_folder)
            if not os.path.exists(target_folder_path):
                os.mkdir(target_folder_path)
                
            f_test = open(os.path.join(target_folder_path, filename), 'wb')
            pickle.dump([X_test, test_labels, funcs, filenames, testcases], f_test)
            f_test.close()


def load_data_binary(dataSetpath, batch_size, maxlen=None, vector_dim=40, seed=113):   
    #load data
    f1 = open(dataSetpath, 'rb')
    # print(pickle.load(f1))
    X, ids, focus, funcs, paths = pickle.load(f1)
    f1.close()
    
    filenames = test_cases = ''
    if len(paths) == 2:
        filenames, test_cases = paths
	
    cut_count = 0
    fill_0_count = 0
    no_change_count = 0
    fill_0 = [0]*vector_dim
    totallen = 0
    if maxlen:
        new_X = []
        for x, i, focu, func, file_name, test_case in zip(X, ids, focus, funcs, filenames, test_cases):
            if len(x) <  maxlen:
                x = x + [fill_0] * (maxlen - len(x))
                new_X.append(x)
                fill_0_count += 1

            elif len(x) == maxlen:
                new_X.append(x)
                no_change_count += 1
                    
            else:
                startpoint = int(focu - round(maxlen / 2.0))
                endpoint =  int(startpoint + maxlen)
                if startpoint < 0:
                    startpoint = 0
                    endpoint = maxlen
                if endpoint >= len(x):
                    startpoint = -maxlen
                    endpoint = None
                new_X.append(x[startpoint:endpoint])
                cut_count += 1
            totallen = totallen + len(x)
    X = new_X
    print(totallen)

    return X, ids, funcs, filenames, test_cases
    # return None, None, None, None, None


if __name__ == "__main__":
    batchSize = 32
    vectorDim = 40
    maxLen = 500
    
    import sys
    sys.path.append('..')
    from Implementation.ProjectDir import CORPUS_TRAINSET_DIR, CORPUS_TESTSET_DIR, MAIN_TRAINSET_DIR, MAIN_TESTSET_DIR

    # raw_traindataSetPath = "./dl_input/cdg_ddg/train/"
    # raw_testdataSetPath = "./dl_input/cdg_ddg/test/"
    # traindataSetPath = "./dl_input_shuffle/cdg_ddg/train/"
    # testdataSetPath = "./dl_input_shuffle/cdg_ddg/test/"
    dealrawdata(CORPUS_TRAINSET_DIR, CORPUS_TESTSET_DIR, MAIN_TRAINSET_DIR, MAIN_TESTSET_DIR, batchSize, maxLen, vectorDim)
