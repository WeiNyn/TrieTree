import logging as logger
import pickle
import sys
import time
from typing import List, Tuple

import pandas as pd

from src.TrieTree import TrieTree

logger.basicConfig(level=logger.INFO)


class TreeBuilder:
    """TreeBuilder object for building tree with DataFrame"""

    def __init__(self, file: str, desc_col: str, label: str, eva: bool = False):
        """
        Create a tree from DataFrame (csv file)

        :param file: path to csv file (only support csv file)
        :param desc_col: column name of descriptions
        :param label: column name of labels
        :param eva: True to turn on evaluation step when create Tree (not recommended)
        """
        self._build_data_frame(file=file, desc_col=desc_col, label=label)
        self._build_corpus(desc_col=desc_col, label=label)
        self._build_voc()
        self._build_tree()
        self.fail_test: List[List[str, List[str], List[str]]] = []
        if eva:
            self.evaluate()
        self.score: Tuple[float, float] = (0.0, 0.0)

    def __str__(self):
        return str(self.tree)

    def _build_data_frame(self, file: str, desc_col: str, label: str):
        df = pd.read_csv(file)
        df = df[[desc_col, label]]
        df = df.dropna(subset=[desc_col, label])
        df = df.drop_duplicates(subset=[desc_col], keep="first")
        df = df.sample(frac=1)
        self.data_frame: pd.DataFrame = df

    def _build_corpus(self, desc_col: str, label: str):
        self.corpus: List[str] = []
        self.search_phrase: List[str] = []
        self.true_key: List[List[str]] = []
        for index, row in self.data_frame.iterrows():
            products = row[label].replace("\r", " ") \
                .replace("\n", " ") \
                .replace("- ", "-") \
                .replace(" -", "-") \
                .split(",")

            des = row[desc_col].replace("\r", " ") \
                .replace("\n", " ") \
                .replace("- ", "-") \
                .replace(" -", "-")

            self.search_phrase.append(des)

            products = [product.strip()
                        for product in products
                        if len(product) > 3 and product.strip() in des]

            self.true_key.append(products)
            self.corpus += products

    def _build_voc(self):
        self.voc: List[str] = []
        for product in self.corpus:
            for char in product:
                self.voc.append(char)

            self.voc = list(set(self.voc))

        self.voc.sort()

    def _build_tree(self):
        self.tree: TrieTree = TrieTree(voc=self.voc)
        self.fail_case: List[str] = self.tree.build(corpus=self.corpus)

    def evaluate(self):
        """
        Evaluate the Tree

        :return: return nothing, this function show how good the tree is
        """
        sys.setrecursionlimit(100000000)
        start_time: float = time.time()
        logger.info("Evaluating")
        predicted_list: List[List[str]] = []
        for sentence in self.search_phrase[:min(100, len(self.search_phrase))]:
            predicted_list.append(self.tree.search(sentence=sentence))
        logger.info("Evaluate matrix built")
        total_word_count: int = 0
        total_true_count: int = 0
        for sentence, true_key, predicted in zip(self.search_phrase[:min(100, len(self.search_phrase))], self.true_key,
                                                 predicted_list):
            total_word_count += len(true_key)
            true_count: int = len(list(set(true_key).intersection(set(predicted))))
            if true_count < len(list(set(true_key))):
                self.fail_test.append([sentence, true_key, predicted])

            total_true_count += true_count

        self.score = (total_true_count / total_word_count)

        logger.info(
            f"Accuracy: {self.score} ({total_true_count}/{total_word_count}); Test {min(100, len(self.search_phrase))} samples in {time.time() - start_time}")

    def clean_tree(self):
        self.search_phrase.clear()
        self.true_key.clear()

    def save_tree(self, file: str) -> Tuple[bool, str]:
        """
        Save tree to a file

        :param file: path to file
        :return: (True/False, exception)
        """
        try:
            pickle.dump(self, open(file, "wb"))
        except Exception as ex:
            return False, ex

        return True, "Success"

    def add_corpus(self, corpus: List[str]):
        """
        Add new keyword to corpus, this function will ignore keyword that contain characters not in vocabulary of the Tree.
        If you still want to insert it, please build the again.

        :param corpus: list of keyword to insert
        :return: return nothing
        """
        for words in corpus:
            if words not in self.search(sentence=words):
                if not self.tree.insert(words=words):
                    self.fail_case.append(words)
                    logger.debug("Can not insert words: ", words)
                else:
                    self.corpus.append(words)
            else:
                logger.info(f"{words} was already in corpus")

    @staticmethod
    def reprocess(text: str) -> str:
        """
        Reprocess string before search

        :param text: a string to reprocess
        :return: a string after processed
        """
        return text.replace("\r", " ") \
            .replace("\n", " ") \
            .replace("- ", "-") \
            .replace(" -", "-")

    def search(self, sentence: str) -> Tuple[List[str], float]:
        """
        Search for every keyword that appear in the given sentence

        :param sentence: the sentence to search (in string format)
        :return: (list of keyword, time to process)
        """
        start_time: float = time.time()
        sentence = self.reprocess(text=sentence)
        return self.tree.search(sentence=sentence), time.time() - start_time

    def search_many(self, sentences: List[str]) -> List[Tuple[List[str], float]]:
        """
        Search all sentence in the given list of sentences

        :param sentences: a list of sentences
        :return: a list of (list of keyword, time to process)
        """
        results: List[Tuple[List[str], float]] = []
        for sentence in sentences:
            results.append(self.search(sentence=sentence))

        return results

    def is_in_corpus(self, word: str) -> Tuple[bool, int]:
        """
        Check if keyword in the corpus or not

        :param word: a string keyword
        :return: (True/False, index of word in corpus)
        """
        if word in self.corpus:
            return True, self.corpus.index(word)
        else:
            return False, 0

    def extract_corpus(self) -> pd.DataFrame:
        """
        Extract corpus of the tree to DataFrame

        :return: DataFrame
        """
        return pd.DataFrame(data=[[s, l] for s, l in zip(self.search_phrase, self.true_key)],
                            columns=["description", "label"])
