import pandas as pd
import numpy as np
from sklearn.feature_extraction import stop_words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import Pipeline

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import RidgeClassifierCV
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import svm

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split



CountVect = CountVectorizer()
TfidVect = TfidfTransformer()


def getTrainTestData():
    dataFrames = []
    fileNames = ['AfterFinalSentimentLabelledCoachellaTweets.csv',
                 'BeforeFinalSentimentLabelledCoachellaTweets.csv',
                 'DuringFinalSentimentLabelledCoachellaTweets.csv',
                 'AfterFinalSentimentLabelledWomansMarchTweets.csv',
                 'BeforeFinalSentimentLabelledWomansMarchTweets.csv',
                 'DuringFinalSentimentLabelledWomansMarchTweets.csv']

    for file in fileNames:
        f1 = pd.read_csv("FinalLabelledTweets/"+file)
        f1 = f1[:249]
        dataframe = {file:f1}
        dataFrames.append(dataframe)

    # for item in dataFrames[:2]:
    #     for key in item.keys():
    #         print(key)
    return dataFrames

def computeFeatures():
    dataframe = pd.read_csv('BeforeFinalSentimentLabelledWomansMarchTweets.csv')

    #BOW
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(dataframe.text)
    print(X_train_counts.shape)

    #TF-IDF
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    print(X_train_tfidf)


def getClassifiers():
    # names = ["Logistic Regression", "Multinomial NB","Bernoulli NB","KNeighborsClassifier",
    #         "RandomForest", "GradientBoostingClassifier","DecisionTreeClassifier","RidgeClassifierCV",
    #          "ExtraTreesClassifier","LinearSVM"]

    names = ["RidgeClassifierCV"]

    classifiers = [
        # LogisticRegression(),
         #MultinomialNB(),
        # BernoulliNB(),
        # KNeighborsClassifier(),
        # RandomForestClassifier(),
        # GradientBoostingClassifier(),
        # DecisionTreeClassifier(),
         RidgeClassifierCV()
        # ExtraTreesClassifier(),
        #svm.LinearSVC()
    ]
    zipped_clf = zip(names, classifiers)
    return zipped_clf




def main():
    #Change params of vect
    #CountVect.set_params(ngram_range=(1, 1),stop_words=stop_words.ENGLISH_STOP_WORDS)

    #Grid Search Parameters
    parameters = {'vect__ngram_range': [(1, 1), (1, 2),(1,3)],
               'tfidf__use_idf': (True, False),
                }

    dataFrames = getTrainTestData()
    stats= []
    for names,clf in getClassifiers():
        text_clf = Pipeline([('vect', CountVect),
                             ('tfidf', TfidVect),
                             ('clf', clf)])

        for item in dataFrames:
            for key, val in item.items():
                X_train, X_test, y_train, y_test = train_test_split(val.text,val.target,test_size=0.2,random_state=10)
                gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
                gs_clf = gs_clf.fit(X_train, y_train)
                #text_clf = text_clf.fit(X_train, y_train)
                #score = text_clf.score(X_test,y_test)
                #print(key,score,names)
                y_pred = gs_clf.predict(X_test)
                conmat = np.array(confusion_matrix(y_test, y_pred, labels=[1, 0,-1]))
                confusion = pd.DataFrame(conmat, index=['Will Attend', 'Not Attending','Cant Say'],
                                         columns=['predicted_1', 'predicted_0','predicted_-1'])

                #print(confusion)
                print(key,"\n")
                print(classification_report(y_test,y_pred))

                #print("Best_Score",gs_clf.best_score_,names,key)
                #print("Best_Params",gs_clf.best_params_,names,key)





if __name__ == '__main__':
    main()

