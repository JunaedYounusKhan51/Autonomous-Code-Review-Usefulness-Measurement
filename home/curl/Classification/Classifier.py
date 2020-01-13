from collections import Counter
import scipy
import numpy as np
import pandas as pd
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score, precision_score, recall_score
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
from sklearn.metrics import classification_report

from sklearn.tree import tree

from ReviewModifier.ReviewModifier import ReviewModifier


class Classifier:

    def __init__(self):
        self.getTrainAndTest()
    '''
    def __init__(self,review,isLast=0):
        self.rm=ReviewModifier(review,isLast)
        self.getTrainAndTest()
    '''
    def feedReview(self,review,isLast=0):
        self.rm=ReviewModifier(review,isLast)


    def getPrediction(self):
        sampleList=self.rm.getReviewModifier()

        decisionList=[]

        #  Decision Tree
        prediction = self.clf_DTree.predict(sampleList)
        #print("Decision Tree Prediction result: %s\n" % prediction)
        decisionList.append(prediction[0])

        # K-Nearest Neighbour
        prediction = self.clf_KNN.predict(sampleList)
        #print("KNN Prediction result: %s\n" % prediction)
        decisionList.append(prediction[0])

        # Support Vector Machine
        prediction = self.clf_SVM.predict(sampleList)
        #print("SVM Prediction result: %s\n" % prediction)
        decisionList.append(prediction[0])

        #print("Decision List: %s" % decisionList)

        #Determinig Most Common
        counter=Counter(decisionList)
        #print("Total Decision in number: %s" % counter.most_common())
        mostVoted=counter.most_common(1);
        #print("Most Voted: %s " % mostVoted)
        return mostVoted[0][0]











    def getTrainAndTest(self):
        #df = pd.read_csv('H:\pc programming\Django(Prac)\ML\Classification\Classification\Review_Testing_Format.txt')
        df=pd.read_csv('Review_Testing_Format.txt')
        df.replace('?', -99999, inplace=True)
        df.drop(['id'], 1, inplace=True)

        X = np.array(df.drop(['class'], 1))
        y = np.array(df['class'])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.10)

        #  Built-In Decision Tree
        self.clf_DTree = tree.DecisionTreeClassifier()
        self.clf_DTree.fit(X_train, y_train)
        accuracy = self.clf_DTree.score(X_test, y_test)
        print("Accuracy in Decision Tree: %s" % accuracy)


        #  Built-In K-Nearest Neighbour
        self.clf_KNN = tree.DecisionTreeClassifier()
        self.clf_KNN.fit(X_train, y_train)
        accuracy = self.clf_KNN.score(X_test, y_test)
        print("Accuracy in KNN: %s" % accuracy)


        #  Built-In Support Vector Machine
        self.clf_SVM = tree.DecisionTreeClassifier()
        self.clf_SVM.fit(X_train, y_train)
        accuracy = self.clf_SVM.score(X_test, y_test)
        print("Accuracy in SVM: %s" % accuracy)


        Y = label_binarize(y, classes=['A','B','C'])
        n_classes = Y.shape[1]

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.5,
                                                            )
        classifier = OneVsRestClassifier(svm.LinearSVC(random_state=None))
        classifier.fit(X_train, Y_train)
        y_score = classifier.decision_function(X_test)
        # For each class
        precision = dict()
        recall = dict()
        average_precision = dict()
        '''
        for i in range(n_classes):
            average_precision[i] = average_precision_score(Y_test[:, i], y_score[:, i])

        average_precision["micro"] = average_precision_score(Y_test, y_score,
                                                             average="micro")
        average_precision["macro"] = average_precision_score(Y_test, y_score,
                                                             average="macro")
        average_precision["weighted"] = average_precision_score(Y_test, y_score,
                                                             average="weighted")
        print('Average precision score, micro-averaged over all classes: {0:0.2f}'
              .format(average_precision["micro"]))

        recall["micro"] = recall_score(Y_test, y_score,average="micro")
        print('Recall score, micro over all classes: {0:0.2f}'
              .format(recall["micro"]))
              '''
        '''
        target_names = ['A', 'B', 'C']
        print(classification_report(y_test, y_score, target_names=target_names))
        '''


