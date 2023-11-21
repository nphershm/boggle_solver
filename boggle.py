# Boggle
# Nick
# Thanksgiving, 20tk

from random import *
from tk import *
from time import time
from copy import copy
import os, sys

#CONSTANTS
WINDOW_SIZE = 400
MIN_WORD_SIZE = 4
GAME_TIME = 60*3 #A normal Game is 3 minutes
OFFICIAL_PIECES = [
    ['W','O','N','D','H','H'],
    ['O','N','D','L','R','H'],
    ['G','E','E','U','A','M'],
    ['F','S','A','R','A','A'],
    ['T','T','O','T','E','M'],
    ['M','E','A','E','E','E'],
    ['M','G','N','A','E','N'],
    ['N','E','C','C','S','T'],
    ['I','T','I','T','E','I'],
    ['I','R','P','S','Y','Y'],
    ['N','U','W','T','O','O'],
    ['P','I','E','S','L','T'],
    ['IN','TH','HE','QU','AN','ER'],
    ['I','L','E','T','S','I'],
    ['E','D','N','A','N','N'],
    ['V','O','R','W','G','R'],
    ['S','E','S','U','N','S'],
    ['A','Y','I','F','R','S'],
    ['P','C','E','I','T','S'],
    ['O','H','D','T','D','N'],
    ['F','S','I','R','A','A'],
    ['K','B','X','Z','J','B'],
    ['L','O','H','D','H','R'],
    ['E','E','E','E','A','A'],
    ['T','U','O','T','O','O']
    ]

def load_words(size=4):
    fname = 'word_list.txt'
    f = open(fname,'r')
    word_list = []
    for i in f:
        if len(i[:-1]) >= size:
            word_list.append(i[:-1].upper())
    f.close()
    return word_list

SCRABBLE_WORDS = load_words()

def word_score(word=''):
    length = len(word) - MIN_WORD_SIZE
    if length < 0: return 0
    elif length == 0: return 1
    elif length == 1: return 2
    elif length == 2: return 3
    elif length == 3: return 5
    else: return 11

class Piece:
    def __init__(self,letters=[]):
        self.letters = letters
        self.letter = choice(letters)

    def get_letter(self):
        return self.letter

    def __str__(self):
        return self.letter
    
    def __repr__(self):
        return self.letter

class Board:
    def __init__(self, side=5,pieces=[]):
        self.alph = 'aabcdeeefghiijkllmnnoopqrrssttuuvwxyz'.upper()
        self.side = side
        self.letters = ''

        # internal representation: [[1,2,3,4,],[2,3,4],....
        c = 0
        if not pieces:
            self.pieces = self.set_pieces_official(side*side)
        else:
            self.pieces = pieces
        array = []
        for i in range(side):
            row = []
            for j in range(side):
                row.append(self.pieces[c])
                self.letters += self.pieces[c].get_letter()
                c += 1
            array.append(row)
        self.array = array

    def set_pieces(self, num=25):
        pieces = []
        for i in range(num):
            letters = []
            for j in range(6):
                letters.append(self.alph[randint(0,len(self.alph)-1)])
            pieces.append(Piece(letters))
        return pieces

    def set_pieces_official(self,num=25):
        p = []
        for i in range(num):
            p.append(Piece(OFFICIAL_PIECES[i]))
        return p

    def get_pieces(self):
        return self.pieces

    def convert_index_to_rc(self, index=1):
        row = index / self.side
        col = index % self.side
        return row, col

    def get_letter_rc(self,r = 2, c = 2):
        side = self.side
        if r <= side and c <= side:
            return self.array[r][c]
        else:
            return None

    def get_letter_index(self,index=1):
        if index >= self.side**2:
            return False
        row = index / self.side
        col = index % self.side
        return self.get_letter_rc(row,col)

    def __str__(self):
        return str(self.side)+' by '+str(self.side)+' board.'

    def __repr__(self):
        toStr = ''
        for i in range(self.side):
            for j in range(self.side):
                toStr += str(self.get_letter_rc(i,j))+' '
            toStr += '\n'
        return toStr

    def get_letter_location(self, letter='a'):
        locations = []
        for i in range(self.side**2):
            if self.get_letter_index(i).get_letter().upper()==letter.upper():
                locations.append(i)
        return locations

    def list_to_word(self, piece_indices=[]):
        """takes a list of integer indices for pieces on the board
        returns a string, formed by joining the letters at each index"""
        word = ''
        for i in piece_indices:
            word += self.get_letter_index(i).get_letter()
        return word

    def valid_word(self, word='',wl=[]):
        if not wl: wl = SCRABBLE_WORDS
        if not len(word) > 0: return False
        if not word.upper() in wl: return False
        #recurse through all possible letter combinations
        loc = self.get_letter_locations(word)
        if not loc: return False
        res = self.get_all_word_paths(loc)
        for w in res: 
            if self.valid_connection_list(w): return True
        return False

    def vword2(self, word,wl=[]):
        if not wl: wl = SCRABBLE_WORDS
        res = self.get_all_paths2(word)
        if word.upper() in wl:
            for w in res:
                if self.valid_connection_list(w): return True
        return False
            
    def get_letter_locations(self, word=''):
        locations = []
        for i in word:
            loc = self.get_letter_location(i)
            if not loc: return False #test that letter is on board.
            locations.append(loc) 
        return locations

    def get_all_word_paths(self, word_loc=[], paths=[]):
        """ Takes word_loc a list of letter locations, 
        returns a list of lists [[path1],[path2],[path3]...]"""
        if not word_loc: return paths
        dest = []
        if not paths:
            for i in word_loc[0]: dest.append([i])
        else:
            newP = len(word_loc[0])
            holder = list(paths)
            for i in word_loc[0]:
                for h in holder:
                    temp = []
                    for j in h:
                        temp.append(j)
                    temp.append(i)
                    dest.append(temp)
        return self.get_all_word_paths(word_loc[1:],dest)

    def letters_on_board(self,word):
        """Tests if the letters in a word are on the board"""
        word = word.upper()
        for l in word:
            if not l in self.letters: return False
        return True

    def get_all_paths2(self,word):
        """
        Given a dictionary ("matches"), consisting of 
        {'word_index': [piece_index, piece_index,...]}
        constructs a nested list of lists
        [[p_i, p_i, p_i, p_i],[p_i,p_i,...],...]
        each nested list is a unique sequence of piece indices
        formed from the dictionary.

        This function is a re-implementation of get_all_paths... it adds 
        support for multiple letters on the same boggle piece: "er", "qu" etc.
        Which are unsupported by the prior function which iterates through 
        the letters in a word individually and seeks them on the board.
        """
        word = word.upper()
        if not self.letters_on_board(word): return []
        matches = self.pieces_in_word(word)
        paths = []
        for k, v in matches.iteritems(): #for each letter in the word match
            if not paths: #first word index
                for i in v[:]:
                    if not paths:
                        paths = [[[i[0]],i[1]]]
                    else:
                        paths.append([[i[0]],i[1]])
            else:
                """
                Given a set of paths, check if path is ready to add a new piece
                """
                dest = []
                for p in paths:
                    if p[1] == k:
                        for i in v: #each new piece
                            h = [p[0][:],p[1]]
                            h[0].append(i[0]) #append the piece
                            h[1] = h[1]+i[1] #update the path_index
                            dest.append(h) #add this new path to the list of paths                
                    elif p[1] > k: #if path is ahead of current piece, copy it to dest
                        dest.append([p[0][:],p[1]])
                paths = dest

        #Finally, strip word index from the paths
        h = []
        for p in paths:
            if word == self.list_to_word(p[0]).upper():
                h.append(p[0][:])
        return h

    def path_is_word(self,word,path):
        word=word.upper()
        if word == self.list_to_word(path):
            return True
        return False

    def valid_word_fast(self, word, word_list=[]):
        if not word_list: word_list = SCRABBLE_WORDS
        word = word.upper()
        if not word in word_list: return False
        if not self.letters_on_board(word): return False
        matches = self.pieces_in_word(word)
        paths=[]
        for k,v in matches.iteritems():
            if k == 0:
                for i in v[:]:
                    if not paths:
                        paths = [[[i[0]],i[1]]]
                    else:
                        paths.append([[i[0]],i[1]])
            else:
                dest = []
                for p in paths:
                    if p[1]==k:
                        for i in v[:]:
                            h = [p[0][:],p[1]]
                            h[0].append(i[0]) 
                            h[1] = h[1]+i[1] 
                            #test h[0]
                            if len(word)==h[1]:
                                if self.path_is_word(word,h[0]) and self.valid_connection_list(h[0]): return True
                            if self.valid_connection_list(h[0]): 
                                dest.append(h)
                    elif p[1]>k:
                        dest.append([p[0][:],p[1]])
                if not dest: 
                    return False
                paths = dest
        else:
            return False
        return False

    def get_valid_word_path(self, word=''):
        paths = self.get_all_word_paths(self.get_letter_locations(word))
        for p in paths:
            if self.valid_connection_list(p): return p
        return False

    def get_valid_word_path2(self,word):
        paths = self.get_all__paths2(word)
        for p in paths:
            if self.valid_connection_list(p): return p
        return False

    def valid_connection_list(self,path=[]):
        """ Make sure that each connection is valid, and no repeats """
        #Count 
        for i in path:
            count = 0
            for j in path:
                if i == j: count += 1
                if count > 1: 
                    return False
        #Check each connection
        for i in range(len(path)-1):
            if not self.valid_connection(path[i],path[i+1]): 
                return False
        return True

    def valid_connection(self, a=1,b=2):
        """ a and b are integer indices of a location on the board """
        ar, ac = self.convert_index_to_rc(a)
        br, bc = self.convert_index_to_rc(b)
        if ac == bc:
            if ar == br - 1 or ar == br + 1: return True
        elif ar == br:
            if ac == bc - 1 or ac == bc + 1: return True
        elif (ar == br +1 or ar == br - 1) and (ac == bc + 1 or ac == bc - 1):
            return True
        else:
            return False
        return False

    def pieces_in_word(self,word):
        #Opposite of valid word: instead of searching from word to board
        #Implement a search from board to word... 
        #For each piece, match to word, record matching piece, matching index, length of match in word.
        word = word.upper()
        pieces = self.get_pieces()
        matches = {}
        for i in range(len(pieces)):
            chars = pieces[i].get_letter().upper()
            len_chars = len(chars)
            if chars in word:
                for j in range(len(word)):
                    if chars == word[j:j+len_chars]:
                        if j in matches.keys():
                            matches[j].append([i,len_chars])
                        else:
                            matches[j] = [[i, len_chars]]
        return matches

class Game:
    def __init__(self,sides=5,pieces=[]):
        self.sides = sides
        self.board = Board(sides,pieces)
        print(self.board.__repr__())
        self.root = Tk()
        self.canvas = None
        self.canvas_pieces = self.toScreen()

    def toScreen(self):
        buff=10
        s = (WINDOW_SIZE - (self.sides + 1) * buff) / self.sides
        #print 's:',s
        self.canvas = Canvas(self.root, width = WINDOW_SIZE, height=WINDOW_SIZE)
        self.canvas.pack()
        pieces = []
        for i in range(self.sides):
            rows = []
            for j in range(self.sides):
                #print 'i',i,'j',j
                x = buff*(j+1) + s * j
                y = buff*(i+1) + s * i
                a = self.canvas.create_rectangle(x, y, x + s, y + s, activefill='blue')
                #print 'create_text:',x+s/2,y+s/2,'get_letter_rc:',self.board.get_letter_rc(i,j)
                b = self.canvas.create_text(x+s/2, y+s/2,text=self.board.get_letter_rc(i, j),font=('Helvetica', s / 3))
                rows.append([a,b])
            pieces.append(rows)
        self.canvas.update()
        return pieces

    def highlight_pieces(self, word):
        p = self.board.get_valid_word_path(word)
        if p:
            for l in p:
                r, c = self.board.convert_index_to_rc(l)
                print('highlighting piece at',r,c)
                #[TODO]determine how to get to the rectangle object for a given index.
                #need to get instance of rectangle/canvas object...
                self.canvas_pieces[r][c][0].config(fill='yellow')

    def new(self):
        self.root.destroy()
        self.__init__(self.sides)

    def valid_word(self,word):
        #return self.board.valid_word(word)
        return self.board.valid_word_fast(word)

    def get_all_words(self,word_list=[]):
        if not word_list: word_list = SCRABBLE_WORDS
        words_on_board = []
        num_words = len(word_list)/100
        for i in word_list:
            if self.valid_word(i):
                print(i)
                words_on_board.append(i)
        return sorted(words_on_board,key=len)

    def pmatch_word_list(self, word, wl):
        for j in range(len(word)):
            if word[:-j] in wl: return True
        return False

    def to_paper(self, words_on_board):
        fname = 'boggle-'+str(self.board.letters[:5])
        f = open(fname+'.tex','w+')
        #write board:
        f.write(r'\documentclass[letterpaper,12pt]{article}'+'\n')
        f.write(r'\pagestyle{empty}'+'\n')
        f.write(r'\usepackage{multicol}'+'\n')
        f.write(r'\begin{document}'+'\n\n')
        f.write(r'\fbox{\Huge Boggle -- '+str(self.board.letters[:5])+'}\n\\hrule\n')
        f.write('\\vspace{2pc}\n\n\\begin{center}\n')
        f.write('{\\large\n\\begin{tabular}{|'+'c|'*self.sides+'}\n')
        c = 0
        for i in range(self.sides):
            line = ''
            for j in range(self.sides):
                line += ' ' + self.board.pieces[c].get_letter()+' '
                c += 1
                if j < self.sides -1: line += '&'
                elif j == self.sides -1: line += r'\\\hline'+'\n'
            f.write(line)
        f.write(r'\end{tabular}'+'\n}\n\n')
        f.write('\\end{center}\n')
        f.write(r'\newpage'+'\n\n')
        f.write(r'\section{Words on Board}'+'\n')
        f.write(r'\begin{multicols}{5}'+'\n')
        for word in words_on_board: f.write(word +'\n\n')
        f.write(r'\end{multicols}'+'\n')
        f.write(r'\end{document}')
        f.close()
        os.system('pst.bat '+fname)
        os.system('clean.bat')
        

        #todo: print multi-column word list on next page.
            
            
def test():
    return Game()

def timer():
    s = time()
    time_remaining = GAME_TIME
    while time_remaining > 0:
        if int(GAME_TIME-(time()-s)) != time_remaining:
            time_remaining = int(GAME_TIME - (time() - s))
            print(format_time(time_remaining))
    print('Out of time.')

def format_time(seconds=0):
    m = seconds / 60
    s = seconds % 60
    return '{0}:{1}'.format(m, s)
    
def play():
    a = Game()
    s = time()
    time_remaining = GAME_TIME
    

def str_to_board(s = ''):
    """A comma separated list of letters on the board
    with given side lengths, dim"""
    t = s.split(',')
    b = []
    for i in t:
        p = []
        for k in range(6):
            
            p.append(i.upper())
        b.append(Piece(p))
    return b

def solve_board(b = ''):
    """
    Takes a string representation of a board
    """
    p = str_to_board(b)
    a = Game(sides=int(len(p)**.5),pieces=p,)
    b = a.get_all_words()
    return a, b
    
def get_my_pieces():
    b= [
        ['u','o','i','h','u'],
        ['a','e','x','d','l'],
        ['er','p','r','r','e'],
        ['n','p','o','e','g'],
        ['d','e','g','s','w']
        ]
    
    pieces = []
    for i in b:
        for j in i:
            letters = []
            for k in range(5):
                letters.append(j.upper())
            pieces.append(Piece(letters))
    return pieces

def go():
    p = get_my_pieces()
    g = Game(pieces=p)
    w = g.board.pieces_in_word('perp')
    p = g.board.get_all_paths2('perp')
    return g, w, p
