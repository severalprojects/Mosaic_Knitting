import JStrings as JS
import tkinter as TK
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser
import random
from functools import partial
import math
import makeblocks as blox
import block as B


class Pattern(TK.Canvas):
    
    def __init__(self, string, rows, cols, window, w, h):
        
        #inheritance: call the constructor of the parent object to initialize its values
        
        self.C = TK.Canvas.__init__(self, window, bg="white", height=w, width=h, cursor="cross")
        
        #vBlock contains a block. 
        self.myBlock = B.block(string, rows, cols) #initialize a block inside vBlock

        self.canEdit = True 
        
        self.canSelect = False

        #"mirror" may contain a reference to another block (for example, where tessalation is displayed)

        self.tesselator = None
        self.repeatH = 1
        self.repeatV = 1

        self.rows = rows
        self.cols = cols
        
        #print(self.myBlock.s)

        self.bind("<Button-1>", self.swapStitch) #connect mouse input to the canvas
        
        self.SCoords = blox.boxCoords(500, 500, cols, rows) #store the coordinates of the stitches 
                                                  
        self.squares = []

        #default colors for now.... 
        self.color1 = "#333333"
        self.color2 = "#dddddd"

        
        
        #self.draw()
        for i in range(rows*cols):
            if self.myBlock.s[i] == "0":
                self.squares.append([self.create_polygon(self.SCoords[i], \
                                                       fill=self.color1, outline="black"), 0]) 
            else:
                self.squares.append([self.create_polygon(self.SCoords[i], \
                                                       fill=self.color2, outline="black"), 1]) 
    def setColor1(self):
        color = colorchooser.askcolor()[1]
        self.color1 = color
        self.draw()
        if self.tesselator: 
            self.tesselator.color1 = color
            self.tesselator.draw()

        
    def setColor2(self):
        color = colorchooser.askcolor()[1]
        self.color2 = color
        self.draw()
        if self.tesselator: 
            self.tesselator.color2 = color
            self.tesselator.draw()
    
    def setTesselator(self, tesser):
        self.tesselator = tesser

    def setRepeat(self, hRep, vRep):
        self.repeatH = hRep
        self.repeatV = vRep

    def noEdit(self):
        self.canEdit = False    

    def makeEditable(self):
        self.canEdit = True

    def updateTess(self, rowClicked, colClicked, blockRows, blockCols):
        for i in range(self.repeatH):
            for j in range(self.repeatV):
                # print(i)
                index = rowClicked*blockCols*self.repeatH+colClicked+blockCols*i+j*self.repeatH*blockCols*blockRows
                # print("tessblock index is:{}".format(index))
                # print("string is this: {}".format(self.myBlock.s[index]))
            
                if self.myBlock.s[index] == '0': #switch this to looking at string. 
                    # print("tess_block_stitch is color1")
                    self.create_polygon(self.SCoords[index], fill=self.color2, outline="black")
                    tempList = list(self.myBlock.s)
                    tempList[index] = "-"
                    self.myBlock.s = "".join(tempList) 

                else:
                    # print("tess_block_stitch is color2")
                    self.create_polygon(self.SCoords[index], fill=self.color1, outline="black")
                    tempList = list(self.myBlock.s)
                    tempList[index] = "0"
                    self.myBlock.s = "".join(tempList) 
        self.pack()        

    def swapStitch(self, event):
        

            
        
        rowClicked = event.y//math.floor((500/self.myBlock.r))
        colClicked = event.x//math.floor((500/self.myBlock.c))
        stitchClicked = rowClicked*(self.myBlock.c) + colClicked
        # print("boxes are {} pixels wide/tall".format(int((500/self.myBlock.r))))
        # print("clicked at {}, {}, which is row {}, col {}".format(event.x, event.y, rowClicked, colClicked))
        # print("which is stitch {}".format(stitchClicked))

        if self.tesselator:
            self.tesselator.updateTess(rowClicked, colClicked, self.rows, self.cols)

        if self.canEdit:
            if self.squares[stitchClicked][1] == 0:
                # print("stitch is color1")
                self.create_polygon(self.SCoords[stitchClicked], fill=self.color2, outline="black")
                # self.itemconfig(self.squares[stitchClicked][0], fill=self.color2)
                # self.itemconfig(self.squares[stitchClicked][0], outline="black")
                # self.itemconfig(self.squares[stitchClicked][0], width="0")
                
                self.squares[stitchClicked][1] = 1
                tempList = list(self.myBlock.s)
                tempList[stitchClicked] = "-"
                self.myBlock.s = "".join(tempList) 
            else:
                # print("stitch is color2")
                self.create_polygon(self.SCoords[stitchClicked], fill=self.color1, outline="black")
                # self.itemconfig(self.squares[stitchClicked][0], fill=self.color1)
                # self.itemconfig(self.squares[stitchClicked][0], outline="black")
                # self.itemconfig(self.squares[stitchClicked][0], width="0")
                self.squares[stitchClicked][1] = 0
                tempList = list(self.myBlock.s)
                tempList[stitchClicked] = "0"
                self.myBlock.s = "".join(tempList)            
            #self.myBlock.bPrint()
            # self.validate(3)
            self.pack()

        # if self.tesselator: #code here where the tessalator goes. 
        #     blockSize = 64
        #     for i in range(4):
        #         self.tesselator.create_polygon(self.tesselator.SCoords[stitchClicked+(i*blockSize)], fill="black")

        # for i in range(self.myBlock.r*self.myBlock.c):
        #     if self.myBlock.s[i] == "0":
        #         self.squares.append([self.create_polygon(self.SCoords[i], \
        #                                                fill=self.color1, outline="black"), 0]) 
        #     else:
        #         self.squares.append([self.create_polygon(self.SCoords[i], \
                
        #                                       fill=self.color2, outline="black"), 1]) 
    
    def bTile(self, hRepeat, vRepeat):
        tessblock = self.myBlock.bTile(hRepeat, vRepeat)
        if self.tesselator:
            self.tesselator.loadBlock(tessblock.s, tessblock.r, tessblock.c)
            self.repeatH = hRepeat
            self.repeatV = vRepeat
        else:     
            self.loadBlock(tessblock.s, tessblock.r, tessblock.c)
        return

    def validate(self, longestRun):
        self.clearErrors()
        self.highlightRuns(self.myBlock.validate(longestRun))
        self.highlightLifts(self.myBlock.findBadLifts())
        return

    def highlightRuns(self, runList):
        for color in runList:
            if color:
                for item in color:
                    for stitch in item:
                        self.highlightRStitch(stitch)

    def highlightLifts(self, liftList):
        for color in liftList:
            if color:
                for stitch in color:
                    self.highlightBLStitch(stitch)                    

    def highlightRStitch(self, thestitch):
        #sCoords list is [UL(x, y), UR(x, y), LR(x, y), LL(x,y)]
        the_ex = self.SCoords[thestitch]
        self.create_line(the_ex[0], the_ex[1], the_ex[4], the_ex[5], width="3")
        self.create_line(the_ex[2], the_ex[3], the_ex[6], the_ex[7], width="3")
        # self.create_polygon(self.SCoords[thestitch], outline="red", fill='')
        # self.itemconfig(self.squares[thestitch][0], outline="red", width="5")
        self.pack()

    def highlightBLStitch(self, thestitch):
        #SCoords list is [UL(x, y), UR(x, y), LR(x, y), LL(x,y)]
        the_ex = self.SCoords[thestitch]
        self.create_line(the_ex[0], the_ex[1], the_ex[4], the_ex[5], width="3")
        self.create_line(the_ex[2], the_ex[3], the_ex[6], the_ex[7], width="3")
        # self.create_polygon(self.SCoords[thestitch], outline="red", fill='')
        # self.itemconfig(self.squares[thestitch][0], outline="red", width="5")
        self.pack()

    def highlightSubBlock(self, UpperLeft, LowerRight):
        #take 2 lists in format [x, y] and draw a highlight square around the appropriate boxes
        return



    def draw(self, theside=None):
        for i in range(self.myBlock.r*self.myBlock.c):
            if self.myBlock.s[i] == "0":
                self.squares.append([self.create_polygon(self.SCoords[i], \
                                                       fill=self.color1, outline="black"), 0]) 
            else:
                self.squares.append([self.create_polygon(self.SCoords[i], \
                
                                              fill=self.color2, outline="black"), 1]) 

        if theside:
            self.pack(side=theside)
        else:
            self.pack()    
    
    def clearErrors(self):
        # for square in self.squares:
        #     self.itemconfig(square[0], outline="black")
        #     self.itemconfig(square[0], width="1")
        self.loadBlock(self.myBlock.s, self.myBlock.r, self.myBlock.c)

    def newRandom(self, rows, cols):
        self.delete("all")
        self.squares = []
        self.myBlock = block(*randomBlock(10, 10))
        self.myBlock.bPrint()
        for i in range(rows*cols):
            if self.myBlock.s[i] == "0":
                self.squares.append([self.create_polygon(self.SCoords[i], \
                                                       fill=self.color1, outline="black"), 0]) 
            else:
                self.squares.append([self.create_polygon(self.SCoords[i], \
                                                       fill=self.color2, outline="black"), 1])
        
        
        self.draw()


########METHODS RELATING TO FILE I/O################################
    #get a comma separated string which will be useful to save
    def getInfo(self):
        blockInfo = [self.myBlock.s, str(self.myBlock.r), str(self.myBlock.c), self.color1, self.color2]
        s = ","
        return s.join(blockInfo)
    def reset(self):
        self.delete("all")
        self.squares = []
        print("reset")

    def loadBlock(self, theString, rows, cols): #method to laod in a new block entirely
        self.reset()
        self.myBlock.r = rows
        self.myBlock.c = cols
        self.SCoords = blox.boxCoords(500, 500, cols, rows)
        self.myBlock = B.block(theString, rows, cols)   
        print ("set my block")  
        self.squares = []   
        for i in range(rows*cols):
            
            if self.myBlock.s[i] == "0":
                self.squares.append([self.create_polygon(self.SCoords[i], \
                                                       fill=self.color1, outline="black"), 0]) 
            else:
                self.squares.append([self.create_polygon(self.SCoords[i], \
                                                       fill=self.color2, outline="black"), 1])
        if self.tesselator:
            self.tesselator.color1 = self.color1
            self.tesselator.color2 = self.color2
            self.bTile(self.repeatH, self.repeatV)

        # print("thesquarearray has {} entries".format(len(self.squares)))
        # self.draw()

        #when you load, load the same block into the tessalator. 
 

        # if self.tesselator:
        #     tessblock = self.myBlock.bTile(self.tesselator.hRepeat, self.tesselator.vRepeat)
        #     self.tesselator.loadBlock(tessblock.s, tessblock.r, tessblock.c)
        #     self.repeatH = hRepeat
        #     self.repeatV = vRepeat    
 

    #generate and load a random valid block
    def randomVBlock(self, rows, cols, runs):
        theblock = blox.randomVBlock(rows, cols, runs)
        self.loadBlock(*theblock)
    
    #generate and load the default block
    def defaultVBlock(self, rows, cols):
        theblock = blox.defaultBlock(rows, cols)
        self.loadBlock(*theblock)


        # num1 = 0
        # num2 = 0
        # lastNode = False
        
        # n1_place = 0
        
        # while not lastNode:
        #     num1 += l1.val*10**n1_place
           
        #     l1 = l1.next
        #     n1_place+=1
        #     if not l1:
        #         lastNode = True
        # lastNode = False
        
        # n2_place = 0
        # while not lastNode:
        #     num2 += l2.val*10**n2_place
        #     l2 = l2.next
        #     n2_place+=1
        #     if not l2:
        #         lastNode = True
      
        
        # theSum = num1 + num2
      
        # sumString = str(theSum)

        
        # sumNums = []
        # for index in range(len(sumString)):
        #     sumNums.append(int(sumString[index]))
        
        # print(sumNums)
        # linkedList = []
        
        # sumNums.reverse()
        
        # for item in sumNums:
        #     linkedList.append(ListNode(item))
        
        
        
        # for node in range(len(linkedList)-1):
        #     linkedList[node].next = linkedList[node+1]
        
        # return linkedList[0]
    