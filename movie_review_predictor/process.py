import clean, pickle
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier


def stream_docs(path):
    """Defines a generator function that reads in and returns
    one document at a time.
    """
    with open(path, 'r', encoding='utf-8') as csv:
        next(csv)
        for line in csv:
            text, label = line[:-3], int(line[-2])
            yield text, label


def get_minibatch(doc_stream, size):
    """Takes a document stream the stream_docs function and
    returns a particular number of documents specified by
    the size parameter.
    """
    docs, y = [], []
    try:
        for _ in range(size):
            text, label = next(doc_stream)
            docs.append(text)
            y.append(label)
    except StopIteration:
        return None, None

    return docs, y


def setup():
    """Sets up a classifier and uses the partial fit
    feature to start the out-of-core machine learning process.
    Returns the classifier.
    """

    # Initialize HashingVectorizer with our tokenizer function and set the number of features to 2**21
    vector = HashingVectorizer(decode_error='ignore', n_features=2**21, preprocessor=None, tokenizer=clean.tokenizer)

    # Reinitialize a logistic regression classifier SGDClassifier
    clf = SGDClassifier(loss='log', random_state=1, n_iter=1)

    # Create a doc_stream
    doc_stream = stream_docs(path='data/imdb_data.csv')

    # Using out-of-core learning, we fit our classifier with our data
    # We iterate over 45 minibatches that consists of 1,000 documents each
    # and use pickle later on to efficiently store our classifier for future use
    #
    # for _ in range(45):
    #     X_train, y_train = get_minibatch(doc_stream, size=1000)
    #     if not X_train: break
    #     X_train = vector.transform(X_train)
    #     clf.partial_fit(X_train, y_train, classes=np.array([0, 1]))

    # We can 'recycle' the last 5,000 reviews by using them to update our model
    #
    # clf = clf.partial_fit(X_test, y_test)

    # Pickle our data to efficiently store and load our classifier for future use
    #
    # with open('data/classifier.pkl', 'wb') as file:
    #     pickle.dump(clf, file)
    pickle_in = open('data/classifier.pkl', 'rb')
    clf = pickle.load(pickle_in)

    # Since we have a total of 50,000 reviews and we have processed 45,000,
    # we can use the remaining 5,000 to evaluate our model's performance and
    # print the accuracy
    X_test, y_test = get_minibatch(doc_stream, size=5000)
    X_test = vector.transform(X_test)
    print('Accuracy:', clf.score(X_test, y_test))
    print()

    return vector, clf


def ask(vectorizer, classifier):
    """Continuously prompt the user to enter a movie title and
    review. Outputs prediction and probability of the movie review.
    """
    classes = {0: 'Negative', 1: 'Positive'}

    while True:
        movie_title = input('Enter Movie Title or press ENTER to quit: ')
        if movie_title == '': break
        movie_review = list(input('Enter Movie Review: '))

        user_entry = vectorizer.transform(movie_review)
        prediction = classes[classifier.predict(user_entry)[0]]
        probability = np.max(classifier.predict_proba(user_entry))

        print('     Movie review analysis for', movie_title)
        print('     Prediction:', prediction)
        print('     Probability:', probability)
        print()

    return
