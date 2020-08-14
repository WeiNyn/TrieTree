# TrieTree

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

# Usage

Place folder TrieTree/src in your project
Install dependencies
```
pip install -r requirements.txt
```
_____________________________________
# Import TrieTreeBuilder


```python
from src.TreeBuilder import TreeBuilder
from src.load_tree import load_tree
```
_______________________________________________
# Build and load
If you have a DataFrame to build new Tree, use the following way to make a new TreeBuilder object
```python
tree_or: TreeBuilder = TreeBuilder(file="CM Description within Context - cm_description_with_context.csv",
                      desc_col="CM_DESCRIPTION_ORIGINAL",
                      label="CM_DESCRIPTION_OPTIONAL_USER_INPUT")
```

With: 
 - 'file': the file path to DataFrame (csv format) file
 - 'desc_col': the name of description column in DataFrame
 - 'label': the name of the label column in DataFrame

To load a tree that have been saved in file
```python
tree: TreeBuilder = load_tree(file="TrieTree.tte")
```

You can also save your tree in a file
```python
tree.save_tree("NewTrieTree.tte")
```
__________________________________________
# Search
To search keyword in sentence
```python
sentence = """1 x 40'HC SAID TO CONTAIN :- 31 ROLLS (31 PALLETS) SARAFIL POLYESTER FILM BRAND NAME: SARAFIL INVOICE NO.X20-2100882 DATED: 04/08/2020 PO NO. 3209993 (E030-53590) H.S.CODE : 3920.62.0090  NET WEIGHT: 17,573.39 KGS GROSS WEIGHT : 42,167.07 LBS  PUBLIC COMPANY LTD."""
```
```python
output = tree.search(sentence=sentence)
```

The output will be a tuple of keywords list and process time
```python
output = (['SARAFIL POLYESTER FILM'], 0.0)
```
You can also search a list of description in one time
```python
sentences = [
    """DESCRIPTION AS PER ATTACHED SHEET  TRANSHIP AT SINGAPORE BY SEASPAN EMERALD V.243N  SHOW LOCAL CHARGE IN FIRST DRAFT EVERY TIME***  ONE (1) CONTAINER ONLY " FREIGHT COLLECT " """,
    """AMBIPUR SPRAY (AIR FRESHENER SPRAY) AMBIPUR INSTANTMATIC LAVENDER BREEZE STARTER SIZE 250 ML. AMBIPUR AIR FRESH & LIGHT SIZE 300 ML. AMBIPUR FRESH & COOL SIZE 300 ML. AMBIPUR LAVENDER BREEZE SIZE 300 ML. AMBIPUR BLUE OCEAN SIZE 300 ML. 5,923 CARTONS (35,538 CANS) N.W. : 10,777.64 Kgs INV.NO. CBP20488 DATE : 31 JULY 2020  HS CODE 33074910 UN 1950 CLASS 2.1 "FREIGHT PREPADE : BY PROCTER & GAMBLE (THAILAND)INTERNATIONAL OPERATIONS SA, SINGAPORE BRANCH 112 MOO 5, TAMBOL BANGSAMAK, AMPHUR BANGPAKONG CHACHOENGSAO 24130 "SEA WAY BILL"  DD: 30 JUL, 2020"""]
```
```python
outputs = tree.search_many(sentences=sentences)
```
```python
outputs = [(['AS PER ATTACHED', 'AS PER ATTACHED SHEET'], 0.0),
          (['AIR', '(AIR FRESHENER SPRAY)', 'SPRAY'], 0.0)]
```
__________________________________________________________
# Modify Tree
To insert new keyword to corpus
```python
new_keywords = ["New keyword", "New keyword 2"]
```
```python
tree.add_corpus(corpus=new_keywords)
```
Check that keyword in the corpus or not
```python
tree.is_in_corpus("New keyword")
```
```python
output = (True, 1807)
```
The second value show the index of keyword in corpus
_______________________________________________________
# Other
add_corpus() function will ignore keyword that contain unknown characters. If you still want to insert it, please build the tree again by a DataFrame.
The tree hold it's DataFrame, to extract the old DataFrame
```python
df = tree.extract_corpus()
```
Keep the DataFrame in tree can be costly, you can extract the corpus and clear the tree by
```python
tree.clean_tree()
```
There are some log using logging, if you don't want these log show in console, try
```python
import logging as logger
logger.basicConfig(level=logger.ERROR)
```
Check the tester.py file for test these function.

__________________________________________________________
I made a new Tree by using bigger corpus at: https://drive.google.com/file/d/1fQCz2U2oqeYkQh4BXgj8i4Igf2om1gdA/view?usp=sharing
