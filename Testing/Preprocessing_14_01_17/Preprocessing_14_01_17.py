# import ner
import concurrent
from concurrent.futures import ALL_COMPLETED
from concurrent.futures import ProcessPoolExecutor

import nltk
import os
import nltk.data
from nltk.corpus.reader import path_similarity, Synset, time
from nltk.parse import stanford
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

def stanford_parser_tree(sentences):
    os.environ[
        'STANFORD_PARSER'] = 'C:/Users/andre/Documents/IA/Chatbot-master/nlp/stanford-parser-full-2016-10-31/stanford-parser.jar'
    os.environ[
        'STANFORD_MODELS'] = 'C:/Users/andre/Documents/IA/Chatbot-master/nlp/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar'

    parser = stanford.StanfordParser(model_path="C:/Users/andre/Documents/IA/Chatbot-master/nlp/englishPCFG.ser.gz")
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
    java_path = "C:\\Program Files\\Java\\jre1.8.0_111\\bin\\java.exe"
    os.environ['JAVAHOME'] = java_path

    from nltk.parse import stanford
    os.environ[
        'STANFORD_PARSER'] = 'C:/Users/andre/Documents/IA/Chatbot-master/nlp/stanford-parser-full-2016-10-31/stanford-parser.jar'
    os.environ[
        'STANFORD_MODELS'] = 'C:/Users/andre/Documents/IA/Chatbot-master/nlp/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar'
    parser = stanford.StanfordDependencyParser(
        model_path="C:/Users/andre/Documents/IA/Chatbot-master/nlp/englishPCFG.ser.gz")

    sentences = parser.raw_parse_sents(sentences)
    return sentences


st = nltk.StanfordNERTagger(
    "C:/Users/andre/Documents/IA/Chatbot-master/nlp/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz",
    "C:/Users/andre/Documents/IA/Chatbot-master/nlp/stanford-ner-2015-12-09/stanford-ner.jar")


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
    synonyms_set = set()
    synonym_info = collections.namedtuple("synonym_info", ["synonym"])
    for synset in synonyms:
        for lemma in synset.lemmas():
            syn_info = synonym_info(lemma.name())
            synonyms_set.add(syn_info)
            # print(lemma)

    return synonyms_set


from multiprocessing import Pool, TimeoutError, Process

def queue_sentence_process(proc_pool_executor, sentence):
    future = proc_pool_executor.submit(process_sentence, sentence)



def batch_async_process(sentences_list):
    """
    Starts asynchronous parsing for the given list of sentences.
    :param sentence_list: a list of (str)sentences
    :return: A list of the parsing results. Every list item is a sentence parsing result
    """
    SIMULTANEOUS_PROC_COUNT = 3
    process_pool_executor = ProcessPoolExecutor(SIMULTANEOUS_PROC_COUNT)
    parsing_results_list = []

    while len(sentences_list) % SIMULTANEOUS_PROC_COUNT != 0:
        sentences_list.append(None)

    sentence_index = 0
    sentence_count = len(sentences_list)
    while sentence_index < sentence_count:
        future_results = []
        while len(future_results) < SIMULTANEOUS_PROC_COUNT and sentence_index < sentence_count:
            current_sentence = sentences_list[sentence_index]
            future_result = process_pool_executor.submit(process_sentence, current_sentence)
            future_results.append(future_result)
            sentence_index += 1

        results = concurrent.futures.wait(future_results, timeout=None, return_when=ALL_COMPLETED)
        for done in results[0]:
            # print("done_future: ", done.result())
            result = done.result()
            if result is not None:
                parsing_results_list.append(result)

    return parsing_results_list


def process_sentence(sentence):
    if sentence is not None:
        # print('Started parsing: "{0}"'.format(sentence))

        # grammar check
        # start_time = time.time()
        text = check_grammar(sentence)
        # print("Grammar check took: " + (time.time() - start_time).__str__() + " seconds.")

        # Stanford parsing trees
        # start_time = time.time()
        sentence_parser_result = stanford_parser_tree(sentence)
        parser_trees_list = list()
        for trees_list in sentence_parser_result:
            for tree in trees_list:
                parser_trees_list.append(tree_to_dict(tree))
        # print("Parsing tree took: " + (time.time() - start_time).__str__() + " seconds.")

        # Stanford dependency trees
        # start_time = time.time()
        dependency_parser_result = stanford_dependency_tree(sentence)
        dependency_trees_list = list()
        for trees_list in dependency_parser_result:
            for dependency_graph in trees_list:
                dependency_trees_list.append(str(dependency_graph))
        # print("Dependency tree took: " + (time.time() - start_time).__str__() + " seconds.")

        ## tokenize each sentence
        # start_time = time.time()
        tokenized_text = tokenize_text(sentence)
        # print("Tokenization took: " + (time.time() - start_time).__str__() + " seconds.")

        aux = dict()
        aux["sentence"] = sentence
        aux["tokenized_sentence"] = tokenized_text
        aux["parsed_tree_dict"] = parser_trees_list[0]
        aux["dependency_tree_str"] = dependency_trees_list[0]

        # Stanford NER
        # start_time = time.time()
        ner_tagged_text = ner_tag_text(sentence)
        aux["ner_tagged_text"] = ner_tagged_text
        # print("NER Tagging took: " + (time.time() - start_time).__str__() + " seconds.")

        ##POS-Tag
        # start_time = time.time()
        pos_tagged_text = pos_tag_text(tokenized_text)
        aux["pos_tagged_text"] = pos_tagged_text
        # print("POS Tagging took: " + (time.time() - start_time).__str__() + " seconds.")

        # Synonyms
        # start_time = time.time()
        synonyms = dict()
        for token in tokenized_text:
            token_syn = list()
            for syn in get_synonyms(token):
                token_syn.append(syn.synonym)
            synonyms[token] = token_syn
        aux["word_synonyms"] = synonyms
        # print("Synoyms took: " + (time.time() - start_time).__str__() + " seconds.")

        print(sentence, "DONE!")
        return aux


def process_text():
    if __name__ == '__main__':
        start_time_zero = time.time()

        path = "input.txt"
        text = open(path, "r").read()
        processed_text = dict()

        try:
            start_time = time.time()
            language = detect(text)  # de adaugat in JSON
        except:
            print("Language detection error: No features in text")
            language = 'unknown'
        finally:
            print("Language detection took: " + (time.time() - start_time).__str__() + " seconds.")
            processed_text["language"] = language

        if language == 'en':
            start_time = time.time()
            sentences_list = get_sentences(text)
            print("Sentence splitting took: " + (time.time() - start_time).__str__() + " seconds.")

            sentences = batch_async_process(sentences_list)

            for result in sentences:
                print(result)

            processed_text["sentences_count"] = len(sentences)
            processed_text["sentences"] = sentences

            # print(path_similarity(Synset('shrimp.n.03'), Synset('pearl.n.01')))

        start_time = time.time()
        with open('jsonfile.json', 'w') as f:
            json.dump(processed_text, f)
        print("JSON dumping took: " + (time.time() - start_time).__str__() + " seconds.")
        print("Total time is: " + (time.time() - start_time_zero).__str__() + " seconds")


# nltk.help.upenn_tagset()


##Fisierul JSON va trebui sa contina ceea ce e cu 'print' mai sus (chiar daca print-urile sunt comentate).


# process_text()


import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler, FileModifiedEvent


class MyHandler(PatternMatchingEventHandler):
    def process(self, event):
        super()


    def on_modified(self, event):
        # print(event._src_path)
        if os.path.basename(event._src_path) == "input.txt":
            print("MODIFICATION OCCURED!")
            print("Starting processing....")
            print(event._src_path)
            process_text()
        self.process(event)


        # else:
            # print("Not our file!")


    def on_created(self, event):
        print("Created")
        self.process(event)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = LoggingEventHandler()
    my_handler = MyHandler()
    observer = Observer()
    observer.schedule(my_handler, "C:\\Users\\andre\\Documents\\IA\\Chatbot-master\\Testing\\Preprocessing_14_01_17", recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()