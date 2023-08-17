import pygame, random, os
from Settings import *

AllTrash = {}

for CurrentPath in os.walk("../Trash"):
    if "\\" in CurrentPath[0]:
        if CurrentPath[0][CurrentPath[0].find("\\") + 1:] not in AllTrash:
            AllTrash[CurrentPath[0][CurrentPath[0].find("\\") + 1:]] = []

        for CurrentFile in CurrentPath[2]:
            if CurrentFile[CurrentFile.rfind("."):] == ".png":
                AllTrash[CurrentPath[0][CurrentPath[0].find("\\") + 1:]].append(CurrentFile)


class Trash:
    def __init__(self):
        self.PositionX = Scale(-100)
        self.PositionY = Height - Scale(175)

        self.Type = random.choice(list(AllTrash))

        self.Gravity = 0
        self.Disabled = False
        self.Hidden = False
        self.GoToPosition = None

        while len(AllTrash[self.Type]) == 0:
            self.Type = random.choice(list(AllTrash))

        self.Trash = random.choice(AllTrash[self.Type])

        self.Surface = pygame.image.load(f"../Trash\{self.Type}\{self.Trash}").convert_alpha()
        self.Surface = Scale(self.Surface)

        self.OriginalSurface = self.Surface
        self.Rotation = 0
        self.RotationSpeed = -7

        self.StopPoint = random.randint(int(Scale(20)), int(Scale(420)))
        self.Stop = False

    def Update(self):
        if not self.Stop and self.GoToPosition == None:
            self.PositionX += self.Speed

        if self.GoToPosition != None:
            self.Rotation += self.RotationSpeed

            self.PositionX += (self.GoToPosition[0] - self.PositionX) / 10
            self.PositionY += (self.GoToPosition[1] - self.PositionY) / 10

            if abs(self.PositionX - self.GoToPosition[0]) < 30:
                self.Hidden = True

        self.Surface = pygame.transform.rotate(self.OriginalSurface, self.Rotation)
        self.Rectangle = self.Surface.get_rect(midbottom=(self.PositionX, self.PositionY))