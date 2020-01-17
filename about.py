import pymorphy2
from transliterate import translit
import random
import re

# initial global lists
MASCULINE_NOUNS = []
FEMININE_NOUNS = []
MASCULINE_ADJECTIVES = []

femaleNames = ['Евгения']

with open("data/musculine_nouns_vars.txt", "rb") as mn:
    MASCULINE_NOUNS = mn.read().decode("UTF-8").split("\r\n")

with open("data/masculine_adjectives_vars.txt", "rb") as mn:
    MASCULINE_ADJECTIVES = mn.read().decode("UTF-8").split("\r\n")

with open("data/feminine_nouns_vars.txt", "rb") as mn:
    FEMININE_NOUNS = mn.read().decode("UTF-8").split("\r\n")


class SwearingGenerator:
    def __init__(self, name):
        self.name = name
        self.masculine_nouns = MASCULINE_NOUNS
        self.masculine_adjectives = MASCULINE_ADJECTIVES
        self.feminine_nouns = FEMININE_NOUNS
        self.gender = self.__getGender(name)

    def __getGender(self, name):
        name = re.sub(r'[\'\,\[\]\{\}\!\@\#\$\%\&\*\(\)\=\-\<\>\?\.\~\`\"\:]', '', name)
        transleted_name = translit(name.lower().title(), "ru")
        morph = pymorphy2.MorphAnalyzer()
        parsed_word = morph.parse(transleted_name)[0]
        if name in femaleNames:
            return 'female'
        if parsed_word.tag.gender == "masc":
            return "male"
        elif parsed_word.tag.gender == "femn":
            return "female"
        else:
            return "unknow"

    def __convert_adjective_to_feminine(self, adjectiveStr):
        if self.gender != "female":
            return adjectiveStr
        else:
            result = re.search(r"ый$|ий$|ой$|ийся$|$ыйся", adjectiveStr)
            if result is None:
                return adjectiveStr
            else:
                result = result.group(0)
                if result == "ый" or result == "ой" or result == "ий":
                    return re.sub(r"ый$|ий$|ой$", "ая", adjectiveStr)
                else:
                    return re.sub(r"ийся$|ыйся$", "аяся", adjectiveStr)

    def getFraseConstructor(self):
        randomModel = random.randint(1, 2)
        frase = ""
        randomDelimetr = ", ты" if random.randint(1, 2) == 2 else " —"
        if randomModel == 1:
            frase = "{0}, ты {1}.".format(self.name, self.getSentance())
        else:
            frase = "{0} {1}{3} {2}.".format(
                self.getSentance(True).capitalize(), self.name, self.getSentance(), randomDelimetr
            )
        return frase

    def getSentance(self, isFirst=False):
        delimiter = [" и ", ", "]
        maxRandomNumber = 2 if isFirst else 3
        wordsCount = random.randint(1, maxRandomNumber)
        word = ""
        nounceArr = (
            self.feminine_nouns if self.gender == "female" else self.masculine_nouns
        )

        def firstNoun():
            wordOfFirstNoun = random.choice(nounceArr)
            if wordOfFirstNoun in word:
                return firstNoun()
            else:
                return wordOfFirstNoun

        def firstAdjective():
            wordOfFirstAdj = random.choice(self.masculine_adjectives)
            if wordOfFirstAdj in word:
                return firstAdjective()
            else:
                return self.__convert_adjective_to_feminine(wordOfFirstAdj)

        if wordsCount == 1:
            word = "{0} {1}".format(firstAdjective(), firstNoun())
        elif wordsCount == 2 and isFirst == True:
            word = "{0} {1}".format(firstAdjective(), firstNoun())
            word = (
                word
                + random.choice(delimiter)
                + "{0} {1}".format(firstAdjective(), firstNoun())
            )
        elif wordsCount == 2 and isFirst == False:
            word = "{0} {1}".format(firstAdjective(), firstNoun())
            word = word + delimiter[0] + "{0} {1}".format(firstAdjective(), firstNoun())
        elif wordsCount == 3 and isFirst == False:
            word += "{0} {1}".format(firstAdjective(), firstNoun())
            word += delimiter[1] + "{0} {1}".format(firstAdjective(), firstNoun())
            word += delimiter[0] + "{0} {1}".format(firstAdjective(), firstNoun())
        return word
