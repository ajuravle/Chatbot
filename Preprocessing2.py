# import ner
import nltk
import nltk.data
from nltk.corpus.reader import path_similarity, Synset
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

import language_check
from langdetect import detect
import collections
import json

# ***************************************************************************************************
# Stanford parser -> constituency tree
# http://nlp.stanford.edu/software/lex-parser.shtml
# installation: http://stackoverflow.com/questions/13883277/stanford-parser-and-nltk
import os
from nltk.parse import stanford


def stanford_parser_tree(sentences):
    os.environ[
        'STANFORD_PARSER'] = 'D:/Facultate anul 3/AI/Projectlibraries/stanford-parser-full-2016-10-31/stanford-parser.jar'
    os.environ[
        'STANFORD_MODELS'] = 'D:/Facultate anul 3/AI/Projectlibraries/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar'

    parser = stanford.StanfordParser(model_path="E:/FII/3/IA/stanford-parser-and-models/jars/englishPCFG.ser.gz")
    sentences = parser.raw_parse_sents((sentences))
    return sentences
    # GUI
    # for line in sentences:
    #     for sentence in line:
    #         print(sentence)
    # sentence.draw()


##Stanford Dependency Parser
##http://nlp.stanford.edu/software/stanford-dependencies.shtml
##installation: http://stackoverflow.com/questions/34053021/stanford-dependency-parser-setup-and-nltk

import nltk
import os


# data={"language-text":{"value":language,
#				"sentence-text":{"value":sentence,
#				"word":{
#				"value":tokenized_text,
#				"morfology":pos_tag_text(tokenized_text),
#				"dictionary":lematize_text(token),
#				"ner":ner_tag_text(sentence),
#				"synonyms":}
#				}
#			}
#		}

def tree_to_dict(tree):
    tree_dict = {}
    for t in tree:
        if isinstance(t, nltk.Tree) and isinstance(t[0], nltk.Tree):
            tree_dict[t.label()] = tree_to_dict(t)
        elif isinstance(t, nltk.Tree):
            tree_dict[t.label()] = t[0]
    return tree_dict


def stanford_dependency_tree(sentences):
    java_path = "C:\\Program Files\\Java\\jre1.8.0_101\\bin\\java.exe"
    os.environ['JAVAHOME'] = java_path

    from nltk.parse import stanford
    os.environ[
        'STANFORD_PARSER'] = 'D:/Facultate anul 3/AI/Projectlibraries/stanford-parser-full-2016-10-31/stanford-parser.jar'
    os.environ[
        'STANFORD_MODELS'] = 'D:/Facultate anul 3/AI/Projectlibraries/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar'
    parser = stanford.StanfordDependencyParser(
        model_path="E:/FII/3/IA/stanford-parser-and-models/jars/englishPCFG.ser.gz")

    sentences = parser.raw_parse_sents(sentences)
    return sentences




st = nltk.StanfordNERTagger(
    "E:/FII/3/IA/stanford-ner-2015-12-09/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz",
    "E:/FII/3/IA/stanford-ner-2015-12-09/stanford-ner-2015-12-09/stanford-ner.jar")


def check_grammar(text):
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(text)
    len(matches)
    text = language_check.correct(text, matches)
    return text


def get_sentences(text):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentenced_text = sent_detector.tokenize(text.strip())
    return sentenced_text


def tokenize_text(text):
    tokenized_text = nltk.tokenize.word_tokenize(text)
    return tokenized_text


def lemmatize_text(text):
    wordnet_lemmatizer = WordNetLemmatizer()
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
    processed_text = dict()

    language = detect(text)  # de adaugat in JSON
    processed_text["language"] = language

    if language == 'en':
        # grammar check
        text = check_grammar(text)

        # sentence splitting
        sentenced_text = get_sentences(text)

        # Stanford parsing trees
        sentence_parser_result = stanford_parser_tree(sentenced_text)
        parser_trees_list = list()
        for trees_list in sentence_parser_result:
            for tree in trees_list:
                parser_trees_list.append(tree_to_dict(tree))
        # sentence.draw()  ##for visual representation and better understanding

        # Stanford dependency trees
        dependency_parser_result = stanford_dependency_tree(sentenced_text)
        dependency_trees_list = list()
        for trees_list in dependency_parser_result:
            for dependency_graph in trees_list:
                dependency_trees_list.append(str(dependency_graph))

        sentences = dict()

        sentence_index = 0
        for sentence in sentenced_text:
            key = "sentence_%d_data" % (sentence_index + 1)
            # sentence_counter = int(sentence_counter + 1)
            # key += str(sentence_counter)
            # print(i.__str__() + '\n' + sentence + '\n')

            ## tokenize each sentence
            tokenized_text = tokenize_text(sentence)

            aux = dict()
            aux["sentence"] = sentence
            aux["tokenized_sentence"] = tokenized_text
            aux["parsed_tree_dict"] = parser_trees_list[sentence_index]
            aux["dependency_tree_str"] = dependency_trees_list[sentence_index]

            ##POS-Tag
            pos_tagged_text = pos_tag_text(tokenized_text)
            aux["pos_tagged_text"] = pos_tagged_text

            ##lemmatize each sentence
            # for token in tokenized_text:
            #     lemmatization = lemmatize_text(token)
            #     print(lemmatization)

            ##Stanford NER
            ner_tagged_text = ner_tag_text(sentence)
            aux["ner_tagged_text"] = ner_tagged_text

            synonyms = dict()
            for token in tokenized_text:
                token_syn = list()
                for syn in get_synonyms(token):
                    token_syn.append(syn.synonym)
                synonyms[token] = token_syn
            aux["words_synonyms"] = synonyms

            sentence_index += 1
            sentences[key] = aux

        processed_text["sentences"] = sentences
        processed_text["sentence_count"] = sentence_index

        # print(path_similarity(Synset('shrimp.n.03'), Synset('pearl.n.01')))

    with open('jsonfile.json', 'w') as f:
        json.dump(processed_text, f)


process_text()

# nltk.help.upenn_tagset()


##Fisierul JSON va trebui sa contina ceea ce e cu 'print' mai sus (chiar daca print-urile sunt comentate).
