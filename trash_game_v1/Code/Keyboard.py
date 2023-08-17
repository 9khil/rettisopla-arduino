import pygame
from Settings import *

KeySize = Scale(100)
KeySpace = (KeySize / Scale(150)) * 20


class Key:
    def __init__(self, Key, Position, Screen):
        self.Key = Key
        self.Position = Position
        self.Screen = Screen

        self.Size = (KeySize, KeySize)
        self.Color = "#555555"

        Font = pygame.font.Font(None, int(Scale(150) * (KeySize / Scale(150))))

        self.Surface = pygame.draw.rect(Screen, self.Color, pygame.rect.Rect(*self.Position, *self.Size), border_radius = int(self.Size[0] / Scale(10)))

        if self.Key == "Backspace":
            self.Label = pygame.image.load("../Keyboard/Backspace.png").convert_alpha()
            self.Label = pygame.transform.scale(self.Label, (Scale(self.Label.get_width() / 10), Scale(self.Label.get_height() / 10)))

        elif self.Key == "Enter":
            self.Label = pygame.image.load("../Keyboard/Enter.png").convert_alpha()
            self.Label = pygame.transform.scale(self.Label, (Scale(self.Label.get_width() / 10), Scale(self.Label.get_height() / 10)))

        else:
            self.Label = Font.render(self.Key, False, "white")

        self.LabelRectangle = self.Label.get_rect(center = (Position[0] + (self.Surface.width / 2), Position[1] + (self.Surface.height / 2)))

        self.Update()

    def Update(self):
        self.Surface = pygame.draw.rect(self.Screen, self.Color, pygame.rect.Rect(*self.Position, *self.Size), border_radius = int(self.Size[0] / Scale(10)))

        self.Screen.blit(self.Label, self.LabelRectangle)


class Keyboard:
    def __init__(self, Screen):
        self.Screen = Screen

        self.Layout = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "Å"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ø", "Æ"],
            ["Z", "X", "C", "V", "B", "N", "M", "Backspace", "Enter", "", ""]
        ]

        self.Keys = []

        for RowIndex, Row in enumerate(self.Layout):
            for ColumnIndex, Column in enumerate(Row):
                self.Keys.append(Key(Column, (((Height - ((KeySize + KeySpace) * (len(self.Layout) - .5))) / 2) + (ColumnIndex * (KeySize + KeySpace)), (Height - ((KeySize + KeySpace) * len(self.Layout))) + (RowIndex * (KeySize + KeySpace))), self.Screen))

        self.SelectedKeyIndex = 0

    def GetInput(self, Key, Variable):
        NewVariable = Variable

        if Key == pygame.K_q:
            if self.SelectedKeyIndex % len(self.Layout[0]) == 0:
                self.SelectedKeyIndex += len(self.Layout[0]) - 1

            else:
                self.SelectedKeyIndex -= 1

        elif Key == pygame.K_w:
            if ((self.SelectedKeyIndex + 1) % len(self.Layout[0])) == 0 and self.SelectedKeyIndex != 0:
                self.SelectedKeyIndex -= len(self.Layout[0]) - 1

            else:
                self.SelectedKeyIndex += 1

        elif Key == pygame.K_e:
            if self.SelectedKeyIndex + len(self.Layout[0]) > len(self.Keys) - 1:
                self.SelectedKeyIndex -= (len(self.Layout) - 1) * len(self.Layout[0])

            else:
                self.SelectedKeyIndex += len(self.Layout[0])

        elif Key == pygame.K_r:
            if self.SelectedKeyIndex + len(self.Layout[0]) < 0:
                self.SelectedKeyIndex += (len(self.Layout) - 1) * len(self.Layout[0])

            else:
                self.SelectedKeyIndex -= len(self.Layout[0])

        elif Key == pygame.K_t:
            if self.Keys[self.SelectedKeyIndex].Key == "Backspace":
                NewVariable = NewVariable[:-1]

            elif self.Keys[self.SelectedKeyIndex].Key == "Enter":
                return True

            else:
                NewVariable += self.Keys[self.SelectedKeyIndex].Key

        return NewVariable

    def Update(self):
        for Key in self.Keys:
            if Key == self.Keys[self.SelectedKeyIndex]:
                Key.Color = "#333333"

            else:
                Key.Color = "#555555"

            Key.Update()