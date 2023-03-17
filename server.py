import socket
import pickle
import pygame
import numpy
import copy
import time

pygame.init()
screen = pygame.display.set_mode((1, 1), pygame.NOFRAME)
clock = pygame.time.Clock()

white = (255, 255, 255)
king_vectors = [(0, 1), (1, 1), (1, 0), (-1, 1), (0, -1), (-1, -1), (-1, 0), (1, -1)]
move = True  # move being true means white to move


def move_valid(G, item, xsquare, ysquare, newposx,
               newposy,
               simulation=False):  # function to see which piece it is and run respective function (could clean this up and put functions in class)

    if newposx <= 0 or newposx >= 9:
        if (item.name[:1] == "wp" and ysquare == 8) or (item.name[:1] == "bp" and ysquare == 1) or piecethere(G,
                                                                                                              xsquare,
                                                                                                              ysquare,
                                                                                                              item):
            return False
        else:
            return True

    if ysquare <= 0 or xsquare <= 0 or ysquare >= 9 or xsquare >= 9:
        return False
    if item.name[1] == "k":
        movevalid = king_moves(G, -(newposx - xsquare), ysquare - newposy, newposx, newposy, item)
    elif item.name[1] == "q":
        movevalid = queen_moves(G, -(newposx - xsquare), ysquare - newposy, newposx, newposy, item)
    elif item.name[1] == "b":
        movevalid = bishop_moves(G, -(newposx - xsquare), ysquare - newposy, newposx, newposy, item)
    elif item.name[1] == "n":
        movevalid = knight_moves(G, -(newposx - xsquare), ysquare - newposy, newposx, newposy, item)
    elif item.name[1] == "r":
        movevalid = rook_moves(G, -(newposx - xsquare), ysquare - newposy, newposx, newposy, item)
    elif item.name[0:2] == "wp":
        movevalid = white_pawn_moves(G, -(newposx - xsquare), ysquare - newposy, newposx, newposy, item.move_num, item,
                                     takenpiece)
        if movevalid and not check_checker(G) and turn:
            item.move_num += 1
            tempitem = None
    elif item.name[0:2] == "bp":
        movevalid = black_pawn_moves(G, -(newposx - xsquare), ysquare - newposy, newposx, newposy, item.move_num, item,
                                     takenpiece)
        if movevalid and not check_checker(G) and turn:
            item.move_num += 1
            tempitem = None
    else:
        movevalid = True

    if simulation == True:
        return movevalid

    return movevalid and not check_checker(G)


def checkmate_checker(G):  # function to check if it is checkmate
    checkmate = True
    global king
    global tempitem
    tempitem = None

    if G.move:  # see whose move it is in order to determine for who we are detecting checkmate
        pieces = [piece for piece in G.wp if piece.name[1] != "k"]
        king = G.wking
        constant = 1
    else:
        pieces = [piece for piece in G.bp if piece.name[1] != "k"]
        king = G.bking
        constant = -1

    tempx, tempy = king.xpos, king.ypos

    for vector in king_vectors:  # checks if there is anywhere the king can legally move to
        blockage = False
        for piece in pieces:
            if (piece.xpos, piece.ypos) == (king.xpos + vector[0], king.ypos + vector[1]):
                blockage = True  # blockage sees if there is a piece of the same colour at the new square

        king.xpos, king.ypos = king.xpos + vector[0], king.ypos + vector[1]

        for i in G.ap:
            if i.xpos == king.xpos and i.ypos == king.ypos and i.name[1] != "k":
                G.ap.remove(i)
                takenpiece = i
                if i.name[0] == "w":
                    G.wp.remove(i)
                else:
                    G.bp.remove(i)
                tempitem = i

        if move_valid(G, king, king.xpos, king.ypos, tempx, tempy, True) and not check_checker(
                G) and king.xpos > 0 and king.ypos > 0 and not blockage:
            if tempitem:
                G.ap.append(tempitem)
                if tempitem.name[0] == "w":
                    G.wp.append(tempitem)
                else:
                    G.bp.append(tempitem)
            checkmate = False
            king.xpos = tempx
            king.ypos = tempy
            continue
        else:
            if tempitem:
                G.ap.append(tempitem)
                if tempitem.name[0] == "w":
                    G.wp.append(tempitem)
                else:
                    G.bp.append(tempitem)
        tempitem = None
        king.xpos = tempx
        king.ypos = tempy

    for checker in G.checking_pieces:
        if checker.name[1] == "b":
            #if checker is a Bishop, check if pieces can block/take it
            for i in range(0, abs(king.xpos - checker.xpos) + 1):
                for piece in pieces:
                    tempx, tempy = piece.xpos, piece.ypos
                    piece.xpos, piece.ypos = checker.xpos + (numpy.sign(king.xpos - checker.xpos) * i), checker.ypos + (
                            numpy.sign(king.ypos - checker.ypos) * i)
                    if i == 0:
                        G.ap.remove(checker)
                        takenpiece = checker
                        if checker.name[0] == "w":
                            G.wp.remove(checker)
                        else:
                            G.bp.remove(checker)
                        tempitem = checker
                    if move_valid(G, piece, piece.xpos, piece.ypos, tempx,
                                  tempy) and not check_checker(G, True):
                        checkmate = False
                        piece.xpos = tempx
                        piece.ypos = tempy
                    else:
                        piece.xpos = tempx
                        piece.ypos = tempy
                    if tempitem:
                        G.ap.append(tempitem)
                        if tempitem.name[0] == "w":
                            G.wp.append(tempitem)
                        else:
                            G.bp.append(tempitem)
                        tempitem = None
        if checker.name[1] == "r":
            # if checker is a rook, check if pieces can block/take it
            if checker.xpos - king.xpos == 0:
                for i in range(0, abs(king.ypos - checker.ypos)):
                    for piece in pieces:
                        tempx = piece.xpos
                        tempy = piece.ypos
                        piece.ypos = checker.ypos + (numpy.sign(king.ypos - checker.ypos) * i)
                        if i == 0:
                            G.ap.remove(checker)
                            takenpiece = checker
                            if checker.name[0] == "w":
                                G.wp.remove(checker)
                            else:
                                G.bp.remove(checker)
                            tempitem = checker
                        if move_valid(G, piece, checker.xpos, piece.ypos, tempx,
                                      tempy) and not check_checker(G, True):
                            checkmate = False
                            piece.xpos = tempx
                            piece.ypos = tempy
                        else:
                            piece.xpos = tempx
                            piece.ypos = tempy
                        if tempitem:
                            G.ap.append(tempitem)
                            if tempitem.name[0] == "w":
                                G.wp.append(tempitem)
                            else:
                                G.bp.append(tempitem)
                            tempitem = None
            if checker.ypos - king.ypos == 0:
                for i in range(0, abs(king.xpos - checker.xpos) + 1):
                    for piece in pieces:
                        tempx = piece.xpos
                        tempy = piece.ypos
                        piece.xpos = checker.xpos + (numpy.sign(king.xpos - checker.xpos) * i)
                        piece.ypos = checker.ypos
                        if i == 0:
                            G.ap.remove(checker)
                            takenpiece = checker
                            if checker.name[0] == "w":
                                G.wp.remove(checker)
                            else:
                                G.bp.remove(checker)
                            tempitem = checker
                        if move_valid(G, piece, piece.xpos, piece.ypos, tempx, tempy) and not check_checker(G, True):
                            checkmate = False
                            piece.xpos = tempx
                            piece.ypos = tempy
                        else:
                            piece.xpos = tempx
                            piece.ypos = tempy
                        if tempitem:
                            G.ap.append(tempitem)
                            if tempitem.name[0] == "w":
                                G.wp.append(tempitem)
                            else:
                                G.bp.append(tempitem)
                            tempitem = None
            pass
        if checker.name[1] == "q":
            # if checker is a Queen, check if pieces can block/take it
            if checker.xpos - king.xpos == 0:
                for i in range(0, abs(king.ypos - checker.ypos)):
                    for piece in pieces:
                        tempx = piece.xpos
                        tempy = piece.ypos
                        piece.xpos = checker.xpos
                        piece.ypos = checker.ypos + ((numpy.sign(king.ypos - checker.ypos) * i))
                        if i == 0:
                            G.ap.remove(checker)
                            takenpiece = checker
                            if checker.name[0] == "w":
                                G.wp.remove(checker)
                            else:
                                G.bp.remove(checker)
                            tempitem = checker

                        if move_valid(G, piece, piece.xpos, piece.ypos, tempx,
                                      tempy) and not check_checker(G, True):
                            checkmate = False
                            piece.xpos = tempx
                            piece.ypos = tempy
                        else:
                            piece.xpos = tempx
                            piece.ypos = tempy
                        if tempitem:
                            G.ap.append(tempitem)
                            if tempitem.name[0] == "w":
                                G.wp.append(tempitem)
                            else:
                                G.bp.append(tempitem)
                            tempitem = None
            if checker.ypos - king.ypos == 0:
                for i in range(0, abs(king.xpos - checker.xpos)):
                    for piece in pieces:
                        tempx = piece.xpos
                        tempy = piece.ypos
                        piece.xpos = checker.xpos + (numpy.sign(king.xpos - checker.xpos) * i)
                        piece.ypos = checker.ypos
                        if i == 0:
                            G.ap.remove(checker)
                            takenpiece = checker
                            if checker.name[0] == "w":
                                G.wp.remove(checker)
                            else:
                                G.bp.remove(checker)
                            tempitem = checker
                        if move_valid(G, piece, piece.xpos, piece.ypos, tempx,
                                      tempy, True) and not check_checker(G, True):
                            checkmate = False
                            piece.xpos = tempx
                            piece.ypos = tempy
                        else:
                            piece.xpos = tempx
                            piece.ypos = tempy
                        if tempitem:
                            G.ap.append(tempitem)
                            if tempitem.name[0] == "w":
                                G.wp.append(tempitem)
                            else:
                                G.bp.append(tempitem)
                        tempitem = None
            else:
                for i in range(0, abs(king.xpos - checker.xpos) + 1):
                    for piece in pieces:
                        tempx = piece.xpos
                        tempy = piece.ypos
                        try:
                            piece.xpos = checker.xpos + (numpy.sign(king.xpos - checker.xpos) * i)
                        except TypeError:
                            pass
                        piece.ypos = checker.ypos + (numpy.sign(king.ypos - checker.ypos) * i)
                        if i == 0:
                            try:
                                G.ap.remove(checker)
                            except ValueError:
                                pass
                            takenpiece = checker
                            if checker.name[0] == "w":
                                G.wp.remove(checker)
                            else:
                                G.bp.remove(checker)
                            tempitem = checker
                        if move_valid(G, piece, piece.xpos, piece.ypos, tempx,
                                      tempy) and not check_checker(G, True):
                            checkmate = False
                            piece.xpos = tempx
                            piece.ypos = tempy
                        else:
                            piece.xpos = tempx
                            piece.ypos = tempy
                        if tempitem:
                            G.ap.append(tempitem)
                            if tempitem.name[0] == "w":
                                G.wp.append(tempitem)
                            else:
                                G.bp.append(tempitem)
                            tempitem = None
        if checker.name[1] == "n":
            # if checker is a knight, check if pieces can take it
            for piece in pieces:
                tempx = piece.xpos
                tempy = piece.ypos
                piece.xpos = checker.xpos
                piece.ypos = checker.ypos
                G.ap.remove(checker)
                takenpiece = checker
                if checker.name[0] == "w":
                    G.wp.remove(checker)
                else:
                    G.bp.remove(checker)
                tempitem = checker
                if move_valid(G, piece, piece.xpos, piece.ypos, tempx,
                              tempy) and not check_checker(G, True):
                    checkmate = False
                    piece.xpos = tempx
                    piece.ypos = tempy
                else:
                    piece.xpos = tempx
                    piece.ypos = tempy
                if tempitem:
                    G.ap.append(tempitem)
                    if tempitem.name[0] == "w":
                        G.wp.append(tempitem)
                    else:
                        G.bp.append(tempitem)
                    tempitem = None
        elif checker.name[1] == "p":
            for piece in pieces:
                tempx = piece.xpos
                tempy = piece.ypos
                piece.xpos = checker.xpos
                piece.ypos = checker.ypos
                G.ap.remove(checker)
                takenpiece = checker
                if checker.name[0] == "w":
                    G.wp.remove(checker)
                else:
                    G.bp.remove(checker)
                tempitem = checker
                if move_valid(G, piece, piece.xpos, piece.ypos, tempx,
                              tempy) and not check_checker(G, True):
                    checkmate = False
                    piece.xpos = tempx
                    piece.ypos = tempy
                else:
                    piece.xpos = tempx
                    piece.ypos = tempy
                if tempitem:
                    G.ap.append(tempitem)
                    if tempitem.name[0] == "w":
                        G.wp.append(tempitem)
                    else:
                        G.bp.append(tempitem)
                    tempitem = None
        G.checking_pieces = []
    return checkmate


def check_checker(G, simulated_move=False):
    if simulated_move:
        white_pieces = G.move
    elif simulated_move == False:
        white_pieces = not G.move

    if white_pieces:
        pieces = G.wp
        king = G.bking
    else:
        pieces = G.bp
        king = G.wking

    #if any pieces can take the king, then they are recorded as a checking piece

    for piece in pieces:
        if piece.name[1] == "k":
            checktake = False
        elif piece.name[1] == "q":
            checktake = queen_moves(G, king.xpos - piece.xpos, king.ypos - piece.ypos, piece.xpos, piece.ypos, piece)
            if checktake:
                G.checking_pieces.append(piece)
                return checktake
        elif piece.name[1] == "b":
            checktake = bishop_moves(G, king.xpos - piece.xpos, king.ypos - piece.ypos, piece.xpos, piece.ypos, piece)
            if checktake:
                G.checking_pieces.append(piece)
                return checktake
        if piece.name[1] == "n":
            checktake = knight_moves(G, piece.xpos - king.xpos, piece.ypos - king.ypos, piece.xpos, piece.ypos, piece)
            if checktake:
                G.checking_pieces.append(piece)
                return checktake
        elif piece.name[1] == "r":
            checktake = rook_moves(G, piece.xpos - king.xpos, piece.ypos - king.ypos, piece.xpos, piece.ypos, piece)
            if checktake:
                G.checking_pieces.append(piece)
                return checktake
        if piece.name[0:2] == "wp":
            checktake = white_pawn_moves(G, king.xpos - piece.xpos, king.ypos - piece.ypos, piece.xpos, piece.ypos,
                                         piece.move_num, piece, takenpiece, True)
            if checktake:
                G.checking_pieces.append(piece)
                return checktake
        elif piece.name[0:2] == "bp":
            checktake = black_pawn_moves(G, piece.xpos - king.xpos, piece.ypos - king.ypos, piece.xpos, piece.ypos,
                                         piece.move_num, piece, takenpiece)
            if checktake:
                G.checking_pieces.append(piece)
                return checktake
    else:
        return False


def piecethere(G, xsquare, ysquare, compare):
    #function to return if a piece is on a square
    for i in G.ap:
        if i.xpos == xsquare and i.ypos == ysquare and i != compare:
            return True
    return False


def piecethereexclude(G, xsquare, ysquare, compare):
    # function to return if a piece of different color is on a square
    for i in G.ap:
        if i.xpos == xsquare and i.ypos == ysquare and i.name[0] != compare.name[0]:
            return True
    return False


def takenpiecechecker(G, takenpiece, xsquare, ysquare, compare):
    # function to check if there is a takenpiece
    if not takenpiece:
        return False
    if takenpiece.xpos == xsquare and takenpiece.ypos == ysquare and takenpiece.name != compare.name:
        return True
    else:
        takenpiece = None
        return False


def king_moves(G, x, y, startx, starty, item):
    #returns the validity of an attempted king move
    if abs(x) < 2 and abs(y) < 2 and not piecethere(G, startx + x, starty + y, item):
        returner = True
        for vector in king_vectors:
            if item.name[0] == "w":
                if G.bking.xpos == startx + x + vector[0] and G.bking.ypos == starty + y + vector[1]:
                    returner = False
                    break
            else:
                if G.wking.xpos == startx + x + vector[0] and G.wking.ypos == starty + y + vector[1]:
                    returner = False
                    break
    else:
        returner = False
    return returner


def queen_moves(G, x, y, startx, starty, queen):
    # returns the validity of an attempted queen move
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
            if abs(x) == i and piecethereexclude(G, vectorx, vectory, queen):
                return True
            elif piecethere(G, vectorx, vectory, queen):
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
            if abs(x) == i and piecethereexclude(G, vectorx, starty, queen):
                return True
            elif piecethere(G, vectorx, starty, queen):
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
            if abs(y) == i and piecethereexclude(G, startx, vectory, queen):
                return True
            elif piecethere(G, startx, vectory, queen):
                returner = False
                break
            else:
                returner = True
    else:
        returner = False
    return returner


def bishop_moves(G, x, y, startx, starty, bishop):
    # returns the validity of an attempted bishop move
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

            if abs(x) == i and piecethereexclude(G, vectorx, vectory, bishop):
                return True
            elif piecethere(G, vectorx, vectory, bishop):
                returner = False
                return returner
            else:
                returner = True
    else:
        returner = False
    return returner


def knight_moves(G, x, y, startx, starty, knight):
    # returns the validity of an attempted knight move
    if (abs(x) == 1 and abs(y) == 2) or (abs(x) == 2 and abs(y) == 1):
        if piecethereexclude(G, startx + x, starty + y, knight) or not piecethere(G, startx + x, starty + y, knight):
            return True
    else:
        return False


def rook_moves(G, x, y, startx, starty, rook):
    # returns the validity of an attempted rook move
    returner = False
    if x == 0 or y == 0:
        if y == 0:
            for i in range(1, abs(x) + 1):
                if x > 0:
                    vectorx = startx + i
                if x < 0:
                    vectorx = startx - i
                if abs(x) == i and piecethereexclude(G, vectorx, starty, rook):
                    return True
                elif piecethere(G, vectorx, starty, rook):
                    return False
                else:
                    returner = True
        elif x == 0:
            for i in range(1, abs(y) + 1):
                if y > 0:
                    vectory = starty + i
                if y < 1:
                    vectory = starty - i
                if abs(y) == i and piecethereexclude(G, startx, vectory, rook):
                    return True
                elif piecethere(G, startx, vectory, rook):
                    return False
                    break
                else:
                    returner = True
    else:
        returner = False

    if returner == True:
        print(x, y, startx, starty)
    return returner


def white_pawn_moves(G, x, y, startx, starty, first, wpa, takenpiece, simulated_move=False):
    # returns the validity of an attempted white pawn move
    if x == 0 and y == -1 and not piecethere(G, startx, starty - 1, wpa):
        return True
    elif abs(x) == 1 and y == -1 and (takenpiecechecker(G, takenpiece, startx + x, starty - 1, wpa) or simulated_move):
        return True
    elif x == 0 and y == -2 and not piecethere(G, startx + x, starty - 2, wpa) and first == 0:
        return True
    else:
        return False


def black_pawn_moves(G, x, y, startx, starty, first, bpa, takenpiece):
    # returns the validity of an attempted black pawn move
    if x == 0 and y == 1 and not piecethere(G, startx, starty + 1, bpa):
        return True
    elif abs(x) == 1 and y == 1 and takenpiecechecker(G, takenpiece, startx + x, starty + 1, bpa):
        return True
    elif x == 0 and y == 2 and not piecethere(G, startx + x, starty + 2, bpa) and first == 0:
        return True
    else:
        return False


def process_request(request, gamenum):
    #function to process requests
    for i in gamenum.ap:
        if i.name == request[0]:
            item = i
            xsquare = request[1]
            ysquare = request[2]
            newposx = item.xpos
            newposy = item.ypos
            break

    global takenpiece
    global turn
    global tempitem
    takenpiece = None
    tempitem = None
    captured = False

    tempx = item.xpos
    tempy = item.ypos
    item.xpos = xsquare
    item.ypos = ysquare
    for i in gamenum.ap:
        #simulates a piece capture
        if i.xpos == xsquare and i.ypos == ysquare and i.name[0] != item.name[0]:
            captured = True
            gamenum.ap.remove(i)
            print(f" removed {i.name}")
            takenpiece = i
            if i.name[0] == "w":
                gamenum.wp.remove(i)
            else:
                gamenum.bp.remove(i)
            tempitem = i

    if item.name[0] == "w" and gamenum.move:
        turn = True
    elif item.name[0] == "b" and not gamenum.move:
        turn = True
    else:
        turn = False

    movevalid = move_valid(gamenum, item, xsquare, ysquare, newposx, newposy)
    #if a piece from the side of the board captures a piece, it is not valid
    if (newposx <= 0 or newposx >= 9) and captured:
        movevalid = False

    if not movevalid or not turn:
        #if the move isn't valid, return it to original state
        item.placerx = 125 + tempx * 75
        item.xpos = tempx
        item.placery = tempy * 75
        item.ypos = tempy
        if tempitem:
            gamenum.ap.append(tempitem)
            if tempitem.name[0] == "w":
                gamenum.wp.append(tempitem)
            else:
                gamenum.bp.append(tempitem)
        return False, None
    if movevalid and turn:
        #if move is valid, change whose move it is
        gamenum.move = not gamenum.move
        if check_checker(gamenum):
            #check for checkmate
            if checkmate_checker(gamenum):
                return "checkmate", None
        try:
            return True, tempitem.name
        except AttributeError:
            return True, None


class Game:
    def __init__(self, wp, bp, move, wking, bking, checking_pieces=[]):
        self.wp = wp
        self.bp = bp
        self.ap = wp + bp
        self.move = move
        self.wking = wking
        self.bking = bking
        self.checking_pieces = checking_pieces


class Piece:
    def __init__(self, name, xpos, ypos, colour, move_num=0):
        self.xpos = xpos
        self.ypos = ypos
        self.colour = colour
        self.name = name
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

    def update(self, x, y):
        self.xpos = x
        self.ypos = y
        self.placerx = 125 + self.xpos * 75
        self.placery = self.ypos * 75


wp = []
for i in range(1, 9):
    wp.append(Piece(f"wp{i}", i, 7, "w"))
wking = Piece(f"wk", 5, 8, "w")
wp.append(wking)
wp.append(Piece(f"wq", 4, 8, "w"))
wp.append(Piece(f"wb1", 3, 8, "w"))
wp.append(Piece(f"wb2", 6, 8, "w"))
wp.append(Piece(f"wn1", 2, 8, "w"))
wp.append(Piece(f"wn2", 7, 8, "w"))
wp.append(Piece(f"wr1", 1, 8, "w"))
wp.append(Piece(f"wr2", 8, 8, "w"))

board = [[" " for i in range(8)] for i in range(8)]
print("".join([f"\n{i}" for i in board]))

bp = []
for i in range(1, 9):
    bp.append(Piece(f"bp{i}", i, 2, "b"))
bking = (Piece(f"bk", 5, 1, "w"))
bp.append(bking)
bp.append(Piece(f"bq", 4, 1, "w"))
bp.append(Piece(f"bb1", 3, 1, "w"))
bp.append(Piece(f"bb2", 6, 1, "w"))
bp.append(Piece(f"bn1", 2, 1, "w"))
bp.append(Piece(f"bn2", 7, 1, "w"))
bp.append(Piece(f"br1", 1, 1, "w"))
bp.append(Piece(f"br2", 8, 1, "w"))

G1 = Game(wp, bp, True, wking, bking)
G2 = copy.deepcopy(G1)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket object
server_socket.bind(('localhost', 8000))  # binds socket to local port
server_socket.listen(4)  # listening for connections

print('Listening for connections...')

for client in range(4):  # accept four clients
    client_socket, client_address = server_socket.accept()
    client_name = client_socket.recv(1024).decode()
    exec(client_name + " =  client_socket")
    print(f"Connected to {client_name}")  # associate with the name sent

while True:
    for client in (
    client1, client2):  # alternates between requests from client1 and client2 as it can't deal with both simultaneously
        client.settimeout(0.00001)
        try:
            data = client.recv(1024)
        except socket.timeout:
            continue
        if not data:
            break
        request = pickle.loads(data)
        print(request)
        result, taken = process_request(request, G1)
        if result == "checkmate":
            # send the clients the relevant checkmate information
            info = pickle.dumps(
                f"checkmate, The {'white' if request[0][0] == 'w' else 'black'} player has delivered checkmate on Board 1")
            for player in client1, client2, client3, client4:
                player.sendall(info)
        else:
            client.sendall(pickle.dumps(result))

        if result and result != "checkmate":  # if a move is valid it send to the other client so their board can update
            if client == client1:
                while True:
                    try:
                        if taken:
                            print("NEWPIECE1")
                            newpiece = pickle.dumps(taken + "new")
                            client3.sendall(newpiece)
                            client4.sendall(newpiece)
                            newpiece = Piece(taken + "new", 0, 8, taken[0])
                            G2.ap.append(newpiece)
                            getattr(G2, newpiece.colour + "p").append(newpiece)
                        client2.sendall(data)  # keep trying to send until recieved
                        break
                    except OSError:
                        pass
            else:
                while True:
                    try:
                        if taken:
                            newpiece = pickle.dumps(taken + "new")
                            client3.sendall(newpiece)
                            client4.sendall(newpiece)
                            newpiece = Piece(taken + "new", 0, 8, taken[0])
                            G2.ap.append(newpiece)
                            getattr(G2, newpiece.colour + "p").append(newpiece)
                        client1.sendall(data)
                        break
                    except OSError:
                        pass

    for client in (
    client3, client4):  # alternates between requests from client1 and client2 as it can't deal with both simultaneously
        client.settimeout(0.00001)
        try:
            data = client.recv(1024)
        except socket.timeout:
            continue
        if not data:
            break
        request = pickle.loads(data)
        result, taken = process_request(request, G2)

        if result == "checkmate":
            info = pickle.dumps(
                f"checkmate, The {'white' if request[0][0] == 'w' else 'black'} player has delivered checkmate on Board 1")
            for player in client1, client2, client3, client4:
                player.sendall(info)
        else:
            client.sendall(pickle.dumps(result))
        if result:  # if a move is valid it send to the other client so their board can update
            if client == client3:
                while True:
                    try:
                        if taken:
                            print("NEWPIECE2")
                            newpiece = pickle.dumps(taken + "new")
                            client1.sendall(newpiece)
                            client2.sendall(newpiece)
                            newpiece = Piece(taken + "new", 0, 8, taken[0])
                            G1.ap.append(newpiece)
                            getattr(G1, newpiece.colour + "p").append(newpiece)
                        client4.sendall(data)  # keep trying to send until recieved
                        break
                    except OSError:
                        pass
            else:
                while True:
                    try:
                        if taken:
                            newpiece = pickle.dumps(taken + "new")
                            client1.sendall(newpiece)
                            client2.sendall(newpiece)
                            newpiece = Piece(taken + "new", 0, 8, taken[0])
                            G1.ap.append(newpiece)
                            getattr(G1, newpiece.colour + "p").append(newpiece)
                        client3.sendall(data)
                        break
                    except OSError:
                        pass

client1.close()
client2.close()
server_socket.close()