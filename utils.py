import numpy as np
import pandas as pd
import pickle
from tqdm import tqdm


def create_kmer_set(X, k, kmer_set={}):
    """
    Return a set of all kmers appearing in the dataset.
    """
    len_seq = len(X[0])
    idx = len(kmer_set)
    for i in range(len(X)):
        x = X[i]
        kmer_x = [x[i:i + k] for i in range(len_seq - k + 1)]
        for kmer in kmer_x:
            if kmer not in kmer_set:
                kmer_set[kmer] = idx
                idx += 1
    return kmer_set


def m_neighbours(kmer, m, recurs=0):
    """
    Return a list of neighbours kmers (up to m mismatches).
    """
    if m == 0:
        return [kmer]

    letters = ['G', 'T', 'A', 'C']
    k = len(kmer)
    neighbours = m_neighbours(kmer, m - 1, recurs + 1)

    for j in range(len(neighbours)):
        neighbour = neighbours[j]
        for i in range(recurs, k - m + 1):
            for l in letters:
                neighbours.append(neighbour[:i] + l + neighbour[i + 1:])
    return list(set(neighbours))


def get_neighbours(kmer_set, m):
    """
    Find the neighbours given a set of kmers.
    """
    kmers_list = list(kmer_set.keys())
    kmers = np.array(list(map(list, kmers_list)))
    num_kmers, kmax = kmers.shape
    neighbours = {}
    for i in range(num_kmers):
        neighbours[kmers_list[i]] = []

    for i in tqdm(range(num_kmers)):
        kmer = kmers_list[i]
        kmer_neighbours = m_neighbours(kmer, m)
        for neighbour in kmer_neighbours:
            if neighbour in kmer_set:
                neighbours[kmer].append(neighbour)
    return neighbours


def load_neighbors(dataset, k, m):
    """
    dataset: 0, 1 or 2\\
    k: len of the kmers
    m: number of possible mismatches
    """
    file_name = 'neighbours_'+str(dataset)+'_'+str(k)+'_'+str(m)+'.p'
    # Load
    neighbours, kmer_set = pickle.load(open('saved_neighbors/'+file_name, 'rb'))
    print('Neighbors correctly loaded!')
    return neighbours, kmer_set


def load_or_compute_neighbors(dataset,k,m):
    """
    dataset: 0, 1 or 2\\
    k: len of the kmers
    m: number of possible mismatches
    """
    
    try:
        #Load the neighbors
        neighbours, kmer_set = load_neighbors(dataset, k, m)
    except:
        print('No file found, creating kmers neighbors')
        #Compute the neighbors
        file_name = 'neighbours_'+str(dataset)+'_'+str(k)+'_'+str(m)+'.p'
        if dataset==0:
            X0_train = pd.read_csv("data/Xtr0.csv", sep=",", index_col=0).values
            X0_test = pd.read_csv("data/Xte0.csv", sep=",", index_col=0).values
            kmer_set = create_kmer_set(X0_train[:,0], k, kmer_set={})
            kmer_set = create_kmer_set(X0_test[:,0], k, kmer_set)
            neighbours = get_neighbours(kmer_set, m)
            pickle.dump([neighbours, kmer_set], open('saved_neighbors/'+file_name, 'wb'))
        elif dataset==1:
            X1_train = pd.read_csv("data/Xtr1.csv", sep=",", index_col=0).values
            X1_test = pd.read_csv("data/Xte1.csv", sep=",", index_col=0).values
            kmer_set = create_kmer_set(X1_train[:,0], k, kmer_set={})
            kmer_set = create_kmer_set(X1_test[:,0], k, kmer_set)
            neighbours = get_neighbours(kmer_set, m)
            pickle.dump([neighbours, kmer_set], open('saved_neighbors/'+file_name, 'wb'))
        elif dataset==2:
            X2_train = pd.read_csv("data/Xtr2.csv", sep=",", index_col=0).values
            X2_test = pd.read_csv("data/Xte2.csv", sep=",", index_col=0).values
            kmer_set = create_kmer_set(X2_train[:,0], k, kmer_set={})
            kmer_set = create_kmer_set(X2_test[:,0], k, kmer_set)
            neighbours = get_neighbours(kmer_set, m)
            pickle.dump([neighbours, kmer_set], open('saved_neighbors/'+file_name, 'wb'))
            
    return neighbours, kmer_set