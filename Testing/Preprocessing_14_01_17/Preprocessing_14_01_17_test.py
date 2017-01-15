import Testing.Preprocessing_14_01_17.Preprocessing_14_01_17 as nlp
import unittest
import json
import time
from pprint import pprint

class TestTextProcessing(unittest.TestCase):
    def test1(self):
        f=open("input.txt","wt")
        f.write("")
        f.close()

        time.sleep(20);

        with open('jsonfile.json') as data_file:
            data = json.load(data_file)

        self.assertNotEqual(data, {})

    def test2(self):
        f=open("input.txt","wt")
        f.write("ha2sf2345odh345lfhfdg4.,54d#$%#^,.65dr4g5544545v545")
        f.close()

        time.sleep(20);

        with open('jsonfile.json') as data_file:
            data = json.load(data_file)

        pprint(data)
        self.assertNotEqual(data, {})

    def test3(self):
        f=open("input.txt","wt")
        f.write("21321345")
        f.close()

        time.sleep(20);

        with open('jsonfile.json') as data_file:
            data = json.load(data_file)

        pprint(data)
        self.assertEqual(data, {'language': 'unknown'})

    def test4(self):
        f=open("input.txt","wt")
        f.write("The Pale Emperor is the ninth studio album by American rock band Marilyn Manson.")
        f.close()

        time.sleep(20);

        with open('jsonfile.json') as data_file:
            data = json.load(data_file)

        pprint(data)
        self.assertNotEqual(data, {'language': 'unknown'})

    def test5(self):
        f=open("input.txt","wt")
        f.write("Ana has apples.")
        f.close()

        time.sleep(20);

        with open('jsonfile.json') as data_file:
            data = json.load(data_file)

        pprint(data)
        self.assertNotEqual(data, {'language': 'unknown'})

    def test6(self):
        f = open("input.txt", "wt")
        f.write("Ion has 12 years old.")
        f.close()

        time.sleep(20);

        with open('jsonfile.json') as data_file:
            data = json.load(data_file)

        pprint(data)
        self.assertNotEqual(data, {'language': 'unknown'})

    def test7(self):
        f = open("input.txt", "wt")
        f.write("This is very important for you to remember – sometimes, you’ll hear and see something but most times, it will be an image that flashed before your closed eyes. ")
        f.close()

        time.sleep(20);

        with open('jsonfile.json') as data_file:
            data = json.load(data_file)

        pprint(data)
        self.assertNotEqual(data, {'language': 'unknown'})

if __name__ == '__main__':
    unittest.main()
