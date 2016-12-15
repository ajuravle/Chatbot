import aiml
import os
from nlp import preprocess as nlp

kernel = aiml.Kernel()
sessionId = 12345

if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles="./knowledge/startup.xml", commands="load aiml b")
    kernel.saveBrain("bot_brain.brn")


def sentence_response(message):
    return nlp.get_sentences(message)[-1]


def aiml_respone(message):
    return kernel.respond(message, sessionId)

if __name__ == "__main__":
    print(aiml_respone(raw_input("You: ")))
