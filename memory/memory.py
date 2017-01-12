from spacy.symbols import *


first_person = ["me", "i", "mine", "my", "we", "ours"]
pron_translate = dict()
pron_translate["me"] = "you"
pron_translate["i"] = "you"
pron_translate["mine"] = "your"
pron_translate["my"] = "your"
pron_translate["ours"] = "your"
pron_translate["we"] = "you"


class Memory:
    def __init__(self, spacy_nlp):
        self.memory = dict()
        self.spacy_nlp = spacy_nlp

    def forget(self):
        self.memory.clear()

    def contains(self, sessionId):
        return sessionId in self.memory

    def respond(self, verbs_subj, sentence_type, sessionId):
        memory = self.memory
        spacy_nlp = self.spacy_nlp
        if sessionId not in memory:
            memory[sessionId] = dict()
        memory_msg = ""
        if sentence_type != "whQuestion":
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
                                    memory_msg = "memorate"
                        elif c.dep in [dobj, pobj, attr]:
                            memory[sessionId][vb][subj] = c.text
                            memory_msg = "memorate"
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
                    memory_msg = ""
                    for subj in subjs:
                        if subj in memory[sessionId][verb]:
                            toks = spacy_nlp(subj)
                            memory_msg = ""
                            for t in toks:
                                if t.lower_ in first_person:
                                    memory_msg += pron_translate[t] + " "
                                else:
                                    memory_msg += t + " "
                            num_subjs -= 1
                            if num_subjs > 2:
                                memory_msg += ", "
                            elif num_subjs == 1:
                                memory_msg += "and "
                    if len(memory_msg) > 0:
                        memory_msg += verb + " "
                        if num_subjs != len(subjs):
                            memory_msg += memory[sessionId][verb][subjs[-1]] + "."
        return memory_msg
