import asyncio
import shutil
from tkinter import *
import tkinter.filedialog as fdialog
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showwarning, OK

import cv2
import os
from PIL import ImageTk
from PIL.Image import ANTIALIAS
from pilkit.processors import resize
from scipy.misc import toimage

from main import draw_counter


class Gui():
    HEIGHT = 800
    WIDTH = 600
    factor_zoom = 1

    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Просмотр изображений")
        self.create_view()

    def show_wait_dialog(self):
        self.top = Toplevel(self.root)

        Label(self.top, text="Ждите, идет обработка контуров...").pack()

    def scale(self, arg):
        if arg.num == 1:
            self.factor_zoom -= 0.1
        old_pick = self.orig
        # pil_image.resize((width, height), Image.ANTIALIAS)
        # self.orig = ImageTk.PhotoImage(
        #     ImageTk.Image.Image.resize(ImageTk.Image.open('test.png'), size=(int (old_pick.height()*self.factor_zoom), int(old_pick.width()*self.factor_zoom)) ))
        process = resize.ResizeToFit(int(old_pick.height() * self.factor_zoom),
                                     int(old_pick.width() * self.factor_zoom), ANTIALIAS)
        self.orig = process.process(ImageTk.Image.open('no_image.png'))
        self.orig.save('no_image.png')

        custom_img = ImageTk.PhotoImage(
            ImageTk.Image.Image.resize(ImageTk.Image.open('no_image.png')))

        self.original_img_label.configure(image=custom_img)
        self.original_img_label.image = custom_img

        print(arg)

    def generate_counter(self):
        self.show_wait_dialog()
        self.root.update()
        try:
            draw_counter(self.fname, (int(self.spinner.get())), self.color[0])
        except Exception as e:
            try:
                os.remove('final.jpg')
            except:
                pass
            print(e)
        finally:
            self.top.destroy()

        custom_img = ImageTk.PhotoImage(
            ImageTk.Image.Image.resize(ImageTk.Image.open('final.jpg'), size=(self.HEIGHT, self.WIDTH)))
        self.custom_img.configure(image=custom_img)
        self.custom_img.image = custom_img
        os.remove('final.jpg')

    #
    def load_file(self):
        self.orig = ImageTk.PhotoImage(
            ImageTk.Image.Image.resize(ImageTk.Image.open(self.fname), size=(self.HEIGHT, self.WIDTH)))
        self.original_img_label.configure(image=self.orig)
        self.original_img_label.image = self.orig

    def color_palette(self):
        self.color = askcolor(color="#AAA",
                              title="Цвет")

    def create_view(self):
        self.generate = Button(text="Сгенерировать", command=self.generate_counter)
        self.choose_pic = Button(text="Выбрать картинку", command=self.logic)
        self.choose_color = Button(text="Выбрать цвет", command=self.color_palette)

        var = StringVar()
        var.set("50")
        self.spinner = Spinbox(from_=1, to=200, textvariable=var, increment=10)

        self.generate.grid(row=1, column=3)
        self.choose_pic.grid(row=2, column=3)
        self.choose_color.grid(row=3, column=3)
        self.spinner.grid(row=4, column=3)
        # self.spinner.config(width=100)

        self.orig = ImageTk.PhotoImage(
            ImageTk.Image.Image.resize(ImageTk.Image.open('no_image.png'), size=(self.HEIGHT, self.WIDTH)))
        self.custom = ImageTk.PhotoImage(
            ImageTk.Image.Image.resize(ImageTk.Image.open('no_image.png'), size=(self.HEIGHT, self.WIDTH)))
        self.original_img_label = Label(self.root, image=self.orig)

        self.custom_img = Label(self.root, image=self.custom)

        self.original_img_label.grid(row=1, column=1)
        self.custom_img.grid(row=1, column=2)

    def logic(self):
        self.fname = fdialog.askopenfilename(filetypes=(("Выбор картинки...", "*.png"),
                                                        ("Картинки", "*.jpeg;*.jpg"),
                                                        ("Все файлы...", "*.*")))
        self.load_file()


gui = Gui()
gui.root.mainloop()
