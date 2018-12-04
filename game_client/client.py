from tkinter import *
from tkinter import font
from random import randint

class Client(Tk):
  def __init__(self,*args,**kwargs):
    Tk.__init__(self,*args,**kwargs)

    # dimensions
    height = 1000
    width = height+(height*0.5)
    # set unresizable
    self.resizable(0,0)
    # title
    self.title("BATTLE CITY")
    # font style
    self.titleFont = font.Font(family="Press Start",size=64,weight="bold")

    container = Frame(self,width=width,height=height,bg="black")
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0,weight=1)
    container.grid_columnconfigure(0,weight=1)
    container.update()

    self.frames = {}
    for F in (StartPage,GameFrame):
      pageName = F.__name__
      frame = F(master=container,controller=self)
      self.frames[pageName] = frame

      frame.grid(row=0,column=0,sticky="nsew")

    self.showFrame("StartPage")

  def showFrame(self,pageName):
    frame = self.frames[pageName]
    frame.tkraise()

  def exit(self):
    self.destroy()

class StartPage(Frame):
  def __init__(self,master,controller):
    Frame.__init__(self,master,bg="black")
    self.controller = controller
    titleImage = PhotoImage(file="title.png")
    title = Label(self,image=titleImage,bg="black")
    title.image = titleImage
    title.pack(side="top",pady=10)

    startButton = Button(self,text="Start game",command=lambda: controller.showFrame("GameFrame"))
    exitButton = Button(self,text="Exit game",command=lambda: controller.exit())

    startButton.pack()
    exitButton.pack()

class GameFrame(Frame):
  def __init__(self,master,controller):
    Frame.__init__(self,master)
    self.controller = controller

    # create game field
    length = self.master.winfo_height()
    side = int(length / 20) * 20

    gameField = GameCanvass(self,side)
    gameField.pack(side=LEFT)

    # create chat field
    chatHeight = self.master.winfo_height()
    chatWidth = self.master.winfo_width() * .2
    chatField = Frame(self,height=chatHeight,width=chatWidth)
    chatField.pack(side=LEFT)


class GameCanvass(Canvas):
  def __init__(self,master,side):
    Canvas.__init__(self,master,height=side,width=side,bg="black")
    self.images = []
    self.inc = side//20
    self.players = ["tankGreenUp.png","tankRed.png"]

    self.getMap = self.readMap("map.txt")
    self.drawMap(self.getMap)
    self.drawSprites(self.getMap)

  def readMap(self,map):
    file = open(map)
    lines = [line.rstrip('\n') for line in file]
    chars = []

    for line in lines:
      charLine = []
      charLine.extend(line)
      chars.append(charLine)

    return chars
  def drawMap(self,getMap):
    self.brickList = []
    for row in range(0,len(getMap)):
      for col in range(0,len(getMap[0])):
        if getMap[col][row] == 'b':
          sprite = PhotoImage(file="brickk.png")
          self.images.append(sprite)
          self.brick = self.create_image(((row*self.inc),(col*self.inc)),image=sprite,anchor=NW,tag="brick")
  def drawSprites(self,getMap):
    self.brickList = []
    for row in range(0,len(getMap)):
      for col in range(0,len(getMap[0])):
        if getMap[col][row] == 't':
          player = Player(self,"tankGreenUp.png",col*self.inc,row*self.inc)

  def checkCollision(self,view):
    bricks = self.find_withtag("brick")
    player = self.find_withtag("player")
    x1, y1, x2, y2 = self.bbox(player)
    overlap = ()
    if view == 'w' :
      overlap = self.find_overlapping(x1, y1-10, x2, y1-10)
    elif view == 's' :
      overlap = self.find_overlapping(x1, y2+10, x2, y2+10)
    elif view == 'a' :
      overlap = self.find_overlapping(x1-10, y1, x1-10, y2)
    elif view == 'd' :
      overlap = self.find_overlapping(x2+10, y1, x2+10, y2)
    for brick in bricks:
      for over in overlap:
        if brick == over: return 1

class Player:
  def __init__(self,master,icon,col,row):
    self.master = master
    self.col = col
    self.row = row
    icon = PhotoImage(file=icon)
    self.master.images.append(icon)
    self.player = self.master.create_image((self.row,self.col),image=icon,anchor=NW,tag="player")
    self.view = ""
    self.master.bind('<Key>', self.move)
    self.master.focus_set()

  def move(self,event):
    deltax = deltay = 0
    check = self.master.checkCollision(self.view)
    if event.char == 'w':
      if self.view == 'w': deltay -= 10
      else:
        self.view = 'w'
      icon = PhotoImage(file="tankGreenUp.png")
      self.master.images.append(icon)
      self.master.itemconfig(self.player,image=icon,anchor=NW)
    elif event.char == 's':
      if self.view == 's': deltay += 10
      else:
        self.view = 's'
      icon = PhotoImage(file="tankGreenDown.png")
      self.master.images.append(icon)
      self.master.itemconfig(self.player,image=icon,anchor=NW)
    elif event.char == 'a':
      if self.view == 'a': deltax -= 10
      else:
        self.view = 'a'
      icon = PhotoImage(file="tankGreenLeft.png")
      self.master.images.append(icon)
      self.master.itemconfig(self.player,image=icon,anchor=NW)
    elif event.char == 'd':
      if self.view == 'd' : deltax += 10
      else:
        self.view = 'd'
      icon = PhotoImage(file="tankGreenRight.png")
      self.master.images.append(icon)
      self.master.itemconfig(self.player,image=icon,anchor=NW)
    if check != 1: self.master.move(self.player,deltax,deltay)

if __name__ == "__main__":
  app = Client()
  app.mainloop()