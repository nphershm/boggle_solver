## Boggle representation v2
## Nick -- Thanksgiving 2023

## implement a boggle board composed of pieces
## provide a Board.get_all_words() or just Board.words attribute
## is working see bottom for implementation

## Level 10 would be to use cv2 to parse an image of a boggle board 

from random import *

class Piece:
    letter = ''

    def __init__(self, letter = 'A'):
        self.letter = letter
    
    def __str__(self):
        return self.letter

PIECES = []
for p in ['a','a','a','b','c','d','e','e','e','f',
          'g','h','i','i','g','qu','j','k','l','m','n',
          'o','o','p','r','s','t','u','v','w','x','y',
          'z','r','s','t','l','n','e']:
    PIECES.append(Piece(p.upper()))

class Board:
    #letters = [] ## an array of letters is a board
    #side = 5
    WORD_LIST = []
    with open('word_list.txt','r') as f:
        for w in f.readlines():
            WORD_LIST.append(w.rstrip('\n').upper())


    def __init__(self, pieces = [], side = 0):
        p_len = len(pieces)
        self.pieces = []
        self.side = side
        if p_len > 9: ### given a board with at least 9 pieces...
            self.side = int(p_len**0.5)
            row = []
            for i in range(self.side**2):
                row.append(pieces[i])
                if len(row) % self.side == 0:
                    self.pieces.append(row)
                    row = []

        else:
            if side < 3: self.side = 5
            for row in range(self.side):
                row = []
                for p in range(self.side):
                    row.append(choice(PIECES))
                self.pieces.append(row)
        
        self.words = self.get_all_words()
    
    def __str__(self):
        b = ''
        for r in range(len(self.pieces)):
            row = ''
            for c in range(len(self.pieces[r])):
                letter = str(self.pieces[r][c])
                row += letter
                row += ' '*(4-len(letter))
            row += '\n'
            b += row
        return b
    
    def get_locations(self, letter = 'A'):
        """Returns an array of locations on the board with that piece"""
        locations = []
        for r in range(self.side):
            for c in range(self.side):
                if (self.pieces[r][c].letter == letter):
                    locations.append([r,c])
        return locations

    def get_letter(self, pos = [1, 2]):
        row = pos[0]
        col = pos[1]
        try:
            return self.pieces[row][col].letter
        except Exception:
            return False
        
    def letters_on_board(self, word = 'query'):
        all_exist = True
        pieces = word_to_pieces(word)
        i = 0 
        while all_exist and i <len(pieces):
            if not self.get_locations(pieces[i].letter): all_exist = False
            i += 1
        return all_exist
    
    def get_all_word_paths(self, word = 'query'):
        """Returns an array of path arrays, containing all possible location paths [[[2,1],[2,2],[3,1]],...]"""
        if not self.letters_on_board(word): return False
        pieces = word_to_pieces(word)
        word_paths = []
        for p in pieces:
            # print('word paths:',word_paths)
            # print('adding ',p.letter,'to word paths')
            # print('locations:',self.get_locations(p.letter))
            
            locs = self.get_locations(p.letter)
            if len(word_paths) == 0:
                for l in locs:
                    word_paths.append([l])
            else:
                new_paths = []
                for w in word_paths:
                    for l in locs:
                        # print('new_paths loop, w',w,'l',l)
                        # print('appended w/l:',w.append(l))

                        ## test that pieces are adjacent or diagonal
                        prev = w[-1]
                        if not l in w and abs(prev[0]-l[0])<2 and abs(prev[1]-l[1])<2:
                            z = w.copy()
                            z.append(l)
                            new_paths.append(z)
                        # else:
                            # print('Skipping l',l,'already in path:',w,'or not adjacent')
                #print('after loop:np:',new_paths,'\n word_paths:',word_paths)
                if new_paths == []: return False
                word_paths = new_paths
        # print('Found ',len(word_paths),'word paths for',word)
        return word_paths

    def get_all_words(self, min_length = 3):
        """returns a list containing all words from word dict on board"""
        on_board = []
        for w in self.WORD_LIST:
            if len(w) >= min_length:
                if self.get_all_word_paths(w): 
                    on_board.append(w)
        print(f'Found {len(on_board)} words on board.')
        return on_board
    
    def list_words(self):
        self.words.sort()
        self.words.sort(key = len) 
        short = len(self.words[0])
        long = len(self.words[-1])
        for my_len in range(short, long+1):
            my_words = []
            for w in self.words: 
                if len(w) == my_len: my_words.append(w)
            print(f'{my_len}-letter words: {len(my_words)}')
            for word in my_words: print(word)
            print('***\n')
    
def word_to_pieces(word = 'query', pieces = PIECES):
    """Given a word returns the Boggle pieces that compose the word in order."""
    i = 0
    my_pieces = []
    word = word.upper()
    while i < len(word):
        look_ahead = 1
        if word[i:i+1] == 'Q': look_ahead = 2
        letter = word[i:i+look_ahead] 
        my_pieces.append(Piece(letter))
        i += look_ahead
    return my_pieces

def makeBoard(pieces = 'A,B,C,D,Qu,F,g,j,N,o,A,p'):
    arr = []
    for p in pieces.upper().split(','):
        arr.append(Piece(p))
    return Board(arr)


# b = Board(side = 5)
# print(b)

# print('Another board...')

# c = Board()
# w = c.get_all_words()
# print(c)

# print(c.get_locations('E'), c.get_locations('D'))
# for p in word_to_pieces('Finally'): print(p, end = " ")
# print()
# for p in word_to_pieces('Query'): print(p, end = " ")
# print()

b = makeBoard('A,C,D,E,F,G,I,N,K,L,O,P,QU,A,E,S,T,L,N,O,R,T,Z,E,R')
choices(b.words,k=20)
print(f'b is a board with {b.side} x {b.side} and {len(b.words)} words.')


c = Board(side=5)
choices(c.words, k = 20)
print(f'c is a board with {c.side} x {c.side} and {len(c.words)} words.')
c.list_words()
print('above output is from c.list_words()')


d = Board(side = 4)
choices(c.words, k = 20)
print(f'd is a board with {d.side} x {d.side} and {len(d.words)} words.')
