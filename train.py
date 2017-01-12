import nltk
import pickle
from nlp import preprocess as nlp
from nltk.stem.snowball import SnowballStemmer
import re

def dialogue_act_features(post):
    stemmer = SnowballStemmer("english")
    features = {}
    lems = nlp.lemmatize_text(post)
    words = nlp.tokenize_text(lems)
    for i in range(len(words)):
        new_word = stemmer.stem(words[i])
        new_word = re.sub(r"(.)\1+", r"\1", new_word)
        features['contains({})'.format(new_word.lower())] = True
    return features
    
def train():
    posts = nltk.corpus.nps_chat.xml_posts()[:]
    featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    instant_classifier = nltk.NaiveBayesClassifier.train(featuresets)
    instant_classifier.show_most_informative_features()
    print(nltk.classify.accuracy(instant_classifier, test_set))
    f = open('sent_classifier.pickle', 'wb')
    pickle.dump(instant_classifier, f)
    f.close()
    
if __name__ == "__main__":
    train()