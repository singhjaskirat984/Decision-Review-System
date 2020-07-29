import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
import time




#width and height of our main screen
SET_WIDTH = 770
SET_HEIGHT = 433

stream = cv2.VideoCapture("video.mp4")
flag=True
def play(speed):
    global flag
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1+speed)
    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(170,25, fill="white", font="Times 27 italic bold", text="Decision Pending")
    flag = not flag

def pending(decision):
    # 1. Display decision pending image
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    # 2. Wait for a second
    time.sleep(1)
    # # 3. Display sponsor image
    # frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    # frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    # frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    # canvas.image = frame
    # canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    # 4. Wait for 1.5 second
    time.sleep(1.5)
    # 5. Display decision image
    if decision=='out':
        frame = cv2.cvtColor(cv2.imread("out.png"), cv2.COLOR_BGR2RGB)
    else:
        frame = cv2.cvtColor(cv2.imread("notout.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    # 6. Wait for 1.5 second
    time.sleep(1.5)

def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()

def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()

#tkinter gui starts here
window = tkinter.Tk()
window.title("Decision Review System")
cv_img = cv2.cvtColor(cv2.imread("drs.png"),cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0,0, anchor= tkinter.NW, image=photo)
canvas.pack()


#buttons to control playback
btn = tkinter.Button(window, text="<< Previous (fast)", width=50,command=partial(play,-25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (slow)", width=50,command=partial(play,-2))
btn.pack()

btn = tkinter.Button(window, text="Forward (fast) >>", width=50,command=partial(play,25))
btn.pack()

btn = tkinter.Button(window, text="Forward (slow) >>", width=50, command=partial(play,2))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out", width=50, command=not_out)
btn.pack()

window.mainloop()