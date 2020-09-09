from src.TreeBuilder import  TreeBuilder
from src.load_tree import load_tree

tree = load_tree("NewTrieTree_new.tte")

print(tree)

import time

start = time.time()
tree.add_corpus(["%$&@#*(%%(", "~qweasdas", "でした"])
print(time.time() - start)

print(tree.search("%$&@#*(%%( ~qweasdas でした"))
