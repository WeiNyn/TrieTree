from src.TreeBuilder import TreeBuilder
from src.load_tree import load_tree

tree: TreeBuilder = TreeBuilder(file="new_merged_csv_removed.csv", desc_col="DESC_SI", label="DESC_BKG", eva=True)

# tree: TreeBuilder = load_tree(file="NewTrieTree.tte")
tree.clean_tree()

print(len(tree.corpus))

tree.save_tree("NewTrieTree_new.tte")

sentence = """" SHIPPER 'S LOAD & COUNT " ============== PO.NO. 4600372760 UHT COCONUT MILK 17-18% FAT 12X1000 ML. ''GRACE'' BRAND  NET WEIGHT: 19,200 KGS. H.S. CODE : 2106.9099 REFERENCE INV. NO.TCN2008/00132"""
print(tree.search(sentence=sentence))
