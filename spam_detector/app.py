import os, sqlite3, vectorizer
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators


app = Flask(__name__)


directory = os.path.dirname(__file__)
classifier = vectorizer.clf
database = os.path.join(directory, 'database/spam.sqlite')


def classify(sms):
    """"Classifies an sms message as either spam or not spam.
    Also returns the probability of the prediction being correct.
    """
    dist = {1: 'Spam', 0: 'Not Spam'}
    X = vectorizer.vector.transform([sms])
    y = classifier.predict(X)[0]
    prob = classifier.predict_proba(X).max()
    return dist[y], '{0:.2f}'.format(prob*100)


def train(sms, label):
    """Uses partial fit to train the existing classifier."""
    sms = vectorizer.vector.transform([sms])
    classifier.partial_fit(sms, label)
    return


def database_add(path, sms, label):
    """Adds an sms and its classification into spam_db."""
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('''INSERT INTO spam_db
                 (sms, detection, date) VALUES
                 (?, ?, DATETIME('now'))''', (sms, label))
    conn.commit()
    conn.close()
    return


class SMSForm(Form):
    """Define a SMSForm class that instantiates a TextAreaField for later usage."""
    sms = TextAreaField('', [validators.DataRequired(), validators.length(min=15)])


@app.route('/')
def index():
    """Renders an SMSForm object onto reviewform.html."""
    form = SMSForm(request.form)
    return render_template('form.html', form=form)


@app.route('/results', methods=['POST'])
def results():
    """Fetches the content of the submitted web form and passes it onto
    the classifier to predict the class label and displays it on reviewform.html.
    """
    form = SMSForm(request.form)
    if request.method == 'POST' and form.validate():
        sms = request.form['sms']
        y, probability = classify(sms)
        return render_template('results.html', content=sms, prediction=y, probability=probability)
    return render_template('form.html', form=form)


@app.route('/thanks', methods=['POST'])
def feedback():
    """Fetches the predicted class label, updates the classifier and
    adds the user entry into the generated database.
    """
    feedback = request.form['feedback_button']
    sms = request.form['sms']
    prediction = request.form['prediction']

    dist = {'Not Spam': 0, 'Spam': 1}
    y = dist[prediction]
    if feedback == 'Incorrect':
        y = int(not(y))
    train(sms, y)
    database_add(database, sms, y)
    return render_template('thanks.html')


if __name__ == '__main__':
    app.run(debug=True)