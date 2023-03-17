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

@pytest.mark.parametrize("wking,bking,queen,wp, bp, expected_result, move,x,y", [
    (Piece(f"wk", 8, 7, "w", wking_image), #TEST CASE 1
            Piece(f"bk", 8, 1, "w", bking_image),
            Piece(f"bq",7,3,"b",bqueen_image),
            [Piece(f"wk", 8, 7, "w", wking_image),
             Piece(f"wb1", 2, 3, "w", wbishop_image),
             Piece(f"wr1", 4, 6, "w", wrook_image),
             Piece(f"wp1", 1, 6, "w", wpawn_image),
             Piece(f"wp2", 2, 5, "w", wpawn_image),
             Piece(f"wp3", 5, 5, "w", wpawn_image),
             Piece(f"wp4", 6, 7, "w", wpawn_image),
             Piece(f"wp5", 7, 7, "w", wpawn_image),
             Piece(f"wp1", 8, 6, "w", wpawn_image),
             Piece(f"wq", 5, 3, "w", wqueen_image)],
            [Piece(f"bk", 8, 1, "b", bking_image),
             Piece(f"bp1", 1, 3, "b", bpawn_image),
             Piece(f"bp2", 2, 4, "b", bpawn_image),
             Piece(f"bp3", 5, 4, "b", bpawn_image),
             Piece(f"bp4", 7, 2, "b", bpawn_image),
             Piece(f"bp5", 8, 3, "b", bpawn_image),
             Piece(f"bb1", 6, 3, "b", bbishop_image),
             Piece(f"br1", 3, 8, "b", brook_image),
             Piece(f"bq",7,3,"b",bqueen_image)],
            False,
            True,
            1,
            1),
            (Piece(f"wk", 8, 7, "w", wking_image), #TEST CASE 2
            Piece(f"bk", 8, 1, "w", bking_image),
            Piece(f"bq",7,3,"b",bqueen_image),
            [Piece(f"wk", 8, 7, "w", wking_image),
             Piece(f"wb1", 2, 3, "w", wbishop_image),
             Piece(f"wr1", 4, 6, "w", wrook_image),
             Piece(f"wp1", 1, 6, "w", wpawn_image),
             Piece(f"wp2", 2, 5, "w", wpawn_image),
             Piece(f"wp3", 5, 5, "w", wpawn_image),
             Piece(f"wp4", 6, 7, "w", wpawn_image),
             Piece(f"wp5", 7, 7, "w", wpawn_image),
             Piece(f"wp1", 8, 6, "w", wpawn_image),
             Piece(f"wq", 5, 3, "w", wqueen_image)],
            [Piece(f"bk", 8, 1, "b", bking_image),
             Piece(f"bp1", 1, 3, "b", bpawn_image),
             Piece(f"bp2", 2, 4, "b", bpawn_image),
             Piece(f"bp3", 5, 4, "b", bpawn_image),
             Piece(f"bp4", 7, 2, "b", bpawn_image),
             Piece(f"bp5", 8, 3, "b", bpawn_image),
             Piece(f"bb1", 6, 3, "b", bbishop_image),
             Piece(f"br1", 3, 8, "b", brook_image),
             Piece(f"bq",7,3,"b",bqueen_image)],
            False,
            True,
            0,
            1),
            (Piece(f"wk", 8, 7, "w", wking_image), #TEST CASE 3
            Piece(f"bk", 8, 1, "w", bking_image),
            Piece(f"bq",7,3,"b",bqueen_image),
            [Piece(f"wk", 8, 7, "w", wking_image),
             Piece(f"wb1", 2, 3, "w", wbishop_image),
             Piece(f"wr1", 4, 6, "w", wrook_image),
             Piece(f"wp1", 1, 6, "w", wpawn_image),
             Piece(f"wp2", 2, 5, "w", wpawn_image),
             Piece(f"wp3", 5, 5, "w", wpawn_image),
             Piece(f"wp4", 6, 7, "w", wpawn_image),
             Piece(f"wp5", 7, 7, "w", wpawn_image),
             Piece(f"wp1", 8, 6, "w", wpawn_image),
             Piece(f"wq", 5, 3, "w", wqueen_image)],
            [Piece(f"bk", 8, 1, "b", bking_image),
             Piece(f"bp1", 1, 3, "b", bpawn_image),
             Piece(f"bp2", 2, 4, "b", bpawn_image),
             Piece(f"bp3", 5, 4, "b", bpawn_image),
             Piece(f"bp4", 7, 2, "b", bpawn_image),
             Piece(f"bp5", 8, 3, "b", bpawn_image),
             Piece(f"bb1", 6, 3, "b", bbishop_image),
             Piece(f"br1", 3, 8, "b", brook_image),
             Piece(f"bq",7,3,"b",bqueen_image)],
            False,
            True,
            0,
            4),
            (Piece(f"wk", 8, 7, "w", wking_image), #TEST CASE 4
            Piece(f"bk", 8, 1, "w", bking_image),
            Piece(f"bq",7,3,"b",bqueen_image),
            [Piece(f"wk", 8, 7, "w", wking_image),
             Piece(f"wb1", 2, 3, "w", wbishop_image),
             Piece(f"wr1", 4, 6, "w", wrook_image),
             Piece(f"wp1", 1, 6, "w", wpawn_image),
             Piece(f"wp2", 2, 5, "w", wpawn_image),
             Piece(f"wp3", 5, 5, "w", wpawn_image),
             Piece(f"wp4", 6, 7, "w", wpawn_image),
             Piece(f"wp5", 7, 7, "w", wpawn_image),
             Piece(f"wp1", 8, 6, "w", wpawn_image),
             Piece(f"wq", 5, 3, "w", wqueen_image)],
            [Piece(f"bk", 8, 1, "b", bking_image),
             Piece(f"bp1", 1, 3, "b", bpawn_image),
             Piece(f"bp2", 2, 4, "b", bpawn_image),
             Piece(f"bp3", 5, 4, "b", bpawn_image),
             Piece(f"bp4", 7, 2, "b", bpawn_image),
             Piece(f"bp5", 8, 3, "b", bpawn_image),
             Piece(f"bb1", 6, 3, "b", bbishop_image),
             Piece(f"br1", 3, 8, "b", brook_image),
             Piece(f"bq",7,3,"b",bqueen_image)],
            False,
            True,
            -3,
            3),
            (Piece(f"wk", 8, 7, "w", wking_image), #TEST CASE 1
            Piece(f"bk", 8, 1, "w", bking_image),
            Piece(f"bq",7,3,"b",bqueen_image),
            [Piece(f"wk", 8, 7, "w", wking_image),
             Piece(f"wb1", 2, 3, "w", wbishop_image),
             Piece(f"wr1", 4, 6, "w", wrook_image),
             Piece(f"wp1", 1, 6, "w", wpawn_image),
             Piece(f"wp2", 2, 5, "w", wpawn_image),
             Piece(f"wp3", 5, 5, "w", wpawn_image),
             Piece(f"wp4", 6, 7, "w", wpawn_image),
             Piece(f"wp5", 7, 7, "w", wpawn_image),
             Piece(f"wp1", 8, 6, "w", wpawn_image),
             Piece(f"wq", 5, 3, "w", wqueen_image)],
            [Piece(f"bk", 8, 1, "b", bking_image),
             Piece(f"bp1", 1, 3, "b", bpawn_image),
             Piece(f"bp2", 2, 4, "b", bpawn_image),
             Piece(f"bp3", 5, 4, "b", bpawn_image),
             Piece(f"bp4", 7, 2, "b", bpawn_image),
             Piece(f"bp5", 8, 3, "b", bpawn_image),
             Piece(f"bb1", 6, 3, "b", bbishop_image),
             Piece(f"br1", 3, 8, "b", brook_image),
             Piece(f"bq",7,3,"b",bqueen_image)],
            False,
            False,
            -1,
            0),
            (Piece(f"wk", 8, 7, "w", wking_image), #TEST CASE 1
            Piece(f"bk", 8, 1, "w", bking_image),
            Piece(f"bq",7,3,"b",bqueen_image),
            [Piece(f"wk", 8, 7, "w", wking_image),
             Piece(f"wb1", 2, 3, "w", wbishop_image),
             Piece(f"wr1", 4, 6, "w", wrook_image),
             Piece(f"wp1", 1, 6, "w", wpawn_image),
             Piece(f"wp2", 2, 5, "w", wpawn_image),
             Piece(f"wp3", 5, 5, "w", wpawn_image),
             Piece(f"wp4", 6, 7, "w", wpawn_image),
             Piece(f"wp5", 7, 7, "w", wpawn_image),
             Piece(f"wp1", 8, 6, "w", wpawn_image),
             Piece(f"wq", 5, 3, "w", wqueen_image)],
            [Piece(f"bk", 8, 1, "b", bking_image),
             Piece(f"bp1", 1, 3, "b", bpawn_image),
             Piece(f"bp2", 2, 4, "b", bpawn_image),
             Piece(f"bp3", 5, 4, "b", bpawn_image),
             Piece(f"bp4", 7, 2, "b", bpawn_image),
             Piece(f"bp5", 8, 3, "b", bpawn_image),
             Piece(f"bb1", 6, 3, "b", bbishop_image),
             Piece(f"br1", 3, 8, "b", brook_image),
             Piece(f"bq",7,3,"b",bqueen_image)],
            False,
            False,
            3,
            3)

    ])


def test_queen(wking,bking,queen,wp,bp,expected_result,move,x,y):
    t = [[" " for i in range(8)] for i in range(8)]
    G = Game(wp, bp, move, wking, bking, [])

    startx,starty = queen.xpos,queen.ypos

    # for piece in G.ap:
    #     print(piece.name, piece.xpos, piece.ypos)
    #     t[piece.ypos - 1][piece.xpos - 1] = piece.name
    # print("".join([f"\n{i}" for i in t]))
    #
    #
    # print(G.checking_pieces)

    if main.check_checker(G) is True:
        assert main.queen_moves(G,x,y,starty,startx,queen) is expected_result


