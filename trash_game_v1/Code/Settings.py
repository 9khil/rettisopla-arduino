import tkinter, pygame

Root = tkinter.Tk()

Width = Root.winfo_screenwidth()
Height = Root.winfo_screenheight()
FPS = 60

def Scale(Number):
    if isinstance(Number, tuple):
        NewNumbers = []

        for CurrentNumber in Number:
            NewNumbers.append(CurrentNumber * (((Width / 2560) + (Height / 1440)) / 2))

        return NewNumbers

    elif isinstance(Number, pygame.surface.Surface):
        SurfaceWidth, SurfaceHeight = Number.get_size()

        return pygame.transform.scale(Number, (SurfaceWidth * (((Width / 2560) + (Height / 1440)) / 2), SurfaceHeight * (((Width / 2560) + (Height / 1440)) / 2)))

    else:
        return Number * (((Width / 2560) + (Height / 1440)) / 2)