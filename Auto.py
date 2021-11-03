from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from Game2048 import Game
import pygame as pg
import sys
import random

n = int(input())

game = Game(n)
game.lock_key = True
clock = pg.time.Clock()


def BestMove():
    game.LeftMove()
    game.RightMove()
    game.UpMove()
    game.DownMove()
    max_score = game.score[0]
    max_move = 0
    game.score[0] = 0
    for i in range(1, 3):
        if max_score < game.score[i]:
            max_score = game.score[i]
            max_move = i
        game.score[i] = 0
    if max_score == 0:
        game.Move(random.randint(0, 3))
    else:
        game.Move(max_move)


while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        game.KeyProcess(event)
    game.PrintScore()
    game.PrintTile()
    BestMove()
    if game.CheckGameOver():
        f = open("2048_result.txt", "a")
        score = "Total Score: " + game.ScoreStr() + " " + str(game.TILE_COUNT) + "x" + str(game.TILE_COUNT)
        f.writelines(score + "\n")
        f.close()
        game.NewGame()
    pg.display.update()
    clock.tick(60)
