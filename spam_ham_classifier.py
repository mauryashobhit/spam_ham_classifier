# -*- coding: utf-8 -*-
"""spam_ham_classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Qxkot18oYctfH6c_IjOzlnf1grUeZMFW
"""

import pandas as pd

messages=pd.read_csv("/content/drive/MyDrive/spam ham/archive.zip (Unzipped Files)/spam.csv",encoding="latin-1")

messages

import re
import nltk
nltk.download("stopwords")

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
corpus=[]

for i in range(0, len(messages)):
    review = re.sub('[^a-zA-Z]', ' ', messages['v2'][i])
    review = review.lower()
    review = review.split()
    
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    corpus.append(review)

corpus

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=2500)
X = cv.fit_transform(corpus).toarray()

y=pd.get_dummies(messages['v1'])
y=y.iloc[:,1].values

X

y

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

from sklearn.naive_bayes import MultinomialNB
spam_detect_model = MultinomialNB().fit(X_train, y_train)

y_pred=spam_detect_model.predict(X_test)

from sklearn.metrics import confusion_matrix ,accuracy_score

print(confusion_matrix(y_test,y_pred))
print(accuracy_score(y_test,y_pred))

import joblib
filename="spam_ham.sav"
joblib.dump(spam_detect_model,filename)

loaded_model=joblib.load(filename)
result=loaded_model.score(X_test,y_test)
print(result)

