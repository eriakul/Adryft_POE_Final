#  cd Desktop/Adryft/Adryft_POE_Final/Computer Vision

# kNN

import cv2
import numpy as np
import matplotlib.pyplot as plt
def knn(k):
    # Feature set containing (x,y) values of 25 known/training data
    trainData = np.random.randint(0,100,(25,2)).astype(np.float32)

    # Labels each one either Red or Blue with numbers 0 and 1
    responses = np.random.randint(0,2,(25,1)).astype(np.float32)

    # Take Red families and plot them
    red = trainData[responses.ravel()==0]
    plt.scatter(red[:,0],red[:,1],80,'r','^')

    # Take Blue families and plot them
    blue = trainData[responses.ravel()==1]
    plt.scatter(blue[:,0],blue[:,1],80,'b','s')



    newcomer = np.random.randint(0,100,(1,2)).astype(np.float32)
    plt.scatter(newcomer[:,0],newcomer[:,1],80,'g','o')

    knn = cv2.ml.KNearest_create()
    knn.train(trainData,cv2.ml.ROW_SAMPLE,responses)
    ret, results, neighbours, dist = knn.findNearest(newcomer, k)

    print ("results: ", results,"\n")
    print ("neighbours: ", neighbours,"\n")
    print ("distances: ", dist)

    plt.show()

def ocr_knn(k_value):
    pass
    img = cv2.imread('digits.png')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Now we split the image to 5000 cells, each 20x20 size
    cells = [np.hsplit(row,100) for row in np.vsplit(gray,50)]
    # Make it into a Numpy array. It size will be (50,100,20,20)
    x = np.array(cells)

    # Now we prepare train_data and test_data.
    train = x[:,:50].reshape(-1,400).astype(np.float32) # Size = (2500,400)
    test = x[:,50:100].reshape(-1,400).astype(np.float32) # Size = (2500,400)

    # Create labels for train and test data
    k = np.arange(10)
    train_labels = np.repeat(k,250)[:,np.newaxis]
    test_labels = train_labels.copy()

    # Initiate kNN, train the data, then test it with test data for k=1
    knn = cv2.ml.KNearest_create()
    knn.train(train,cv2.ml.ROW_SAMPLE,train_labels)
    ret, result, neighbours, dist = knn.findNearest(test, k_value)

    # Now we check the accuracy of classification
    # For that, compare the result with test_labels and check which are wrong
    matches = result==test_labels
    correct = np.count_nonzero(matches)
    accuracy = correct*100.0/result.size
    print(accuracy)

if __name__ == "__main__":
    ocr_knn(5)
