import re

def validate_aiml_document(path):
    try:
        with open(path, 'r') as content_file:
            content = content_file.read()

        content = content.replace("\n","")
        return re.match(".*<aiml>.*(<category>.*<pattern>.*</pattern>.*<template>.*</template>.*</category>)*.*</aiml>.*", content) != None

    except Exception as e:
        print type(e),str(e)

    except Exception as e:
        print type(e),str(e)


def main():
    print validate_aiml_document("../knowledge/Computers.aiml")
    print validate_aiml_document("../knowledge/geography.aiml")
    print validate_aiml_document("../knowledge/history.aiml")
    print validate_aiml_document("../knowledge/literature.aiml")
    print validate_aiml_document("../knowledge/salutations.aiml") # lipseste <aiml> ... </aiml> 13.12.2016
main()
