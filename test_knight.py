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

@pytest.mark.parametrize("wking,bking,knight,wp, bp, expected_result, move,x,y", [
    (Piece(f"wk", 4, 8, "w", wking_image), #TEST CASE 1
            Piece(f"bk", 6, 2, "w", bking_image),
            Piece(f"wn1",6,7,"w",wknight_image),
            [Piece(f"wk", 4, 8, "w", wking_image),
             Piece(f"wn1", 6, 7, "w", wknight_image),
             Piece(f"wr1", 1, 7, "w", wrook_image),
             Piece(f"wp1", 2, 7, "w", wpawn_image),
             Piece(f"wq", 7, 5, "w", wqueen_image)],
            [Piece(f"bk", 7, 2, "b", bking_image),
             Piece(f"bp1", 6, 2, "b", bpawn_image),
             Piece(f"bb1", 5, 5, "b", bbishop_image),
             Piece(f"br1", 2, 2, "b", brook_image)],
            True,
            True,
            2,
            -1),
    (Piece(f"wk", 4, 8, "w", wking_image), #TEST CASE 2
            Piece(f"bk", 6, 2, "w", bking_image),
            Piece(f"wn1",6,7,"w",wknight_image),
            [Piece(f"wk", 4, 8, "w", wking_image),
             Piece(f"wn1", 6, 7, "w", wknight_image),
             Piece(f"wr1", 1, 7, "w", wrook_image),
             Piece(f"wp1", 2, 7, "w", wpawn_image),
             Piece(f"wq", 7, 5, "w", wqueen_image)],
            [Piece(f"bk", 7, 2, "b", bking_image),
             Piece(f"bp1", 6, 2, "b", bpawn_image),
             Piece(f"bb1", 5, 5, "b", bbishop_image),
             Piece(f"br1", 2, 2, "b", brook_image)],
            True,
            True,
            -1,
            -2),
    (Piece(f"wk", 4, 8, "w", wking_image), #TEST CASE 3
            Piece(f"bk", 6, 2, "w", bking_image),
            Piece(f"wn1",6,7,"w",wknight_image),
            [Piece(f"wk", 4, 8, "w", wking_image),
             Piece(f"wn1", 6, 7, "w", wknight_image),
             Piece(f"wr1", 1, 7, "w", wrook_image),
             Piece(f"wp1", 2, 7, "w", wpawn_image),
             Piece(f"wq", 7, 5, "w", wqueen_image)],
            [Piece(f"bk", 7, 2, "b", bking_image),
             Piece(f"bp1", 6, 2, "b", bpawn_image),
             Piece(f"bb1", 5, 5, "b", bbishop_image),
             Piece(f"br1", 2, 2, "b", brook_image)],
            True,
            False,
            0,
            -2),
    (Piece(f"wk", 4, 8, "w", wking_image), #TEST CASE 4
            Piece(f"bk", 6, 2, "w", bking_image),
            Piece(f"wn1",6,7,"w",wknight_image),
            [Piece(f"wk", 4, 8, "w", wking_image),
             Piece(f"wn1", 6, 7, "w", wknight_image),
             Piece(f"wr1", 1, 7, "w", wrook_image),
             Piece(f"wp1", 2, 7, "w", wpawn_image),
             Piece(f"wq", 7, 5, "w", wqueen_image)],
            [Piece(f"bk", 7, 2, "b", bking_image),
             Piece(f"bp1", 6, 2, "b", bpawn_image),
             Piece(f"bb1", 5, 5, "b", bbishop_image),
             Piece(f"br1", 2, 2, "b", brook_image)],
            True,
            False,
            1,
            -2),
    (Piece(f"wk", 4, 8, "w", wking_image), #TEST CASE 5
            Piece(f"bk", 6, 2, "w", bking_image),
            Piece(f"wn1",6,7,"w",wknight_image),
            [Piece(f"wk", 4, 8, "w", wking_image),
             Piece(f"wn1", 6, 7, "w", wknight_image),
             Piece(f"wr1", 1, 7, "w", wrook_image),
             Piece(f"wp1", 2, 7, "w", wpawn_image),
             Piece(f"wq", 7, 5, "w", wqueen_image)],
            [Piece(f"bk", 7, 2, "b", bking_image),
             Piece(f"bp1", 6, 2, "b", bpawn_image),
             Piece(f"bb1", 5, 5, "b", bbishop_image),
             Piece(f"br1", 2, 2, "b", brook_image)],
            True,
            False,
            -1,
            2)

    ])


def test_knight(wking,bking,knight,wp,bp,expected_result,move,x,y):
    t = [[" " for i in range(8)] for i in range(8)]
    G = Game(wp, bp, move, wking, bking, [])

    startx,starty = knight.xpos,knight.ypos

    # for piece in G.ap:
    #     print(piece.name, piece.xpos, piece.ypos)
    #     t[piece.ypos - 1][piece.xpos - 1] = piece.name
    # print("".join([f"\n{i}" for i in t]))
    #
    #
    # print(G.checking_pieces)

    if main.check_checker(G) is True:
        assert main.knight_moves(G,x,y,starty,startx,knight) is expected_result


