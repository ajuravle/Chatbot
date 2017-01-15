import aiml
import unittest

# Create the kernel and learn AIML files
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")

class TestAIML(unittest.TestCase):

    def test_aiml1(self):
        print 1,kernel.respond("")
        self.assertEqual(kernel.respond(""),"")

    def test_aiml2(self):
        print 2,kernel.respond("WHAT IS YOUR FAVORITE SONG")
        self.assertNotEqual(kernel.respond("WHAT IS YOUR FAVORITE SONG"),"")

    def test_aiml3(self):
         self.assertNotEqual(kernel.respond("WHAT DO YOU THINK ABOUT OBAMA"), "")

    def test_aiml4(self):
         self.assertNotEqual(kernel.respond("WHAT IS EVEREST"), "")

    def test_aiml5(self):
        print 5,kernel.respond("DO YOU SING")
        self.assertNotEqual(kernel.respond("DO YOU SING"), "")

    def test_aiml6(self):
         self.assertEqual(kernel.respond("WHO IS HARRY POTTER?"), "Harry Potter is the main character from the books and movies with the same name")
    def test_aiml7(self):
         self.assertEqual(kernel.respond("WHO IS HITLER?"), "Some say Hitler was the most evil man who ever lived.")

    def test_aiml8(self):
        print 8,kernel.respond("ARE YOU A NICE PERSON?")
        self.assertNotEqual(kernel.respond("ARE YOU A NICE PERSON?"), "")

    def test_aiml9(self):
        self.assertNotEqual(kernel.respond("WHAT IS YOUR NAME?"), "")

    def test_aiml10(self):
        self.assertNotEqual(kernel.respond("WHAT DO YOU KNOW ABOUT EVEREST?"), "")



if __name__ == '__main__':
    unittest.main()