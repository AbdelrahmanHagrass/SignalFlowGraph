


import tkinter as tk

import tkinter.font as tkFont
import easygui
from graphSolveGain import SolveFinalGain
from graphRender import RenderSignalFlowGraph

import Maison
import Structs
maxNoOfNodes = 20

appName = 'Signal Flow Graph'


class App (tk.Frame):
    def __init__(self, root=None, splashWindow=None):
        super().__init__(root)

        self.root = root

        self.grid(sticky='nsew')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frameMatrix = tk.Frame(self)
        frameControls = tk.Frame(self)

        frameMatrix.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=10, pady=10)
        for i in range(0, maxNoOfNodes+1):
            frameMatrix.grid_rowconfigure(i, weight=1)
            frameMatrix.grid_columnconfigure(i, weight=1)

        frameControls.grid(row=0, column=1, sticky='ns', padx=10, pady=10)

        self.noOfNodesTkStr = tk.StringVar()
        tempOptions = [str(i)+' Nodes' for i in range(1, maxNoOfNodes+1)]
        self.noOfNodesSelector = tk.OptionMenu(frameControls, self.noOfNodesTkStr, *tempOptions)
        self.noOfNodesSelector.config(font=defaultFont)
        self.noOfNodesSelector['menu'].config(font=optionMenuItemFont)
        self.noOfNodesSelector.grid(sticky='ew')
        self.noOfNodesTkStr.set('Click here to select the Number of Nodes')
        noOfNodesSelectorCallback = lambda internalName, index, triggerMode: self.RedrawMatrix()
        self.noOfNodesTkStr.trace('w', noOfNodesSelectorCallback)

        tk.Label(frameControls).grid(pady=10)

        self.buttonSolve = tk.Button(frameControls, text='Solve', command=self.SolveGraph,font=tkFont.Font,bg='black',fg='blue')
        self.buttonDraw = tk.Button(frameControls, text='Draw The graph', command=self.DrawGraph,font=tkFont.Font,bg='black',fg='blue')

        self.buttonSolve.grid(sticky='E')

        self.buttonDraw.grid(sticky='E')

        tk.Label(frameControls).grid(pady=10)



        self.rowLabels = []
        self.columnLabels = []
        for i in range(maxNoOfNodes):
            self.rowLabels.append(tk.Label(frameMatrix, text=str(i), relief=tk.SUNKEN, width=3, font=defaultFont))
            self.rowLabels[i].grid(row=i+1, column=0, sticky='nsew', padx=4, pady=4)
            self.rowLabels[i].grid_remove()
            self.columnLabels.append(tk.Label(frameMatrix, text=str(i), relief=tk.SUNKEN, width=3, font=defaultFont))
            self.columnLabels[i].grid(row=0, column=i+1, sticky='nsew', padx=4, pady=4)
            self.columnLabels[i].grid_remove()

        self.textBoxes = []
        for i in range(maxNoOfNodes):
            self.textBoxes.append([])
            for j in range(maxNoOfNodes):
                self.textBoxes[i].append(tk.Entry(frameMatrix, width=3, font=defaultFont))
                self.textBoxes[i][j].grid(row=i+1, column=j+1, sticky='nsew', padx=4, pady=4)
                self.textBoxes[i][j].grid_remove()
                self.textBoxes[i][j].bind('<FocusIn>', self.HighlightNodes)
                self.textBoxes[i][j].bind('<FocusOut>', self.UnhighlightNodes)

        self.update_idletasks()
        CenterifyWindow(self.root)

        if splashWindow:
            splashWindow.destroy()
        self.root.deiconify()
        self.update_idletasks()

    def RedrawMatrix (self):
        self.noOfNodes = int(self.noOfNodesTkStr.get().split()[0])
        self.grid_remove()

        for i in range(maxNoOfNodes):
            if i < self.noOfNodes:
                self.rowLabels[i].grid()
                self.columnLabels[i].grid()
            else:
                self.rowLabels[i].grid_remove()
                self.columnLabels[i].grid_remove()

        for i in range(maxNoOfNodes):
            for j in range(maxNoOfNodes):
                if i < self.noOfNodes and j < self.noOfNodes:
                    self.textBoxes[i][j].grid()
                else:
                    self.textBoxes[i][j].grid_remove()

        self.grid()
        self.update_idletasks()
        CenterifyWindow(self.root)

    def HighlightNodes (self, event):
        for i in range(self.noOfNodes):
            for j in range(self.noOfNodes):
                if self.textBoxes[i][j] == event.widget:
                    self.rowLabels[i].config(bg='grey')
                    self.columnLabels[j].config(bg='grey')

    def UnhighlightNodes (self, event):
        for i in range(self.noOfNodes):
            for j in range(self.noOfNodes):
                if self.textBoxes[i][j] == event.widget:
                    self.rowLabels[i].config(bg=defaultWindowBgColour)
                    self.columnLabels[j].config(bg=defaultWindowBgColour)

    def ExtractMatrix (self):
        matrix = []
        if(not hasattr(self,"noOfNodes")):
            easygui.msgbox("please enter an adjancency matrix representing the Graph!", title="simple gui")
            return None;
        for i in range(self.noOfNodes):
            matrix.append([])
            for j in range(self.noOfNodes):
                matrix[i].append(self.textBoxes[i][j].get())
        return matrix

    def PreprocessMatrix (self, matrix):
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == '':
                    matrix[i][j] = '0'
        return matrix

    def DrawGraph (self):
        matrix = self.ExtractMatrix()
        matrix = self.PreprocessMatrix(matrix)
        RenderSignalFlowGraph(matrix)

    def SolveGraph (self):
        matrix = self.ExtractMatrix()
        matrix = self.PreprocessMatrix(matrix)


        resultRaw = SolveFinalGain(matrix)
        if(resultRaw=="No Path Found"):
            easygui.msgbox("There is No Path", title="No Path Found");
        self.ShowSolved(resultRaw)

    def ShowSolved (self, resultRaw):
        popup = tk.Toplevel(self)
        popup.title('Final Gain')
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(0, weight=1)
        popup.grid_rowconfigure(1, weight=1)

        frameRaw = tk.LabelFrame(popup, text='Raw Form')
        #framePretty = tk.LabelFrame(popup, text='Pretty Form')

        frameRaw.grid(sticky='nsew', padx=10, pady=10)
        frameRaw.grid_columnconfigure(0, weight=1)
        frameRaw.grid_rowconfigure(0, weight=1)
       # framePretty.grid(sticky='nsew', padx=10, pady=10)
       # framePretty.grid_columnconfigure(0, weight=1)
        #framePretty.grid_rowconfigure(0, weight=1)

        labelRaw = tk.Entry(frameRaw, font=monoFont, relief='flat', justify='center')
        labelRaw.insert(0, resultRaw)
        labelRaw.config(state='readonly', readonlybackground='white')
#        labelPretty = tk.Label(framePretty, text=resultPretty, font=monoFont, bg='white')

        labelRaw.grid(sticky='nsew', padx=10, pady=10)
       # labelPretty.grid(sticky='nsew', padx=10, pady=10)

        popup.update_idletasks()
        width, height, posX, posY = ParseWindowGeometry(popup.geometry())
        if width < 200:
            width = 200
        if height < 150:
            height = 150
        posX = (screenWidth-width)//2
        posY = (screenHeight-height)//2
        popup.geometry('{}x{}+{}+{}'.format(width, height, posX, posY))

        popup.focus()
        popup.grab_set()
        self.wait_window(popup)

    def ChangeFontSize (self):
        fontSize = int(self.fontSizeTkStr.get().split()[0])
        defaultFont['size'] = fontSize
        monoFont['size'] = fontSize

        if fontSize < 8:
            optionMenuItemFont['size'] = 8
        elif fontSize < 12:
            optionMenuItemFont['size'] = fontSize
        else:
            optionMenuItemFont['size'] = 12

def ParseWindowGeometry (string):
    temp1 = string.split('+')
    temp2 = temp1[0].split('x')
    return int(temp2[0]), int(temp2[1]), int(temp1[1]), int(temp1[2]) # W,H,X,Y

def CenterifyWindow (toplevelWindow):
    width, height, posX, posY = ParseWindowGeometry(toplevelWindow.geometry())
    posX = (screenWidth-width)//2
    posY = (screenHeight-height)//2
    toplevelWindow.geometry('+{}+{}'.format(posX, posY))


if __name__ == '__main__':
    root = tk.Tk()

    root.withdraw()

    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()

    splashWindow = tk.Toplevel(root)
    splashWindow.withdraw()
    splashWindow.grid_columnconfigure(0, weight=1)
    tk.Label(splashWindow, text=appName+'\n\nLOADING...').grid(sticky='ew', padx=10, pady=15)
    splashWindow.update()
    splashWindow.deiconify()
    CenterifyWindow(splashWindow)
    splashWindow.title('')
    splashWindow.focus()
    splashWindow.grab_set()
    splashWindow.update()

    tempLabel = tk.Label(root, text='Specimen')
    defaultWindowBgColour = tempLabel['background']
    defaultFont = tkFont.Font(font='TkDefaultFont')
    monoFont = tkFont.Font(font='TkFixedFont')
    optionMenuItemFont = tkFont.Font(font='TkDefaultFont')
    tempLabel.destroy()

    root.title(appName)
    root.grid()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    app = App(root, splashWindow)
    root.mainloop()
