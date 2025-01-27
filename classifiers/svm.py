import numpy as np
import cvxopt
from cvxopt import matrix
import cvxpy as cp

class SVM():
    """
    SVM implementation
    
    Usage:
        svm = SVM(kernel='linear', C=1)
        svm.fit(X_train, y_train)
        svm.predict(X_test)
    """

    def __init__(self, kernel, C=1.0, tol_support_vectors=1e-4):
        """
        kernel: Which kernel to use
        C: float > 0, default=1.0, regularization parameter
        tol_support_vectors: Threshold for alpha value to consider vectors as support vectors
        """
        self.kernel = kernel
        self.C = C
        self.tol_support_vectors = tol_support_vectors

    def fit(self, X, y):

        self.X_train = X
        n_samples = X.shape[0]
        print("Computing the kernel...")
        self.X_train_gram = self.kernel.gram(X)
        print("Done!")

        #Define the optimization problem to solve

        P = self.X_train_gram
        q = -y.astype('float')
        G = np.block([[np.diag(np.squeeze(y).astype('float'))],[-np.diag(np.squeeze(y).astype('float'))]])
        h = np.concatenate((self.C*np.ones(n_samples),np.zeros(n_samples)))

        #Solve the problem
        #With cvxopt

        P=matrix(P)
        q=matrix(q)
        G=matrix(G)
        h=matrix(h)
        solver = cvxopt.solvers.qp(P=P,q=q,G=G,h=h)
        x = solver['x']
        self.alphas = np.squeeze(np.array(x))

        #Retrieve the support vectors
        self.support_vectors_indices = np.squeeze(np.abs(np.array(x))) > self.tol_support_vectors
        self.alphas = self.alphas[self.support_vectors_indices]
        self.support_vectors = self.X_train[self.support_vectors_indices]

        print(len(self.support_vectors), "support vectors out of",len(self.X_train), "training samples")

        return self.alphas


    def predict(self, X):
        """
        X: array (n_samples, n_features)\\
        Return: float array (n_samples,)
        """
        K = self.kernel.gram(X, self.support_vectors)
        y = np.dot(K, self.alphas)
        return y

    def predict_classes(self, X, threshold=0):
        """
        X: array (n_samples, n_features)\\
        Return: 0 and 1 array (n_samples,)
        """
        K = self.kernel.gram(X, self.support_vectors)
        y = np.dot(K, self.alphas)
        return np.where(y > threshold, 1, -1)

