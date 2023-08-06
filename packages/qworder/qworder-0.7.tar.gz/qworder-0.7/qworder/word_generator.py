# Generate all possible words of given length
import multiprocessing
import time
from itertools import product, chain
from typing import Dict

from tqdm import tqdm

from qworder.cascading_rules import Cascader


class WordGenerator:

    def __init__(self, input_set: list, length: int, cascader: Cascader = None):
        self.output = []
        self.input_set = input_set
        self.length = length
        self.cascader = cascader if cascader else None
        self.pbar = tqdm()

    def _remove_unnecessary(self, length: int = 0) -> None:
        if length == 1:
            return
        if length == 0:
            length = self.length
        for letter in self.input_set:
            self.output.remove(letter * length)

    def get_words_dictionary(self) -> Dict[int, list]:
        words = {}
        length = self.length
        for k in range(1, length + 1):
            self.length = k
            words[k] = self.generate_words()
            self.output = []
        return words

    def generate_words(self, processes=1, chunk_size=1024):
        self.pbar.update(1)
        return permutations(self.length, self.input_set, processes, chunk_size)


def permutations(length, input_set, processes=None, chunk_size=1024):
    results = []
    with multiprocessing.Pool(processes) as workers:
        perms = []
        for perm in tqdm(product(input_set, repeat=length)):
            perms.append("".join(perm))
            if len(perms) == chunk_size:
                result = workers.map(process, perms)
                results.append(list(filter(None, result)))
                perms = []
    return list(chain.from_iterable(results)) if len(results) != 0 else perms


def process(perm):
    cascader = Cascader()
    if not cascader.is_cascadable(perm):
        return perm
    else:
        return None


if __name__ == '__main__':
    depth = 5
    c = Cascader()
    w = WordGenerator(['H', 'T', 'S'], depth, cascader=c)
    w.output = []
    start_time = time.time()
    words = w.generate_words(chunk_size=100)
    print(len(words))
    print("--- %s seconds ---" % (time.time() - start_time))