import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import random
import time
import accuracy_estimate

# build the window
window = tk.Tk()
window.title("Vision Checker")
window_w = window.winfo_screenwidth()
window_h = window.winfo_screenheight()
window.geometry("%dx%d" % (window_w, window_h))
# window.rowconfigure(1, weight=1)
# window.rowconfigure(2, weight=1)
# window.rowconfigure(3, weight=1)
# window.rowconfigure(4, weight=1)
# window.rowconfigure(5, weight=1)
# window.columnconfigure(1, weight=1)
# window.columnconfigure(2, weight=1)
# window.columnconfigure(3, weight=1)
# window.columnconfigure(4, weight=1)
# window.columnconfigure(5, weight=1)

canvas = tk.Canvas(window, width=window_w, height=window_h)
canvas.grid(column=0, row=0)

# label candidates
pic = ["Up", "Down", "Right", "Left"]
picpos = random.randint(0,3)

# add lights
r = 20
x = int(window_w/2)
y = r + 2
up_light = canvas.create_oval(x-r, y-r, x+r, y+r, fill="")
y = int(window_h*0.85)
down_light = canvas.create_oval(x-r, y-r, x+r, y+r, fill="")
x = int(window_w*0.15)
y = int(window_h/2)
left_light = canvas.create_oval(x-r, y-r, x+r, y+r, fill="")
x = int(window_w*0.85)
right_light = canvas.create_oval(x-r, y-r, x+r, y+r, fill="")

# set the standard
w = 40
h = 40
ratio = [9.0, 4.5, 3.0, 2.25, 1.8, 1.5, 1.29, 1.11, 1.0, 0.9, 0.75, 0.6, 0.45]
level = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0]
pos = 0
reverse = False
jump = 2
correct = 0
wrong = 0

# function for changing candidate
def change(dire):
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

    canvas.update()
    
    if correct >= 3:
        if reverse or pos == 12:
            output = True
        else:
            if wrong > 0 or pos == 11:
                jump = 1
                wrong = 0
            pos += jump
            update_pic_size()
            correct = 0
    elif wrong >= 2:
        if pos == 1 or pos == 0:
            pos = 0
            output = True
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
    reset_light()
    if output:
        output_result()
        return False
    # pick a new picture
    picpos = random.randint(0,3)
    # label.config(image=gifIm[picpos])
    # label.image = gifIm[picpos]
    canvas.itemconfig(label, image=gifIm[picpos])
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


def output_result():
    global window
    for widget in window.winfo_children():
        widget.destroy()
    result_text = tk.Label(
        window, 
        text = "The result is "+str(level[pos]),
        font=("Arial", 50),
        width=20, height=7
        )
    result_text.pack()
    print("The result is", level[pos])

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
# scale_w = 2
# scale_h = 2
# gifUp = gifUp.subsample(scale_w, scale_h)
# gifDown = gifDown.subsample(scale_w, scale_h)
# gifLeft = gifLeft.subsample(scale_w, scale_h)
# gifRight = gifRight.subsample(scale_w, scale_h)

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
label = canvas.create_image(int(window_w/2), int(window_h*0.45), anchor=tk.CENTER, image=gifIm[picpos])

# add text labels
picvar = tk.StringVar()
picvar.set(pic[picpos])
result = canvas.create_text(
    int(window_w*0.85), 
    int(window_h*0.78), 
    text="",
    font=("Arial 25 bold")
    )
# result = tk.Label(
#         window, 
#         text="",
#         font=("Arial", 20),
#         width=10, height=1
#         )
# result.grid(column=3, row=4)

# add buttons
# buttonUp = ttk.Button(window, text="Up", command=lambda:change(0))
# buttonUp.grid(column=3, row=1)
# buttonDown = ttk.Button(window, text="Down", command=lambda:change(1))
# buttonDown.grid(column=3, row=5)
# buttonLeft = ttk.Button(window, text="Left", command=lambda:change(2))
# buttonLeft.grid(column=1, row=3)
# buttonRight = ttk.Button(window, text="Right", command=lambda:change(3))
# buttonRight.grid(column=5, row=3)

def start():
    testing = True
    while True:
        testing = change(time_to_test())

# bind the keyboard
# window.bind("<Up>", lambda event: change(0))
# window.bind("<Down>", lambda event: change(1))
# window.bind("<Left>", lambda event: change(2))
# window.bind("<Right>", lambda event: change(3))
window.bind("<Return>", start)


window.mainloop()
