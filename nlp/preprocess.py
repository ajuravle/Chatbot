import nltk
import ner
import nltk.data
from nltk.corpus.reader import path_similarity, Synset
from nltk.stem import WordNetLemmatizer
import language_check
from nltk.corpus import wordnet as wn
import collections

from langdetect import detect

st = nltk.StanfordNERTagger(
    "nlp/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz",
    "nlp/stanford-ner-2015-12-09/stanford-ner.jar")

tool = language_check.LanguageTool('en-US')
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
wordnet_lemmatizer = WordNetLemmatizer()


def check_grammar(text):
    matches = tool.check(text)
    len(matches)
    text = language_check.correct(text, matches)
    return text


def get_sentences(text):
    sentenced_text = sent_detector.tokenize(text.strip())
    return sentenced_text


def tokenize_text(text):
    tokenized_text = nltk.tokenize.word_tokenize(text)
    return tokenized_text


def lemmatize_text(text):
    return wordnet_lemmatizer.lemmatize(text)


def pos_tag_text(text):
    return nltk.pos_tag(text)


def ner_tag_text(text):
    return st.tag(text.split())


def get_synonyms(word):
    synonyms = wn.synsets(word)
    synonyms_list = list()
    synonym_info = collections.namedtuple("synonym_info", ["synonym"])
    for synset in synonyms:
        for lemma in synset.lemmas():
            syn_info = synonym_info(lemma.name())
            synonyms_list.append(syn_info)
            # print(lemma)
    return synonyms_list


def process_text():
    path = "input.txt"
    text = open(path, "r").read()

    ##grammar check
    text = check_grammar(text)

    ##sentence splitting
    sentenced_text = get_sentences(text)

    i = 0
    for sentence in sentenced_text:
        i = int(i + 1)
        print (i.__str__() + '\n' + sentence + '\n')
        ## tokenize each sentence
        tokenized_text = tokenize_text(sentence)

        ##POS-Tag
        print(pos_tag_text(tokenized_text))

        ##lemmatize each sentence
        # for token in tokenized_text:
        # print(lemmatize_text(token))

        ##Stanford NER
        # print(ner_tag_text(sentence))

    # print(detect("War doesn't show who's right, just who's left."))
    # print(detect("Ein, zwei, drei, some dogs were here before you vier"))
    for syn in get_synonyms('small'):
        print (syn)
        # print(path_similarity(Synset('shrimp.n.03'), Synset('pearl.n.01')))


if __name__ == "__main__":
    process_text()
