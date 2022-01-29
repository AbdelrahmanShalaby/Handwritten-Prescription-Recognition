from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk
import cv2 as cv
import os
import glob
#import test


class ScrolledCanvas(Frame):

    cnt=0
    def Select_Image_Display_It(self):
        # global Filename
        self.Filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.img = cv.cvtColor(cv.imread(self.Filename), cv.COLOR_BGR2RGB)
        width, height, channals = self.img.shape
        self.canv.config(width=1300, height=700, scrollregion=(0, 0, height, width), highlightthickness=0)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.img))

        self.imgtag = self.canv.create_image(0, 0, anchor="nw", image=self.photo)

    def Perform(self):
        import test
        f = open("decoded.txt", "r")

        res = f.read()

        lines = res.split("\n")
        #print(lines)
        for line in lines:
            self.T.insert(END, line+'\n')
        #exit()

    def __init__(self, parent=None):
          #self.Filename=""
          Frame.__init__(self, parent)
          self.master.title("Prescription Recognition")
          self.master.configure(background='gray')
          # w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
          # self.master.geometry("%dx%d+0+0" % (w, h))
          open('D:/Important Files/Graduation Project/Proto/samples/Testing_List', 'w').close()
          files = glob.glob("D:/Important Files/Graduation Project/Proto/samples/Images/000033/Testing/*")
          for f in files:
              os.remove(f)
          self.pack()
          self.canv = Canvas(self.master, relief=SUNKEN)
          self.B2 = Button(self.master, text="Run", command=self.Perform)
          # self.B.place(x=0, y=0)
          self.B2.pack(side=BOTTOM)
          self.B = Button(self.master, text="Browse", command=self.Select_Image_Display_It)
          #self.B.place(x=0, y=0)
          self.B.pack(side=BOTTOM)


          self.T = Text(self.master, height=10, width=200)
          self.T.pack(side=BOTTOM)
          #self.T.place(x=0,y=200)

          self.sbarV = Scrollbar(self.master, orient=VERTICAL)
          self.sbarH = Scrollbar(self.master, orient=HORIZONTAL)

          self.sbarV.config(command=self.canv.yview)
          self.sbarH.config(command=self.canv.xview)

          self.canv.config(yscrollcommand=self.sbarV.set)
          self.canv.config(xscrollcommand=self.sbarH.set)

          self.sbarV.pack(side=RIGHT, fill=Y)
          self.sbarH.pack(side=BOTTOM, fill=X)

          self.canv.pack(side=LEFT,expand=YES,fill=BOTH)
          # self.im=Image.open("003.jpg")
          # width,height=self.im.size
          #self.canv.config(scrollregion=(0,0,width,height))
          #self.im2=ImageTk.PhotoImage(self.img)

    def getpoint1(self,event):
        global x, y
        XX = self.canv.canvasx(event.x)
        YY = self.canv.canvasy(event.y)

        print("X_New, Y_New: ",XX,YY)
        x, y = XX, YY
        x2 = x - 5
        y2 = y - 5
        self.id2=self.canv.create_oval(x, y, x2, y2, fill='red')
        print("X,Y: ", x, y)


    def getpoint2(self,event):
        global x1, y1
        XX = self.canv.canvasx(event.x)
        YY = self.canv.canvasy(event.y)
        x1, y1 = XX, YY
        x2 = x1 + 5
        y2 = y1 + 5
        self.id3=self.canv.create_oval(x1, y1, x2, y2, fill='green')
        print("X1,Y1: ", x1, y1)

    def drawline(self,event):
        self.id1=self.canv.create_rectangle(x, y, x1, y1)
        # get the points and crop from original image
        # 7awl t-display el sora bdl el sora el kbera
        # save el sora b-name
        XX=int(x)
        YY=int(y)
        XX1=int(x1)
        YY1=int(y1)
        print(XX,YY,XX1,YY1)
        self.cropped = self.img[YY:YY1, XX:XX1]
        self.cropped=cv.cvtColor(self.cropped, cv.COLOR_BGR2RGB)
        img_name="TestImage"
        self.cnt+=1
        img_name+=str(self.cnt)
        path="D:/Important Files/Graduation Project/Proto/samples/Images/000033/Testing"
        cv.imwrite(path+"/"+img_name+".jpg",self.cropped)

        f = open("D:/Important Files/Graduation Project/Proto/samples/Testing_List", "a")
        f.writelines(img_name+"\n")
        f.close()
        height, width, no_channels = self.cropped.shape
        #self.canvas = tk.Canvas(self.window, width=width, height=height)
        #self.canvas.pack()
        self.cropped = cv.cvtColor(self.cropped, cv.COLOR_RGB2BGR)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.cropped))
        self.canv.create_image(0,0, image=self.photo,anchor="nw")
        self.canv.after(1, self.canv.delete, self.id1)
        self.canv.after(1, self.canv.delete, self.id2)
        self.canv.after(1, self.canv.delete, self.id3)



Prog=ScrolledCanvas()

Prog.master.bind('q', Prog.getpoint1)
Prog.master.bind('w', Prog.getpoint2)
Prog.master.bind('f', Prog.drawline)
#
# ScrolledCanvas.canv.bind('q', ScrolledCanvas.getpoint1)
# ScrolledCanvas.canv.bind('w', ScrolledCanvas.getpoint2)
# ScrolledCanvas.canv.bind('<Button-1>', ScrolledCanvas.drawline)
# ScrolledCanvas().mainloop()
mainloop()