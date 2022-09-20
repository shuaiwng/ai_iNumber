from PIL import Image
import numpy as np
import os
import math


def read_img(path):
    img = Image.open(path).convert('L')
    pixels = img.load()
    lst = []
    for i in range(28):
        for j in range(28):
            lst.append(pixels[i,j])
    return lst


def get_files_num_list(data_path):
    files_num_list = []
    for path, subdirs, files in os.walk(data_path):
        for file in files:
            files_num_list.append([os.path.join(path,file), path[-1]])
    return files_num_list


def init_params():
    W1 = np.random.rand(10, 784) - 0.5
    b1 = np.random.rand(10, 1) -0.5
    W2 = np.random.rand(10, 10) - 0.5
    b2 = np.random.rand(10, 1) -0.5
    return W1, b1, W2, b2



def softmax(Z):
    '''Probabilities between 0 and 1'''
    return np.exp(Z) / np.sum(np.exp(Z), axis=0)


def ReLU(Z):
    return np.maximum(0, Z)


def forward_prop(W1, b1, W2, b2, X):
    Z1 = W1.dot(X) + b1
    A1 = ReLU(Z1)
    Z2 = W2.dot(A1) + b2
    A2 = softmax(Z2)    
    return Z1, A1, Z2, A2


def deriv_ReLU(Z):
    return Z > 0


def backward_prop(Z1, A1, Z2, A2, W2, X, Y):
    m = Y.shape[1]
    dZ2 = A2 - Y_train
    dW2 = 1 / m * dZ2.dot(A1.T)
    db2 = 1 / m * np.sum(dZ2, 0)
    dZ1 = W2.T.dot(dZ2) * deriv_ReLU(Z1)
    dW1 = 1 / m * dZ1.dot(X.T)
    db1 = 1 / m * np.sum(dZ1, 0)
    return dW1, db1, dW2, db2


def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1
    W2 = W2 - alpha * dW2
    b2 = b2 - alpha * db2
    return W1, b1, W2, b2
    

def get_predictions(A2):
    a2_shape = A2.shape
    pred_map = np.zeros(a2_shape)
    for i in range(a2_shape[1]):
        pred_map[np.argmax(A2[:,i])][i] = 1
    return pred_map


def get_accuracy(predictions, Y):
    return np.sum(np.multiply(predictions, Y)) / Y.shape[1]


def gradient_descent(X, Y, iterations, alpha):
    W1, b1, W2, b2 = init_params()
    for i in range(iterations):
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
        dW1, db1, dW2, db2 = backward_prop(Z1, A1, Z2, A2, W2, X, Y)
        W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)
        if i % 10 == 0:
            print("Iteration: ", i)
            print("Accuracy: ", get_accuracy(get_predictions(A2), Y))
    return W1, b1, W2, b2


if __name__ == "__main__": 
    files_num_list = get_files_num_list("./mnist_png/testing/")
    lth = len(files_num_list)

    Y_train = np.zeros([10, lth])
    for i in range(lth):
        one_hot = np.zeros([10, 1])
        one_hot[int(files_num_list[i][1])] = 1
        Y_train[:,i] = one_hot.ravel()

    X_train = np.zeros([28*28, lth])
    for i in range(lth):
        lst = read_img(files_num_list[i][0])
        X_train[:,i] = np.array(lst).T
    X_train = np.divide(X_train, 255)

    W1, b1, W2, b2 = gradient_descent(X_train, Y_train, 1000, 0.1)
  

    




