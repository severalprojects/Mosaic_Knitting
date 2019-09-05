import JStrings as JS
import tkinter as TK
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser
import random
from functools import partial
import math
import block as B
import makeblocks as blox
import pattern as P

                
def swapSinString(string, stitchList): ##take a string and list of coords and swap those stitches
    asList = list(string)
    for stitch in stitchList:
        if asList[stitch] == "0":
            asList[stitch] = "-"
        else:
            asList[stitch] = "O"  
    swappedString = "".join(asList)   
    return swappedString       

##############FILE I/O METHODS

def saveBlock(): 
    
    filename = TK.filedialog.asksaveasfilename(initialdir = "./",title = "Save Block As...")
    saveFile = open(filename, "w")
    saveFile.write(myPattern.getInfo())
    saveFile.close()   

def openBlock(Pattern): 
    
    filename = TK.filedialog.askopenfilename(initialdir = "./",title = "Choose Block File")
    thefile = open(filename, "r")
    bString = thefile.read()
    thefile.close()
    block = bString.split(",")
    b = block[0]
    r = int(block[1])
    c = int(block[2])

    
    Pattern.reset()
    

    Pattern.makeEditable()

    if block[3] and block[4]:
        Pattern.color1 = block[3]
        Pattern.color2 = block[4]
        Pattern.draw()

    Pattern.loadBlock(b, r, c)

def getColor():
    color = colorchooser.askcolor()
    print(color[1]) 

#####################################

############METHODS TO GENERATE INITIAL BLOCK#################

def buttonTile(theBlock, hRepeat, vRepeat):
    theBlock.bTile(hRepeat, vRepeat)
    

#####MAIN PROGRAM HERE.....###############

tessconstant = 4

theWindow = TK.Tk()


theBlock=blox.randomVBlock(8,8, 3) 
 

myPattern = P.Pattern(*theBlock, theWindow, 500, 500)
myPattern.myBlock.bPrint()
pattern2 = P.Pattern(*theBlock, theWindow, 500, 500)
pattern2.setRepeat(tessconstant, tessconstant)



myPattern.pack(side="left")

myPattern.setTesselator(pattern2)
myPattern.makeEditable()

pattern2.pack(side="right")
pattern2.noEdit()
# pattern2.makeSelectable()

myPattern.bTile(tessconstant, tessconstant)

B = TK.Button(theWindow, text ="tesselate", command = partial(myPattern.bTile, tessconstant, tessconstant))
V = TK.Button(theWindow, text ="validate", command = partial(myPattern.validate, 3))
SaveButton = TK.Button(theWindow, text ="save block", command = saveBlock)
RandomButton = TK.Button(theWindow, text ="random block", command = partial(myPattern.randomVBlock, 8, 8, 3))
DefaultButton = TK.Button(theWindow, text ="default block", command = partial(myPattern.defaultVBlock, 8, 8))
LoadButton = TK.Button(theWindow, text ="load", command = partial(openBlock, myPattern))
C1Button= TK.Button(theWindow, text="color1", command=myPattern.setColor1)
C2Button= TK.Button(theWindow, text="color2", command=myPattern.setColor2)


V.pack()
B.pack()
SaveButton.pack()
RandomButton.pack()
DefaultButton.pack()
LoadButton.pack()
C1Button.pack()
C2Button.pack()

theWindow.mainloop()
