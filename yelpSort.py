import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import re, collections
import sys

w1 = wordnet.synsets("store")
l = list()
##file = open('sample.txt')
##synonyms = []
##iter = 0
##for i in w1:
##    print(w1[iter].definition())
##    iter += 1
##    for j in w1[0].lemmas():
##        print("l:",j)
##        synonyms.append(j.name())
##
##print(set(synonyms))
# isBgs = open("isBgs.txt").readlines()
file = open("sample.txt")
evid = open("ReviewCount.txt")
r = file.readlines()
count = 0
nor = 0
flags = 0
BGS = False
#We go through the file first to look for certain key terms in our list
#If the string of words is found in the file, we automatically call it a bgs
#and pass it into the store db.
'''
for i in range(0,len(r)):
    for j in isBgs:
        if j in  r[i].lower():
            BGS = true
            #pass it into the store db code goes here.
            sys.exit()
'''
#Next thing we check to see if the name of the shop contains the base word game, e.g. game, gamer, gaming, games, all would be advertisements of the main selling point of games, therefore board games.

#Code to check if the name of the store contains the base word game goes here.


'''
If the initial check fails, we need to create a different method to search for.
A game store by definition of reviews will contain at least one of the following items.
A list of genre's of games, such as card games, board games, trading card games, Role playing games
    NOTE: Must be an obscure term within the genre, so adjectives such as physical, mental, exciting, may not refer to an actual board game
    (E.g: Escape Room store: Exodus Escape Room.txt store)
     By Definition of a  store as well: this merchandise will be known as a selection, stock, or even "store" as a Verb describing an object.
     This SELECTION of items must be items that we deem are merchandise of a board game store, therefore a reviewer of a board game store must describe
     a "Stock" of genres of games that are appropriate
A "Community" centered around gaming, so terms such as gaming community
    Within a community setting we can search for the following items,
    Tournaments (If the string game is mentioned as a subject within a review) we can assume the types of tournaments are game tournaments)
    Gaming "Area": Basically an area where people are able to actually play games, this is commonly refered to in reviews as tables, gaming area, etc.
It must also be a "store", meaning by definition the only type of description of a store should ever be a "board game store" as a singular noun, or NNS
    The merchandise of a store must be in consistence with that of the geek culture, meaning we must check the selection of stock the reviewers describe.
    The stock must contain MAINLY stock in relations to games and maybe comic books. If a stores main attraction by reviewers is noted to be other stock that is not considered secondary
    E.g, t-shirts, snacks, etc. Then it is not a gaming store.
'''
stopwords = set(stopwords.words("english"))
stopwords.update(['.',',','!'])
swl = []
bagofwords = []
checkWords = []
isBgs = False;
repeated = 0
#After the simple cases above, we need to use multiple conditions in order to determine if a buisness is a store.
for a in range(0,len(r)):
    if "game" not in r:
        #Note a board game store, if they dont talk about games, we cant determine the merchandise.
        sys.exit()
    checkWords.extend(["selection","inventory","stock","store","own","possess","have"])
    if any(word in r for word in checkWords):
        checkwords[:] = [] #Empty the list for a new check
        if(str != '/n'):
        #Here would be where we check if a word is in a sentence.
            checkWords.extend(["board game", "card game"])
                words = nltk.word_tokenize(r[a])
                for sw in words:
                    sw = sw.lower()
                    if sw not in stopwords:    
                        swl.append(sw)
                bagofwords.append(collections.Counter(swl))
                for i in sent_tokenize(str):
                    checkWords.extend["game", "selection"]
                    if all(word in i.lower() for word in checkWords):
                        #If more than 1 reviewer mentions the word game and selection in the same sentence, its safe to assume that games are the main selling point of the store.
                        #Therefore, by making sure the subject of a sentence is refering games, we can assume ambiguous words can also be referring as a sdescription to this.
                        ambiguousWords = ["magic","card","staff","customer","play","puzzles","online","community","players", "dice", "board game","card game", "boardgames","tournaments"]
                       if repeated > 1: 
                           Bgs = True
                        #Since they mentioned game and selection we can check now for certain games mentioned that can be ambiguous.
                       else if  any(ambiguousWords in i.lower():
                            Bgs = True
                       else:
                           repeated += 1
                words = nltk.word_tokenize(i)
                tag = nltk.pos_tag(words)
                    ne = nltk.ne_chunk(tag)
                    print()
                    for j in tag:
                        if j[0] not in stopwords:
                            print(j)
                    print()
    else:
        #If they dont mention any words of possession, we cannot determine what the store has.
        Bgs = False
'''
POS tag list:
CC	Coordinating conjunction
CD	Cardinal number
DT	Determiner
EX	Existential there
FW	Foreign word
IN	Preposition or subordinating conjunction
JJ	Adjective
JJR	Adjective, comparative
JJS	Adjective, superlative
LS	List item marker
MD	Modal
NN	Noun, singular or mass
NNS	Noun, plural
NNP	Proper noun, singular
NNPS	Proper noun, plural
PDT	Predeterminer
POS	Possessive ending
PRP	Personal pronoun
PRP$	Possessive pronoun
RB	Adverb
RBR	Adverb, comparative
RBS	Adverb, superlative
RP	Particle
SYM	Symbol
TO	to
UH	Interjection
VB	Verb, base form
VBD	Verb, past tense
VBG	Verb, gerund or present participle
VBN	Verb, past participle
VBP	Verb, non-3rd person singular present
VBZ	Verb, 3rd person singular present
WDT	Wh-determiner
WP	Wh-pronoun
WP$	Possessive wh-pronoun
WRB	Wh-adverb
'''
