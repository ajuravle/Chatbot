import aiml, sys
from nlp import preprocess as nlp

# Create the kernel and learn AIML files

kernel = aiml.Kernel()
kernel.learn("./startup.xml")
kernel.respond("load aiml b")


def sentence_response(message):
	return nlp.get_sentences(message)[-1]

def aiml_respone(message):
	return kernel.respond(message)
