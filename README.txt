Chat bot

Informatii necesare in ceea ce priveste chatbot-ul

LOCAL INSTALLING STEPS (pentru modulul 4, necesar la testare)
PAS I
descarca arhiva de pe GitHub

PAS II
trebuie sa iti instalezi python 2.7 versiunea pe 64 biti
iti dau eu un link
https://www.python.org/ftp/python/2.7.13/python-2.7.13.amd64.msi

PAS III
dupa ce instalezi python
pip install -r /path/to/requirements.txt
trebuie sa dai comanda asta
este un fisier "requirements.txt in codul de pe github
sa dai calea catre el
(exemplu pip install -r C:/Users/AndreeaI/Chatbot-Master/requirements.txt)
(atentie, pentru cei carora nu le merge pip pot pune inainte py -2 -m <comanda de mai sus>)

PAS IV
intri pe http://aka.ms/vcpython27 si descarci installerul dupa cate il rulezi 

PAS V
apoi urmeaza o parte mai lunga de downloadat
"pip install -U spacy"
(la fel, py -2 -m pip install -U spacy)
(daca apar promptere de la microsoft .net dai install)

PAS VI
si dupa "python -m spacy.en.download all"

PAS VII 
Du-te in folderul cu chatbot
Deschide un cmd acolo (shift + Click Dreapta)
Scrie python sau py -2 (dupa caz)
vezi daca e versiunea 2.7 pe 64 biti
>>>import nltk 
>>>nltk.download()
aici ar trebui sa se deschida o noua fereastra, daca se intampla asta 
daca nu se deschide o noua fereastra ci apare nltk downloader si un meniu cu mai multe optiuni (in aceasi fereastra) urmeaza pasul VIII A 

PAS VIII A 
Descarca urmatoarele 2 arhive de pe wetransfer
https://wetransfer.com/downloads/9546a1e85517bb15153e18d3b3ebea1b20161227201605/8e9b6a
https://wetransfer.com/downloads/d3d927efef88c91b32f76d77cd6e6ba320161227202259/ca8648
ATENTIE EXPIRA IN 7 ZILE. dupa le puteti cere de la Cristi sau de la mine. 
dearhiveaza fisierele in dosarul nlp din bot el urmand sa aiba urmatoarele foldere si fisiere 
	->chunkers
	->corpora
	->grammars
	->help
	->misc
	->models
	->sentiment
	->standford....
	->stemmers
	->taggers
	->tokenizers
	->.gitignore
	->__init__(.py)
	->__init__(.pyc)
	->preprocess(.py)
	->preprocess(.pyc)
	
PAS IX
downloadezi arhiva de la link-ul https://l.facebook.com/l.php?u=https%3A%2F%2Fpypi.python.org%2Fpackages%2F9a%2F5a%2F6aaa7bef798504cafe5ecd06cf4d274c492f387c5e1e58e57dc53f672f61%2Fner-0.1.tar.gz%23md5%3Dd4fa19d0d2496e8aedc5354a34281e04&h=wAQFIPdR_
o dezarhivezi dupa care rulezi comanda 
->python setup.py install (sau py -2 setup.py install)

->pip install pattern sau py -2 -m pip install pattern

PAS X
pip install flask
apoi python server.py
si astepti sa porneasca toate chestiile (poate dura vreo 2 minute)
dupa ce se termina intra pe http://localhost:5000/
