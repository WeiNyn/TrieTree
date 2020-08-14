from src.TreeBuilder import TreeBuilder as TreeBuilder
from src.load_tree import load_tree

"""If you have new DataFrame to build a tree, use this way to make new tree"""
tree_or: TreeBuilder = TreeBuilder(file="CM Description within Context - cm_description_with_context.csv",
                                   desc_col="CM_DESCRIPTION_ORIGINAL",
                                   label="CM_DESCRIPTION_OPTIONAL_USER_INPUT")

print("Tree: ", str(tree_or), "\n")
"""-------------------------------------------------------------------------------------------------------"""


"""This way will load a tree from file"""
tree: TreeBuilder = load_tree(file="TrieTree.tte")

print("Tree from file: ", str(tree), "\n")
"""-------------------------------------------------------------------------------------------------------"""


"""To save a tree to file"""
save_result = tree.save_tree("NewTrieTree.tte")
print("Save Tree: ", str(save_result), "\n")
"""-------------------------------------------------------------------------------------------------------"""


"""To search keyword in function"""
sentence = """1 x 40'HC SAID TO CONTAIN :- 31 ROLLS (31 PALLETS) SARAFIL POLYESTER FILM BRAND NAME: SARAFIL INVOICE NO.X20-2100882 DATED: 04/08/2020 PO NO. 3209993 (E030-53590) H.S.CODE : 3920.62.0090  NET WEIGHT: 17,573.39 KGS GROSS WEIGHT : 42,167.07 LBS  PUBLIC COMPANY LTD."""
output = tree.search(sentence=sentence)

print("Search result: ", str(output), "\n")
"""-------------------------------------------------------------------------------------------------------"""


"""output = (['SARAFIL POLYESTER FILM'], 0.0)"""

"""To search a list of sentence"""
sentences = [
    """DESCRIPTION AS PER ATTACHED SHEET  TRANSHIP AT SINGAPORE BY SEASPAN EMERALD V.243N  SHOW LOCAL CHARGE IN FIRST DRAFT EVERY TIME***  ONE (1) CONTAINER ONLY " FREIGHT COLLECT " """,
    """AMBIPUR SPRAY (AIR FRESHENER SPRAY) AMBIPUR INSTANTMATIC LAVENDER BREEZE STARTER SIZE 250 ML. AMBIPUR AIR FRESH & LIGHT SIZE 300 ML. AMBIPUR FRESH & COOL SIZE 300 ML. AMBIPUR LAVENDER BREEZE SIZE 300 ML. AMBIPUR BLUE OCEAN SIZE 300 ML. 5,923 CARTONS (35,538 CANS) N.W. : 10,777.64 Kgs INV.NO. CBP20488 DATE : 31 JULY 2020  HS CODE 33074910 UN 1950 CLASS 2.1 "FREIGHT PREPADE : BY PROCTER & GAMBLE (THAILAND)INTERNATIONAL OPERATIONS SA, SINGAPORE BRANCH 112 MOO 5, TAMBOL BANGSAMAK, AMPHUR BANGPAKONG CHACHOENGSAO 24130 "SEA WAY BILL"  DD: 30 JUL, 2020"""]

outputs = tree.search_many(sentences=sentences)

print("Search results: ", str(outputs), "\n")
"""-------------------------------------------------------------------------------------------------------"""


"""output = [(['AS PER ATTACHED', 'AS PER ATTACHED SHEET'], 0.0),
           (['AIR', '(AIR FRESHENER SPRAY)', 'SPRAY'], 0.0)]"""

"""To add new keyword to corpus"""
new_keywords = ["New keyword", "New keyword 2"]

print("Check keyword: ", tree.is_in_corpus("New keyword"), "\n")

tree.add_corpus(corpus=new_keywords)

print("Check keyword after insert: ", tree.is_in_corpus("New keyword"), "\n")
"""-------------------------------------------------------------------------------------------------------"""


"""This will ignore some keyword that contain unknown characters. If you still want to ad it, please build the Tree again."""

"""You can extract the corpus of the tree to new DataFrame"""
df = tree.extract_corpus()

print("Corpus that extracted from tree:\n ", df.head(5), "\n")
"""-------------------------------------------------------------------------------------------------------"""


"""Keep DataFrame in Tree can be costly, clear the tree by"""
tree.clean_tree()

print("Search Phrase of tree after cleaned:", tree.search_phrase, "\n")
