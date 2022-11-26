## coding: utf-8
'''
This python file is used to split database into 80% train set and 20% test set, tranfer the original code into vector, creating input file of deap learning model.
'''

from gensim.models.word2vec import Word2Vec
import pickle
import os
import numpy as np
import random
import gc
import shutil

'''
generate_corpus function
-----------------------------
This function is used to create input of deep learning model

# Arguments
    w2vModelPath: the path saves word2vec model
    samples: the list of sample
    
'''
def generate_corpus(w2vModelPath, samples): 
    model = Word2Vec.load(w2vModelPath)
    print("begin generate input...")
    dl_corpus = [[model[word] for word in sample] for sample in samples]
    print("generate input success...")

    return dl_corpus

'''
get_dldata function
-----------------------------
This function is used to create input of deep learning model

# Arguments
    filepath: the path saves data
    dlTrainCorpusPath: the path saves train dataset
    dlTestCorpusPath: the path saves test dataset
    split: split ratio
    seed: random number seed 
    
'''
def get_dldata(filepath, dlTrainCorpusPath, dlTestCorpusPath, split=0.8, seed=113):
    folders = os.listdir(filepath)
    np.random.seed(seed)
    np.random.shuffle(folders)

    folders_train = folders[:int(len(folders)*split)]
    folders_test = folders[int(len(folders)*split):]
      
    for mode in ["api", "arraysuse", "pointersuse", "integeroverflow"]:
        if mode == "api":
            N = 4
            num = [0,1,2,3,4]
        if mode == "arraysuse":
            N = 2
            num = [0,1]
        if mode == "integeroverflow":
            N = 2
            num = [0,1]
        if mode == "pointersuse":
            N =6
            num = [0,1,2,3,4,5]
        for i in num:
            train_set = [[], [], [], [], [], []]
            ids = []
            for folder_train in folders_train[int(i*len(folders_train)/N) : int((i+1)*len(folders_train)/N)]:
                for filename in os.listdir(os.path.join(filepath, folder_train)):
                    if mode in filename:
                        if folder_train not in os.listdir(dlTrainCorpusPath):   
                            folder_path = os.path.join(dlTrainCorpusPath, folder_train)
                            os.mkdir(folder_path)
                        shutil.copyfile(os.path.join(filepath, folder_train, filename), os.path.join(dlTrainCorpusPath, folder_train, filename))
                        f = open(os.path.join(filepath, folder_train, filename), 'rb')
                        data = pickle.load(f)
                        id_length = len(data[1])
                        for j in range(id_length):
                            ids.append(folder_train)
                        for n in range(5):
                            train_set[n] = train_set[n] + data[n]
                        train_set[-1] = ids
            if train_set[0] == []:
                continue
            f_train = open(dlTrainCorpusPath + mode + "_" + str(i)+ "_.pkl", 'wb')
            pickle.dump(train_set, f_train, protocol=pickle.HIGHEST_PROTOCOL)
            f_train.close()
            del train_set
            gc.collect()     
                    
    for mode in ["api", "arraysuse", "pointersuse", "integeroverflow"]:
        N = 4
        num = [0,1,2,3]
        if mode == "pointersuse":
            N = 8
            num = [4,5]
        for i in num:
            test_set = [[], [], [], [], [], []]
            ids = []
            for folder_test in folders_test[int(i*len(folders_test)/N) : int((i+1)*len(folders_test)/N)]:
                for filename in os.listdir(os.path.join(filepath, folder_test)):
                    if mode in filename:
                        if folder_test not in os.listdir(dlTestCorpusPath):
                            folder_path = os.path.join(dlTestCorpusPath, folder_test)
                            os.mkdir(folder_path)
                        shutil.copyfile(os.path.join(filepath, folder_test, filename), os.path.join(dlTestCorpusPath, folder_test, filename))
                        f = open(os.path.join(filepath, folder_test, filename), 'rb')
                        data = pickle.load(f)
                        id_length = len(data[1])
                        for j in range(id_length):
                            ids.append(folder_test)
                        for n in range(5):
                            test_set[n] = test_set[n] + data[n]
                        test_set[-1] = ids
            if test_set[0] == []:
                continue
            f_test = open(dlTestCorpusPath + mode + "_" + str(i)+ ".pkl", 'wb')
            pickle.dump(test_set, f_test, protocol=pickle.HIGHEST_PROTOCOL)
            f_test.close()
            del test_set
            gc.collect()

if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from Implementation.ProjectDir import CORPUS_DIR, W2V_MODEL_PATH, VECTOR_DIR, CORPUS_TRAINSET_DIR, CORPUS_TESTSET_DIR

    # CORPUS_DIR = "./data/cdg_ddg/corpus/"
    # VECTOR_DIR = "./data/cdg_ddg/vector/"
    # W2V_MODEL_PATH = "./w2v_model/wordmodel3"
    print("turn the corpus into vectors...")
    for corpusfiles in os.listdir(CORPUS_DIR):
        print(corpusfiles)
        if corpusfiles not in os.listdir(VECTOR_DIR): 
            folder_path = os.path.join(VECTOR_DIR, corpusfiles)
            os.mkdir(folder_path)
        for corpusfile in os.listdir(os.path.join(CORPUS_DIR, corpusfiles)):
            corpus_path = os.path.join(CORPUS_DIR, corpusfiles, corpusfile)
            f_corpus = open(corpus_path, 'rb')
            data = pickle.load(f_corpus)
            f_corpus.close()
            data[0] = generate_corpus(W2V_MODEL_PATH, data[0])
            vector_path = os.path.join(VECTOR_DIR, corpusfiles, corpusfile)
            f_vector = open(vector_path, 'wb')
            pickle.dump(data, f_vector, protocol=pickle.HIGHEST_PROTOCOL)
            f_vector.close()
    print("w2v over...")

    print("spliting the train set and test set...")
    # dlTrainCorpusPath = "./dl_input/cdg_ddg/train/"
    # dlTestCorpusPath = "./dl_input/cdg_ddg/test/"
    get_dldata(VECTOR_DIR, CORPUS_TRAINSET_DIR, CORPUS_TESTSET_DIR)
    
    print("success!")
