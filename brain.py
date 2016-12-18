import aiml
import os
from nlp import preprocess as nlp
import nltk
import re
from nltk.stem.porter import PorterStemmer
import pattern.en as pattern_en
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")

sessionId = 12345

dialog_tags = """Accept, Bye, Clarify, Continuer, Emotion, Emphasis,
Greet, No Answer, Other, Reject, Statement, System, Wh-Question, Yes Answer,
Yes/No Question."""

filler_short_responses = ["Okay, I listen.", "Let's see...", "Bring it on!", "I am all ears", "You have my attention"]


def dialogue_act_features(post):
    features = {}

    lems = nlp.lemmatize_text(post)
    words = nlp.tokenize_text(lems)

    for i in range(len(words)):
        new_word = stemmer.stem(words[i])
        new_word = re.sub(r"(.)\1+", r"\1", new_word)
        features['contains({})'.format(new_word.lower())] = True

    # for i in range(len(words) - 1):
    #    stems = [porter_stemmer.stem(words[i]), porter_stemmer.stem(words[i + 1])]
    #    new_word = re.sub(r"(.)\1+", r"\1", stems[0] + ' ' + stems[1])
    #    features['contains({})'.format(new_word.lower())] = True
    print(features)
    return features


class Brain:
    def __init__(self):
        self.instant_classifier = None
        self.kernel = aiml.Kernel()
        if os.path.isfile("bot_brain.brn"):
            self.kernel.bootstrap(brainFile="bot_brain.brn")
        else:
            self.kernel.bootstrap(learnFiles="./knowledge/startup.xml", commands="load aiml b")
            self.kernel.saveBrain("bot_brain.brn")
        self.train()

    def train(self):
        posts = nltk.corpus.nps_chat.xml_posts()[:]
        featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts ]
        size = int(len(featuresets) * 0.1)
        train_set, test_set = featuresets[size:], featuresets[:size]
        self.instant_classifier = nltk.NaiveBayesClassifier.train(featuresets)
        self.instant_classifier.show_most_informative_features()
        print(nltk.classify.accuracy(self.instant_classifier, test_set))

    def process_sentiment(self, message):
        client_sentiment = pattern_en.sentiment(message)
        print pattern_en.sentiment(message).assessments
        sent = client_sentiment
        return sent

    def process(self, message):
        if message == "train":
            self.train()
            return "It is nice to learn new stuff."

        response = ""

        self.process_sentiment(message)

        sentences = nlp.get_sentences(message)
        for sentence in sentences:
            pos_tags = nlp.pos_tag_text(sentence)
            # print pattern_en.suggest(message)
            sentence_type = self.instant_classifier.classify(dialogue_act_features(sentence))
            aiml_response = self.kernel.respond(sentence_type, sessionId)
            response += sentence_type + ' ' + aiml_response
        response += "."

        # tone generator : eg. concatenate : I'm not exactly sure, but ...
        s = pattern_en.parse(message, lemmata=True)
        s = pattern_en.Sentence(s)
        print pattern_en.modality(s)

        return response
