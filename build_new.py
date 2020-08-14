from src.TreeBuilder import TreeBuilder
from src.load_tree import load_tree

# tree: TreeBuilder = TreeBuilder(file="new_merged_csv.csv", desc_col="DESC_SI", label="DESC_BKG", eva=True)

tree: TreeBuilder = load_tree(file="NewTrieTree.tte")
tree.clean_tree()
print(len(tree.corpus))

tree.save_tree("NewTrieTree.tte")

sentence = """FILTERS HS-CODE:391740 401699,730630,730799, 732690,830710,842123, 842129,842131,842199, 847989,870892, AES: X20190203225619"""
print(tree.search(sentence=sentence))
