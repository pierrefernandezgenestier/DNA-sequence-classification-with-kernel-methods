## IMPORTS ##

import numpy as np
import pandas as pd
from tqdm import tqdm

from kernels import LinearKernel, GaussianKernel, PolynomialKernel, SpectrumKernel, MismatchKernel
from classifiers.svm import SVM

## PARAMETERS ##

kernel = 'rbf' # 'linear' 'rbf' or 'poly' #TODO: Add support for spectrum and mismatch
C = 10.0 #Parameter C for SVM
gamma = 10.0 #Parameter gamma for SVM (only for 'rbf' or 'poly')
coef0 = 1.0 #Parameter coef0 for SVM (only for 'poly')
degree = 3 #Parameter degree for SVM (only for 'poly')

shuffle = True #Shuffle the data
rescale_y = True #Rescale labels to -1 and 1
k_fold = 5 #Number of folds for cross_validation

cross_validate_0 = True #Choose to cross_validate on dataset 0 or not
cross_validate_1 = True #Choose to cross_validate on dataset 1 or not
cross_validate_2 = True #Choose to cross_validate on dataset 2 or not

## LOAD DATA ##

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


## PREPROCESS DATA ##

#Rescaling labels
Y0_train = np.where(Y0_train == 0, -1, 1)
Y1_train = np.where(Y1_train == 0, -1, 1)
Y2_train = np.where(Y2_train == 0, -1, 1)


#Shuffling
if shuffle:

    shuffling_0 = np.random.permutation(len(X0_mat100_train))
    X0_train = X0_train[shuffling_0]
    X0_mat100_train = X0_mat100_train[shuffling_0]
    Y0_train = Y0_train[shuffling_0]

    shuffling_1 = np.random.permutation(len(X1_mat100_train))
    X1_train = X1_train[shuffling_1]
    X1_mat100_train = X1_mat100_train[shuffling_1]
    Y1_train = Y1_train[shuffling_1]

    shuffling_2 = np.random.permutation(len(X2_mat100_train))
    X2_train = X2_train[shuffling_2]
    X2_mat100_train = X2_mat100_train[shuffling_2]
    Y2_train = Y2_train[shuffling_2]


print("Kernel:", kernel)
print("C:", C)
if kernel == 'rbf' or kernel == 'poly':
    print("Gamma:", gamma)
if kernel == 'poly':
    print("Coef0:", coef0)
    print("Degree:", degree)
print()


## CROSS-VALIDATE ON DATASET 0 ##

if cross_validate_0:

    print("Cross-validating on dataset 0...")

    val_accs_0 = []

    split = np.linspace(0,len(X0_mat100_train),num=k_fold+1).astype(int)
    #print(split)

    for i in range(k_fold):

        print("Doing fold", i+1,"...")
        print()

        frac_val = 1.0/k_fold

        indices_val = np.arange(len(X0_mat100_train))[split[i]:split[i+1]]
        indices_train = np.concatenate([np.arange(len(X0_mat100_train))[0:split[i]],np.arange(len(X0_mat100_train))[split[i+1]:]]) 

        X0_mat100_train_,X0_mat100_val_ = X0_mat100_train[indices_train],X0_mat100_train[indices_val]
        Y0_train_,Y0_val_ = Y0_train[indices_train],Y0_train[indices_val]

        print('Doing SVM')

        if kernel=='linear':
            svm = SVM(kernel=LinearKernel(),C=C)
        elif kernel=='rbf':
            svm = SVM(kernel=GaussianKernel(sigma=np.sqrt(0.5/gamma),normalize=False),C=C)
        elif kernel=='poly':
            svm = SVM(kernel=PolynomialKernel(gamma=gamma,coef0=coef0,degree=degree),C=C)

        svm.fit(X0_mat100_train_, Y0_train_)

        pred_train = svm.predict_classes(X0_mat100_train_)
        print("Accuracy on train:", np.sum(np.squeeze(pred_train)==np.squeeze(Y0_train_)) / len(Y0_train_))

        pred_val = svm.predict_classes(X0_mat100_val_)
        val_acc = np.sum(np.squeeze(pred_val)==np.squeeze(Y0_val_)) / len(Y0_val_)
        print("Accuracy on val:", val_acc)

        val_accs_0.append(val_acc.copy())

    print(val_accs_0)
    print("Mean accuracy on val over the k folds (dataset 0):", np.mean(val_accs_0))


## Dataset 1 ##


if cross_validate_1:

    print("Cross-validating on dataset 1...")

    val_accs_1 = []

    split = np.linspace(0,len(X1_mat100_train),num=k_fold+1).astype(int)
    #print(split)

    for i in range(k_fold):

        print("Doing fold", i+1,"...")
        print()

        frac_val = 1.0/k_fold

        indices_val = np.arange(len(X1_mat100_train))[split[i]:split[i+1]]
        indices_train = np.concatenate([np.arange(len(X1_mat100_train))[0:split[i]],np.arange(len(X1_mat100_train))[split[i+1]:]]) 

        X1_mat100_train_,X1_mat100_val_ = X1_mat100_train[indices_train],X1_mat100_train[indices_val]
        Y1_train_,Y1_val_ = Y1_train[indices_train],Y1_train[indices_val]

        print('Doing SVM')

        if kernel=='linear':
            svm = SVM(kernel=LinearKernel(),C=C)
        elif kernel=='rbf':
            svm = SVM(kernel=GaussianKernel(sigma=np.sqrt(0.5/gamma),normalize=False),C=C)
        elif kernel=='poly':
            svm = SVM(kernel=PolynomialKernel(gamma=gamma,coef0=coef0,degree=degree),C=C)

        svm.fit(X1_mat100_train_, Y1_train_)

        pred_train = svm.predict_classes(X1_mat100_train_)
        print("Accuracy on train:", np.sum(np.squeeze(pred_train)==np.squeeze(Y1_train_)) / len(Y1_train_))

        pred_val = svm.predict_classes(X1_mat100_val_)
        val_acc = np.sum(np.squeeze(pred_val)==np.squeeze(Y1_val_)) / len(Y1_val_)
        print("Accuracy on val:", val_acc)

        val_accs_1.append(val_acc.copy())

    print(val_accs_1)
    print("Mean accuracy on val over the k folds (dataset 1):", np.mean(val_accs_1))


## Dataset 2 ##

if cross_validate_2:

    print("Cross-validating on dataset 2...")

    val_accs_2 = []

    split = np.linspace(0,len(X2_mat100_train),num=k_fold+1).astype(int)
    #print(split)

    for i in range(k_fold):

        print("Doing fold", i+1,"...")
        print()

        frac_val = 1.0/k_fold

        indices_val = np.arange(len(X2_mat100_train))[split[i]:split[i+1]]
        indices_train = np.concatenate([np.arange(len(X2_mat100_train))[0:split[i]],np.arange(len(X2_mat100_train))[split[i+1]:]]) 

        X2_mat100_train_,X2_mat100_val_ = X2_mat100_train[indices_train],X2_mat100_train[indices_val]
        Y2_train_,Y2_val_ = Y2_train[indices_train],Y2_train[indices_val]

        print('Doing SVM')

        if kernel=='linear':
            svm = SVM(kernel=LinearKernel(),C=C)
        elif kernel=='rbf':
            svm = SVM(kernel=GaussianKernel(sigma=np.sqrt(0.5/gamma),normalize=False),C=C)
        elif kernel=='poly':
            svm = SVM(kernel=PolynomialKernel(gamma=gamma,coef0=coef0,degree=degree),C=C)

        svm.fit(X2_mat100_train_, Y2_train_)

        pred_train = svm.predict_classes(X2_mat100_train_)
        print("Accuracy on train:", np.sum(np.squeeze(pred_train)==np.squeeze(Y2_train_)) / len(Y2_train_))

        pred_val = svm.predict_classes(X2_mat100_val_)
        val_acc = np.sum(np.squeeze(pred_val)==np.squeeze(Y2_val_)) / len(Y2_val_)
        print("Accuracy on val:", val_acc)

        val_accs_2.append(val_acc.copy())

    print(val_accs_2)
    print("Mean accuracy on val over the k folds (dataset 2):", np.mean(val_accs_2))



print("Summary:")

if cross_validate_0:
    print("Mean accuracy on val over the k folds (dataset 0):", np.mean(val_accs_0))
if cross_validate_1:
    print("Mean accuracy on val over the k folds (dataset 1):", np.mean(val_accs_1))
if cross_validate_2:
    print("Mean accuracy on val over the k folds (dataset 2):", np.mean(val_accs_2))