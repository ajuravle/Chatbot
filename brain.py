import aiml
import os
from nlp import preprocess as nlp
import nltk
import re
from nltk.stem.porter import PorterStemmer
import pattern.en as pattern_en
from nltk.stem.snowball import SnowballStemmer
import spacy
from spacy.symbols import *
from spacy.tokens.token import Token

spacy_nlp = spacy.load('en')

stemmer = SnowballStemmer("english")

dialog_tags = """Accept, Bye, Clarify, Continuer, Emotion, Emphasis,
Greet, No Answer, Other, Reject, Statement, System, Wh-Question, Yes Answer,
Yes/No Question."""

filler_short_responses = ["Okay, I listen.", "Let's see...", "Bring it on!", "I am all ears", "You have my attention"]

sessionId = 12345

memory = dict()


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
    # print(features)
    return features


first_person = ["me", "i", "mine", "my", "we", "ours"]
pron_translate = dict()
pron_translate["me"] = "you"
pron_translate["i"] = "you"
pron_translate["mine"] = "your"
pron_translate["my"] = "your"
pron_translate["ours"] = "your"
pron_translate["we"] = "you"


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
        self.interest = 10

    def train(self):
        posts = nltk.corpus.nps_chat.xml_posts()[:]
        featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
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
        if message == "forget":
            memory.clear()
            return "I am reborn. So much free space :) maybe you will use files to store memory and not RAM..."
        if sessionId not in memory:
            memory[sessionId] = dict()

        res_msg = ""
        # print pattern_en.suggest(message) -- suggestions
        self.process_sentiment(message)
        memory_msg = ""
        memorate = False

        s = nlp.get_sentences(message)

        doc = spacy_nlp(message)
        for w in doc:
            print "(", w, w.dep_, w.pos_, w.head, ")"

        for sentence in s:
            sentence_type = self.instant_classifier.classify(dialogue_act_features(sentence))

            verbs_subj = set()
            sentence = sentence[0].upper() + sentence[1:]
            doc = spacy_nlp(sentence)
            for possible_subject in doc:
                if (
                                possible_subject.dep == nsubj or possible_subject.dep == nsubjpass) and possible_subject.head.pos == VERB:
                    verbs_subj.add((possible_subject, possible_subject.head))

            # MEMORY MODULE
            if sentence_type == "Statement":
                # insert into memory
                for i in verbs_subj:

                    subjs = []

                    subjects = [i[0]]
                    for tok in i[0].children:
                        if tok.dep == conj:
                            subjects.append(tok)

                    for subj in subjects:
                        predec = ""
                        for tok in subj.children:
                            if tok.dep_ == "poss" or tok.dep == amod:
                                predec += tok.lower_
                        if len(predec) > 0:
                            subjs.append(predec + " " + subj.lower_)
                        else:
                            subjs.append(subj.lower_)

                    vb = i[1].lower_
                    if vb not in memory[sessionId]:
                        memory[sessionId][vb] = dict()
                    for subj in subjs:
                        for c in i[1].children:
                            if c.dep in [prep]:
                                memory[sessionId][vb][subj] = c.lower_ + " "
                                for c_prep in c.children:
                                    if c_prep.dep in [dobj, pobj, attr]:
                                        memory[sessionId][vb][subj] += c_prep.text
                                        memorate = True
                            elif c.dep in [dobj, pobj, attr]:
                                memory[sessionId][vb][subj] = c.text
                                memorate = True
                print str(memory)
            elif sentence_type == "whQuestion":
                for i in verbs_subj:
                    subjs = []

                    subjects = [i[0]]
                    for tok in i[0].children:
                        if tok.dep == conj:
                            subjects.append(tok)

                    for subj in subjects:
                        predec = ""
                        for tok in subj.children:
                            if tok.dep_ == "poss" or tok.dep == amod:
                                predec += tok.lower_
                        if len(predec) > 0:
                            subjs.append(predec + " " + subj.lower_)
                        else:
                            subjs.append(subj.lower_)

                    max_similarity = 0
                    verb = i[1].lower_
                    for j in memory[sessionId]:
                        p_word = spacy_nlp(j)
                        similarity = i[1].similarity(p_word[0])
                        if similarity > max_similarity:
                            max_similarity = similarity
                            verb = j
                    if max_similarity > 0.5 and verb in memory[sessionId]:
                        num_subjs = len(subjs)
                        for subj in subjs:
                            if subj in memory[sessionId][verb]:
                                toks = nlp.tokenize_text(subj)
                                memory_msg = ""
                                for t in toks:
                                    if t in first_person:
                                        memory_msg += pron_translate[t] + " "
                                    else:
                                        memory_msg += t + " "
                                num_subjs -= 1
                                if num_subjs > 2:
                                    memory_msg += ", "
                                elif num_subjs == 1:
                                    memory_msg += "and "
                        memory_msg += verb + " "
                        if num_subjs != len(subjs):
                            memory_msg += memory[sessionId][verb][subjs[-1]] + "."

    # tone generator : eg. concatenate : I'm not exactly sure, but ...
        s = pattern_en.parse(message, lemmata=True)
        s = pattern_en.Sentence(s)
        print pattern_en.modality(s)

        aiml_response = self.kernel.respond(message, sessionId)
        if len(aiml_response) < 3:
            response = "I don't know that...but maybe you can teach me."
        else:
            response = aiml_response

        if len(response) < 2:
            if len(memory_msg) > 0:
                response = "You told me that " + memory_msg
            elif memorate is True:
                response = "Sure, I'll remember that. Thanks for the information."
        return response
