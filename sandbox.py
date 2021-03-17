"""
Sandbox file to try things messily 
"""

# %% Imports
import numpy as np
import pandas as pd
from sklearn.kernel_ridge import KernelRidge
from sklearn.svm import SVC

from kernels import LinearKernel, GaussianKernel, PolynomialKernel, SpectrumKernel, MismatchKernel

from classifiers.logistic_regression import LogisticRegression
from classifiers.ridge_regression import RidgeRegression
from classifiers.svm import SVM

# %% Read csv files
# shape (2000,1): string
X0_train = pd.read_csv("data/Xtr0.csv", sep=",", index_col=0).values
X1_train = pd.read_csv("data/Xtr1.csv", sep=",", index_col=0).values
X2_train = pd.read_csv("data/Xtr2.csv", sep=",", index_col=0).values

# shape (2000,100): float
X0_mat100_train = pd.read_csv("data/Xtr0_mat100.csv", sep=" ", header=None).values
X1_mat100_train = pd.read_csv("data/Xtr1_mat100.csv", sep=" ", header=None).values
X2_mat100_train = pd.read_csv("data/Xtr2_mat100.csv", sep=" ", header=None).values

# shape (2000,1): string
X0_test = pd.read_csv("data/Xte0.csv", sep=",", index_col=0).values
X1_test = pd.read_csv("data/Xte1.csv", sep=",", index_col=0).values
X2_test = pd.read_csv("data/Xte2.csv", sep=",", index_col=0).values

# shape (2000,100): float
X0_mat100_test = pd.read_csv("data/Xte0_mat100.csv", sep=" ", header=None).values
X1_mat100_test = pd.read_csv("data/Xte1_mat100.csv", sep=" ", header=None).values
X2_mat100_test = pd.read_csv("data/Xte2_mat100.csv", sep=" ", header=None).values

# shape (2000,1): 0 or 1
Y0_train = pd.read_csv("data/Ytr0.csv", sep=",", index_col=0).values
Y1_train = pd.read_csv("data/Ytr1.csv", sep=",", index_col=0).values
Y2_train = pd.read_csv("data/Ytr2.csv", sep=",", index_col=0).values


"""
# %%
kernel = LinearKernel()
ridge = RidgeRegression(kernel=kernel, alpha=0.01)
ridge.fit(X0_mat100_train, Y0_train)
# %%
ridge.predict(X0_mat100_train)

# KRR with sklearn
# ridge = KernelRidge(alpha=0.001, kernel='linear')
# ridge.fit(X0_mat100_train, Y0_train2)
# ridge.predict(X0_mat100_train)

# Kernel logistic regression
# logreg = LogisticRegression(kernel=kernel, lambda_=0.01)
# Y0_train_scaled = np.where(Y0_train == 0, -1, 1)
# logreg.fit(X0_mat100_train, Y0_train)
# logreg.predict(X0_mat100_train)

"""

## Preprocessing

fraction_of_data = 0.2 #Put a small value for faster tests
split_ratio = 0.8 #Ratio of data in train set
shuffle = True #Shuffle the data
rescale_y = True #Rescale labels to -1 and 1

#Stack the data
X_mat_train_full = np.vstack((X0_mat100_train,X1_mat100_train,X2_mat100_train))
X_train_full = np.vstack((X0_train,X1_train,X2_train))
Y_train_full = np.vstack((Y0_train,Y1_train,Y2_train))

if rescale_y:
    Y_train_full = np.where(Y_train_full == 0, -1, 1)

#Shuffle the data
if shuffle:
    shuffling = np.random.permutation(len(X_mat_train_full))
    X_mat_train_full = X_mat_train_full[shuffling]
    X_train_full = X_train_full[shuffling]
    Y_train_full = Y_train_full[shuffling]

#Take a fraction of the data
nb_samples = int(fraction_of_data*len(X_mat_train_full))
X_mat_train_full = X_mat_train_full[:nb_samples]
X_train_full = X_train_full[:nb_samples]
Y_train_full = Y_train_full[:nb_samples]

#Split the data into train and val
nb_in_train = int(split_ratio*len(X_mat_train_full))
X_mat_train,X_mat_val = X_mat_train_full[:nb_in_train],X_mat_train_full[nb_in_train:]
X_train,X_val = X_train_full[:nb_in_train],X_train_full[nb_in_train:]
Y_train,Y_val = Y_train_full[:nb_in_train],Y_train_full[nb_in_train:]


print("Real classes distribution:")
print(len(Y_train_full), "samples")
print(np.sum(Y_train_full== 1), "positive")
print(np.sum(Y_train_full==-1), "negative")
print()

print("Training classes distribution:")
print(len(Y_train), "samples")
print(np.sum(Y_train== 1), "positive")
print(np.sum(Y_train==-1), "negative")
print()

print("Validation classes distribution:")
print(len(Y_val), "samples")
print(np.sum(Y_val== 1), "positive")
print(np.sum(Y_val==-1), "negative")
print()

compare_both_svms = False
test_scikit_svm = False
test_our_svm = False
grid_search_SVM = False
test_spectrum = True
test_mismatch = False


if compare_both_svms:

    ## Compare the results of SKlearn SVM and ours

    #Parameters
    kernel = 'poly' # 'linear' 'rbf' or 'poly'
    C = 1.0
    gamma = 1/(X_mat_train.shape[1] * X_mat_train.var())
    coef0 = 1.0
    degree = 3

    print("Kernel:", kernel)
    print("C:", C)
    if kernel != 'linear':
        print("Gamma:", gamma)
    if kernel == 'poly':
        print("Coef0:", coef0)
        print("Degree:", degree)
    print()

    #Sklearn SVM
    print("Applying Sklearn SVM...")
    svm_scikit = SVC(C=C,kernel=kernel,gamma=gamma,coef0=coef0,degree=degree)
    svm_scikit.fit(X_mat_train, np.squeeze(Y_train))
    svm_scikit_classes_train = svm_scikit.predict(X_mat_train)
    svm_scikit_classes_val = svm_scikit.predict(X_mat_val)

    print("Accuracy on train (sklearn SVM):", np.sum(svm_scikit_classes_train==np.squeeze(Y_train))/len(Y_train))
    print("Accuracy on val (sklearn SVM):", np.sum(svm_scikit_classes_val==np.squeeze(Y_val))/len(Y_val))
    print()

    #Our SVM
    print("Applying our SVM...")
    if kernel=='linear':
        our_svm = SVM(kernel=LinearKernel(),C=C)
    elif kernel=='rbf':
        our_svm = SVM(kernel=GaussianKernel(sigma=np.sqrt(0.5/gamma),normalize=False),C=C)
    elif kernel=='poly':
        our_svm = SVM(kernel=PolynomialKernel(gamma=gamma,coef0=coef0,degree=degree),C=C)
    our_svm.fit(X_mat_train, Y_train)
    our_svm_classes_train = our_svm.predict_classes(X_mat_train)
    our_svm_classes_val = our_svm.predict_classes(X_mat_val)

    print("Accuracy on train (our SVM):", np.sum(np.squeeze(our_svm_classes_train)==np.squeeze(Y_train))/len(Y_train))    
    print("Accuracy on val (our SVM):", np.sum(np.squeeze(our_svm_classes_val)==np.squeeze(Y_val))/len(Y_val))
    print()

    #Comparison
    print("Similarity on train between sklearn SVM and our SVM:",np.sum(np.squeeze(our_svm_classes_train)==np.squeeze(svm_scikit_classes_train))/len(Y_train))
    print("Similarity on val between sklearn SVM and our SVM:",np.sum(np.squeeze(our_svm_classes_val)==np.squeeze(svm_scikit_classes_val))/len(Y_val))
    print()


if test_scikit_svm:

    ## Test SKLearn SVM

    #Parameters
    kernel = 'poly' # 'linear' 'rbf' or 'poly'
    C = 1.0
    gamma = 1/(X_mat_train.shape[1] * X_mat_train.var())
    coef0 = 1.0
    degree = 3

    print("Kernel:", kernel)
    print("C:", C)
    if kernel != 'linear':
        print("Gamma:", gamma)
    if kernel == 'poly':
        print("Coef0:", coef0)
        print("Degree:", degree)
    print()

    #Sklearn SVM
    print("Applying Sklearn SVM...")
    svm_scikit = SVC(C=C,kernel=kernel,gamma=gamma,coef0=coef0,degree=degree)
    svm_scikit.fit(X_mat_train, np.squeeze(Y_train))
    svm_scikit_classes_train = svm_scikit.predict(X_mat_train)
    svm_scikit_classes_val = svm_scikit.predict(X_mat_val)

    print("Accuracy on train (sklearn SVM):", np.sum(svm_scikit_classes_train==np.squeeze(Y_train))/len(Y_train))
    print("Accuracy on val (sklearn SVM):", np.sum(svm_scikit_classes_val==np.squeeze(Y_val))/len(Y_val))

if test_our_svm:

    ## Test our SVM implementation

    #Parameters
    kernel = 'poly' # 'linear' 'rbf' or 'poly'
    C = 1.0
    gamma = 1/(X_mat_train.shape[1] * X_mat_train.var())
    coef0 = 1.0
    degree = 3

    print("Kernel:", kernel)
    print("C:", C)
    if kernel != 'linear':
        print("Gamma:", gamma)
    if kernel == 'poly':
        print("Coef0:", coef0)
        print("Degree:", degree)
    print()

    #Our SVM
    print("Applying our SVM...")
    if kernel=='linear':
        our_svm = SVM(kernel=LinearKernel(),C=C)
    elif kernel=='rbf':
        our_svm = SVM(kernel=GaussianKernel(sigma=np.sqrt(0.5/gamma),normalize=False),C=C)
    elif kernel=='poly':
        our_svm = SVM(kernel=PolynomialKernel(gamma=gamma,coef0=coef0,degree=degree),C=C)
    our_svm.fit(X_mat_train, Y_train)
    our_svm_classes_train = our_svm.predict_classes(X_mat_train)
    our_svm_classes_val = our_svm.predict_classes(X_mat_val)

    print("Accuracy on train (our SVM):", np.sum(np.squeeze(our_svm_classes_train)==np.squeeze(Y_train))/len(Y_train))    
    print("Accuracy on val (our SVM):", np.sum(np.squeeze(our_svm_classes_val)==np.squeeze(Y_val))/len(Y_val))



if grid_search_SVM:

    ## Grid search to find the best parameters for the SVM, using the SKLearn implementation

    max_val_acc = 0
    max_C = 0
    max_gamma = 0

    kernels = ['linear','rbf','poly']
    Cs = [10**i for i in range(-2,4)]
    gammas = [10**i for i in range(0,4)]
    coef0s = [1.0]
    degrees = [2,3,4,5]

    for kernel in kernels:
        for C in Cs:
            for gamma in gammas:
                for coef0 in coef0s:
                    for degree in degrees:

                        print("Kernel:", kernel)
                        print("C:", C)
                        if kernel != 'linear':
                            print("Gamma:", gamma)
                        if kernel == 'poly':
                            print("Coef0:", coef0)
                            print("Degree:", degree)
                        print()

                        try:

                            #Sklearn SVM
                            print("Applying Sklearn SVM...")
                            svm_scikit = SVC(C=C,kernel=kernel,gamma=gamma,coef0=coef0,degree=degree)
                            svm_scikit.fit(X_mat_train, np.squeeze(Y_train))
                            svm_scikit_classes_train = svm_scikit.predict(X_mat_train)
                            svm_scikit_classes_val = svm_scikit.predict(X_mat_val)

                            acc_train = np.sum(svm_scikit_classes_train==np.squeeze(Y_train))/len(Y_train)
                            acc_val = np.sum(svm_scikit_classes_val==np.squeeze(Y_val))/len(Y_val)

                            print("Accuracy on train (sklearn SVM):", acc_train)
                            print("Accuracy on val (sklearn SVM):", acc_val)
                            print()

                            if acc_val > max_val_acc:
                                max_val_acc = acc_val
                                max_C = C
                                max_gamma = gamma
                                max_kernel = kernel
                                max_degree = degree
                                max_coef0 = coef0
                        
                        except:
                            print("Error when applying SVM. Resume with next parameters...")
                            print()

                        if kernel!='poly':
                            break
                    if kernel!='poly':
                        break
                if kernel == 'linear':
                    break

    print("Best val acc:",max_val_acc)
    print("Best kernel:",kernel)
    print("Best C:",max_C)
    print("Best gamma:", max_gamma)
    print("Best degree:", max_degree)
    print("Best coef0:", max_coef0)


if test_spectrum:

    ## First tests using the spectrum kernel (does not work for the moment)

    #Parameters
    C = 1.0
    k = 12

    print("Kernel: Spectrum")
    print("C:", C)
    print("K:", k)
    print()

    #Our SVM
    print("Applying our SVM...")

    our_svm = SVM(kernel=SpectrumKernel(k=k),C=C)

    our_svm.fit(X_train[:,0], Y_train)
    our_svm_classes_train = our_svm.predict_classes(X_train[:,0])
    our_svm_classes_val = our_svm.predict_classes(X_val[:,0])

    print("Accuracy on train (our SVM):", np.sum(np.squeeze(our_svm_classes_train)==np.squeeze(Y_train))/len(Y_train))    
    print("Accuracy on val (our SVM):", np.sum(np.squeeze(our_svm_classes_val)==np.squeeze(Y_val))/len(Y_val))


if test_mismatch:

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

        for i in range(num_kmers):
            kmer = kmers_list[i]
            kmer_neighbours = m_neighbours(kmer, m)
            for neighbour in kmer_neighbours:
                if neighbour in kmer_set:
                    neighbours[kmer].append(neighbour)
        return neighbours


    def embed_data(X, neighbours, kmer_set):
        """
        Embed data.
        """
        X_emb = [{} for i in range(len(X))]
        for i in range(len(X)):
            x = X[i]
            kmer_x = [x[j:j + k] for j in range(len(X[0]) - k + 1)]
            for kmer in kmer_x:
                neigh_kmer = neighbours[kmer]
                for neigh in neigh_kmer:
                    idx_neigh = kmer_set[neigh]
                    if idx_neigh in X_emb[i]:
                        X_emb[i][idx_neigh] += 1
                    else:
                        X_emb[i][idx_neigh] = 1
        return X_emb

    k = 12
    m = 2

    kmer_set = create_kmer_set(X0_train[:,0], k)
    # kmer_set = create_kmer_set(X1_train[:,0], k, kmer_set)
    # kmer_set = create_kmer_set(X2_train[:,0], k, kmer_set)

    neighbours = get_neighbours(kmer_set, m)

    X_emb = embed_data(X, neighbours, kmer_set)

    mismatch_kernel = MismatchKernel(k, m)

    G = mismatch_kernel.gram(np.array(X_emb))