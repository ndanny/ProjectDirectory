# Takes a single message and cleans it of HTML markup,
# turns word casings to lowercase, removes punctuations,
# and tokenizes message while removing certain stop words from
# the nltk.corpus.

import re
from string import punctuation
from nltk.corpus import stopwords

# Uncomment the following three lines if stopwords are not downloaded
#
# import nltk
# nltk.download('stopwords'')


def tokenizer(message):
    stop = stopwords.words('english')
    message = re.sub('<[^>]*>', '', message.lower())
    message = ''.join(c for c in message if c not in punctuation)
    return [w for w in message.split() if message not in stop]
