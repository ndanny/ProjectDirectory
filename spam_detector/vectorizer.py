import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer


##### Create a dataframe for our spam dataset
df = pd.read_csv('information/spam.csv')


##### Split the dataframe into its respective columns as X and y
X = df['sms'].as_matrix()
y = df['detected'].as_matrix()


##### Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


##### Create a vectorizer to learn the vocabulary using CountVectorizer()
stopwords = open('information/stop_words.pkl', 'rb')
vector = CountVectorizer(stop_words=stopwords)
vector.fit(X_train)


##### Transform train and test data using our new vectorizer
X_train, X_test = vector.transform(X_train), vector.transform(X_test)


##### Use the Multinomial Naive Bayes machine learning model as our classifier
clf = MultinomialNB()
clf.fit(X_train, y_train)