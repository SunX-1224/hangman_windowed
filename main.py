"""
TODO:
    create window
    main menu :: choice = ( single player + 2 players )
    game window ( single player / 2 players )
    char echo
    hangman graphic
    game end logic
    scoreboard
    optional (predictiing mechanism)
"""
import pygame
from random import randint

pygame.init()
RUNTIME = True

class GameWin:
    TILE_SET = pygame.image.load("assests.png")
    __bg_color = (80,80,40)
    font = pygame.font.SysFont("Corbel", 45)
    font2 = pygame.font.SysFont("Corbel", 36)
    R_DATA = {
        "ground" : (0,0,256,9),
        "pole"   : (0,0,8,256),
        "beam"   : (0,0,144,6),
        "rope"   : (34,77,12,79),
        "head"   : (20,22,45,46),
        "body"   : (84,22,38,91),
        "l_hand" : (132,33,25,48),
        "r_hand" : (162,33,27,48),
        "l_leg"  : (207,36,9,47),
        "r_leg"  : (236,36,9,47),
        "solo"   : (57,116,120,26),
        "pvp"    : (57,165,91,27),
        "title"  : (56,221,198,29),
        "exit"   : (150,165,120,32)
    }
    __size = {
        'ground': (256, 9),
        'pole': (8, 256),
        'beam': (144, 6),
        'rope': (12, 79),
        'head': (45, 46),
        'body': (38, 91),
        'l_hand': (25, 48),
        'r_hand': (25, 48),
        'l_leg': (9, 47),
        'r_leg': (9, 47),
        'solo': (120, 26),
        'pvp': (91, 27),
        'title': (198, 29),
        'exit' : (120,32)
    }
    P_DATA = {
        "ground": (130, 360),
        "pole": (130, 104),
        "beam": (130, 104),
        "rope": (210, 100),
        "head": (195, 150),
        "body": (198, 196),
        "l_hand": (173, 200),
        "r_hand": (236, 200),
        "l_leg": (198, 267),
        "r_leg": (228, 267),
        "solo": (190, 160),
        "pvp": (200, 260),
        "title": (155, 50),
        "exit" : (400,470)
    }

    __surfaces = {}
    __menu_data = ["title", "solo", "pvp", "exit"]
    __game_data = ["title", "ground", "pole", "beam", "rope", "head", "body", "l_hand", "r_hand", "l_leg", "r_leg", "exit"]
    __runtime_data = ["title", "exit", "ground"]

    _word = ""
    _guess_count = 0
    MAX_GUESSES = 9
    MAX_ROUNDS = 5
    l_word = []
    l_guessed = []

    def __init__(self):
        self.is_menu = True
        self.is_game = False
        self.solo = False
        self.pvp = False
        self.is_transit = False
        self.transit_msg = ""
        self.matchCount = 0
        self.p1score = 0
        self.p2score = 0

        self.window = pygame.display.set_mode((512,512))
        pygame.display.set_caption("HangMan")
        self.__create_surface()

    def main_menu(self):
        self.window.fill(self.__bg_color)
        for item in self.__menu_data:
            self.window.blit(self.__surfaces[item], self.P_DATA[item])
        pygame.display.update()

    def GetWord(self):
        with open("__words.txt", 'r') as file:
            line = file.readline().split()
            wrd_index = randint(0, len(line))
            return line[wrd_index]

    def transit(self):
        self.window.fill(self.__bg_color)
        self.window.blit(self.__surfaces["exit"],self.P_DATA["exit"])
        message = self.font2.render(self.transit_msg, True, (150,150,150))
        self.window.blit(message, (50,100))
        message = self.font2.render("WORD : "+self._word.upper(), True, (150,150,150))
        self.window.blit(message, (120, 140))
        if self.pvp:
            self.matchCount += 1
            if self.matchCount == 2 * self.MAX_ROUNDS:
                text = self.font2.render("END OF THE MATCH", True, (150,150,150))
                self.window.blit(text, (100,250))
                text = self.font2.render("SCORES", True, (30, 50, 50), (150,150,150))
                self.window.blit(text, (100, 300))
                text = self.font2.render("PLAYER 1 : " + str(self.p1score), True, (150,150,150))
                self.window.blit(text, (100, 350))
                text = self.font2.render("PLAYER 2 : " + str(self.p2score), True, (150, 150, 150))
                self.window.blit(text, (100, 400))

        pygame.display.update()
        pygame.time.delay(2000)
        if self.solo: self.initiate_match(False, True)
        if self.pvp:
            if self.matchCount == 2 * self.MAX_ROUNDS:
                pygame.time.delay(2000)
                self.reset_data()
            else: self.initiate_match(True, False)

    def vert_write(self, text, position):
        surf = []
        for i,char in enumerate(text):
            surf.append((self.font2.render(char, True, (200,200,200)),(position[0], position[1]+i*36)))
        self.window.blits(surf)

    def game_loop(self):
        self.window.fill(self.__bg_color)
        for item in self.__runtime_data:
            self.window.blit(self.__surfaces[item], self.P_DATA[item])
        text = self.font.render(' '.join(self.l_guessed), True, (150,150,150))
        self.window.blit(text, (150,400))

        if self.pvp:
            plr = "PLAYER1" if self.matchCount%2==0 else "PLAYER2"
            self.vert_write(plr, (20, 90))
            self.vert_write(plr, (470, 90))

        if ''.join(self.l_guessed) == self._word:
            self.transit_msg = "YAY !!! YOU GOT IT RIGHT !"
            self.is_game = False
            self.is_transit = True
            if self.pvp:
                if self.matchCount%2==0:self.p1score+=1
                else:self.p2score+=1

        if self._guess_count == self.MAX_GUESSES:
            self.transit_msg = "SORRY !! NO LUCK THIS TIME !"
            self.is_game = False
            self.is_transit = True
        pygame.display.update()

    def __create_surface(self):
        surfaces = [pygame.Surface(size) for size in self.__size.values()]
        for i,key in enumerate(self.R_DATA.keys()):
            surfaces[i].fill(self.__bg_color)
            surfaces[i].blit(self.TILE_SET, (0,0), self.R_DATA[key])

        self.__surfaces = {key : surfaces[i] for i,key in enumerate(self.R_DATA.keys())}

    def event_handler(self):
        global RUNTIME
        check_rect = lambda m, p, s:(p[1] < m[1] < p[1]+s[1])&(p[0] < m[0] < p[0]+s[0])
        for event in pygame.event.get():
            m = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                RUNTIME = False
                print("Exit")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_menu:
                    if check_rect(m,self.P_DATA["solo"], self.__size["solo"]):
                        self.initiate_match(False, True)

                    elif check_rect(m,self.P_DATA["pvp"], self.__size["pvp"]):
                        self.initiate_match(True, False)
                        self.matchCount = 0

                    elif check_rect(m,self.P_DATA["exit"], self.__size["exit"]): RUNTIME = False

                if self.is_game or self.is_transit:
                    if check_rect(m,self.P_DATA["exit"], self.__size["exit"]):
                        self.reset_data()

            if event.type == pygame.KEYDOWN and self._guess_count != self.MAX_GUESSES:
                if self.is_game:
                    inchar = event.unicode
                    flag = True
                    for i in range(len(self.l_word)):
                        if inchar == self.l_word[i]:
                            self.l_guessed[i] = inchar
                            self.l_word[i] = "N/A"
                            flag = False
                    self._guess_count += flag
                    if flag: self.__runtime_data.append(self.__game_data[1+self._guess_count])

    def reset_data(self):
        self.is_game, self.solo, self.pvp, self.is_transit = False, False, False, False
        self.is_menu = True
        self._word = ""
        self.l_word = []
        self.l_guessed = []
        self._guess_count = 0
        self.__runtime_data = ["title", "exit", "ground"]

    def initiate_match(self, pvp, solo):
        self.pvp,self.solo = pvp, solo
        self.is_game = True
        self.is_menu = False
        self.is_transit = False
        self._guess_count = 0
        self._word = self.GetWord()
        self.l_word = [self._word[i] for i in range(len(self._word))]
        self.l_guessed = ['-' for i in range(len(self._word))]
        self.__runtime_data = ["title", "exit", "ground"]

def main():
    global RUNTIME
    gameWin = GameWin()

    while RUNTIME:
        if gameWin.is_menu: gameWin.main_menu()
        if gameWin.is_game: gameWin.game_loop()
        if gameWin.is_transit: gameWin.transit()
        gameWin.event_handler()

    pygame.quit()

if __name__ == "__main__":
    main()
