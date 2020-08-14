from typing import List, Any, Optional, Dict, Text


class TrieNode:
    """TrieNode object represent a node in a src"""

    def __init__(self, voc_size: int, is_eow: bool = False):
        self.voc_size: int = voc_size
        self.child_nodes: List[Optional[TrieNode]] = [None] * self.voc_size
        self.isEOW: bool = is_eow

    def add_child(self, idx: int):
        self.child_nodes[idx] = TrieNode(voc_size=self.voc_size)

    def __str__(self):
        return f"child: {[x for x in self.child_nodes if x is not None]}"


class TrieTree:
    """src object"""

    def __init__(self, voc: List[str]):
        """
        Build a tree by using vocabulary

        :param voc: a list of characters to make a vocabulary
        """
        voc.sort()
        if " " not in voc:
            voc.append(" ")
        self.voc_size: int = len(voc)
        self.char2idx: Dict[Text, Any] = self._char2idx(voc=voc)
        self.idx2char: List[str] = voc
        self.space_idx: int = self.char2idx.get(" ")
        self.separators: List[str] = ["-", '"', "'", "("]
        self.root: TrieNode = TrieNode(voc_size=self.voc_size, is_eow=False)
        self.node_count = 1

    def __str__(self):
        return f"Tree with {self.node_count} nodes"

    def add_separators(self, separators: List[str]):
        """
        Add new separators

        :param separators: a string
        :return: return nothing
        """
        self.separators = list(set(self.separators + separators))

    @staticmethod
    def _char2idx(voc: List[str]) -> Dict[Text, Any]:
        """Dictionary for get index of character"""

        idx2char: Dict[Text, int] = {}
        for idx, char in enumerate(voc):
            idx2char[char] = idx

        return idx2char

    def insert(self, words: str) -> bool:
        """
        Insert words into the tree, return True or False

        :param words: word to insert
        :return: True/False
        """

        cur_node: TrieNode = self.root
        for char in words:
            if self.char2idx.get(char, None) is None:
                return False

        for char in words:
            idx: int = self.char2idx.get(char, None)

            if not cur_node.child_nodes[idx]:
                cur_node.add_child(idx=idx)
                self.node_count += 1

            cur_node = cur_node.child_nodes[idx]

        cur_node.isEOW = True

        return True

    def build(self, corpus: List[str]) -> List[str]:
        """
        Build a tree by using corpus

        :param corpus: a list of string, corpus of the tree
        :return: return a list of string that represent cases that tree can not insert
        """

        fail_case: List[str] = []
        for words in corpus:
            if not self.insert(words=words):
                fail_case.append(words)

        return fail_case

    def search(self, sentence: str) -> List[str]:
        """
        Search any match words in the sentence

        :param sentence: the string to search on
        :return: list of keyword found in this sentence
        """

        cur_node: TrieNode = self.root
        found_words: List[str] = []
        cur_word: str = ""
        mark_idx: int = 0

        for index, char in enumerate(sentence):
            idx: int = self.char2idx.get(char, self.space_idx)

            if idx == self.space_idx and mark_idx == 0:
                mark_idx = index

            if index == 0 and char in self.separators:
                mark_idx = 1

            if cur_node.child_nodes[idx]:
                cur_word += char
                if cur_node.child_nodes[idx].isEOW:
                    found_words.append(cur_word)
                    mark_idx = index

                cur_node = cur_node.child_nodes[idx]

            else:
                if mark_idx == 0:
                    if len(sentence) > index + 1:
                        found_words += self.search(sentence[index + 1:])
                        return list(set(found_words))
                    else:
                        return list(set(found_words))
                else:
                    if len(sentence) > mark_idx:
                        found_words += self.search(sentence[mark_idx:])
                        return list(set(found_words))
                    else:
                        return list(set(found_words))

        return list(set(found_words))
