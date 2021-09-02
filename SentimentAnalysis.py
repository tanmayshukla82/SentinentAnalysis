# -*- coding: utf-8 -*-
"""2014912_MiniProject_Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YdpaLVVymlmtJx4xp7A-D-uORdmq6cqv
"""

# Importing libraries for data manipulation
import pandas as pd
import numpy as np
import re
import string

# Reading Dataset
df = pd.read_csv('drive/MyDrive/dataset/data.csv',
                 encoding='ISO-8859-1', 
                 names=[
                        'target',
                        'id',
                        'date',
                        'flag',
                        'user',
                        'text'])
df.head()

# deleting unwnated columns
cols = ["id" , "date" , "flag" , "user"]
for col in cols:
  del df[col]

df.head()

#to check the two classes
df.target.unique()

# A graph representation of the classes available in the dataset
import matplotlib.pyplot as plt

classes = df.target.unique()
counts = []

for i in classes:
  count = len(df[df.target==i])
  counts.append(count)

plt.bar(['negative', 'positive'], counts)
plt.show()

# Data preprocessing
def preprocessing(text):
  #convert all text to lowercase
  text = text.lower()
  
  #removal of hyperlinks,,:
  text = re.sub(r'@[a-zA-Z0-9]+','',text)
  text = re.sub(r'RT[\s]+','',text)
  text = re.sub(r'https?://\S+','',text)
  text = re.sub(r':','',text)
  text = re.sub(r'\n','',text)
  text = re.sub(r'-','',text)
  text = re.sub(r',','',text)
  return text

df['text'] = df['text'].apply(preprocessing)
df.head()

#Formation of world cloud
all_words = ' '.join([text for text in df['text']])
from wordcloud import WordCloud,STOPWORDS
stopWords = set(STOPWORDS) 
wordcloud = WordCloud(stopwords=stopWords, width=800, height=500, random_state=21, max_font_size=110).generate(all_words)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

normal_words =' '.join([text for text in df['text'][df['target'] == 0]])

wordcloud = WordCloud(stopwords=stopWords, width=800, height=500, random_state=21, max_font_size=110).generate(normal_words)
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

normal_words =' '.join([text for text in df['text'][df['target'] ==4 ]])

wordcloud = WordCloud(stopwords=stopWords, width=800, height=500, random_state=21, max_font_size=110).generate(normal_words)
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

#importing libraries for model training
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Splitting data for training and testing in the ratio of 80:20
x = df['text']
y = df['target']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=32)

# Conversion of bag of word of text to matrix
  from sklearn.feature_extraction.text import TfidfVectorizer
  vectorizer = TfidfVectorizer()

  X_train = vectorizer.fit_transform(x_train)
  X_test = vectorizer.transform(x_test)

#model training
model = LogisticRegression(max_iter=1500)
model.fit(X_train, y_train)

#testing

score = model.score(X_test, y_test)
print("Accuracy:", score)

# Confusion Matrix allows us to know how many time the output was predicted correctly
from sklearn.metrics import confusion_matrix
y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred, labels=df.target.unique())
df_cm = pd.DataFrame(cm, index=df.target.unique(), columns=df.target.unique())
df_cm

# tesing 
tweet = 'I love my country'
vectTweet = vectorizer.transform(np.array([tweet]))  # vectorizes the tweet using our vectorizer

prediction = model.predict(vectTweet)  # predicts class of the tweet
print("positive" if prediction==[4] else "Negative")