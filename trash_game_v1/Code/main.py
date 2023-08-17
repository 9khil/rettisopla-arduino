import pygame, time, pickle, os
from Animation import *
from Bin import *
from Box import *
from Heart import *
from Icons import *
from Overview import *
from Score import *
from Settings import *
from Timer import *
from Trash import *
from Keyboard import *

Keybinds = {
    "Elektrisk": pygame.K_q,
    "Farlig": pygame.K_w,
    "Mat": pygame.K_e,
    "Papp og Papir": pygame.K_r,
    "Restavfall": pygame.K_t
}


class Game:
    def __init__(self):
        pygame.init()

        self.Screen = pygame.display.set_mode((Width, Height))
        self.Clock = pygame.time.Clock()

        pygame.display.set_caption("TRASH GAME")
        pygame.mouse.set_visible(False)

        self.Background = pygame.image.load("../Graphics/Background.png").convert_alpha()
        self.Background = pygame.transform.scale(self.Background, (Width, Height)).convert_alpha()

        self.LoadScores()
        self.LoadStartMenu()

    def LoadScoreBoard(self):
        self.GameState = "Game Over"

        self.SaveScores()

        self.Icons[2].Position = (Scale(200), Height - Scale(400))
        self.Icons[3].Position = (Scale(200), Scale(400))

        self.Icons[2].Size = Scale(500)
        self.Icons[3].Size = Scale(500)

        self.Icons[2].Update()
        self.Icons[3].Update()

        self.ScoreSprites = []

        Index = 0
        Place = 0
        for CurrentScore in reversed(sorted(self.Scores.items())):
            Place += 1

            for CurrentName in sorted(CurrentScore[1]):
                Index += 1
                self.ScoreSprites.append(Score(Place, CurrentScore[0], CurrentName, ((Width / 2), Index * Scale(200))))

    def LoadScores(self):
        if "Scores" in os.listdir(".."):
            self.Scores = pickle.load(open("../Scores", "rb"))

        else:
            self.Scores = {}

    def SaveScores(self):
        if self.Score.Number not in list(self.Scores.keys()):
            self.Scores[self.Score.Number] = []

        self.Scores[self.Score.Number].append(self.Name)

        pickle.dump(self.Scores, open("../Scores", "wb"))

    def Sort(self, Type):
        if len(self.Trash) > 0:
            for CurrentTrash in self.Trash:
                if self.PickUpBox.Rectangle.colliderect(CurrentTrash.Rectangle) and not CurrentTrash.Disabled:
                    if CurrentTrash.Type == Type:
                        for CurrentBin in self.Bins:
                            if CurrentBin.Type == CurrentTrash.Type:
                                CurrentTrash.GoToPosition = (CurrentBin.PositionX, CurrentBin.PositionY)
                                CurrentTrash.Disabled = True

                        self.Score.Number += 1 * self.Multiplier.Number
                        self.Score.Update()

                        self.Streak.Number += 1
                        self.Streak.Update()

                        pygame.mixer.Sound("../Sounds/Correct.mp3").play()

                        if self.Streak.Number > self.HighestStreak:
                            self.HighestStreak = self.Streak.Number

                    else:
                        self.Wrong()
                        CurrentTrash.Gravity = Scale(-7)
                        CurrentTrash.Disabled = True

    def Wrong(self):
        self.Streak.Number = 0
        self.Streak.Update()

        pygame.mixer.Sound("../Sounds/Fail.mp3").play()

        Fail = True
        Enabled = False

        for CurrentHeart in reversed(self.Hearts):
            if CurrentHeart.Enabled:
                if not Enabled:
                    CurrentHeart.Enabled = False
                    CurrentHeart.Update()

                    Enabled = True

                else:
                    Fail = False
                    break

        if Fail:
            self.LoadScoreBoard()
            pygame.mixer.Sound("../Sounds/Death.mp3").play()


    def GameOver(self):
        self.GameState = "Game Over"

        self.SaveScores()

        Font = pygame.font.Font(None, int(Scale(500)))

        self.YouLost = Font.render("YOU LOST", False, "black")
        self.YouLostRectangle = self.YouLost.get_rect(center = (Width / 2, Height / 4))

        self.Score.Position = (Width / 2, Height / 2)
        self.Score.Update()

    def LoadGame(self):
        self.GameState = "Game"

        self.NewTrashTime = 5
        self.NewTrashTimer = Timer(self.NewTrashTime)
        self.TrashSpeedTimer = Timer()

        self.Score = Overview("Score", (Scale(150), Scale(50)))
        self.Streak = Overview("Streak", (Scale(450), Scale(50)))
        self.Multiplier = Overview("Multiplier", (Scale(750), Scale(50)))

        self.HighestStreak = 0
        self.KeyLog = ""

        if hasattr(self, "RGB"):
            delattr(self, "RGB")

        self.Trash = []
        self.Hearts = []
        self.Bins = []

        for i in range(10):
            self.Hearts.append(Heart((((Scale(60)) + (i * (Scale(100)))), (((Scale(50)) - (self.Score.Box.get_height() / 2)) + ((Scale(75)) / 2)) + 60)))

        for Path in os.walk("../Bins"):
            for FileIndex, File in enumerate(reversed(Path[2])):
                self.Bins.append(Bin((Width - (Scale(110))) - (FileIndex * (Scale(150))), f"../Bins/{File}", list(Keybinds.keys())[(len(Keybinds) - 1) - FileIndex]))

        for Path in os.walk("../Conveyor Belt"):
            Frames = []

            for File in Path[2]:
                Frames.append(f"../Conveyor Belt/{File}")

        self.ConveyorBelt = Animation(Frames)

        self.PickUpBox = Box((self.ConveyorBelt.Image.get_size()[0] - Scale(300), Height - Scale(335)), "../Graphics/Pick Up Box.png", True)
        self.FailedItemBox = Box((Scale(1900), Height - Scale(10)), "../Graphics/Failed Item Box.png")

    def LoadStartMenu(self):
        self.GameState = "Start Menu"

        Font = pygame.font.Font(None, int(Scale(100)))

        self.Title = pygame.image.load("../Graphics/Title.png")
        self.Title = Scale(self.Title)
        self.TitleRectangle = self.Title.get_rect(center = (Width / 2, Height / 4))

        self.Message = Font.render('PRESS RETURN TO START', False, "black")
        self.MessageRectangle = self.Message.get_rect(center = (Width / 2, Height / 1.75))

        self.Name = ""

        self.MessageTimer = Timer()

        self.Keyboard = Keyboard(self.Screen)

        self.Icons = []

        for Path in os.walk("../Icons"):
            for FileIndex, File in enumerate(Path[2]):
                self.Icons.append(Icon((Scale(250), Scale(250) + (Scale(250) * FileIndex)), f"../Icons/{File}"))

    def Run(self):
        while True:
            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    exit()

                elif Event.type == pygame.KEYDOWN:
                    if self.GameState == "Game":
                        if not hasattr(self, "RGB") and len(self.Trash) <= 1:
                            self.KeyLog += Event.unicode

                            if "rreeqwqw".casefold() in self.KeyLog.casefold():
                                self.RGB = pygame.image.load("../Secret/RGB.png")
                                self.RGB = pygame.transform.scale(self.RGB, (Width, Height))
                                self.RGB.set_alpha(100)

                        for CurrentKeybind in Keybinds.items():
                            if Event.key == CurrentKeybind[1]:
                                self.Sort(CurrentKeybind[0])

                    elif self.GameState == "Game Over":
                        if Event.key == pygame.K_r:
                            for CurrentScore in self.ScoreSprites:
                                CurrentScore.PositionY -= 150

                        elif Event.key == pygame.K_e:
                            for CurrentScore in self.ScoreSprites:
                                CurrentScore.PositionY += 150

                        else:
                            self.LoadStartMenu()

                    elif self.GameState == "Start Menu":
                        Key = self.Keyboard.GetInput(Event.key, self.Name)

                        if Key == True:
                            if self.Name != "":
                                self.LoadGame()

                        else:
                            if len(Key) < 11:
                                self.Name = Key

            self.Screen.blit(self.Background, (0, 0))

            if self.GameState == "Start Menu":
                self.Screen.blit(self.Title, self.TitleRectangle)

                for CurrentIcon in self.Icons:
                    self.Screen.blit(CurrentIcon.Surface, CurrentIcon.Rectangle)

                if self.MessageTimer >= 1:
                    if self.MessageTimer >= 2:
                        self.MessageTimer.Reset()

                else:
                    self.Screen.blit(self.Message, self.MessageRectangle)

                Font = pygame.font.Font(None, int(Scale(125)))

                NameChooser = Font.render(self.Name, False, "black")
                NameChooserRectangle = NameChooser.get_rect(center = (Width / 2, Height / 1.5))

                self.Screen.blit(NameChooser, NameChooserRectangle)

                self.Keyboard.Update()

            elif self.GameState == "Game":
                self.Multiplier.Number = 2 ** int(self.Streak.Number / 5)
                self.Multiplier.Update()

                self.Screen.blit(self.Streak.Box, self.Streak.Rectangle)
                self.Screen.blit(self.Score.Box, self.Score.Rectangle)
                self.Screen.blit(self.Multiplier.Box, self.Multiplier.Rectangle)

                if self.NewTrashTimer >= self.NewTrashTime:
                    self.Trash.append(Trash())

                    self.NewTrashTimer.Reset()

                for CurrentTrash in self.Trash:
                    if CurrentTrash.PositionY >= Height - 30:
                        if not CurrentTrash.Disabled:
                            self.Wrong()

                        CurrentTrash.Disabled = True

                    if CurrentTrash.PositionX >= self.ConveyorBelt.Image.get_width() + 200 + CurrentTrash.StopPoint:
                        CurrentTrash.Stop = True

                    if CurrentTrash.PositionX > self.ConveyorBelt.Image.get_width() - (CurrentTrash.Surface.get_width() / 1.3) and CurrentTrash.GoToPosition == None or (CurrentTrash.Disabled and not CurrentTrash.Hidden):
                        if CurrentTrash.PositionY < Height - Scale(20):
                            CurrentTrash.Gravity += Scale(.1)
                            CurrentTrash.PositionY += CurrentTrash.Gravity

                        if not CurrentTrash.Stop:
                            CurrentTrash.Rotation += CurrentTrash.RotationSpeed

                    CurrentTrash.Speed = (self.TrashSpeedTimer / 20) + 2
                    CurrentTrash.Update()

                    if not CurrentTrash.Hidden:
                        self.Screen.blit(CurrentTrash.Surface, CurrentTrash.Rectangle)

                self.PickUpBox.Update()

                self.Screen.blit(self.PickUpBox.Surface, self.PickUpBox.Rectangle)
                self.Screen.blit(self.FailedItemBox.Surface, self.FailedItemBox.Rectangle)

                self.ConveyorBelt.Update()
                self.Screen.blit(self.ConveyorBelt.Image, (Scale(-15), Height - (Scale(190))))

                for CurrentBin in self.Bins:
                    self.Screen.blit(CurrentBin.Surface, CurrentBin.Rectangle)

                    for Label in CurrentBin.Labels:
                        self.Screen.blit(*Label)

                for CurrentHeart in self.Hearts:
                    self.Screen.blit(CurrentHeart.HeartContainer, CurrentHeart.Rectangle)

                if hasattr(self, "RGB"):
                    self.Screen.blit(self.RGB, (0, 0))

            elif self.GameState == "Game Over":
                for CurrentScore in self.ScoreSprites:
                    CurrentScore.Update()

                    self.Screen.blit(CurrentScore.Box, CurrentScore.BoxRectangle)

                for CurrentIcon in self.Icons[2:4]:
                    self.Screen.blit(CurrentIcon.Surface, CurrentIcon.Rectangle)

            pygame.display.flip()
            self.Clock.tick(FPS)


if __name__ == "__main__":
    Game().Run()