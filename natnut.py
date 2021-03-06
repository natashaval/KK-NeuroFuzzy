import anfis
from membership import membershipfunction, mfDerivs
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
import membershipsteven as mbpstev
import numpy as np

wine = load_wine()
X = wine.data
Y = wine.target

''' Reduced Feature unsupervised learning'''
# https://kite.com/python/docs/sklearn.datasets.lfw.Bunch
# https://scikit-learn.org/stable/modules/feature_selection.html
# https://scikit-learn.org/stable/modules/unsupervised_reduction.html


pca = PCA(n_components = 4)
X_less = pca.fit_transform(X)
print (X_less.shape)
wine.data = X_less
X = X_less


# print(X)
# print(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.33)

y_size = Y_test.tolist()
print("Length of Y test: ", len(y_size))

def get_membership(dataset):
    mf = []
    for i in range(4): # feature_size
        gauss = []
        for j, tname in enumerate(dataset.target_names): # target_class
            filtered = []
            for k, target in enumerate(dataset.target):
                # print(j, target)
                if (target == j):
                    filtered.append(dataset.data[k][i])
                    #print(dataset.data[k][i])
            gauss.append(['gaussmf', {'mean': np.mean(filtered), 'sigma': np.var(filtered)}])
            print("\n==")
        mf.append(gauss)
        print("\n++++")
    return mf

mf = get_membership(wine)
# jika feature = 2; gauss = 3
# jika feature = 4; gauss =
#mf = mbpstev.get_mf(wine)
print(mf)


mfc = membershipfunction.MemFuncs(mf)
anf = anfis.ANFIS(X_train, Y_train, mfc)
anf.trainHybridJangOffLine(epochs = 5)

Y_predict = []

for i in range(len(Y_test)):
    res = round(anf.fittedValues[Y_test[i]][0],6)
    print ("Y test: " + str(Y_test[i]), "Y predicted: " + str(res))
    if abs(res-0) > abs(res-1) < abs(res-2):
        Y_predict.append(0)
    elif abs(res-0) < abs(res-1) < abs(res-2):
        Y_predict.append(1)
    elif abs(res-0) > abs(res-1) > abs(res-2):
        Y_predict.append(2)

# print(classification_report(Y_test, Y_predict))

# anf.plotErrors()
anf.plotResults()

