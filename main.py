import pygame
import time
import numpy

#
# import pygame_menu
# TODO: -Checking checking, -checkmate, en passant, castling, promotion, sounds
# TODO: -checkmate
# TODO: -en passant
# TODO: -castling
# TODO: - promotion
# TODO: - sounds


pygame.init()  # initialises pygame, screen and clock
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

# sets up some important constants
white = (255, 255, 255)  # constant for white colour
image_constant = (75, 75)  # constant for image scaling
king_vectors = [(0, 1), (1, 1), (1, 0), (-1, 1), (0, -1), (-1, -1), (-1, 0), (1, -1)]  # possible king move vectors
move = True  # move being true means white to move

# loads all the images from the Images folder and then scales all
board_image = pygame.image.load(
    r"Images\board.png")
wking_image = pygame.image.load(
    r"Images\wking.png").convert_alpha()
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

wking_image = pygame.transform.scale(wking_image, image_constant)
wqueen_image = pygame.transform.scale(wqueen_image, image_constant)
wbishop_image = pygame.transform.scale(wbishop_image, image_constant)
wknight_image = pygame.transform.scale(wknight_image, image_constant)
wrook_image = pygame.transform.scale(wrook_image, image_constant)
wpawn_image = pygame.transform.scale(wpawn_image, image_constant)

bking_image = pygame.transform.scale(bking_image, image_constant)
bqueen_image = pygame.transform.scale(bqueen_image, image_constant)
bbishop_image = pygame.transform.scale(bbishop_image, image_constant)
bknight_image = pygame.transform.scale(bknight_image, image_constant)
brook_image = pygame.transform.scale(brook_image, image_constant)
bpawn_image = pygame.transform.scale(bpawn_image, image_constant)

board = [[" " for i in range(8)] for i in range(8)]  # creates a list of lists of blank text board


def board_text(ap):  # function to print out a text version of the board
    for piece in ap:
        piece.place()
    print("".join([f"\n{i}" for i in board]))


def move_valid(item, xsquare, ysquare, wp, bp, wking, bking, newposx,
               newposy):  # function to see which piece it is and run respective function (could clean this up and put functions in class)
    if item.name[1] == "k":
        movevalid = king_moves(-(newposx - xsquare), ysquare - newposy, newposx, newposy, item)
    elif item.name[1] == "q":
        movevalid = queen_moves(-(newposx - xsquare), ysquare - newposy, newposx, newposy, item)
    elif item.name[1] == "b":
        movevalid = bishop_moves(-(newposx - xsquare), ysquare - newposy, newposx, newposy, item)
    elif item.name[1] == "n":
        movevalid = knight_moves(-(newposx - xsquare), ysquare - newposy, newposx, newposy, item)
    elif item.name[1] == "r":
        movevalid = rook_moves(-(newposx - xsquare), ysquare - newposy, newposx, newposy, item)
    elif item.name[0:2] == "wp":
        movevalid = white_pawn_moves(-(newposx - xsquare), ysquare - newposy, newposx, newposy, item.move_num, item,
                                     takenpiece)
        if movevalid and not check_checker(wp, bp, wking, bking) and turn:
            item.move_num += 1
            tempitem = None
    elif item.name[0:2] == "bp":
        movevalid = black_pawn_moves(-(newposx - xsquare), ysquare - newposy, newposx, newposy, item.move_num, item,
                                     takenpiece)
        if movevalid and not check_checker(wp, bp, wking, bking) and turn:
            item.move_num += 1
            tempitem = None
    else:
        movevalid = True
    return movevalid and not check_checker(wp, bp, wking, bking)


def checkmate_checker(wp, bp, wking, bking, checking_pieces):  # function to check if it is checkmate
    checkmate = True
    global king
    if move:  # see whose move it is in order to determine for who we are detecting checkmate
        pieces = wp
        king = wking
        constant = 1
    else:
        pieces = bp
        king = bking
        constant = -1

    tempx, tempy = king.xpos, king.ypos
    for vector in king_vectors:  # checks if there is anywhere the king can legally move to
        king.xpos, king.ypos = king.xpos + vector[0], king.ypos + vector[1]
        blockage = False
        for piece in pieces:
            if (piece.xpos, piece.ypos) == (king.xpos, king.ypos) and piece != king:
                blockage = True  # blockage sees if there is a piece of the same colour at the new square
        if move_valid(king, king.xpos, king.ypos, wp, bp, wking, bking, tempx, tempy) and not check_checker(wp, bp,
                                                                                                            wking,
                                                                                                            bking) and king.xpos > 0 and king.ypos > 0 and not blockage:
            checkmate = False
            continue
        king.xpos = tempx
        king.ypos = tempy

    for checker in checking_pieces:
        if checker.name[1] == "b":
            for i in range(0, abs(king.xpos - checker.xpos) + 1):
                for piece in pieces:
                    tempx, tempy = piece.xpos, piece.ypos
                    piece.xpos, piece.ypos = checker.xpos + (numpy.sign(king.xpos - checker.xpos) * i), checker.ypos + (
                                numpy.sign(king.ypos - checker.ypos) * i)
                    if i == 0:
                        ap.remove(checker)
                        takenpiece = checker
                        if checker.name[0] == "w":
                            wp.remove(checker)
                        else:
                            bp.remove(checker)
                        tempitem = checker
                    if move_valid(piece, piece.xpos, piece.ypos, wp, bp, wking, bking, tempx,
                                  tempy) and not check_checker(wp, bp, wking, bking):
                        checkmate = False
                        piece.xpos = tempx
                        piece.ypos = tempy
                    else:
                        piece.xpos = tempx
                        piece.ypos = tempy
                    if tempitem:
                        ap.append(tempitem)
                        if tempitem.name[0] == "w":
                            wp.append(tempitem)
                        else:
                            bp.append(tempitem)
                        tempitem = None
        elif checker.name[1] == "r":
            if checker.xpos - king.xpos == 0:
                for i in range(0, abs(king.ypos - checker.ypos)):
                    for piece in pieces:
                        tempx = piece.xpos
                        tempy = piece.ypos
                        piece.ypos = checker.ypos + (numpy.sign(king.ypos - checker.ypos) * i)
                        if i == 0:
                            ap.remove(checker)
                            takenpiece = checker
                            if checker.name[0] == "w":
                                wp.remove(checker)
                            else:
                                bp.remove(checker)
                            tempitem = checker
                        if move_valid(piece, checker.xpos, piece.ypos, wp, bp, wking, bking, tempx,
                                      tempy) and not check_checker(wp, bp, wking, bking):
                            checkmate = False
                            piece.xpos = tempx
                            piece.ypos = tempy
                        else:
                            piece.xpos = tempx
                            piece.ypos = tempy
                        if tempitem:
                            ap.append(tempitem)
                            if tempitem.name[0] == "w":
                                wp.append(tempitem)
                            else:
                                bp.append(tempitem)
                            tempitem = None
            if checker.ypos - king.ypos == 0:
                for i in range(0, abs(wking.xpos - checker.xpos) + 1):
                    for piece in pieces:
                        tempx = piece.xpos
                        tempy = piece.ypos
                        piece.xpos = checker.xpos + (numpy.sign(king.xpos - checker.xpos) * i)
                        piece.ypos = checker.ypos
                        if i == 0:
                            ap.remove(checker)
                            takenpiece = checker
                            if checker.name[0] == "w":
                                wp.remove(checker)
                            else:
                                bp.remove(checker)
                            tempitem = checker
                        if move_valid(piece, piece.xpos, piece.ypos, wp, bp, wking, bking, tempx, tempy):
                            checkmate = False
                            piece.xpos = tempx
                            piece.ypos = tempy
                        else:
                            piece.xpos = tempx
                            piece.ypos = tempy
                        if tempitem:
                            ap.append(tempitem)
                            if tempitem.name[0] == "w":
                                wp.append(tempitem)
                            else:
                                bp.append(tempitem)
                            tempitem = None
            pass
        elif checker.name[1] == "q":
            if checker.xpos - king.xpos == 0:
                for i in range(0, abs(king.ypos - checker.ypos) + 1):
                    for piece in pieces:
                        tempx = piece.xpos
                        tempy = piece.ypos
                        piece.xpos = checker.xpos
                        piece.ypos = checker.ypos + (constant * i)
                        if i == 0:
                            ap.remove(checker)
                            takenpiece = checker
                            if checker.name[0] == "w":
                                wp.remove(checker)
                            else:
                                bp.remove(checker)
                            tempitem = checker

                        if move_valid(piece, checker.xpos, checker.ypos + (constant * i), wp, bp, wking, bking, tempx,
                                      tempy):
                            checkmate = False
                            piece.xpos = tempx
                            piece.ypos = tempy
                        else:
                            piece.xpos = tempx
                            piece.ypos = tempy
                        if tempitem:
                            ap.append(tempitem)
                            if tempitem.name[0] == "w":
                                wp.append(tempitem)
                            else:
                                bp.append(tempitem)
                            tempitem = None
            if checker.ypos - king.ypos == 0:
                for i in range(0, abs(wking.xpos - checker.xpos) + 1):
                    for piece in pieces:
                        tempx = piece.xpos
                        tempy = piece.ypos
                        piece.xpos = checker.xpos + (numpy.sign(king.xpos - checker.xpos) * i)
                        piece.ypos = checker.ypos
                        if i == 0:
                            ap.remove(checker)
                            takenpiece = checker
                            if checker.name[0] == "w":
                                wp.remove(checker)
                            else:
                                bp.remove(checker)
                            tempitem = checker
                        if move_valid(piece, piece.xpos, piece.ypos, wp, bp, wking, bking, tempx,
                                      tempy):
                            checkmate = False
                            piece.xpos = tempx
                            piece.ypos = tempy
                        else:
                            piece.xpos = tempx
                            piece.ypos = tempy
                        if tempitem:
                            ap.append(tempitem)
                            if tempitem.name[0] == "w":
                                wp.append(tempitem)
                            else:
                                bp.append(tempitem)
                            tempitem = None
            else:
                for i in range(0, abs(king.xpos - checker.xpos) + 1):
                    for piece in pieces:
                        tempx = piece.xpos
                        tempy = piece.ypos
                        piece.xpos = checker.xpos + (numpy.sign(king.xpos - checker.xpos) * i)
                        piece.ypos = checker.ypos + (numpy.sign(king.ypos - checker.ypos) * i)
                        if i == 0:
                            ap.remove(checker)
                            takenpiece = checker
                            if checker.name[0] == "w":
                                wp.remove(checker)
                            else:
                                bp.remove(checker)
                            tempitem = checker
                        if move_valid(piece, piece.xpos, piece.ypos, wp, bp, wking, bking, tempx,
                                      tempy):
                            checkmate = False
                            piece.xpos = tempx
                            piece.ypos = tempy
                        else:
                            piece.xpos = tempx
                            piece.ypos = tempy
                        if tempitem:
                            ap.append(tempitem)
                            if tempitem.name[0] == "w":
                                wp.append(tempitem)
                            else:
                                bp.append(tempitem)
                            tempitem = None
        elif checker.name[1] == "n":
            for piece in pieces:
                if piece.name[1] == "k":
                    continue
                tempx = piece.xpos
                tempy = piece.ypos
                piece.xpos = checker.xpos
                piece.ypos = checker.ypos
                ap.remove(checker)
                takenpiece = checker
                if checker.name[0] == "w":
                    wp.remove(checker)
                else:
                    bp.remove(checker)
                tempitem = checker
                if move_valid(piece, piece.xpos, piece.ypos, wp, bp, wking, bking, tempx,
                              tempy):
                    checkmate = False
                    piece.xpos = tempx
                    piece.ypos = tempy
                else:
                    piece.xpos = tempx
                    piece.ypos = tempy
                if tempitem:
                    ap.append(tempitem)
                    if tempitem.name[0] == "w":
                        wp.append(tempitem)
                    else:
                        bp.append(tempitem)
                    tempitem = None
        elif checker.name[1] == "p":
            for piece in pieces:
                tempx = piece.xpos
                tempy = piece.ypos
                piece.xpos = checker.xpos
                piece.ypos = checker.ypos
                ap.remove(checker)
                takenpiece = checker
                if checker.name[0] == "w":
                    wp.remove(checker)
                else:
                    bp.remove(checker)
                tempitem = checker
                if move_valid(piece, piece.xpos, piece.ypos, wp, bp, wking, bking, tempx,
                              tempy):
                    checkmate = False
                    piece.xpos = tempx
                    piece.ypos = tempy
                else:
                    piece.xpos = tempx
                    piece.ypos = tempy
                if tempitem:
                    ap.append(tempitem)
                    if tempitem.name[0] == "w":
                        wp.append(tempitem)
                    else:
                        bp.append(tempitem)
                    tempitem = None
        checking_pieces = None
    return checkmate


def check_checker(wp, bp, wking, bking):
    global checking_pieces
    checking_pieces = []
    if move:
        pieces = bp
        king = wking
    else:
        pieces = wp
        king = bking
    global piece

    for piece in pieces:
        if piece.name[1] == "k":
            checktake = False
        elif piece.name[1] == "q":
            checktake = queen_moves(king.xpos - piece.xpos, king.ypos - piece.ypos, piece.xpos, piece.ypos, piece)
            if checktake:
                checking_pieces.append(piece)
                return checktake
        elif piece.name[1] == "b":
            checktake = bishop_moves(king.xpos - piece.xpos, king.ypos - piece.ypos, piece.xpos, piece.ypos, piece)
            if checktake:
                checking_pieces.append(piece)
                return checktake
        elif piece.name[1] == "n":
            checktake = knight_moves(piece.xpos - king.xpos, piece.ypos - king.ypos, king.xpos, king.ypos, piece)
            if checktake:
                checking_pieces.append(piece)
                return checktake
        elif piece.name[1] == "r":
            checktake = rook_moves(piece.xpos - king.xpos, piece.ypos - king.ypos, king.xpos, king.ypos, piece)
            if checktake:
                checking_pieces.append(piece)
                return checktake
        elif piece.name[0:2] == "wp":
            checktake = white_pawn_moves(piece.xpos - king.xpos, piece.ypos - king.ypos, king.xpos, king.ypos,
                                         piece.move_num, piece, takenpiece)
            if checktake:
                checking_pieces.append(piece)
                return checktake
        elif piece.name[0:2] == "bp":
            checktake = black_pawn_moves(piece.xpos - king.xpos, piece.ypos - king.ypos, king.xpos, king.ypos,
                                         piece.move_num, piece, takenpiece)
            if checktake:
                checking_pieces.append(piece)
                return checktake
    else:
        return False


def piecethere(xsquare, ysquare, compare):
    for i in ap:
        if i.xpos == xsquare and i.ypos == ysquare and i != compare:
            return True

    return False


def piecethereexclude(xsquare, ysquare, compare):
    for i in ap:
        if i.xpos == xsquare and i.ypos == ysquare and i.name[0] != compare.name[0]:
            return True
    return False


def takenpiecechecker(takenpiece, xsquare, ysquare, compare):
    if not takenpiece:
        return False
    if takenpiece.xpos == xsquare and takenpiece.ypos == ysquare and takenpiece.name != compare.name:
        return True
    else:
        takenpiece = None
        return False


def king_moves(x, y, startx, starty, item):
    if abs(x) < 2 and abs(y) < 2 and not piecethere(startx + x, starty + y, item):
        returner = True
        for vector in king_vectors:
            if item.name[0] == "w":
                if bking.xpos == startx + x + vector[0] and bking.ypos == starty + y + vector[1]:
                    returner = False
                    break
            else:
                if wking.xpos == startx + x + vector[0] and wking.ypos == starty + y + vector[1]:
                    returner = False
                    break
    else:
        returner = False
    return returner


def queen_moves(x, y, startx, starty, queen):
    returner = True
    if x == 0 and y == 0:
        returner = False
    elif abs(x) == abs(y):
        for i in range(0, abs(x) + 1):
            if x < 0:
                vectorx = startx - i
            elif x > 0:
                vectorx = startx + i
            if y < 0:
                vectory = starty - i
            elif y > 0:
                vectory = starty + i
            if abs(x) == i and piecethereexclude(vectorx, vectory, queen):
                return True
            elif piecethere(vectorx, vectory, queen):
                returner = False
                return returner
            else:
                returner = True
    elif y == 0:
        for i in range(1, abs(x) + 1):
            if x > 0:
                vectorx = startx + i
            if x < 0:
                vectorx = startx - i
            if abs(x) == i and piecethereexclude(vectorx, starty, queen):
                return True
            elif piecethere(vectorx, starty, queen):
                returner = False
                break
            else:
                returner = True
    elif x == 0:

        for i in range(1, abs(y) + 1):
            if y > 0:
                vectory = starty + i
            if y < 1:
                vectory = starty - i
            if abs(y) == i and piecethereexclude(startx, vectory, queen):
                return True
            elif piecethere(startx, vectory, queen):
                returner = False
                break
            else:
                returner = True
    else:
        returner = False
    return returner


def bishop_moves(x, y, startx, starty, bishop):
    global returner
    if abs(x) == abs(y):
        for i in range(1, abs(x) + 1):
            if x < 0:
                vectorx = startx - i
            elif x > 0:
                vectorx = startx + i
            if y < 0:
                vectory = starty - i
            elif y > 0:
                vectory = starty + i

            if abs(x) == i and piecethereexclude(vectorx, vectory, bishop):
                return True
            elif piecethere(vectorx, vectory, bishop):
                returner = False
                return returner
            else:
                returner = True
    else:
        returner = False
    return returner


def knight_moves(x, y, startx, starty, knight):
    if (abs(x) == 1 and abs(y) == 2) or (abs(x) == 2 and abs(y) == 1):
        if piecethereexclude(startx + x, starty + y, knight) or not piecethere(startx + x, starty + y, knight):
            return True
    else:
        return False


def rook_moves(x, y, startx, starty, rook):
    if x == 0 or y == 0:
        if y == 0:
            for i in range(1, abs(x) + 1):
                if x > 0:
                    vectorx = startx + i
                if x < 0:
                    vectorx = startx - i
                if abs(x) == i and piecethereexclude(vectorx, starty, rook):
                    return True
                elif piecethere(vectorx, starty, rook):
                    returner = False
                    break
                else:
                    returner = True
        elif x == 0:

            for i in range(1, abs(y) + 1):
                if y > 0:
                    vectory = starty + i
                if y < 1:
                    vectory = starty - i
                if abs(y) == i and piecethereexclude(startx, vectory, rook):
                    return True
                elif piecethere(startx, vectory, rook):
                    returner = False
                    break
                else:
                    returner = True
    else:
        returner = False
    return returner


def white_pawn_moves(x, y, startx, starty, first, wpa, takenpiece):
    if x == 0 and y == -1 and not piecethere(startx, starty - 1, wpa):
        return True
    elif abs(x) == 1 and y == -1 and takenpiecechecker(takenpiece, startx + x, starty - 1, wpa):
        return True
    elif x == 0 and y == -2 and not piecethere(startx + x, starty - 1, wpa) and first == 0:
        return True
    else:
        return False


def black_pawn_moves(x, y, startx, starty, first, bpa, takenpiece):
    if x == 0 and y == 1 and not piecethere(startx, starty + 1, bpa):
        return True
    elif abs(x) == 1 and y == 1 and takenpiecechecker(takenpiece, startx + x, starty + 1, bpa):
        return True
    elif x == 0 and y == 2 and not piecethere(startx + x, starty + 1, bpa) and first == 0:
        return True
    else:
        return False


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


wp = []
for i in range(1, 9):
    wp.append(Piece(f"wp{i}", i, 7, "w", wpawn_image))
wking = Piece(f"wk", 5, 8, "w", wking_image)
wp.append(wking)
wp.append(Piece(f"wq", 4, 8, "w", wqueen_image))
wp.append(Piece(f"wb1", 3, 8, "w", wbishop_image))
wp.append(Piece(f"wb2", 6, 8, "w", wbishop_image))
wp.append(Piece(f"wn1", 2, 8, "w", wknight_image))
wp.append(Piece(f"wn2", 7, 8, "w", wknight_image))
wp.append(Piece(f"wr1", 1, 8, "w", wrook_image))
wp.append(Piece(f"wr2", 8, 8, "w", wrook_image))

bp = []
for i in range(1, 9):
    bp.append(Piece(f"bp{i}", i, 2, "b", bpawn_image))
bking = (Piece(f"bk", 5, 1, "w", bking_image))
bp.append(bking)
bp.append(Piece(f"bq", 4, 1, "w", bqueen_image))
bp.append(Piece(f"bb1", 3, 1, "w", bbishop_image))
bp.append(Piece(f"bb2", 6, 1, "w", bbishop_image))
bp.append(Piece(f"bn1", 2, 1, "w", bknight_image))
bp.append(Piece(f"bn2", 7, 1, "w", bknight_image))
bp.append(Piece(f"br1", 1, 1, "w", brook_image))
bp.append(Piece(f"br2", 8, 1, "w", brook_image))

ap = wp + bp
for i in ap:
    i.place()

if __name__ == "__main__":
    pygame.init()
    surface = pygame.display.set_mode((1000, 800))


def snapper(x, y):
    snapposx, snapposy = 0, 0
    for i in range(1, 9):
        if 200 + (i - 1) * 75 < x < 200 + i * 75:
            snapposx = i
            break
    for i in range(1, 9):
        if 75 + (i - 1) * 75 < y < 75 + i * 75:
            snapposy = i
            break
    return snapposx, snapposy


# menu = pygame_menu.Menu("CHESS", 1000, 600, theme=pygame_menu.themes.THEME_GREEN)
# menu.add.button("START", start_game)
# menu.mainloop(surface)
run = True
takenpiece = None

board_text(ap)

while __name__ == "__main__":
    turn = True
    clock.tick(120)
    screen.fill(white)
    if check_checker(wp, bp, wking, bking):
        if checkmate_checker(wp, bp, wking, bking, checking_pieces):
            print("CHECKMATE")
            time.sleep(1000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.blit(board_image, (200, 75))
    for i in ap:
        screen.blit(i.image, (i.placerx, i.placery))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            for j in range(1, 9):
                if 200 + (j - 1) * 75 < x < 200 + j * 75:
                    newposx = j
                    break
            for j in range(1, 9):
                if 75 + (j - 1) * 75 < y < 75 + j * 75:
                    newposy = j
                    break
            for i in ap:
                if i.xpos == newposx and i.ypos == newposy:
                    i.placerx = x
                    i.placery = y
                    item = i
        if pygame.mouse.get_pressed()[0] and item:
            x, y = pygame.mouse.get_pos()
            item.placerx = x - 75 / 2
            item.placery = y - 75 / 2
        if not pygame.mouse.get_pressed()[0]:

            try:
                x, y = pygame.mouse.get_pos()
                xsquare, ysquare = snapper(x,
                                           y)  # xsquare and ysquare are the squares the piece is trying to be placed on
                item.placerx = 125 + xsquare * 75
                item.placery = ysquare * 75
                displacex = abs(newposx - xsquare)  # displacex and displacey represent absolute vector
                displacey = abs(newposy - ysquare)
                movevalid = True
                tempx = item.xpos
                tempy = item.ypos
                item.xpos = xsquare
                item.ypos = ysquare
                for i in ap:
                    if i.xpos == xsquare and i.ypos == ysquare and i.name[0] != item.name[0]:
                        ap.remove(i)
                        takenpiece = i
                        if i.name[0] == "w":
                            wp.remove(i)
                        else:
                            bp.remove(i)
                        tempitem = i
                if item.name[0] == "w" and move:
                    turn = True
                elif item.name[0] == "b" and not move:
                    turn = True
                else:
                    turn = False

                movevalid = move_valid(item, xsquare, ysquare, wp, bp, wking, bking, newposx, newposy)

                if movevalid and turn:
                    tempitem = None
                if not movevalid or not turn:
                    item.placerx = 125 + tempx * 75
                    item.xpos = tempx
                    item.placery = tempy * 75
                    item.ypos = tempy
                    if tempitem:
                        ap.append(tempitem)
                        if tempitem.name[0] == "w":
                            wp.append(tempitem)
                        else:
                            bp.append(tempitem)
                if movevalid and turn:
                    move = not move
                    for i in ap:
                        if i.xpos == xsquare and i.ypos == ysquare and i.name[0] != item.name[0]:
                            ap.remove(i)
                            if i.name[0] == "w":
                                wp.remove(i)
                            else:
                                bp.remove(i)

            except AttributeError:
                pass
            except NameError:
                pass
            item = None

    pygame.display.update()