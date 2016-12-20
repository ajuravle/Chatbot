from nlp import preprocess as nlp

def test_check_grammar():

    if nlp.check_grammar("Whats IP?") == "What's IP?": print "Whats IP?","correct"
    else: print "ex.1","wrong",nlp.check_grammar("Whats IP?")

    if nlp.check_grammar("Where are Romania?") == "Where is Romania?": print "Where are Romania?","correct"
    else: print "ex.2","wrong",nlp.check_grammar("Where are Romania?")

    list = []
    list.append("Rachel is very smart. She began reading when she was three years old.")
    list.append("Rachel is very smart; she began reading when she was three years old.")
    list.append("Rachel is very smart, and she began reading when she was three years old.")
    list.append("Rachel is very smart, she began reading when she was three years old.")
    list.append("Rachel is very smart; as a result, she began reading when she was three years old.")

    if nlp.check_grammar("Rachel is very smart, she began reading when she was three years old.") in list:
        print  "ex.3", "correct"
    else:
        print  "ex.3","wrong",nlp.check_grammar("Rachel is very smart, she began reading when she was three years old.")

    if nlp.check_grammar(" Everybody must bring their own lunch.") == "Everybody must bring his own lunch." or nlp.check_grammar(" Everybody must bring their own lunch.") == "Everybody must bring her own lunch.":
        print "ex.4", "correct"
    else:
        print "ex.4", "wrong",nlp.check_grammar(" Everybody must bring their own lunch.")

    if nlp.check_grammar("My mothers cabin is next to his' cabin.") == "My mother's cabin is next to his cabin.":
        print "ex.5", "correct"
    else:
        print "ex.5", "wrong",nlp.check_grammar("My mothers cabin is next to his' cabin.")

    if nlp.check_grammar("Its a cold day in October.") == "It's a cold day in October.":
        print "ex.6", "correct"
    else:
        print "ex.6", "wrong",nlp.check_grammar("Its a cold day in October.")

    if nlp.check_grammar("The recipes is good for beginning chefs.") == "The recipes are good for beginning chefs.":
        print "ex.7", "correct"
    else:
        print "ex.7", "wrong",nlp.check_grammar("The recipes is good for beginning chefs.")

    if nlp.check_grammar("At eight years old, my father gave me a pony for Christmas.") == "When I was eight years old, my father gave me a pony for Christmas.":
        print "ex.8", "correct"
    else:
        print "ex.8", "wrong",nlp.check_grammar("At eight years old, my father gave me a pony for Christmas.")

    if nlp.check_grammar("I go to the store and I bought milk.") == "I go to the store and I buy milk.":
        print "ex.9", "correct"
    else:
        print "ex.9", "wrong",nlp.check_grammar("I go to the store and I bought milk.")

    if nlp.check_grammar("Matt like fish.") == "Matt likes fish.":
        print "ex.10", "correct"
    else:
        print "ex.10", "wrong",nlp.check_grammar("Matt like fish.")

    if nlp.check_grammar("Anna and Pat are married and he has been married for 20 years.") == "Anna and Pat are married and they have been married for 20 years.":
        print "ex.11", "correct"
    else:
        print "ex.11", "wrong",nlp.check_grammar("Anna and Pat are married and he has been married for 20 years.")

    if nlp.check_grammar("Everyone forgot their notebook.") == "Everyone forgot his notebook." or nlp.check_grammar("Everyone forgot their notebook.") == "Everyone forgot her notebook.":
        print "ex.12", "correct"
    else:
        print "ex.12", "wrong",nlp.check_grammar("Everyone forgot their notebook.")

#test_check_grammar()
#test gramar checked
#nu tine cont de timpurile verbale si alte chestii de exprimare
#corecteaza sintaxa cuvintelor
