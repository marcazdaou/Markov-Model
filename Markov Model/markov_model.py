from symboltable import SymbolTable
import stdio
import stdrandom
import sys


class MarkovModel(object):
    # Creates a Markov model of order k from the given text.
    def __init__(self, text, k):
        self._k = k
        self._st = SymbolTable()
        circ_text = text + text[0:k]
        for i in range(len(circ_text) - k):
            # Check if the current substring exists in the dictionary
            if circ_text[i:i + k] not in self._st:
                self._st[circ_text[i:i + k]] = {}
            # Check if the next character exists as a key in the substring's dictionary
            if circ_text[k + i] not in self._st[circ_text[i:i + k]]:
                self._st[circ_text[i:i + k]][circ_text[k + i]] = 0
            self._st[circ_text[i:i + k]][circ_text[k + i]] += 1

    # Returns the order this Markov model.
    def order(self):
        return self._k

    # Returns the number of occurrences of kgram in this Markov model; and 0 if kgram is
    # nonexistent. Raises an error if kgram is not of length k.
    def kgram_freq(self, kgram):
        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' + str(self._k))
        if kgram not in self._st:
            return 0
        return sum(self._st[kgram].values())

    # Returns number of times character c follows kgram in this Markov model; and 0 if kgram is
    # nonexistent or if it is not followed by c. Raises an error if kgram is not of length k.
    def char_freq(self, kgram, c):
        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' + str(self._k))
        if kgram not in self._st or c not in self._st[kgram]:
            return 0
        return self._st[kgram][c]

    # Returns a random character following kgram in this Markov model. Raises an error if kgram is
    # not of length k or if kgram is nonexistent.
    def rand(self, kgram):
        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' + str(self._k))
        if kgram not in self._st:
            raise ValueError('Unknown kgram ' + kgram)
        values = self._st[kgram].values()
        total = sum(values)
        probabilities = []
        for value in values:
            probabilities.append(value / total)
        random_index = stdrandom.discrete(probabilities)
        keys = list(self._st[kgram].keys())
        return keys[random_index]

    # Generates and returns a string of length n from this Markov model, the first k characters of
    # which is kgram.
    def gen(self, kgram, n):
        string = kgram
        while len(string) < n:
            string += self.rand(string[-self._k:])
        return string

    # Replaces unknown characters (~) in corrupted with most probable characters from this Markov
    # model, and returns that string.
    def replace_unknown(self, corrupted):
        original = ''
        for i in range(len(corrupted)):
            if corrupted[i] == '~':
                kgram_before = corrupted[i - self._k: i]
                kgram_after = corrupted[i + 1: i + self._k + 1]
                hypotheses = list(self._st[kgram_before].keys())
                probs = []
                for hypothesis in hypotheses:
                    context = kgram_before + hypothesis + kgram_after
                    p = 1.0
                    for i in range(0, self._k + 1):
                        kgram = context[i: i + self._k]
                        next_char = context[i + self._k]
                        if kgram not in self._st or next_char not in self._st[kgram]:
                            p *= 0.0
                            break
                        else:
                            # p *= self._st[kgram][next_char]
                            p *= self.char_freq(kgram, next_char) / self.kgram_freq(kgram)
                    probs.append(p)
                original += hypotheses[_argmax(probs)]
            else:
                original += corrupted[i]
        return original


# Given a list a, _argmax returns the index of the maximum value in a.
def _argmax(a):
    return a.index(max(a))


# Unit tests the data type [DO NOT EDIT].
def _main():
    text = sys.argv[1]
    k = int(sys.argv[2])
    model = MarkovModel(text, k)
    a = []
    while not stdio.isEmpty():
        kgram = stdio.readString()
        char = stdio.readString()
        a.append((kgram.replace('-', ' '), char.replace('-', ' ')))
    for kgram, char in a:
        if char == ' ':
            stdio.writef('freq(%s) = %s\n', kgram, model.kgram_freq(kgram))
        else:
            stdio.writef('freq(%s, %s) = %s\n', kgram, char, model.char_freq(kgram, char))


if __name__ == '__main__':
    _main()
