# Boggle Solver

I re-wrote this project in 2023 from scratch with the goal to check our word lists on a board against a thorough word search of the board.

Thanks to [github/redbo/scrabble](https://github.com/redbo/scrabble/tree/master) for providing a 178k word dictionary which is used here.

```
a = makeBoard('A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,QU,R,S,T,U,V,W,X,Y,Z')
choices(a.words,k = 10) # selects k = 10 words
a.list_words(with_scores = False) # prints words sorting by length w/ option of scores as well.
```

boggle.Board objects have a number of functions that are called by the **__init__()** function to search the board for words in the dictionary.

## How do we find if a given word exists on the board?

**get_all_word_paths** Start with an empty list. For the first piece required in the word, find all locations of that piece on the board (I use [row, col] to denote a position, [0, 0] is top left, on a 5x5 board, [0, 4] is top right, [4, 0] bottom left, and [4, 4] bottom right)... each of these may be the first position of a completed word path. *For example* if there are two A's on the board at [2, 3] and [4, 1] we start our tree of possible word paths with [[[2, 3]], [[4, 1]]].

For each consecutive piece in the word, find all locations of that piece and for each location test against all existing word paths: does the location exist adjacent to the last letter of the word path **and** has the location not already been used? If **YES** to both then append the location to the word path and continue searching. 

*To continue the example* the next letter is N and it exists in three locations [2, 4], [3, 0], and [0, 0]. We will check each of these locations of N against each of the previous locations [2, 3] and [4, 1].

[last position], [next position]
[2,4], [2,3] #the next position is one square to the left, so it *is adjacent* and it has not been previously used... so it is a possible next square in a valid word path

[2,4], [4,1] #the position is 2 steps down and 3 to the left so it *is NOT adjacent* and cannot be part of a valid word path

[3,0], [2, 3] # not adjacent
[3,0], [4, 1] # diagonal (is adjacent) and not previously used... valid word path

[0, 0], [2, 3] # not adjacent
[0, 0], [4, 1] # not adjacent

So, now the two possible word paths to spell AN are
[[[2, 4], [2, 3]], [[3, 0], [4, 1]]]

We continue this process for each additional letter in the word as long as there are *at least* one valid word path for each additional letter. We return either **false** if no valid word path exists or **an array of word paths** in the format [[word path], [word path], [word path], ....] where a word path is a list of position lists.

## Usage

**Q: How do I find all words on a boggle board that I just played**
*A:* Follow the following commands into a python interpreter running in the project directory (has **boggle.py** in the path)

```
from boggle import *
a = makeBoard('A,B,C,...comma sep board here, left-to-right') # define the board
a.list_words(True) #
```
