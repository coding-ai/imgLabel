from tkinter import *
from PIL import ImageTk, Image
import os
import pandas as pd

class ImgLabel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent=None)
        self.img_path = 'images'
        self.img_list = []
        self.filename = []
        self.width = 800
        self.height = 600

        self.user_input = StringVar()
        self.class_name = []
        self.xmin = []
        self.ymin = []
        self.xmax = []
        self.ymax = []

        self.x = self.y = 0
        self.canvas = Canvas(self)
        self.canvas.config(width=900, height=700)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.rect = None

        self.start_x = None
        self.start_y = None

        for img in os.listdir(self.img_path):
            self.img_list.append(ImageTk.PhotoImage(Image.open(os.path.join(self.img_path,img)).resize((800,600),Image.ANTIALIAS)))
            self.filename.append(img)

        self.status = Label(root, text="Image 1 of " + str(len(self.img_list)), bd=1, relief=SUNKEN, anchor=E)

        # self.img_label = Label(image=self.img_list[0])
        self.canvas.create_image(50,50,anchor=NW,image=self.img_list[0])

        self.button_back = Button(root, text="<<", command=self.back, state=DISABLED)
        self.button_exit = Button(root, text="Exit Program", command=root.quit)
        self.button_forward = Button(root, text=">>", command=lambda: self.forward(2))

        self.run()

    def forget(self):

        self.canvas.create_image(50,50,anchor=NW,image='')
        self.canvas.pack_forget()
        self.button_forward.pack_forget()
        self.status.pack_forget()
        self.button_back.pack_forget()
    
    def forward(self, image_number):
        
        self.forget()

        self.canvas = Canvas(self)
        self.canvas.config(width=900, height=700)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.rect = None

        self.start_x = None
        self.start_y = None

        self.curX = None
        self.curY = None

        self.canvas.create_image(50,50,anchor=NW,image=self.img_list[image_number-1])
        # self.img_label.grid_forget()
        # self.img_label = Label(image=self.img_list[image_number-1])
        # self.canvas.create_image(0,0,anchor="nw",image=self.img_label)
        self.button_forward = Button(root, text=">>", command=lambda: self.forward(image_number+1))
        self.button_back = Button(root, text="<<", command=lambda: self.back(image_number-1))

        if image_number == (len(self.img_list)):
            self.button_forward = Button(root, text=">>", state=DISABLED)

        # self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        # self.canvas.bind("<B1-Motion>", self.on_move_press)
        # self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.status = Label(root, text="Image " + str(image_number) + " of " + str(len(self.img_list)), bd=1, relief=SUNKEN, anchor=E)

        self.run()

        self.make_csv()

    def back(self, image_number):
        
        # self.img_label.grid_forget()
        # self.img_label = Label(image=self.img_list[image_number-1])
        # self.canvas.create_image(0,0,anchor="nw",image=self.img_label)

        self.forget()

        self.canvas = Canvas(self)
        self.canvas.config(width=900, height=700)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Double-Button-1>", self.make_csv)

        self.rect = None

        self.start_x = None
        self.start_y = None

        self.canvas.create_image(50,50,anchor=NW,image=self.img_list[image_number-1])
        self.button_forward = Button(root, text=">>", command=lambda: self.forward(image_number+1))
        self.button_back = Button(root, text="<<", command=lambda: self.back(image_number-1))

        if image_number == 1:
            self.button_back = Button(root, text="<<", state=DISABLED)


        # self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        # self.canvas.bind("<B1-Motion>", self.on_move_press)
        # self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.status = Label(root, text="Image " + str(image_number) + " of " + str(len(self.img_list)), bd=1, relief=SUNKEN, anchor=E)

        self.run()

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red')

    def on_move_press(self, event):
        self.curX = self.canvas.canvasx(event.x)
        self.curY = self.canvas.canvasy(event.y)

        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if event.x > 0.9*w:
            self.canvas.xview_scroll(1, 'units')
        elif event.x < 0.1*w:
            self.canvas.xview_scroll(-1, 'units')
        if event.y > 0.9*h:
            self.canvas.yview_scroll(1, 'units')
        elif event.y < 0.1*h:
            self.canvas.yview_scroll(-1, 'units')

        self.canvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def get_text(self,event=None):
        self.class_name.append(self.user_input.get())

    def on_button_release(self, event):

        self.entry = Entry(root, textvariable=self.user_input)
        self.canvas.create_window(450,680,window=self.entry)
        self.canvas.bind("<Return>",self.get_text())
        self.xmin.append(self.start_x-50)
        self.ymin.append(self.start_y-50)
        self.xmax.append(self.curX-50)
        self.ymax.append(self.curY-50)

    def run(self):

        self.canvas.grid(row=0, column=0)
        self.button_back.pack(anchor=W,side=BOTTOM)
        self.button_exit.pack(anchor=CENTER,side=BOTTOM)
        self.button_forward.pack(anchor=E,side=BOTTOM)
        self.status.pack(anchor=CENTER,side=BOTTOM)

    def make_csv(self):
        print(self.width, self.height, self.class_name, self.xmin, self.ymin, self.xmax, self.ymax)


if __name__ == "__main__":
    root = Tk()
    root.resizable(False,False)
    app = ImgLabel(root)
    app.pack()
    root.title('Image Labeler Tool')
    root.mainloop()