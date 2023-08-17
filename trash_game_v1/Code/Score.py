import pygame, pickle
from Settings import *


class Score:
    def __init__(self, Place, Score, Name, Position):
        self.Place = Place
        self.Score = Score
        self.Name = Name
        self.PositionX, self.PositionY = Position

        Font = pygame.font.Font(None, int(Scale(100)))

        self.Box = pygame.image.load("../Graphics/Score Box.png")
        self.Box = pygame.transform.scale(self.Box, (Scale(1750), Scale(175)))

        self.PlaceLabel = Font.render(str(self.Place), False, "black")
        self.PlaceRectangle = self.PlaceLabel.get_rect(center = (self.PlaceLabel.get_width() + Scale(40), self.Box.get_height() / 2))

        self.NameLabel = Font.render(self.Name, False, "black")
        self.NameRectangle = self.NameLabel.get_rect(center = (self.PlaceRectangle.midright[0] + (self.NameLabel.get_width() / 2) + Scale(100), self.Box.get_height() / 2))

        self.ScoreLabel = Font.render(str(self.Score), False, "black")
        self.ScoreRectangle = self.ScoreLabel.get_rect(center = ((self.Box.get_width() / 2) + Scale(200), self.Box.get_height() / 2))

        self.Box.blit(self.PlaceLabel, self.PlaceRectangle)
        self.Box.blit(self.NameLabel, self.NameRectangle)
        self.Box.blit(self.ScoreLabel, self.ScoreRectangle)

        self.Update()

    def Update(self):
        self.BoxRectangle = self.Box.get_rect(center = (self.PositionX, self.PositionY))