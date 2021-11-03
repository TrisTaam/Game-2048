from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import random
import sys
import numpy as np
import pygame as pg


class Game:
    def __init__(self, tile_count):
        pg.init()
        pg.display.set_caption('2048')
        self.TILE_SIZE = 50
        self.TILE_BORDER_SIZE = 5
        self.TILE_COUNT = tile_count
        self.TOTAL_SCORE_HEIGHT = 35
        self.GAME_WIDTH = self.TILE_SIZE * self.TILE_COUNT + self.TILE_BORDER_SIZE * (self.TILE_COUNT - 1)
        self.GAME_HEIGHT = self.GAME_WIDTH + self.TOTAL_SCORE_HEIGHT
        self.GAME_SIZE = (self.GAME_WIDTH,
                          self.GAME_HEIGHT)
        self.main_tile = np.array([[0] * self.TILE_COUNT] * self.TILE_COUNT)
        self.score = [0] * 4
        self.BG_COLOR = (187, 173, 160)
        self.font1 = pg.font.SysFont("arial", 20)
        self.font2 = pg.font.SysFont("arial", 15)
        self.screen = pg.display.set_mode(self.GAME_SIZE)
        self.total_score = 0
        self.lock_key = False
        self.NewGame()

    @staticmethod
    def GetColor(value):
        x = {
            0: (205, 193, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46)
        }
        return x.get(value, (45, 131, 179))

    def LeftMove(self):
        res = self.main_tile.copy()
        for i in range(self.TILE_COUNT):
            temp = []
            kt = True
            for j in range(self.TILE_COUNT):
                if res[i, j] != 0:
                    if len(temp) == 0:
                        temp.append(res[i, j])
                    elif res[i, j] == temp[len(temp) - 1] and kt:
                        temp[len(temp) - 1] *= 2
                        self.score[0] += temp[len(temp) - 1]
                        kt = False
                    else:
                        temp.append(res[i, j])
                        kt = True

            while len(temp) < self.TILE_COUNT:
                temp.append(0)
            res[i] = temp.copy()
        return res

    def RightMove(self):
        res = self.main_tile.copy()
        for i in range(self.TILE_COUNT):
            temp = []
            kt = True
            for j in reversed(range(self.TILE_COUNT)):
                if res[i, j] != 0:
                    if len(temp) == 0:
                        temp.append(res[i, j])
                    elif res[i, j] == temp[len(temp) - 1] and kt:
                        temp[len(temp) - 1] *= 2
                        self.score[1] += temp[len(temp) - 1]
                        kt = False
                    else:
                        temp.append(res[i, j])
                        kt = True
            temp = temp[::-1]
            while len(temp) < self.TILE_COUNT:
                temp.insert(0, 0)
            res[i] = temp.copy()
        return res

    def UpMove(self):
        res = self.main_tile.copy()
        for i in range(self.TILE_COUNT):
            temp = []
            kt = True
            for j in range(self.TILE_COUNT):
                if res[j, i] != 0:
                    if len(temp) == 0:
                        temp.append(res[j, i])
                    elif res[j, i] == temp[len(temp) - 1] and kt:
                        temp[len(temp) - 1] *= 2
                        self.score[2] += temp[len(temp) - 1]
                        kt = False
                    else:
                        temp.append(res[j, i])
                        kt = True
            while len(temp) < self.TILE_COUNT:
                temp.append(0)
            res[:, i] = temp.copy()
        return res

    def DownMove(self):
        res = self.main_tile.copy()
        for i in range(self.TILE_COUNT):
            temp = []
            kt = True
            for j in reversed(range(self.TILE_COUNT)):
                if res[j, i] != 0:
                    if len(temp) == 0:
                        temp.append(res[j, i])
                    elif res[j, i] == temp[len(temp) - 1] and kt:
                        temp[len(temp) - 1] *= 2
                        self.score[3] += temp[len(temp) - 1]
                        kt = False
                    else:
                        temp.append(res[j, i])
                        kt = True
            temp = temp[::-1]
            while len(temp) < self.TILE_COUNT:
                temp.insert(0, 0)
            res[:, i] = temp.copy()
        return res

    def RandomTile(self):
        x = random.randint(0, self.TILE_COUNT - 1)
        y = random.randint(0, self.TILE_COUNT - 1)
        while self.main_tile[x, y] != 0:
            x = random.randint(0, self.TILE_COUNT - 1)
            y = random.randint(0, self.TILE_COUNT - 1)
        a = random.randint(0, 9)
        if a == 9:
            self.main_tile[x, y] = 4
        else:
            self.main_tile[x, y] = 2

    def Play(self):
        clock = pg.time.Clock()
        while 1:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                self.KeyProcess(event)
            self.PrintScore()
            self.PrintTile()
            pg.display.update()
            clock.tick(60)

    def PrintTile(self):
        x = 0
        y = self.TOTAL_SCORE_HEIGHT
        for i in range(self.TILE_COUNT):
            for j in range(self.TILE_COUNT):
                pg.draw.rect(self.screen,
                             self.GetColor(self.main_tile[i, j]),
                             (x, y, self.TILE_SIZE, self.TILE_SIZE))
                if self.main_tile[i, j] != 0:
                    text = self.font2.render(str(self.main_tile[i, j]), 1, (0, 0, 0))
                    text_size = self.font2.size(str(self.main_tile[i, j]))
                    self.screen.blit(text,
                                     (x + int((self.TILE_SIZE - text_size[0]) / 2),
                                      y + int((self.TILE_SIZE - text_size[1]) / 2)))
                x += (self.TILE_SIZE + self.TILE_BORDER_SIZE)
            x = 0
            y += (self.TILE_SIZE + self.TILE_BORDER_SIZE)

    def PrintScore(self):
        self.screen.fill(self.BG_COLOR)
        header = self.ScoreStr()
        if self.CheckGameOver():
            header += " Game Over!"
        text = self.font1.render(header, 1, (0, 0, 0))
        text_size = self.font1.size(header)
        self.screen.blit(text,
                         (0,
                          int((self.TOTAL_SCORE_HEIGHT - text_size[1]) / 2)))

    def KeyProcess(self, event):
        if not self.lock_key:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.Move(0)
                elif event.key == pg.K_RIGHT:
                    self.Move(1)
                elif event.key == pg.K_UP:
                    self.Move(2)
                elif event.key == pg.K_DOWN:
                    self.Move(3)
            if event.type == pg.KEYUP:
                if event.key == pg.K_n:
                    self.NewGame()

    def NewGame(self):
        self.total_score = 0
        self.score = [0] * 4
        self.main_tile = np.array([[0] * self.TILE_COUNT] * self.TILE_COUNT)
        x1 = random.randint(0, self.TILE_COUNT - 1)
        y1 = random.randint(0, self.TILE_COUNT - 1)
        self.main_tile[x1, y1] = 2
        x2 = random.randint(0, self.TILE_COUNT - 1)
        y2 = random.randint(0, self.TILE_COUNT - 1)
        while x1 == x2 and y1 == y2:
            x2 = random.randint(0, self.TILE_COUNT - 1)
            y2 = random.randint(0, self.TILE_COUNT - 1)
        self.main_tile[x2, y2] = 2

    def CheckGameOver(self):
        for i in range(self.TILE_COUNT):
            for j in range(self.TILE_COUNT):
                if self.main_tile[i, j] == 0:
                    return False
        global score
        if (self.main_tile != self.LeftMove()).any():
            return False
        if (self.main_tile != self.RightMove()).any():
            return False
        if (self.main_tile != self.UpMove()).any():
            return False
        if (self.main_tile != self.DownMove()).any():
            return False
        return True

    def Move(self, value):
        if value == 0:
            self.score[0] = 0
            temp = self.LeftMove().copy()
            if (self.main_tile != temp).any():
                self.main_tile = temp.copy()
                self.RandomTile()
                self.total_score += self.score[0]
        elif value == 1:
            self.score[1] = 0
            temp = self.RightMove()
            if (self.main_tile != temp).any():
                self.main_tile = temp.copy()
                self.RandomTile()
                self.total_score += self.score[1]
        elif value == 2:
            self.score[2] = 0
            temp = self.UpMove()
            if (self.main_tile != temp).any():
                self.main_tile = temp.copy()
                self.RandomTile()
                self.total_score += self.score[2]
        elif value == 3:
            self.score[3] = 0
            temp = self.DownMove()
            if (self.main_tile != temp).any():
                self.main_tile = temp.copy()
                self.RandomTile()
                self.total_score += self.score[3]

    def ScoreStr(self):
        s1 = str(self.total_score)
        s2 = ""
        d = 0
        for i in reversed(s1):
            d += 1
            s2 = i + s2
            if d % 3 == 0:
                s2 = "." + s2
        if s2[0] == ".":
            s2 = s2.replace(".", "", 1)
        return s2


def main():
    n = int(input())
    game = Game(n)
    game.Play()


if __name__ == '__main__':
    main()
