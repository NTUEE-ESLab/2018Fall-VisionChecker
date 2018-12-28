import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import random
import time

# build the window
window = tk.Tk()
window.title("Vision Checker")
window.geometry("%dx%d" % (window.winfo_screenwidth(), window.winfo_screenheight()))
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)
window.rowconfigure(4, weight=1)
window.rowconfigure(5, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=1)
window.columnconfigure(4, weight=1)
window.columnconfigure(5, weight=1)

# label candidates
pic = ["Up", "Down", "Right", "Left"]
picpos = random.randint(0,3)

# function for changing candidate
def change(dire):
    global picpos
    if picpos == dire:
        result.config(text="Correct!", fg="green")
    else: 
        result.config(text="Wrong!", fg="red")
    window.update_idletasks()
    time.sleep(2)
    result.config(text="")
    picpos = random.randint(0,3)
    label.config(image=gifIm[picpos])
    label.image = gifIm[picpos]
    # picvar.set(pic[picpos])

# load the pictures
imUp = Image.open("image/Up_9x9.gif")
imDown = Image.open("image/Down_9x9.gif")
imLeft = Image.open("image/Left_9x9.gif")
imRight = Image.open("image/Right_9x9.gif")
w = 600
h = 600
gifUp = ImageTk.PhotoImage(imUp.resize((w, h), Image.ANTIALIAS))
gifDown = ImageTk.PhotoImage(imDown.resize((w, h), Image.ANTIALIAS))
gifLeft = ImageTk.PhotoImage(imLeft.resize((w, h), Image.ANTIALIAS))
gifRight = ImageTk.PhotoImage(imRight.resize((w, h), Image.ANTIALIAS))
gifIm = [gifUp, gifDown, gifLeft, gifRight]
scale_w = 2
scale_h = 2
# gifUp = gifUp.subsample(scale_w, scale_h)
# gifDown = gifDown.subsample(scale_w, scale_h)
# gifLeft = gifLeft.subsample(scale_w, scale_h)
# gifRight = gifRight.subsample(scale_w, scale_h)

# add the picture
# label = tk.Label(window, image=gifIm[picpos])
label = tk.Label(window, image=gifIm[picpos])
label.image = gifIm[picpos]
label.grid(column=2, row=2, columnspan=3, rowspan=2, sticky="NEWS")

# add text labels
picvar = tk.StringVar()
picvar.set(pic[picpos])
#label = tk.Label(
#        window, 
#        textvariable=picvar, 
#        font=("Arial", 50)
#        )
result = tk.Label(
        window, 
        text="",
        font=("Arial", 20),
        width=10, height=1
        )
result.grid(column=3, row=4)

# add buttons
buttonUp = ttk.Button(window, text="Up", command=lambda:change(0))
buttonUp.grid(column=3, row=1)
buttonDown = ttk.Button(window, text="Down", command=lambda:change(1))
buttonDown.grid(column=3, row=5)
buttonLeft = ttk.Button(window, text="Left", command=lambda:change(2))
buttonLeft.grid(column=1, row=3)
buttonRight = ttk.Button(window, text="Right", command=lambda:change(3))
buttonRight.grid(column=5, row=3)


# bind the keyboard
window.bind("<Up>", lambda event: change(0))
window.bind("<Down>", lambda event: change(1))
window.bind("<Left>", lambda event: change(2))
window.bind("<Right>", lambda event: change(3))

window.mainloop()
