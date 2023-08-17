import time, pygame
from Settings import *


class Animation:
    def __init__(self, Frames, FPS = 60):
        self.Frames = Frames
        self.FPS = FPS

        self.FrameIndex = 0

        self.StartTime = time.time()

        self.Update()

    def Update(self):
        if time.time() - self.StartTime >= 1 / self.FPS:
            if self.FrameIndex != len(self.Frames) - 1:
                self.FrameIndex += 1

            else:
                self.FrameIndex = 0

        self.Image = pygame.image.load(self.Frames[self.FrameIndex]).convert_alpha()
        self.Image = Scale(self.Image)