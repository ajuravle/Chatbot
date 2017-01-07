import unittest
import brain

b = brain.Brain()

class TestBrain(unittest.TestCase):

    def test_dialogue_act_features(self):
        self.assertEqual(brain.dialogue_act_features("Ana has apples"), {'contains(ana)': True, 'contains(has)': True, 'contains(apl)': True})

    def test_dialogue_act_features_null(self):
        self.assertEqual(brain.dialogue_act_features(""), {})

if __name__ == '__main__':
    unittest.main()