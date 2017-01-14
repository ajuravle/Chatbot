from nlp import preprocess as nlp
import unittest

class TestTextProcessingComponents(unittest.TestCase):

    # test get_sentences(text)
    def test_get_sentences1(self):
        self.assertEqual(nlp.get_sentences(""),[])

    def test_get_sentences2(self):
        self.assertEqual(nlp.get_sentences("Ana has apples."),["Ana has apples."])

    def test_get_sentences3(self):
        self.assertEqual(nlp.get_sentences("Ana has apples. Ana has oranges."), ["Ana has apples.", "Ana has oranges."])

    def test_get_sentences4(self):
        self.assertEqual(nlp.get_sentences("Ana has apples... Ana has oranges"), ["Ana has apples...", "Ana has oranges."])

    def test_get_sentences5(self):
        self.assertEqual(nlp.get_sentences("sjfhnsdgfjgdhig chjsdgfug efidbgucbd"), ["sjfhnsdgfjgdhig chjsdgfug efidbgucbd"])

    def test_get_sentences6(self):
        self.assertEqual(nlp.get_sentences("Ana has: apples, oranges and lemons."), ["Ana has: apples, oranges and lemons."])

    #---------------------------------------------------------------------------------------------------------------------

    #test tokenize_text(text)
    def test_tokenize_text1(self):
        self.assertEqual(nlp.tokenize_text(""), [])

    def test_tokenize_text2(self):
        self.assertEqual(nlp.tokenize_text("Ana has apples."), ['Ana', 'has', 'apples', '.'])

    def test_tokenize_text3(self):
        self.assertEqual(nlp.tokenize_text("..."), ['...'])

    def test_tokenize_text4(self):
        self.assertEqual(nlp.tokenize_text("This is Mihai-Viteazul."), ['This', 'is', 'Mihai-Viteazul', '.'])

    # ---------------------------------------------------------------------------------------------------------------------

    # test lemmatize_text(text) -> text = cuvant  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def test_lemmatize_text1(self):
        self.assertEqual(nlp.lemmatize_text(""), "")

    def test_lemmatize_text2(self):
        self.assertEqual(nlp.lemmatize_text("are"), "be")

    def test_lemmatize_text3(self):
        self.assertEqual(nlp.lemmatize_text("am"), "be")

    def test_lemmatize_text4(self):
        self.assertEqual(nlp.lemmatize_text("cars"), "car")

    def test_lemmatize_text5(self):
        self.assertEqual(nlp.lemmatize_text("bought"), "buy")

    def test_lemmatize_text6(self):
        self.assertEqual(nlp.lemmatize_text("walked"), "walk")

    def test_lemmatize_text7(self):
        self.assertEqual(nlp.lemmatize_text("Ana"), "Ana")

    # ---------------------------------------------------------------------------------------------------------------------

    # test pos_tag_text(text) -> text = lista cuvinte !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def test_pos_tag_text1(self):
        self.assertEqual(nlp.pos_tag_text([]), [])

    def test_pos_tag_text2(self):
        self.assertEqual(nlp.pos_tag_text(['Ana','has','apples']), [('Ana', 'NNP'), ('has', 'VBZ'), ('apples', 'NNS')])

    # ---------------------------------------------------------------------------------------------------------------------

    # test ner_tag_text(text)

    def test_ner_tag_text1(self):
        self.assertEqual(nlp.ner_tag_text(""), [])

    def test_ner_tag_text2(self):
        self.assertEqual(nlp.ner_tag_text("Ana"), [('Ana', 'PERSON')])

    def test_ner_tag_text3(self):
        self.assertEqual(nlp.ner_tag_text("Everest"), [('Everest', 'O')])

    def test_ner_tag_text4(self):
        self.assertEqual(nlp.ner_tag_text("apple"), [('apple', 'O')])


    # ---------------------------------------------------------------------------------------------------------------------

    # test get_synonyms(text)

    def test_get_synonyms1(self):
        self.assertEqual(nlp.get_synonyms(""), [])

    def test_get_synonyms2(self):
        self.assertNotEqual(nlp.get_synonyms("paradigm"), [])

    def test_get_synonyms3(self):
        self.assertNotEqual(nlp.get_synonyms("fortify"), [])

    def test_get_synonyms4(self):
        self.assertNotEqual(nlp.get_synonyms("failure"), [])

    def test_get_synonyms5(self):
        self.assertEqual(nlp.get_synonyms("dtcfyghtdrct"), [])

if __name__ == '__main__':
    unittest.main()