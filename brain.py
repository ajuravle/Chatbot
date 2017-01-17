import aiml, os, re
import pattern.en as pattern_en
from pattern.en import wordnet
import spacy
from spacy.symbols import *
from spacy.tokens.token import Token
import search
import json, random
import pickle
from memory import memory
import language_check

tool = language_check.LanguageTool('en-US')
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


emotion_th = dict()
emotion_th["NEUTER"] = 0.1
emotion_th["SUPER HAPPY"] = 1.0
emotion_th["GOOD SURPRISE"] = 1.0
emotion_th["FEAR"] = 0.5
emotion_th["COOL"] = 0.5
emotion_th["SAD"] = 0.5
emotion_th["ANGER"] = 0.9


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

# bot_topics = [ "INTRO", "NAME", "HOBBY", "THINK", "JOKE", "SEARCH", "NEWS", "FACT" ]
bot_topics = ["GREET", "INTRO", "NAME", "HOBBY", "THINK", "JOKE", "FACT", "REVIEW"]

def song_suggestion():
    response = ""
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
                break
    return response

def song_review():
    response = ""
    with open('reviews.json') as data_file:
        data = json.load(data_file)
        choice = random.choice(data)
        if random.random() < 0.5:
            response += "Do you know \""
        else:
            response += "Have you heard about \""
        response += choice["song"] + "\" by " + choice["artist"] + "? "
        response += choice["review"]
    return response

def reformulate(data_in):
    try:
        doc = spacy_nlp(unicode(data_in))
    except:
        return data_in
    response = ""

    map_pos = dict()
    map_pos["ADJ"] = pattern_en.ADJECTIVE
    map_pos["NOUN"] = pattern_en.NOUN
    map_pos["VERB"] = pattern_en.VERB
    map_pos["ADV"] = pattern_en.ADVERB

    for tok in doc:
        # print(tok.text)
        if tok.pos_ in map_pos:
            try:
                partofspeech = map_pos[tok.pos_]
                s = wordnet.synsets(tok.lower_, pos=partofspeech)[0]
                syn_list = [ s.gloss, s.synonyms, s.hypernym, s.meronyms()]
                if partofspeech in [pattern_en.VERB, pattern_en.ADJECTIVE]:
                    sim = s.similar()
                    if len(sim) > 0:
                        response += random.choice(sim).synonyms[0] + " "
                    else:
                        response += tok.text_with_ws
                else:
                    if len(syn_list[1]) > 0:
                        response += random.choice(syn_list[1]) + " "
                    else:
                        response += tok.text_with_ws
                    if random.random() < 0.05:
                        if len(syn_list[0]) > 0:
                            response += "... By definition " + tok.text + " is "
                            response += syn_list[0]
                            response += "..."
                    elif random.random() < 0.5:
                        if len(syn_list[2].synonyms) > 0:
                            response += "(" + syn_list[2].synonyms[0] + " ) "
                    elif random.random() < 0.1:
                        if len(syn_list[3]) > 0:
                            response += "... consists of "
                            numberof = len(syn_list[3])
                            if numberof > 0:
                                for syn in syn_list[3]:
                                    if numberof == 2:
                                        response += syn.synonyms[0] + " and "
                                    else:
                                        response += syn.synonyms[0] + "..."
                                    numberof -= 1
            except IndexError:
                response += tok.text_with_ws
            except Exception as e:
                # print(e)
                response += " "
        else:
            response += tok.text_with_ws
    if len(response) > 1:
        response = response[0].upper() + response[1:]
    return response


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
        # print pattern_en.sentiment(message).assessments
        return client_sentiment

    def process(self, message):
        # print pattern_en.suggest(message) -- suggestions
        if message == ">!train":
            self.train()
            return ("It is nice to learn new stuff.", 1000)
        if message == ">!forget":
            self.memory.forget()
            return ("I am reborn. So much free space :) maybe you will use files to store memory and not RAM...", 1000)
        if message == ">!memory":
            return (str(self.memory.memory), 1000)
        if message == ">!load_page":
            if self.memory.contains_id(sessionId) is False:
                # response = "Hello! My name is Chad and I am passionate about music."
                # response += "We can share our experiences and maybe we can get along."
                expect[sessionId] = ["GREET", "INTRO", "NAME"]
            else:
                response = "Welcome back!"
                response += song_suggestion()
                return (response, 1000)


        bot_topic = expect[sessionId][0]
        if message in [">!not_exists"] or bot_topic in ["GREET", "INTRO", "NAME"]:
            expect[sessionId].append(random.choice(bot_topics[3:]))
            allow_reformulate = True
            if bot_topic == "FACT":
                response = song_suggestion()
                allow_reformulate = False
            elif bot_topic == "REVIEW":
                response = song_review()
                allow_reformulate = False
            else:
                bot_topic_aiml = "Q " + bot_topic
                try:
                    aiml_response = self.kernel.respond(bot_topic_aiml, sessionId)
                except:
                    aiml_response = ""
                response = aiml_response
            expect[sessionId].pop(0)
            if len(response) > 0 and allow_reformulate is True:
                response = reformulate(response)
            return (response, 2000)

        try:
            if random.random() < 0.1:
                expect[sessionId].append(random.choice(bot_topics[3:]))

            matches = tool.check(unicode(message))
            message = language_check.correct(unicode(message), matches)
            # print(message)
            doc = spacy_nlp(message)
            '''for w in doc:
                print "(", w, w.dep_, w.pos_, w.head, ")"'''

            data = []

            random_strings = 0
            num_tokens = 0

            for span in doc.sents:
                tokens = [doc[i] for i in range(span.start, span.end)]
                sentence = ''.join(doc[i].text_with_ws for i in range(span.start, span.end)).strip()
                sentence_no_punct = ''.join(doc[i].text_with_ws for i in range(span.start, span.end) if doc[i].is_punct is False).strip()

                num_tokens += len(tokens)
                for tok in tokens:
                    if tok.is_oov:
                        random_strings += 1

                sentence_type = self.instant_classifier.classify(dialogue_act_features(tokens))
                # print(sentence_type)

                new_data = dict()
                new_data["type"] = sentence_type.upper()
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
                for possible_subject in span:
                    if (possible_subject.dep == nsubj or possible_subject.dep == nsubjpass) and possible_subject.head.pos == VERB:
                        verbs_subj.add((possible_subject, possible_subject.head))

                try:
                    aiml_response = self.kernel.respond(sentence_no_punct.upper(), sessionId)
                except:
                    aiml_response = ""
                new_data["aiml"] = aiml_response

                if len(verbs_subj) > 0:
                    new_data["memory"] = self.memory.respond(verbs_subj, sentence_type, sessionId)
                else:
                    new_data["memory"] = ""
                data.append(new_data)

            arr_response = []

            wait = num_tokens * 100

            if random_strings / num_tokens > 0.3:
                random_response = [
                    "I can't understand what you're saying.",
                    "If you want us to have a nice conversation, try to write undersandable words",
                    "How about we have a normal conversation?",
                    "Hey, please try to write something readable.Thank you!",
                    "Don't write like that, because if I would do it, you wouldn't like it",
                    "I noticed you like to tap random keys on your keyboard! Funny, but please don't do it anymore",
                    "Heh. I also like to play tap-related games on my mobile device, but not on my keyboard.",
                    "Please consider using your keyboard for writing actual words" ]
                response = random.choice(random_response)
                return (response, wait)

            for sent in data:
                sentence_response = ""

                if len(sent["aiml"]) > 0:
                    sentence_response += aiml_response
                else:
                    if len(sent["memory"]) > 0:
                        if sent["memory"] == "memorate":
                            sentence_response += self.kernel.respond("memorate", sessionId)
                        else:
                            sentence_response += sent["memory"]
                    else:
                        sentence_type = sent["type"]
                        try:
                            aiml_sent_type_res = self.kernel.respond(sentence_type, sessionId)
                        except:
                            aiml_sent_type_res = ""
                        if len(aiml_sent_type_res) > 1:
                            sentence_response += " " + aiml_sent_type_res

                emoi = self.kernel.respond(sent["emotion"])
                if random.random() <= emotion_th[sent["emotion"]]:
                    sentence_response += " " + emoi
                
                if len(sentence_response) > 1:
                    sentence_response = sentence_response[0].upper() + sentence_response[1:]
                    arr_response.append(sentence_response)

            response = ""

            for res in arr_response:
                response += res + " "

            if len(response) > 0:
                response = reformulate(response)
            else:
                aiml_generic = self.kernel.respond("FILTER INSULT", sessionId)
                response = aiml_generic

        except Exception as e:
            response = str(e)
            if random.random() < 0.5:
                response = song_review()
            else:
                response = song_suggestion()
            wait = 100

        return (response, wait)


if __name__ == "__main__":
    song_review()
