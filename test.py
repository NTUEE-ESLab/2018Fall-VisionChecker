#!/usr/bin/env python
# import matplotlib
# matplotlib.use("Agg")
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import random
import time
# from accuracy_estimate import timeToTest
# from utils import detector_utils as detector_utils
from picamera.array import PiRGBArray
from picamera import PiCamera
from methodHSV import soEasyTest
import cv2
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

video1 = cv2.VideoCapture(0)
#camera = PiCamera()
#camera.resolution = (320, 240)
#camera.framerate = 32
#rawCapture = PiRGBArray(camera)
# detection_graph, sess = detector_utils.load_inference_graph()

# build the window
window = tk.Tk()
window.title("Vision Checker")
window.attributes("-fullscreen", True)
window_w = window.winfo_screenwidth()
window_h = window.winfo_screenheight()
window.geometry("%dx%d" % (window_w, window_h))

canvas = tk.Canvas(window, width=window_w, height=window_h)
canvas.grid(column=0, row=0)


# label candidates
pic = ["Up", "Down", "Right", "Left"]
picpos = random.randint(0,3)

# set the standard
w = 20
h = 20
ratio = [9.0, 4.5, 3.0, 2.25, 1.8, 1.5, 1.29, 1.11, 1.0, 0.9, 0.75, 0.6, 0.45]
level = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0]
delay = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.7, 0.9, 1.1, 1.1, 1.1]
pos = 0
reverse = False
jump = 2
correct = 0
wrong = 0

# add lights
r = 20
x = int(window_w/2)
y = r + 20
up_light = canvas.create_oval(x-r, y-r, x+r, y+r, outline="")
y = int(window_h*0.85)
down_light = canvas.create_oval(x-r, y-r, x+r, y+r, outline="")
x = int(window_w*0.15)
y = int(window_h/2)
left_light = canvas.create_oval(x-r, y-r, x+r, y+r, outline="")
x = int(window_w*0.85)
right_light = canvas.create_oval(x-r, y-r, x+r, y+r, outline="")


# function for changing candidate
def change(dire):
    # print("start change. dire is", dire)
    if dire == 4:
        return True

    global picpos, correct, wrong, pos, reverse, jump
    output = False

    if picpos == dire:
        # result.config(text="Correct!", fg="green")
        canvas.itemconfig(result, text="Correct!", fill="green")
        correct += 1
    else: 
        # result.config(text="Wrong!", fg="red")
        canvas.itemconfig(result, text="Wrong!", fill="red")
        wrong += 1
    change_light(dire)
    # canvas.itemconfig(instruct, text="hand back to the middle")

    canvas.update()
    # print("warning and light loaded.")
    
    if correct >= 3:
        if reverse or pos == 12:
            output = True
        else:
            if pos >= 8:
                jump = 1
            wrong = 0
            pos += jump
            update_pic_size()
            correct = 0
    elif wrong >= 3:
        if pos == 1 or pos == 0:
            pos = 0
            output = True
        else:
            reverse = True
            jump = 1
            pos -= jump
            update_pic_size()
            correct = 0
            wrong = 0
            
    # window.update_idletasks()   # update the warning text
    # time.sleep(2)               # hold for two seconds
    time.sleep(1)               # hold for one seconds
    # result.config(text="")
    canvas.itemconfig(result, text="")
    # canvas.itemconfig(instruct, text="")
    reset_light()
    if output:
        output_result()
        return False

    # pick a new picture
    picpos = random.randint(0,3)
    canvas.itemconfig(label, image=gifIm[picpos])
    canvas.update()
    time.sleep(delay[pos])
    return True

def change_light(dire):
    if dire == 0:
        canvas.itemconfig(up_light, fill="red")
    elif dire == 1:
        canvas.itemconfig(down_light, fill="red")
    elif dire == 2:
        canvas.itemconfig(left_light, fill="red")
    elif dire == 3:
        canvas.itemconfig(right_light, fill="red")

def reset_light():
    canvas.itemconfig(up_light, fill="")
    canvas.itemconfig(down_light, fill="")
    canvas.itemconfig(left_light, fill="")
    canvas.itemconfig(right_light, fill="")


def clear_canvas():
    global canvas, wrong, correct, pos
    canvas.itemconfig(label, image="")
    canvas.itemconfig(up_light, fill="", outline="")
    canvas.itemconfig(down_light, fill="", outline="")
    canvas.itemconfig(left_light, fill="", outline="")
    canvas.itemconfig(right_light, fill="", outline="")
    canvas.itemconfig(result, text="")
    canvas.itemconfig(instruct, text="")

# def output_result():
#     global window
#     for widget in window.winfo_children():
#         widget.destroy()
#     result_text = tk.Label(
#         window, 
#         text = "The result is "+str(level[pos]),
#         font=("Arial", 50),
#         width=20, height=7
#         )
#     result_text.pack()
#     window.update_idletasks()
#     print("The result is", level[pos])
def output_result():
    global canvas, wrong, correct, pos, reverse
    clear_canvas()

    result_text = canvas.create_text(
        int(window_w*0.5), 
        int(window_h*0.45), 
        anchor=tk.CENTER,
        text="The result is " + str(level[pos]),
        font=("Arial 80 bold")
    )
    canvas.update()
    time.sleep(5)
    canvas.delete(result_text)
    
    wrong = 0
    correct = 0
    pos = 0
    reverse = False
    update_pic_size()

    canvas.update()


# load the pictures
imUp = Image.open("image/Up_9x9.gif")
imDown = Image.open("image/Down_9x9.gif")
imLeft = Image.open("image/Left_9x9.gif")
imRight = Image.open("image/Right_9x9.gif")
gifUp = ImageTk.PhotoImage(imUp.resize((int(w * ratio[pos]), int(h * ratio[pos])), Image.ANTIALIAS))
gifDown = ImageTk.PhotoImage(imDown.resize((int(w * ratio[pos]), int(h * ratio[pos])), Image.ANTIALIAS))
gifLeft = ImageTk.PhotoImage(imLeft.resize((int(w * ratio[pos]), int(h * ratio[pos])), Image.ANTIALIAS))
gifRight = ImageTk.PhotoImage(imRight.resize((int(w * ratio[pos]), int(h * ratio[pos])), Image.ANTIALIAS))
gifIm = [gifUp, gifDown, gifLeft, gifRight]
welcome_png = Image.open("image/welcome1.png")
imWelcome = ImageTk.PhotoImage(welcome_png.resize((int(window_w * 0.55), int(window_h * 0.25)), Image.ANTIALIAS))
# scale_w = 2
# scale_h = 2
# gifUp = gifUp.subsample(scale_w, scale_h)
# gifDown = gifDown.subsample(scale_w, scale_h)
# gifLeft = gifLeft.subsample(scale_w, scale_h)
# gifRight = gifRight.subsample(scale_w, scale_h)

welcome = canvas.create_image(
    int(window_w*0.5),
    int(window_h*0.45),
    anchor = tk.CENTER,
    image=imWelcome
)
canvas.update()
time.sleep(3)
canvas.delete(welcome)
canvas.update()
time.sleep(0.5)

start_sign = canvas.create_text(
    int(window_w*0.5), 
    int(window_h*0.45), 
    anchor=tk.CENTER,
    text="Press button to start",
    font=("Arial 60 bold")
)

label = canvas.create_image(int(window_w/2), int(window_h*0.45), anchor=tk.CENTER, image="")
canvas.update()

def update_pic_size():
    # print("update!")
    global gifUp, gifDown, gifLeft, gifRight, gifIm
    gifUp = ImageTk.PhotoImage(imUp.resize((int(w * ratio[pos]), int(h * ratio[pos])), Image.ANTIALIAS))
    gifDown = ImageTk.PhotoImage(imDown.resize((int(w * ratio[pos]), int(h * ratio[pos])), Image.ANTIALIAS))
    gifLeft = ImageTk.PhotoImage(imLeft.resize((int(w * ratio[pos]), int(h * ratio[pos])), Image.ANTIALIAS))
    gifRight = ImageTk.PhotoImage(imRight.resize((int(w * ratio[pos]), int(h * ratio[pos])), Image.ANTIALIAS))
    gifIm = [gifUp, gifDown, gifLeft, gifRight]


# add the picture 
# label = tk.Label(window, image=gifIm[picpos])
# label.image = gifIm[picpos]
# label.grid(column=2, row=2, columnspan=3, rowspan=2, sticky="NEWS")

# add text labels
picvar = tk.StringVar()
picvar.set(pic[picpos])
result = canvas.create_text(
    int(window_w*0.85), 
    int(window_h*0.78), 
    text="",
    font=("Arial 50 bold")
    )
instruct = canvas.create_text(
    int(window_w*0.15), 
    int(window_h*0.78), 
    text="",
    fill="black",
    font=("Arial 18 bold")
)
# result = tk.Label(
#         window, 
#         text="",
#         font=("Arial", 20),
#         width=10, height=1
#         )
# result.grid(column=3, row=4)



def start(ch):
    global canvas, start_sign

    canvas.itemconfig(start_sign, text="Place the red dot right on your chest")

    count = 0
    inter = 0.05

    while count < 5:
        # camera.capture(rawCapture, format="bgr")
        _, frame = video1.read()
        # rawCapture.truncate(0)
        frame = (np.fliplr(frame)).copy()
        h, w, ch = frame.shape
        cv2.circle(
            frame, 
            (w//2, h//2), 
            10,
            (0, 0, 255),
            -1
        )
        cv2.imshow("camera", frame)
        k = cv2.waitKey(5)
        count += inter

    cv2.destroyAllWindows()
    canvas.delete(start_sign)

    canvas.itemconfig(up_light, outline="black")
    canvas.itemconfig(down_light, outline="black")
    canvas.itemconfig(left_light, outline="black")
    canvas.itemconfig(right_light, outline="black")
    canvas.itemconfig(label, image=gifIm[picpos])

    canvas.update()

    res = True
    while(res):
        temp = soEasyTest(video1)
        print("timeTotest is done, the direction is ",temp)
        res = change(temp)
        print(GPIO.input(18))
        if GPIO.input(18)== False:
            clear_canvas()
            break
    
    start_sign = canvas.create_text(
        int(window_w*0.5), 
        int(window_h*0.45), 
        anchor=tk.CENTER,
        text="Press button to start",
        font=("Arial 60 bold")
    )


# bind the keyboard
# window.bind("<Up>", lambda event: change(0))
# window.bind("<Down>", lambda event: change(1))
# window.bind("<Left>", lambda event: change(2))
# window.bind("<Right>", lambda event: change(3))
window.bind("<Return>", lambda event: start(0))
GPIO.add_event_detect(18, GPIO.FALLING, callback=start, bouncetime=500)

window.mainloop()

cv2.destroyAllWindows()
