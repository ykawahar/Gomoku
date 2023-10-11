""" ==================================================
COMP 123 Project
Getiria Onsongo

                --- GOMOKU ---
By:
Yuki Kawahara
Daniel Fang

Dec 12 2019

This program runs a game of Gomoku.
Line up five same-color pieces to win!

Created on Python 3.7.4
====================================================="""
from tkinter import *
import PIL.Image as Image
import PIL.ImageTk as ImageTk
# =====================================================


def returnClick(event):
    """When a click is made, sets clickX and clickY as the x,y values of the position of the mouse cursor."""
    global clickX, clickY
    clickX = event.x
    clickY = event.y
    # print("return", clickX, clickY)


def makePoints():
    """ Makes a list of tuples of the coordinates of intersections of the Gomoku gridlines."""
    lst = []
    for x in range(15):
        for y in range(15):
            lst.append((((y + 1) * 32), ((x + 1) * 32)))
    return lst


# -----------  global variables ------------

clickX = 0
clickY = 0

point = makePoints()

boardScreen = False


# -----------  Game ------------
class GameScreen:

    def __init__(self):
        self.gameMenu = Tk()
        self.gameMenu.title("Gomoku")
        self.gameMenu.geometry("650x300")
        self.win = False
        self.tie = False

        #  -----------  Menu Widgets ------------
        self.startButton = Button(self.gameMenu, text="Start Game", relief=GROOVE,
                                  justify=CENTER, bd=5, command=self.goGame, width=8, fg="red")
        self.startButton.place(x=550, y=100)

        self.quitButton = Button(self.gameMenu, text="Quit", command=self.goQuit, relief=GROOVE,
                                 justify=CENTER, bd=5, width=8)
        self.quitButton.place(x=550, y=200)

        # Adds background image
        pic = Image.open("Gomokubg.png")
        self.turtlePic = ImageTk.PhotoImage(pic)
        imgLabel = Label(self.gameMenu, image=self.turtlePic)
        imgLabel.grid(row=0, column=0)

    # -----------  Functions of menu window ------------
    def goQuit(self):
        """ Closes the menu screen and quits the game"""
        self.gameMenu.destroy()

    def goGame(self):
        """ Opens the board and starts the game"""
        global boardScreen
        if not boardScreen:
            self.gameMenu.destroy()
        else:
            self.gameWin.destroy()
        self.gameWin = Tk()
        self.gameWin.title("Gomoku")
        self.gameWin.colorVal = "black"  # Starts as black
        self.gameWin.whitePieces = []
        self.gameWin.blackPieces = []
        self.gameWin.filled_spaces = 0
        boardScreen = True

        #  -----------  Board ------------
        self.gameBoard = Canvas(self.gameWin, bg="Wheat", width=500, height=500, relief=RAISED)
        self.gameBoard.grid(row=1, column=1)
        self.gameBoard.bind("<Button-1>", self.placePiece)

        for i in range(15):  # Board setup Lines and Dots
            self.gameBoard.create_line(32, 32 * (i + 1), 480, 32 * (i + 1), fill="black")
            self.gameBoard.create_line(32 * (i + 1), 32, 32 * (i + 1), 480, fill="black")
        self.gameBoard.create_oval(254, 254, 258, 258, fill="black")
        self.gameBoard.create_oval(126, 126, 130, 130, fill="black")
        self.gameBoard.create_oval(126, 382, 130, 386, fill="black")
        self.gameBoard.create_oval(382, 126, 386, 130, fill="black")
        self.gameBoard.create_oval(382, 382, 386, 386, fill="black")

        #  -----------  Frame ------------
        self.gameFrame = Frame(self.gameWin, width = 200, height = 500)
        self.gameFrame.grid(row=1, column=2)
        self.gameFrame.grid_propagate(False)

        quitButton = Button(self.gameFrame, text="Quit", command=self.quitCallback)
        quitButton.grid(row=2, column=1)

        self.turnLabel = Label(self.gameFrame, bg = "aquamarine", text= "Black's Turn", font = "Calibri 20", relief=GROOVE)
        self.turnLabel.grid(row = 1, column = 1, padx = 30, pady = 50)

        self.winLabel = Label(self.gameFrame, text = "", font = "Fixedsys 22 bold")
        self.winLabel.grid(row = 0, column = 1, pady = 50)

        self.resetButton = Button(self.gameFrame, text="Reset Board", command=self.reset)
        self.resetButton.grid(row=3, column=1)

        #  -----------  Pieces ------------
        # Create invisible pieces (for testing)
        # for coord in point:
        #     self.gameBoard.create_oval((coord[0] - 10), (coord[1] - 10), (coord[0] + 10), (coord[1] + 10)

    # -----------  Functions of board window ------------

    def turnChange(self):
        """ Changes settings to the next player """
        # global self.gameWin.colorVal
        if self.gameWin.colorVal == "black":
            self.gameWin.colorVal = "white"
            self.turnLabel['text'] = "White's Turn"
        else:
            self.gameWin.colorVal = "black"
            self.turnLabel['text'] = "Black's Turn"

    def prepareWin(self):
        """ Sets the game to end with a win."""
        # global self.gameWin.colorVal
        self.win = True
        self.winLabel["text"] = self.gameWin.colorVal.title() + " Wins!"

    def prepareTie(self):
        """ Sets the game to end if all places are full"""
        if self.gameWin.filled_spaces >= 225:
            self.tie = True
            self.winLabel["text"] = "Tie!"
        else:
            pass

    def checkLine(self, list, count, inX, inY, xMod, yMod):
        """ Checks whether pieces of the same color are lined up.
        Parameters (list of pieces to check, count, current x value, current y value,
        x direction to count, y direction to count)"""
        sameColors = count
        for i in range(5):
            (x, y) = (inX + (i+1) * 32 * xMod, inY + (i+1) * 32 * yMod)
            if (x, y) in list:
                sameColors = sameColors + 1
            else:
                break
        return sameColors

    def checkWinN(self, x, y):
        """Checks for a diagonal (negative slope) win"""
        # Define the list
        if self.gameWin.colorVal == "black":
            lst = self.gameWin.blackPieces
        else:
            lst = self.gameWin.whitePieces

        count = 0
        count = self.checkLine(lst, count, x, y, -1, 1) # Check Top Left Direction
        count = self.checkLine(lst, count, x, y, 1, -1) # Check Bottom Right Direction
        if count >= 4:
            self.prepareWin()
        else:
            pass

    def checkWinP(self, x, y):
        """Checks for a diagonal (positive slope) win"""
        # Define the list
        if self.gameWin.colorVal == "black":
            lst = self.gameWin.blackPieces
        else:
            lst = self.gameWin.whitePieces

        count = 0
        count = self.checkLine(lst, count, x, y, 1, 1) # Check Top Right Direction
        count = self.checkLine(lst, count, x, y, -1, -1) # Check Bottom Left Direction
        if count >= 4:
            self.prepareWin()
        else:
            self.checkWinN(x, y)

    def checkWinV(self, x, y):
        """ Checks for a vertical win"""
        # Define the list
        if self.gameWin.colorVal == "black":
            lst = self.gameWin.blackPieces
        else:
            lst = self.gameWin.whitePieces

        count = 0
        count = self.checkLine(lst, count, x, y, 0, 1) # Check Down Direction
        count = self.checkLine(lst, count, x, y, 0, -1) # Check Up Direction
        if count >= 4:
            self.prepareWin()
        else:
            self.checkWinP(x, y)

    def checkWinH(self, x, y):
        """ Checks for a horizontal win"""
        # Define the list
        if self.gameWin.colorVal == "black":
            lst = self.gameWin.blackPieces
        else:
            lst = self.gameWin.whitePieces
        # Check Win
        count = 0
        count = self.checkLine(lst, count, x, y, 1, 0) # Check Right Direction
        count = self.checkLine(lst, count, x, y, -1, 0) # Check Left Direction
        if count >= 4:
            self.prepareWin()
        else:
            self.checkWinV(x, y)

    def placePiece(self, event):
        """ Checks if a piece can be placed at a location, and if possible places a piece.'"""
        coordNums = [32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480]    # Possible coord Values
        returnClick(event)
        x = clickX
        y = clickY

        newX = min(coordNums, key=lambda i: abs(i - x))  # Changes to nearest coord val
        newY = min(coordNums, key=lambda i: abs(i - y))  # Changes to nearest coord val
        # print("SHOW", newX, newY)
        pos = tuple((newX, newY))
        if not self.win and not self.tie:
            if (pos in point) and (pos not in self.gameWin.whitePieces) and (pos not in self.gameWin.blackPieces):
                if self.gameWin.colorVal == "black":
                    self.gameBoard.create_oval((newX - 10), (newY - 10), (newX + 10), (newY + 10),
                                         fill="black")
                    self.gameWin.blackPieces.append(pos)
                    self.gameWin.filled_spaces = self.gameWin.filled_spaces + 1
                    self.prepareTie()
                    self.checkWinH(newX, newY)
                    if not self.win and not self.tie:
                       self.turnChange()
                else:
                    self.gameBoard.create_oval((newX - 10), (newY - 10), (newX + 10), (newY + 10),
                                              fill="white")
                    self.gameWin.whitePieces.append(pos)
                    self.gameWin.filled_spaces = self.gameWin.filled_spaces + 1
                    self.prepareTie()
                    self.checkWinH(newX, newY)
                    if not self.win and not self.tie:
                        self.turnChange()
        else:
            pass

    def quitCallback(self):
        """Destroys the game window"""
        self.gameWin.destroy()

    def reset(self):
        """ Resets the Game to the starting conditions."""
        global clickX, clickY

        clickX = 0
        clickY = 0

        self.win = False
        self.tie = False
        self.goGame()

    def run(self):
        """ Run the GameScreen class"""
        self.gameMenu.mainloop()


# ====================================================
game = GameScreen()
game.run()
