import aiml, os, re
import pattern.en as pattern_en
import spacy
from spacy.symbols import *
from spacy.tokens.token import Token
import search
import json, random
import pickle
from memory import memory


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

dialog_tags = """Accept, Bye, Clarify, Continuer, Emotion, Emphasis,
Greet, No Answer, Other, Reject, Statement, System, Wh-Question, Yes Answer,
Yes/No Question."""

filler_short_responses = ["Okay, I listen.", "Let's see...", "Bring it on!", "I am all ears", "You have my attention"]

sessionId = 12345

expect = dict()

first_person = ["me", "i", "mine", "my", "we", "ours"]
pron_translate = dict()
pron_translate["me"] = "you"
pron_translate["i"] = "you"
pron_translate["mine"] = "your"
pron_translate["my"] = "your"
pron_translate["ours"] = "your"
pron_translate["we"] = "you"


def get_emotion(polarity):
    emotion = "NEUTER"
    if polarity > 0.8:
        emotion = "SUPER HAPPY"
    elif polarity > 0.3:
        emotion = "GOOD SURPRISE"
    elif polarity < -0.4:
        emotion = "FEAR"
    elif polarity > 0.4:
        emotion = "COOL"
    elif polarity < -0.1:
        emotion = "SAD"
    elif polarity < -0.7:
        emotion = "ANGER"
    return emotion


class Brain:
    def __init__(self):
        self.instant_classifier = None
        self.kernel = aiml.Kernel()
        if os.path.isfile("bot_brain.brn"):
            self.kernel.bootstrap(brainFile="bot_brain.brn")
        else:
            self.kernel.bootstrap(learnFiles="./knowledge/startup.xml", commands="load aiml b")
            self.kernel.saveBrain("bot_brain.brn")
        self.load_classifier()
        self.interest = 10
        self.memory = memory.Memory(spacy_nlp)

    def load_classifier(self):
        f = open('sent_classifier.pickle', 'rb')
        self.instant_classifier = pickle.load(f)
        f.close()

    def process_sentiment(self, message):
        client_sentiment = pattern_en.sentiment(message)
        print pattern_en.sentiment(message).assessments
        return client_sentiment

    def process(self, message):
        # print pattern_en.suggest(message) -- suggestions
        if message == ">!train":
            self.train()
            return "It is nice to learn new stuff."
        if message == ">!forget":
            self.memory.forget()
            return "I am reborn. So much free space :) maybe you will use files to store memory and not RAM..."
        if message == ">!load_page":
            if self.memory.contains_id(sessionId) is False:
                response = "Hello! My name is Chad and I am passionate about music."
                response += "We can share our experiences and maybe we can get along."
                response += "Would you mind telling me your name first?"
                expect[sessionId] = "name"
            else:
                response = "Welcome back!"
                with open('results.json') as data_file:
                    data = json.load(data_file)
                    for i in range(10):
                        if 'musicrecording' in data['items'][i]['pagemap']:
                            mr = data['items'][i]['pagemap']['musicrecording']
                            which = random.randint(0, len(mr) - 1)
                            if 'name' not in mr[which]:
                                response += " Did you know that " + mr[which]['byartist'] + " has released a new song?"
                            else:
                                response += " You can check out this cool song, " + mr[which]['name'] + ", by " + \
                                            mr[which]['byartist']
            return response

        doc = spacy_nlp(message)
        '''for w in doc:
            print "(", w, w.dep_, w.pos_, w.head, ")"'''

        data = []

        for span in doc.sents:
            tokens = [doc[i] for i in range(span.start, span.end)]
            sentence = ''.join(doc[i].text_with_ws for i in range(span.start, span.end)).strip()

            sentence_type = self.instant_classifier.classify(dialogue_act_features(tokens))
            print(sentence_type)
            print(sentence)

            new_data = dict()
            new_data["type"] = sentence_type
            polarity, subjective = pattern_en.sentiment(sentence)
            sent = pattern_en.parse(sentence, lemmata=True)
            sent = pattern_en.Sentence(sent)
            modality = pattern_en.modality(sent)
            mood = pattern_en.mood(sent)
            new_data["polarity"] = polarity
            new_data["subjective"] = subjective
            new_data["modality"] = modality
            new_data["mood"] = mood
            new_data["emotion"] = get_emotion(polarity)

            verbs_subj = set()
            sentence = sentence[0].upper() + sentence[1:]
            doc = spacy_nlp(sentence)
            for possible_subject in doc:
                if (
                                possible_subject.dep == nsubj or possible_subject.dep == nsubjpass) and possible_subject.head.pos == VERB:
                    verbs_subj.add((possible_subject, possible_subject.head))

            if sentence_type not in ["Greet", "Bye", "Reject"]:
                try:
                    aiml_response = self.kernel.respond(sentence, sessionId)
                except:
                    aiml_response = ""
                new_data["aiml"] = aiml_response
            else:
                new_data["aiml"] = ""
            new_data["memory"] = self.memory.respond(verbs_subj, sentence_type, sessionId)
            data.append(new_data)

        arr_response = []

        for sent in data:
            sentence_response = ""

            sentence_type = sent["type"]
            try:
                aiml_sent_type_res = self.kernel.respond(sentence_type, sessionId)
            except:
                aiml_sent_type_res = ""
            if random.random() <= 0.3 or sentence_type in ["Greet", "Bye", "Reject"]:
                sentence_response += " " + aiml_sent_type_res

            if len(sent["aiml"]) > 0:
                sentence_response += aiml_response
            elif len(sent["memory"]) > 0:
                if sent["memory"] == "memorate":
                    sentence_response += self.kernel.respond("memorate", sessionId)
                else:
                    sentence_response += sent["memory"]

            emoi = self.kernel.respond(sent["emotion"])
            if random.random() <= 0.8:
                sentence_response += emoi
            
            if len(sentence_response) > 0:
                sentence_response = sentence_response[0].upper() + sentence_response[1:]
                arr_response.append(sentence_response)

        response = ""

        if len(arr_response) == 0:
            response = "Don't know that'"
        for res in arr_response:
            response += res + " "

        return response
