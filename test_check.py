import pytest
import main
import pygame


wqueen_image = pygame.image.load(r"Images\wqueen.png")
wbishop_image = pygame.image.load(r"Images\wbishop.png")
wknight_image = pygame.image.load(r"Images\wknight.png")
wrook_image = pygame.image.load(r"Images\wrook.png")
wpawn_image = pygame.image.load(r"Images\wpawn.png")

bking_image = pygame.image.load(r"Images\bking.png")
bqueen_image = pygame.image.load(r"Images\bqueen.png")
bbishop_image = pygame.image.load(r"Images\bbishop.png")
bknight_image = pygame.image.load(r"Images\bknight.png")
brook_image = pygame.image.load(r"Images\brook.png")
bpawn_image = pygame.image.load(r"Images\bpawn.png")

board_image = pygame.image.load(
    r"Images\board.png")
wking_image = pygame.image.load(
    r"Images\wking.png").convert_alpha()

class Piece:
    def __init__(self, name, xpos, ypos, colour, image=wking_image, move_num=0):
        self.xpos = xpos
        self.ypos = ypos
        self.colour = colour
        self.name = name
        self.image = image
        self.placerx = 125 + self.xpos * 75
        self.placery = self.ypos * 75
        self.move_num = move_num

    def info(self):
        print(self.xpos, self.ypos)
        pass

    def namer(self):
        print(self.name)

    def place(self):
        board[self.ypos - 1][self.xpos - 1] = self.name

class Game:
    def __init__(self,wp,bp, move, wking, bking, checking_pieces=[]):
        self.wp = wp
        self.bp = bp
        self.ap = wp + bp
        self.move = move
        self.wking = wking
        self.bking = bking
        self.checking_pieces = checking_pieces


board = [[" " for i in range(8)] for i in range(8)]

@pytest.mark.parametrize("wking,bking,wp, bp, expected_result, move", [
    (Piece(f"wk", 7, 8, "w", wking_image), #TEST CASE 1
        Piece(f"bk", 7, 2, "w", bking_image),
        [Piece(f"wk", 7, 8, "w", wking_image),
         Piece(f"wb1", 3, 8, "w", wbishop_image),
         Piece(f"wn1", 2, 8, "w", wknight_image),
         Piece(f"wn2", 3, 1, "w", wknight_image),
         Piece(f"wr1", 1, 8, "w", wrook_image),
         Piece(f"wr2", 5, 8, "w", wrook_image),
         Piece(f"wp1", 1, 7, "w", wpawn_image),
         Piece(f"wp2", 2, 6, "w", wpawn_image),
         Piece(f"wp3", 3, 4, "w", wpawn_image),
         Piece(f"wp4", 4, 3, "w", wpawn_image),
         Piece(f"wp5", 6, 7, "w", wpawn_image),
         Piece(f"wp6", 7, 7, "w", wpawn_image),
         Piece(f"wp7", 8, 7, "w", wpawn_image)],
        [Piece(f"bk", 7, 2, "b", bking_image),
         Piece(f"bp1", 6, 2, "b", bpawn_image),
         Piece(f"bp2", 7, 3, "b", bpawn_image),
         Piece(f"bp3", 1, 3, "b", bpawn_image)],
        True,
        False),
    (Piece(f"wk", 7, 8, "w", wking_image), #TEST CASE 2
        Piece(f"bk", 5, 1, "b", bking_image),
        [Piece(f"wk", 7, 8, "w", wking_image),
         Piece(f"wp1", 1, 7, "w", wpawn_image),
        Piece(f"wp2", 2, 7, "w", wpawn_image),
        Piece(f"wp3", 3, 7, "w", wpawn_image),
        Piece(f"wp4", 4, 6, "w", wpawn_image),
        Piece(f"wp5", 6, 7, "w", wpawn_image),
        Piece(f"wp6", 7, 6, "w", wpawn_image),
        Piece(f"wp7", 8, 7, "w", wpawn_image),
        Piece(f"wq", 6, 8, "w", wqueen_image),
        Piece(f"wr1", 1, 8, "w", wrook_image),
        Piece(f"wn1", 3, 4, "w", wpawn_image),
     ],
     [  Piece(f"bk", 5, 1, "b", bking_image),
        Piece(f"bp1", 1, 2, "b", bpawn_image),
        Piece(f"bp2", 3, 3, "b", bpawn_image),
        Piece(f"bp3", 6, 2, "b", bpawn_image),
        Piece(f"bp4", 7, 2, "b", bpawn_image),
        Piece(f"bp5", 8, 2, "b", bpawn_image),
        Piece(f"bq", 7, 4, "b", bqueen_image),
        Piece(f"br1", 1, 1, "b", brook_image),
        Piece(f"br2", 8, 1, "b", brook_image),
        Piece(f"bn1", 7, 1, "b", bpawn_image)],
     False,
     True
     ),
    (Piece(f"wk", 2, 7, "w", wking_image), #TEST CASE 3
        Piece(f"bk", 7, 1, "b", bking_image),
        [Piece(f"wk", 2, 7, "w", wking_image),
        Piece(f"wq", 5, 4, "w", wqueen_image),
        Piece(f"wb1", 4, 3, "w", wbishop_image),
     ],
     [  Piece(f"bk", 7, 1, "b", bking_image),
        Piece(f"bp1", 2, 5, "b", bpawn_image),
        Piece(f"bp2", 6, 2, "b", bpawn_image),
        Piece(f"bp3", 8, 2, "b", bpawn_image),
        Piece(f"bq", 2, 1, "b", bqueen_image)],
     False,
     False
    ),
    (Piece(f"wk", 8, 1, "w", wking_image), #TEST CASE 4
        Piece(f"bk", 6, 3, "b", bking_image),
        [Piece(f"wk", 8, 1, "w", wking_image),
         Piece(f"wp1", 8, 2, "w", wpawn_image),
        Piece(f"wp2", 7, 2, "w", wpawn_image)],
        [Piece(f"bk", 6, 3, "b", bking_image),
        Piece(f"bb1", 1, 8, "b", bbishop_image),
        Piece(f"bn1", 8, 3, "b", bknight_image)],
        False,
        True),
    (Piece(f"wk", 7, 8, "w", wking_image), #TEST CASE 5
        Piece(f"bk", 5, 1, "b", bking_image),
        [Piece(f"wk", 7, 8, "w", wking_image),
         Piece(f"wp1", 1, 7, "w", wpawn_image),
        Piece(f"wp2", 2, 7, "w", wpawn_image),
        Piece(f"wp3", 3, 7, "w", wpawn_image),
        Piece(f"wp4", 4, 6, "w", wpawn_image),
        Piece(f"wp5", 6, 7, "w", wpawn_image),
        Piece(f"wp6", 7, 7, "w", wpawn_image),
        Piece(f"wp7", 8, 7, "w", wpawn_image),
        Piece(f"wq", 4, 8, "w", wqueen_image),
        Piece(f"wr1", 1, 8, "w", wrook_image),
        Piece(f"wr2", 6, 8, "w", wrook_image),
        Piece(f"wn1", 3, 6, "w", wpawn_image),
        Piece(f"wn2", 6, 6, "w", wpawn_image),
         Piece(f"wb1", 3, 8, "w", wbishop_image),
         Piece(f"wb2", 3, 3, "w", wbishop_image)
     ],
     [  Piece(f"bk", 5, 1, "b", bking_image),
        Piece(f"bp1", 1, 2, "b", bpawn_image),
        Piece(f"bp2", 2, 2, "b", bpawn_image),
        Piece(f"bp3", 3, 4, "b", bpawn_image),
        Piece(f"bp4", 6, 2, "b", bpawn_image),
        Piece(f"bp5", 7, 2, "b", bpawn_image),
        Piece(f"bp6", 8, 2, "b", bpawn_image),
        Piece(f"bq", 4, 1, "b", bqueen_image),
        Piece(f"br1", 1, 1, "b", brook_image),
        Piece(f"br2", 8, 1, "b", brook_image),
        Piece(f"bn1", 7, 1, "b", bpawn_image),
        Piece(f"bb1", 3, 1, "b", bbishop_image),
        Piece(f"bb2", 6, 3, "b", bbishop_image)],
     False,
     False
    ),
    (Piece(f"wk", 8, 8, "w", wking_image), #TEST CASE 6
        Piece(f"bk", 3, 1, "b", bking_image),
        [Piece(f"wk", 8, 8, "w", wking_image),
         Piece(f"wp1", 1, 7, "w", wpawn_image),
        Piece(f"wp2", 3, 5, "w", wpawn_image),
        Piece(f"wp3", 4, 4, "w", wpawn_image),
        Piece(f"wp4", 6, 7, "w", wpawn_image),
        Piece(f"wp5", 7, 7, "w", wpawn_image),
        Piece(f"wp6", 8, 7, "w", wpawn_image),
        Piece(f"wq", 4, 1, "w", wqueen_image),
        Piece(f"wr1", 1, 8, "w", wrook_image),
        Piece(f"wr2", 6, 8, "w", wrook_image),
        Piece(f"wn1", 4, 7, "w", wpawn_image),
        Piece(f"wb1", 2, 3, "w", wbishop_image),
     ],
     [  Piece(f"bk", 3, 1, "b", bking_image),
        Piece(f"bp1", 1, 3, "b", bpawn_image),
        Piece(f"bp2", 2, 2, "b", bpawn_image),
        Piece(f"bp3", 4, 3, "b", bpawn_image),
        Piece(f"bp4", 5, 4, "b", bpawn_image),
        Piece(f"bp5", 6, 3, "b", bpawn_image),
        Piece(f"bp6", 7, 3, "b", bpawn_image),
        Piece(f"bp7", 8, 2, "b", bpawn_image),
        Piece(f"bq", 2, 7, "b", bqueen_image),
        Piece(f"bn1", 6, 2, "b", bpawn_image),
        Piece(f"br1", 8, 1, "b", brook_image),
        Piece(f"bb1", 6, 1, "b", bbishop_image)],
     False,
     False
    ),
    (Piece(f"wk", 7, 8, "w", wking_image), #TEST CASE 7
        Piece(f"bk", 1, 5, "b", bking_image),
        [Piece(f"wk", 7, 8, "w", wking_image),
         Piece(f"wp1", 6, 7, "w", wpawn_image),
        Piece(f"wp2", 7, 7, "w", wpawn_image),
        Piece(f"wp3", 8, 6, "w", wpawn_image),
        Piece(f"wq", 2,5, "w", wqueen_image),
        Piece(f"wr1", 3, 8, "w", wrook_image),
        Piece(f"wn1", 4, 4, "w", wpawn_image),
        Piece(f"wn2", 6, 2, "w", wpawn_image),
     ],
     [  Piece(f"bk", 1, 5, "b", bking_image),
        Piece(f"bp1", 1, 2, "b", bpawn_image),
        Piece(f"bp2", 1, 3, "b", bpawn_image),
        Piece(f"bp3", 6, 3, "b", bpawn_image),
        Piece(f"bp4", 8, 2, "b", bpawn_image),
        Piece(f"br1", 1, 7, "b", brook_image),
    ],
     True,
     False
    ),
    (Piece(f"wk", 7, 6, "w", wking_image), #TEST CASE 8
        Piece(f"bk", 5, 1, "b", bking_image),
        [Piece(f"wk", 7, 6, "w", wking_image),
         Piece(f"wp1", 1, 6, "w", wpawn_image),
        Piece(f"wp2", 2, 7, "w", wpawn_image),
        Piece(f"wp3", 3, 7, "w", wpawn_image),
        Piece(f"wp4", 5, 6, "w", wpawn_image),
        Piece(f"wp5", 7, 7, "w", wpawn_image),
        Piece(f"wr1", 4, 7, "w", wrook_image),
        Piece(f"wb1", 2, 6, "w", wbishop_image)
     ],
     [  Piece(f"bk", 1, 4, "b", bking_image),
        Piece(f"bp1", 1, 2, "b", bpawn_image),
        Piece(f"bp2", 2, 2, "b", bpawn_image),
        Piece(f"bp3", 3, 2, "b", bpawn_image),
        Piece(f"bp4", 5, 4, "b", bpawn_image),
        Piece(f"bp5", 8, 3, "b", bpawn_image),
        Piece(f"bp6", 8, 5, "b", bpawn_image),
        Piece(f"br1", 5, 2, "b", brook_image),
        Piece(f"bn1", 3, 3, "b", bpawn_image),
        Piece(f"bb1", 5, 5, "b", bbishop_image)],
     True,
     True
    ),
    (Piece(f"wk", 3, 8, "w", wking_image), #TEST CASE 9
        Piece(f"bk", 4, 1, "b", bking_image),
        [Piece(f"wk", 3, 8, "w", wking_image),
         Piece(f"wp1", 1, 7, "w", wpawn_image),
        Piece(f"wp2", 2, 7, "w", wpawn_image),
        Piece(f"wp3", 3, 7, "w", wpawn_image),
        Piece(f"wq", 8, 2, "w", wqueen_image),
        Piece(f"wr1", 1, 1, "w", wrook_image),
        Piece(f"wb1", 6, 7, "w", wbishop_image)
     ],
     [  Piece(f"bk", 4, 1, "b", bking_image),
        Piece(f"bp1", 2, 5, "b", bpawn_image),
        Piece(f"bp2", 3, 5, "b", bpawn_image)],
     True,
     False
    ),
    (Piece(f"wk", 5, 8, "w", wking_image), #TEST CASE 10
        Piece(f"bk", 6, 2, "b", bking_image),
        [Piece(f"wk", 5, 8, "w", wking_image),
         Piece(f"wp1", 6, 6, "w", wpawn_image),
        Piece(f"wp2", 7, 5, "w", wpawn_image),
        Piece(f"wp3", 8, 7, "w", wpawn_image),
        Piece(f"wb1", 6, 8, "w", wbishop_image),
        Piece(f"wr1", 8, 8, "w", wrook_image),
        Piece(f"wn1", 3, 3, "w", wpawn_image),
     ],
     [  Piece(f"bk", 6, 2, "b", bking_image),
        Piece(f"bp1", 1, 2, "b", bpawn_image),
        Piece(f"bp2", 7, 2, "b", bpawn_image),
        Piece(f"bp3", 8, 2, "b", bpawn_image),
        Piece(f"bb1", 1, 8, "b", bbishop_image),
        Piece(f"bb2", 6, 4, "b", bbishop_image),
        Piece(f"br1", 1, 7, "b", brook_image),
        Piece(f"br2", 2, 8, "b", brook_image),
        Piece(f"bn1", 6, 3, "b", bpawn_image)],
     True,
     True
     ),
    (Piece(f"wk", 7, 8, "w", wking_image), #TEST CASE 11
        Piece(f"bk", 5, 1, "b", bking_image),
        [Piece(f"wk", 7, 8, "w", wking_image),
         Piece(f"wp1", 1, 7, "w", wpawn_image),
        Piece(f"wp2", 3, 5, "w", wpawn_image),
        Piece(f"wp3", 6, 7, "w", wpawn_image),
        Piece(f"wp4", 7, 6, "w", wpawn_image),
        Piece(f"wp5", 8, 5, "w", wpawn_image),
        Piece(f"wq", 1, 5, "w", wqueen_image),
        Piece(f"wr1", 2, 8, "w", wrook_image),
        Piece(f"wr2", 6, 8, "w", wrook_image),
        Piece(f"wn1", 3, 2, "w", wpawn_image),
        Piece(f"wb1", 6, 3, "w", wbishop_image),
        Piece(f"wb2", 5, 7, "w", wpawn_image),
     ],
     [  Piece(f"bk", 5, 1, "b", bking_image),
        Piece(f"bp1", 1, 2, "b", bpawn_image),
        Piece(f"bp2", 4, 6, "b", bpawn_image),
        Piece(f"bp3", 6, 2, "b", bpawn_image),
        Piece(f"bp4", 8, 4, "b", bpawn_image),
        Piece(f"bq", 2, 3, "b", bqueen_image),
        Piece(f"br1", 1, 1, "b", brook_image),
        Piece(f"bn1", 2, 1, "b", bpawn_image),
        Piece(f"bb1", 6, 1, "b", bbishop_image),
        Piece(f"bb2", 5, 3, "b", bbishop_image)],
     False,
     True
     ),
    (Piece(f"wk", 6, 7, "w", wking_image), #TEST CASE 12
        Piece(f"bk", 8, 1, "b", bking_image),
        [Piece(f"wk", 6, 7, "w", wking_image),
        Piece(f"wr1", 8, 8, "w", wrook_image),
        Piece(f"wn1", 6, 3, "w", wpawn_image),
        Piece(f"wb1", 6, 1, "w", wbishop_image)
     ],
     [  Piece(f"bk", 8, 1, "b", bking_image)],
     False,
     True
     ),
    (Piece(f"wk", 5, 8, "w", wking_image), #TEST CASE 13
        Piece(f"bk", 5, 1, "b", bking_image),
        [Piece(f"wk", 5, 8, "w", wking_image),
         Piece(f"wp1", 1, 7, "w", wpawn_image),
        Piece(f"wp2", 2, 7, "w", wpawn_image),
        Piece(f"wp3", 3, 5, "w", wpawn_image),
        Piece(f"wp4", 6, 7, "w", wpawn_image),
        Piece(f"wp5", 7, 7, "w", wpawn_image),
        Piece(f"wp6", 8, 7, "w", wpawn_image),
        Piece(f"wq", 4, 1, "w", wqueen_image),
        Piece(f"wn1", 2, 8, "w", wknight_image),
        Piece(f"wb1", 3, 8, "w", wbishop_image),
        Piece(f"wn2", 6, 6, "w", wknight_image),
        Piece(f"wr1", 1, 8, "w", wrook_image),
        Piece(f"wn1", 8, 8, "w", wpawn_image),
     ],
     [  Piece(f"bk", 5, 1, "b", bking_image),
        Piece(f"bp1", 1, 2, "b", bpawn_image),
        Piece(f"bp2", 1, 3, "b", bpawn_image),
        Piece(f"bp3", 5, 4, "b", bpawn_image),
        Piece(f"bp4", 6, 2, "b", bpawn_image),
        Piece(f"bp5", 7, 2, "b", bpawn_image),
        Piece(f"bp6", 8, 2, "b", bpawn_image),
        Piece(f"br1", 1, 1, "b", brook_image),
        Piece(f"br2", 8, 1, "b", brook_image),
        Piece(f"bn1", 6, 3, "b", bpawn_image),
        Piece(f"bb1", 3, 1, "b", bbishop_image),
        Piece(f"bb2", 6, 1, "b", bbishop_image)],
     False,
     False
     ),
    (Piece(f"wk", 3, 2, "w", wking_image), #TEST CASE 14
        Piece(f"bk", 7, 3, "b", bking_image),
        [Piece(f"wk", 3, 2, "w", wking_image),
         Piece(f"wp1", 1, 7, "w", wpawn_image),
        Piece(f"wp2", 3, 6, "w", wpawn_image),
        Piece(f"wp3", 6, 7, "w", wpawn_image),
        Piece(f"wp4", 7, 6, "w", wpawn_image),
        Piece(f"wp5", 8, 7, "w", wpawn_image),
        Piece(f"wn1", 2, 5, "w", wknight_image),
        Piece(f"wr1", 1, 8, "w", wrook_image),
        Piece(f"wr2", 3, 2, "w", wrook_image),
     ],
     [  Piece(f"bk", 7, 3, "b", bking_image),
        Piece(f"bp1", 1, 3, "b", bpawn_image),
        Piece(f"bp2", 3, 5, "b", bpawn_image),
        Piece(f"bp3", 6, 3, "b", bpawn_image),
        Piece(f"bp4", 8, 3, "b", bpawn_image),
        Piece(f"br1", 4, 1, "b", brook_image),
        Piece(f"br2", 4, 8, "b", brook_image),
        Piece(f"bb1", 2, 2, "b", bbishop_image)],
     False,
     True
     ),
    (Piece(f"wk", 5, 8, "w", wking_image), #TEST CASE 15
        Piece(f"bk", 8, 1, "b", bking_image),
        [Piece(f"wk", 5, 8, "w", wking_image),
         Piece(f"wp1", 1, 7, "w", wpawn_image),
        Piece(f"wp2", 3, 6, "w", wpawn_image),
        Piece(f"wp3", 4, 5, "w", wpawn_image),
        Piece(f"wp4", 6, 7, "w", wpawn_image),
        Piece(f"wp5", 7, 7, "w", wpawn_image),
        Piece(f"wp6", 8, 7, "w", wpawn_image),
        Piece(f"wq", 5, 4, "w", wqueen_image),
        Piece(f"wn1", 7, 4, "w", wknight_image),
        Piece(f"wb1", 6, 2, "w", wbishop_image),
        Piece(f"wb2", 3, 8, "w", wbishop_image),
        Piece(f"wr1", 1, 8, "w", wrook_image),
        Piece(f"wn1", 8, 8, "w", wpawn_image),
     ],
     [  Piece(f"bk", 8, 1, "b", bking_image),
        Piece(f"bp1", 1, 2, "b", bpawn_image),
        Piece(f"bp2", 2, 2, "b", bpawn_image),
        Piece(f"bp3", 3, 2, "b", bpawn_image),
        Piece(f"bp4", 4, 2, "b", bpawn_image),
        Piece(f"bp5", 7, 3, "b", bpawn_image),
        Piece(f"bp6", 8, 2, "b", bpawn_image),
        Piece(f"bq", 4, 1, "b", bqueen_image),
        Piece(f"br1", 1, 1, "b", brook_image),
        Piece(f"br2", 6, 1, "b", brook_image),
        Piece(f"bn1", 1, 4, "b", bpawn_image),
        Piece(f"bb1", 3, 1, "b", bbishop_image)],
     False,
     False
     ),
    (Piece(f"wk", 3, 8, "w", wking_image), #TEST CASE 16
        Piece(f"bk", 5, 1, "b", bking_image),
        [Piece(f"wk", 3, 8, "w", wking_image),
         Piece(f"wp1", 1, 7, "w", wpawn_image),
        Piece(f"wp2", 2, 7, "w", wpawn_image),
        Piece(f"wp3", 3, 7, "w", wpawn_image),
        Piece(f"wp4", 5, 5, "w", wpawn_image),
        Piece(f"wp5", 7, 7, "w", wpawn_image),
        Piece(f"wq", 4, 7, "w", wqueen_image),
        Piece(f"wn1", 3, 6, "w", wknight_image),
        Piece(f"wb1", 2, 4, "w", wbishop_image),
        Piece(f"wb2", 3, 4, "w", wbishop_image),
        Piece(f"wr1", 4, 8, "w", wrook_image),
        Piece(f"wn1", 8, 4, "w", wpawn_image),
     ],
     [  Piece(f"bk", 5, 1, "b", bking_image),
        Piece(f"bp1", 1, 2, "b", bpawn_image),
        Piece(f"bp2", 2, 2, "b", bpawn_image),
        Piece(f"bp3", 5, 4, "b", bpawn_image),
        Piece(f"bp4", 6, 2, "b", bpawn_image),
        Piece(f"bp5", 8, 3, "b", bpawn_image),
        Piece(f"bq", 6, 6, "b", bqueen_image),
        Piece(f"br1", 1, 1, "b", brook_image),
        Piece(f"br2", 7, 5, "b", brook_image),
        Piece(f"bn1", 2, 3, "b", bpawn_image),
        Piece(f"bb1", 3, 1, "b", bbishop_image)],
     False,
     False
     ),
    (Piece(f"wk", 5, 8, "w", wking_image), #TEST CASE 17
        Piece(f"bk", 7, 1, "b", bking_image),
        [Piece(f"wk", 5, 8, "w", wking_image),
         Piece(f"wp1", 1, 7, "w", wpawn_image),
        Piece(f"wp2", 2, 7, "w", wpawn_image),
        Piece(f"wp3", 3, 6, "w", wpawn_image),
        Piece(f"wp4", 4, 5, "w", wpawn_image),
        Piece(f"wp5", 6, 7, "w", wpawn_image),
        Piece(f"wp6", 7, 5, "w", wpawn_image),
        Piece(f"wp7", 8, 5, "w", wpawn_image),
        Piece(f"wq", 5, 6, "w", wqueen_image),
        Piece(f"wn1", 4, 7, "w", wknight_image),
        Piece(f"wn2", 6, 6, "w", wknight_image),
        Piece(f"wb1", 4, 6, "w", wbishop_image),
        Piece(f"wr1", 4, 8, "w", wrook_image),
        Piece(f"wr2", 8, 8, "w", wrook_image),
     ],
     [  Piece(f"bk", 7, 1, "b", bking_image),
        Piece(f"bp1", 1, 3, "b", bpawn_image),
        Piece(f"bp2", 2, 4, "b", bpawn_image),
        Piece(f"bp3", 3, 2, "b", bpawn_image),
        Piece(f"bp4", 4, 4, "b", bpawn_image),
        Piece(f"bp5", 5, 3, "b", bpawn_image),
        Piece(f"bp6", 6, 2, "b", bpawn_image),
        Piece(f"bp7", 7, 2, "b", bpawn_image),
        Piece(f"bp8", 8, 3, "b", bpawn_image),
        Piece(f"bq", 4, 1, "b", bqueen_image),
        Piece(f"br1", 1, 1, "b", brook_image),
        Piece(f"br2", 6, 1, "b", brook_image),
        Piece(f"bn1", 3, 3, "b", bknight_image),
        Piece(f"bn2", 7, 7, "b", bknight_image),
        Piece(f"bb1", 3, 1, "b", bbishop_image)],
     False,
     True
     ),
    (Piece(f"wk", 7, 8, "w", wking_image), #TEST CASE 18
        Piece(f"bk", 7, 1, "b", bking_image),
        [Piece(f"wk", 7, 8, "w", wking_image),
         Piece(f"wp1", 1, 6, "w", wpawn_image),
        Piece(f"wp2", 2, 7, "w", wpawn_image),
        Piece(f"wp3", 3, 6, "w", wpawn_image),
        Piece(f"wp4", 5, 4, "w", wpawn_image),
        Piece(f"wp5", 6, 7, "w", wpawn_image),
        Piece(f"wq", 3, 2, "w", wqueen_image),
        Piece(f"wr1", 5, 8, "w", wrook_image),
        Piece(f"wr2", 6, 8, "w", wrook_image),
     ],
     [  Piece(f"bk", 7, 1, "b", bking_image),
        Piece(f"bp1", 1, 4, "b", bpawn_image),
        Piece(f"bp2", 2, 3, "b", bpawn_image),
        Piece(f"bp3", 4, 4, "b", bpawn_image),
        Piece(f"bp4", 5, 3, "b", bpawn_image),
        Piece(f"bp5", 7, 4, "b", bpawn_image),
        Piece(f"bq", 7, 5, "b", bqueen_image),
        Piece(f"br1", 6, 1, "b", brook_image),],
     False,
     True
     )




    ])


def test_check(wking,bking,wp,bp,expected_result,move):
    t = [[" " for i in range(8)] for i in range(8)]
    G = Game(wp, bp, move, wking, bking, [])

    print(G.checking_pieces)
    print(expected_result)

    for piece in G.ap:
        print(piece.name, piece.xpos, piece.ypos)
        t[piece.ypos - 1][piece.xpos - 1] = piece.name
    print("".join([f"\n{i}" for i in t]))


    print(G.checking_pieces)

    if main.check_checker(G) is True:
        assert main.checkmate_checker(G) is expected_result




    print("here")