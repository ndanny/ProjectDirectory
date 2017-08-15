# This program utilizes the concept of stochastic gradient descent
# to train a classifier with a dataset consisting of movie reviews.
# The program will give a score to the dataset.

import read, process


def main():
    # Read the files dataset and create a csv file, if not exists
    read.process('acllmdb')

    # Run the setup() function from process.py which returns
    # the vectorizer and classifier that we need to predict movie reviews
    vectorizer, classifier = process.setup()

    # Prompt user for their review for a movie
    process.ask(vectorizer, classifier)


if __name__ == '__main__':
    main()
