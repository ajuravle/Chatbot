from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from random import randint
import nltk.data


def reformulate(init_sentence):
	"""
	Reformulates a given input text.
	Code written by:
	- Ene Andrei
	- Gurau Marian
	- Latu Bogdan
	:param init_sentence: Sentence to be reformulated (str)
	:return: A reformulated sentence (str)
	"""

	output = ""
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	tokenized = tokenizer.tokenize(init_sentence)
	words = word_tokenize(init_sentence)
	tagged = nltk.pos_tag(words)
	
	for i in range(0,len(words)):
		replacements = []
		
		for syn in wordnet.synsets(words[i]):
			
			if tagged[i][1] == 'NNP' or tagged[i][1] == 'DT':
				break
			
			word_type = tagged[i][1][0].lower()
			
			if syn.name().find("."+word_type+"."):
				r = syn.name()[0:syn.name().find(".")]
				replacements.append(r)
	
		if len(replacements) > 0:
			replacement = replacements[randint(0,len(replacements)-1)]
			output = output + " " + replacement
		else:
			output = output + " " + words[i]
		#print(replacements)
	print (output)

reformulate("In truth money stopped meaning anything to most people two generations ago because the government provides all necessities for free.")
