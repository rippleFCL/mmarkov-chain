import enum
import random
from collections import defaultdict


class Probby(object):
    def __init__(self):
        self.next_words = {}

    def add_next_word(self, word):
        if word in self.next_words:
            self.next_words[word] += 1
        else:
            self.next_words[word] = 1

    def get_next_word(self):
        if len(self.next_words) == 0:
            return "", 0
        word = random.choices(list(self.next_words.keys()), list(self.next_words.values()), k=1)
        return word[0], self.next_words[word[0]]


class MEGABRAIN(object):
    def __init__(self, max_depth=3, coheasion=2):
        self.token_map = defaultdict(Probby)
        self.max_depth = max_depth
        self.coheasion = coheasion

    def cook(self, hi):
        hi = hi.replace("?", " ?").replace("!", " !").replace(".", " .").replace(",", " ,")
        sentance = hi.split()
        new_sentance = []
        while True:
            token_id = " ".join((sentance + new_sentance)[-self.max_depth :])
            coheasion = self.coheasion
            while True:
                coheasion -= 1
                next_word, probability = self.token_map[token_id].get_next_word()
                if (
                    not new_sentance
                    and not (next_word != "." and next_word != "!" and next_word != "?" and next_word != ",")
                    and coheasion
                ):
                    continue
                if probability > 1 :
                    new_sentance.append(next_word)
                    break
                if not coheasion:
                    continue
                token_id = " ".join(token_id.split(" ")[1:])
            if new_sentance[-1].endswith(".") or new_sentance[-1].endswith("!") or new_sentance[-1].endswith("?"):
                break
        start = " ".join(sentance)
        if not (start.endswith(".") or start.endswith("!") or start.endswith("?")):
            new_sentance =sentance + new_sentance

        output = " ".join(new_sentance)
        output = output.replace(" ?", "?").replace(" !", "!").replace(" .", ".").replace(" ,", ",")
        return output

    def hear(self, speach, output=False):
        words = speach.split()
        count = 0
        for word_pos in range(len(words)):
            count += 1
            if output and count % int(len(words) / 100) == 0:
                print(f"{count}/{len(words)} {int(count / len(words)*100)}%")
            if word_pos >= self.max_depth:
                depth = self.max_depth
            else:
                depth = word_pos
            for word_walk_back in range(depth):
                token_id = " ".join(words[word_pos - (word_walk_back) : word_pos])
                self.token_map[token_id].add_next_word(words[word_pos])
            if word_pos == 0:
                self.token_map[""].add_next_word(words[word_pos])
        print(f"{len(words)}/{len(words)}")
        print("done")


bigboi = MEGABRAIN(5)


def load_dataset(model: MEGABRAIN, filename: str, processor):
    with open(filename) as f:
        data = []
        lines = f.readlines()[:300000]
        for line in lines:
            line_processed = processor(line)
            if line_processed:
                data.append(line_processed)
        model.hear(" ".join(data), True)


def replace_punc(string):
    return string.replace("?", " ?").replace("!", " !").replace(".", " .").replace(",", " ,")


def strip_human(string):
    return replace_punc(string.replace("Human 2: ", "").replace("Human 1: ", ""))


def strip_bee(string):
    if string.upper() == string:
        return ""
    if string.strip() == ":":
        return ""

    return replace_punc(string.replace("- ", ""))


load_dataset(bigboi, "trainin_data.txt", strip_human)
load_dataset(bigboi, "beemove.txt", strip_bee)
load_dataset(bigboi, "squished.txt", replace_punc)
load_dataset(bigboi, "en.txt", replace_punc)


# load_dataset(bigboi, "beemove.txt", strip_bee)


def let_it_cook():
    while 1:
        hi = input("me: ")
        bigboi.hear(hi)
        print(f"bot: {bigboi.cook(hi)}")


let_it_cook()
