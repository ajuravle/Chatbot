import nltk
import pickle
from nlp import preprocess as nlp
from nltk.stem.snowball import SnowballStemmer
import re
import spacy

spacy_nlp = spacy.load('en')

def dialogue_act_features(post):
    tokens = spacy_nlp(unicode(post))
    features = {}
    for tok in tokens:
        if not tok.is_space:
            new_word = tok.lemma_.lower()
            features['contains({})'.format(new_word)] = True
            features['contains({})'.format('>>>>'+tok.dep_ + ' ' + tok.tag_)] = True
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