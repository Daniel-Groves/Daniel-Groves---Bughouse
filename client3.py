# client3.py
import pygame
import socket
import pickle

pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption('CLIENT 3')
clock = pygame.time.Clock()

checkmate = False
font = pygame.font.Font('freesansbold.ttf', 16)
black = (0,0,0)
image_constant = (75, 75)
white = (255, 255, 255)
king_vectors = [(0, 1), (1, 1), (1, 0), (-1, 1), (0, -1), (-1, -1), (-1, 0), (1, -1)]
move = True  # move being true means white to move
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

number2 = pygame.image.load(r"Images\2.png")
number3 = pygame.image.load(r"Images\3.png")
number4 = pygame.image.load(r"Images\4.png")
number5 = pygame.image.load(r"Images\5.png")
number6 = pygame.image.load(r"Images\6.png")
number7 = pygame.image.load(r"Images\7.png")
number8 = pygame.image.load(r"Images\8.png")


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

class Game:
    def __init__(self,wp,bp, move, wking, bking, checking_pieces=[]):
        self.wp = wp
        self.bp = bp
        self.ap = wp + bp
        self.move = move
        self.wking = wking
        self.bking = bking
        self.checking_pieces = checking_pieces

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

    def update(self,x,y):
        self.xpos = x
        self.ypos = y
        self.placerx = 125 + self.xpos * 75
        self.placery = self.ypos * 75

    def add_image(self):
        if self.name[1] == "p":
            self.image = wpawn_image
        elif self.name[1] == "q":
            self.image = wqueen_image
        elif self.name[1] == "r":
            self.image = wrook_image
        elif self.name[1] == "n":
            self.image = wknight_image
        elif self.name[1] == "b":
            self.image = wbishop_image

    def update_image(self):
        images = {
            "wp": wpawn_image,
            "wq": wqueen_image,
            "wr": wrook_image,
            "wb": wbishop_image,
            "wn": wknight_image,
            "wk": wking_image,
            "bp": bpawn_image,
            "bq": bqueen_image,
            "br": brook_image,
            "bb": bbishop_image,
            "bn": bknight_image,
            "bk": bking_image
        }
        self.image = images.get(self.name[:2],self.image)

    def update_position(self):
        #method to update position to square off the side of the board
        positions = {
            "wp": (0,8),
            "wq": (0,4),
            "wr": (0,5),
            "wb": (0,6),
            "wn": (0,7),
            "bp": (9,1),
            "bq": (9,5),
            "br": (9,4),
            "bb": (9,3),
            "bn": (9,2)
        }
        self.xpos, self.ypos = positions.get(self.name[:2])[0],positions.get(self.name[:2])[1]
        self.placerx = 125 + self.xpos * 75
        self.placery = self.ypos * 75
        print("updated")

class Bubble:
    def __init__(self,xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.counter = 0
        self.image = None

    def add(self,numb=1):
        self.counter += numb

    def update_image(self):
        #method to update bubble image
        images = {
            "0": None,
            "1": None,
            "2": number2,
            "3": number3,
            "4": number4,
            "5": number5,
            "6": number6,
            "7": number7,
            "8": number8,
        }
        self.image = images.get(str(self.counter))

#creation of original set-up
wp = []
for i in range(1, 9):
    wp.append(Piece(f"wp{i}", i, 7, "w",wpawn_image))
wking = Piece(f"wk", 5, 8, "w", wking_image)
wp.append(wking)
wp.append(Piece(f"wq", 4, 8, "w", wqueen_image))
wp.append(Piece(f"wb1", 3, 8, "w", wbishop_image))
wp.append(Piece(f"wb2", 6, 8, "w", wbishop_image))
wp.append(Piece(f"wn1", 2, 8, "w", wknight_image))
wp.append(Piece(f"wn2", 7, 8, "w", wknight_image))
wp.append(Piece(f"wr1", 1, 8, "w", wrook_image))
wp.append(Piece(f"wr2", 8, 8, "w", wrook_image))

board = [[" " for i in range(8)] for i in range(8)]
print("".join([f"\n{i}" for i in board]))

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


#creation of bubbles
bubbles = []
for i in range(8,3,-1):
    bubbles.append(Bubble(0,i))

for i in range(1,6):
    bubbles.append(Bubble(9,i))

G = Game(wp, bp, True, wking, bking)

clock.tick(120)
screen.fill(white)
# print(check_checker(wp, bp, wking, bking))



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8000))

client_socket.send("client3".encode())

while True:
    newposx, newposy = None, None
    clock.tick(120)
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.blit(board_image, (200, 75))
    for i in G.ap:
        #detects for an attempt at picking up/moving a piece
        screen.blit(i.image, (i.placerx, i.placery))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            for j in range(0, 10):
                if 200 + (j - 1) * 75 < x < 200 + j * 75:
                    newposx = j
                    break
            for j in range(0, 10):
                if 75 + (j - 1) * 75 < y < 75 + j * 75:
                    newposy = j
                    break
            for i in G.ap:
                if i.xpos == newposx and i.ypos == newposy:
                    i.placerx = x
                    i.placery = y
                    item = i
                    break
        if pygame.mouse.get_pressed()[0] and item:
            x, y = pygame.mouse.get_pos()
            item.placerx = x - 75 / 2
            item.placery = y - 75 / 2
        if not pygame.mouse.get_pressed()[0]:
            #deals with a piece being placed
            try:
                x, y = pygame.mouse.get_pos()
                xsquare, ysquare = snapper(x,
                                           y)  # xsquare and ysquare are the squares the piece is trying to be placed on
                item.placerx = 125 + xsquare * 75
                item.placery = ysquare * 75
                movevalid = True
                tempx = item.xpos
                tempy = item.ypos
                item.xpos = xsquare
                item.ypos = ysquare
                for i in G.ap:
                    #removes captured piece
                    if i.xpos == xsquare and i.ypos == ysquare and i.name[0] != item.name[0]:
                        G.ap.remove(i)
                        takenpiece = i
                        if i.name[0] == "w":
                            G.wp.remove(i)
                        else:
                            G.bp.remove(i)
                        tempitem = i

                if G.move == True:
                    # send the data to the server and recieves a result of the validity
                    data = pickle.dumps([item.name, xsquare, ysquare])
                    while True:
                        try:
                            client_socket.sendall(data)
                            break
                        except OSError:
                            pass
                    client_socket.settimeout(100000)
                    result = pickle.loads(client_socket.recv(1024))
                else:
                    result = False
                print(result)
                if type(result) != bool and type(result) != list and result.split(",")[0] == "checkmate":
                    #deals with the result being checkmate
                    screen.blit(font.render(f"{result.split(',')[1]}", True, black), (285,20))
                    checkmate = True
                elif result:
                    tempitem = None
                    if item.name[-1] == "w":
                        #if a new piece is placed, change the number on the relevant bubble
                        for bubble in bubbles:
                            if bubble.xpos == tempx and bubble.ypos == tempy:
                                bubble.add(-1)
                if not result:
                    #if the move isn't valid, revert to original state
                    item.placerx = 125 + tempx * 75
                    item.xpos = tempx
                    item.placery = tempy * 75
                    item.ypos = tempy
                    if tempitem:
                        G.ap.append(tempitem)
                        if tempitem.name[0] == "w":
                            G.wp.append(tempitem)
                        else:
                            G.bp.append(tempitem)
                if result:
                    #if valid, update whose move it is
                    G.move = not G.move
            except AttributeError:
                pass
            except NameError:
                pass
            item = None

            client_socket.settimeout(0.0000001)  # Set a short timeout
            try:
                #attempt to receive new moves or pieces or checkmate from the other board
                result = pickle.loads(client_socket.recv(1024))
                if type(result) != bool and type(result) != list and result.split(",")[0] == "checkmate":
                    screen.blit(font.render(f"{result.split(',')[1]}", True, black), (285, 20))
                    checkmate = True
                elif type(result) == str:
                    #if a new piece is created, update it correctly as well as updating relevant bubble
                    newpiece = Piece(result, 0, 8, result[0])
                    newpiece.update_image()
                    newpiece.update_position()
                    G.ap.append(newpiece)
                    for bubble in bubbles:
                        if bubble.xpos == newpiece.xpos and bubble.ypos == newpiece.ypos:
                            bubble.add(1)
                    getattr(G,newpiece.colour + "p").append(newpiece)
                else:
                    #if a move is made by the opponent, make the relevant changes to the clients game
                    G.move = not G.move
                    for i in G.ap:
                        if i.xpos == result[1] and i.ypos == result[2]:
                            G.ap.remove(i)
                            if i.name[0] == "w":
                                G.wp.remove(i)
                            else:
                                G.bp.remove(i)
                        if i.name == result[0]:
                            if i.name[-1] == "w":
                                if i.xpos == 0 or i.xpos == 9:
                                    for bubble in bubbles:
                                        if bubble.xpos == i.xpos and bubble.ypos == i.ypos:
                                            bubble.add(-1)
                            i.xpos, i.ypos = result[1],result[2]
                            i.placerx = 125 + result[1] * 75
                            i.placery = result[2] * 75
            except socket.timeout:
                # No result was received within the timeout
                continue
    for bubble in bubbles:
        #display all the bubbles
        bubble.update_image()
        if bubble.image:
            screen.blit(bubble.image, (125 + bubble.xpos * 75, bubble.ypos * 75 + 50))
        else:
            pass



    pygame.display.update()
    if checkmate:
        #end the game loop if checkmate is reached
        while True:
            clock.tick(120)
