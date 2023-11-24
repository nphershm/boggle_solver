# Boggle Solver

I re-wrote this project in 2023 from scratch with the goal to check our word lists on a board against a thorough word search of the board.

Thanks to [github/redbo/scrabble](https://github.com/redbo/scrabble/tree/master) for providing a 178k word dictionary which is used here.

```
a = makeBoard('A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,QU,R,S,T,U,V,W,X,Y,Z')
choices(a.words,k = 10) # selects k = 10 words
a.list_words(with_scores = False) # prints words sorting by length w/ option of scores as well.
```

boggle.Board objects have a number of functions that are called by the **__init__()** function to search the board for words in the dictionary.

The search algorithm can be understand with the following psuedocode

Convert a word into boggle pieces (note that qu is a single piece)
**letters_on_board()** For each piece in the word check if that piece exists on the board
    If any word piece fails to be found return False (word cannot be found)

**get_all_word_paths** Start with an empty list. For the first piece required in the word, find all locations of that piece on the board... each of these may be the first position of a completed word path. For each consecutive piece in the word, find all locations of that piece and for each location test against all existing word paths: does the location exist adjacent to the last letter of the word path? **and** has the location not already been used? if **YES** to both then append the location to the word path and continue searching. Return false if any piece required in the word fails to meet criteria and be able to continue the word path... Return a list of lists of piece locations, which use [row, col] 0-indexed format, of words... something like [[[3, 1], [2, 0], [2, 1], [2, 2]]].
