# import time
import tkinter as tk
import os
from tkinter import filedialog, ttk
from tkinter import *
from tkinter import font
from PIL import ImageTk

root = tk.Tk()
root.title("Escape Traffic")
root.iconbitmap('icon.ico')
streets = ["university","airport","swaileh","jordan","yarmouk","autostrad","mecca","gardens","abu-nusair","almadena","alsaada"]

# background image
bgc = ImageTk.PhotoImage(file='data/aaa.png')
canvas = Canvas(root, width=600, height=500)
bg_label = Label(root, image=bgc)
bg_label.place(x=0,y=0,relheight=1,relwidth=1)

# color tuples
Font_tuple = ("Comic Sans MS", 20, "bold")
Font_tuple2 = ("Comic Sans MS", 10, "bold")

# street selections
selection = "university"

# dropdown list for streets
def selected(event):
    global selection
    selection = clicked.get()

    top = Toplevel()
    ll1 = Label(top, text="Successfully saved")
    ll1.pack()
    # time.sleep(3)
    # top.destroy()

l1 = Label(root, text="Streets:", font=("Comic Sans MS", 13, "bold"), fg="white", bg="#0A1931")
l1.place(x=200,y=75)

clicked = StringVar()
clicked.set(streets[0])

ddl = OptionMenu(root, clicked, *streets,command=selected)
ddl.place(x=320,y=75)

# new_button = Button(root, text="Select", command=selected, font=Font_tuple2,width=5, fg='white', bg="#263D42")
# new_button.place(x=380,y=75)

# end of dropdown list


def video_detect():
    filename = filedialog.askopenfilename(
        initialdir="/", title="Select file",filetypes=(("video", "*.mp4;*.avi;*.amv;*.flv;*.mkv;*.webm"),("all files", "*.*")))
    if filename:
        os.system('cmd /c "python detect_video.py --street {} --video {}"'.format(selection,filename))

def image_detect():
    filename = filedialog.askopenfilename(
        initialdir="/", title="Select file",filetypes=(("Photos", "*.PNG;*JPEG;*.JPG;*.WeBP,*.BMP,*.SVG"),("all files", "*.*")))
    if filename:
        os.system('cmd /c "python detect.py --images {}"'.format(filename))

def webcam_detect():
    os.system('cmd /c "python detect_video.py --street {} --video 0"'.format(selection))
def external_detect():
    os.system('cmd /c "python detect_video.py --street {} --video 1"'.format(selection))

def image_detect_and_save():
    filename = filedialog.askopenfilename(
        initialdir="/", title="Select Image",filetypes=(("Photos", "*.PNG;*JPEG;*.JPG;*.WeBP,*.BMP,*.SVG"),("all files", "*.*")))
    if filename:
        save_spot = filedialog.askdirectory(
            initialdir="/", title="Select where to save")
        if save_spot:
            os.system('cmd /c "python detect.py --images {} --output {}/"'.format(filename,save_spot))

def video_detect_and_save():
    filename = filedialog.askopenfilename(
        initialdir="/", title="Select Video",filetypes=(("video", "*.mp4;*.avi;*.amv;*.flv;*.mkv;*.webm"),("all files", "*.*")))
    if filename:
        save_spot = filedialog.askdirectory(
            initialdir="/", title="Select where to save")
        if save_spot:
            os.system('cmd /c "python detect_video.py --street {} --video {} --output {}/a.avi"'.format(selection,filename,save_spot))

def webcam_detect_and_save():
    save_spot = filedialog.askdirectory(
        initialdir="/", title="Select where to save")
    if save_spot:
        os.system('cmd /c "python detect_video.py --street {} --video 0 --output {}/saved.avi"'.format(selection,save_spot))
def external_detect_and_save():
    save_spot = filedialog.askdirectory(
        initialdir="/", title="Select where to save")
    if save_spot:
        os.system('cmd /c "python detect_video.py --street {} --video 1 --output {}/saved.avi"'.format(selection,save_spot))

# for hover effects

def on_enter(e):
    e.widget['background'] = 'green'

def on_leave(e):
    e.widget['background'] = '#263D42'





#bg image
# bg_image = Image.open('C:\\Users\\STUDENT\\Desktop\\project\\data\\aaa.png')
# bgc = ImageTk.PhotoImage(file="data/aaa.jpg")
# bgc = PhotoImage(file="data/aaa.png")
# bgc = PhotoImage(file="C:\\Users\\STUDENT\\Desktop\\project\\data\\aaa.png")
# bgc = PhotoImage(file="C://Users//STUDENT//Desktop//project//data//aaa.png")
# bgc = open("C:\Users\STUDENT\Desktop\Escape-traffic\data\aaa.png")


# canvas.place(x=0, y=0, relheight=1, relwidth=1)
# canvas.create_image(0, 0, image=bgc, anchor="nw")
# root.configure(bg="#fff5de")


# ddl = ttk.Combobox(root, value = streets, width=10)
# ddl.place(x=410,y=50)
# ddl.current(0)


# for images detections
root.geometry('600x475')
root.resizable(False,False)
title = tk.Label(root, text = "Escape Traffic", font=Font_tuple, bg="#0A1931", fg="white")
title.place(x=210,y=0)


# for images
detect_images = tk.Button(root, text="Image Detection", width=25, padx = 10,font=Font_tuple2,
                     pady=10, fg='white', bg="#263D42", command=image_detect)
detect_images.place(x=50,y=150)

# for images and save
detect_image_and_save = tk.Button(root, text="Image Detection & Save", width=25, padx = 10,font=Font_tuple2,
                     pady=10, fg='white', bg="#263D42", command=image_detect_and_save)
detect_image_and_save.place(x=320,y=150)

# for videos detections
detect_video = tk.Button(root, text="Video Detection", width=25, padx = 10,font=Font_tuple2,
                     pady=10, fg='white', bg="#263D42", command=video_detect)
detect_video.place(x=50,y=225)


# for videos and save
detect_video_and_save = tk.Button(root, text="Video Detection & Save", width=25, padx = 10,font=Font_tuple2,
                     pady=10, fg='white', bg="#263D42", command=video_detect_and_save)
detect_video_and_save.place(x=320,y=225)


# for webcam detections
detect_webcam = tk.Button(root, text="Webcam Detection", width=25, padx = 10,font=Font_tuple2,
                     pady=10, fg='white', bg="#263D42", command=webcam_detect)
detect_webcam.place(x=50,y=300)


# for webcam and save
detect_webcam_and_save = tk.Button(root, text="Webcam Detection & Save", width=25, padx = 10,font=Font_tuple2,
                     pady=10, fg='white', bg="#263D42", command=webcam_detect_and_save)
detect_webcam_and_save.place(x=320,y=300)


# for External Cameras
detect_external = tk.Button(root, text="External Camera Detection", width=25, padx = 10,font=Font_tuple2,
                     pady=10, fg='white', bg="#263D42", command=external_detect)
detect_external.place(x=50,y=375)


# for External Cameras and save
detect_external_and_save = tk.Button(root, text="External Camera Detection & Save", width=25, padx = 10,font=Font_tuple2,
                     pady=10, fg='white', bg="#263D42", command=external_detect_and_save)
detect_external_and_save.place(x=320,y=375)




# for hover effect
detect_images.bind("<Enter>", on_enter)
detect_images.bind("<Leave>", on_leave)
detect_image_and_save.bind("<Enter>", on_enter)
detect_image_and_save.bind("<Leave>", on_leave)
detect_video.bind("<Enter>", on_enter)
detect_video.bind("<Leave>", on_leave)
detect_video_and_save.bind("<Enter>", on_enter)
detect_video_and_save.bind("<Leave>", on_leave)
detect_webcam.bind("<Enter>", on_enter)
detect_webcam.bind("<Leave>", on_leave)
detect_webcam_and_save.bind("<Enter>", on_enter)
detect_webcam_and_save.bind("<Leave>", on_leave)
detect_external.bind("<Enter>", on_enter)
detect_external.bind("<Leave>", on_leave)
detect_external_and_save.bind("<Enter>", on_enter)
detect_external_and_save.bind("<Leave>", on_leave)





root.mainloop()