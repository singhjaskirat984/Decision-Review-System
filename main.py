import tkinter # used For GUI

import cv2 # used to Read the images from Storage

# pip install pillow
import PIL.Image, PIL.ImageTk # after reading images from CV2 we use these to display/pack images in Tkinter GUI

from functools import partial # Partial func is used to disguise a func as non parameterised when it is parameterised 
# i.e command property in button of tkinter library takes only func name in it (eg: command = play) play is a function here
# but we need to give speed variable as argument to play function so we use (command = partial(play, 25)

import threading # mainloop of tkinter GUi will be blocked if we dont use threading

import imutils # to resize the images 

import time # to use time.sleep(1)



#width and height of our main screen
SET_WIDTH = 770
SET_HEIGHT = 433

# capturing video using CV2
stream = cv2.VideoCapture("video.mp4")

flag=True

# speed function to manage the speed of video or see video frames as per our need
def play(speed):
    global flag
    # Reads the Frame on which we are right now talking about this cv2.CAP_PROP_POS_FRAMES
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    # takes the present frame number example 100 and then adds speed value to it i.e if speed is fast fwd i.e 25 then next frame shown will be 125
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1+speed)
    # grabbed is a boolean which grabs the frame and returns true or false acc to it
    grabbed, frame = stream.read() # after setting the stream to our desired frame stream is read once again
    if not grabbed:
        exit()
    # Now these 5 lines are used to display the frame in that video which we want to display
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) 
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    if flag:
        # this is to create blinking effect on screen for decison pending
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
    # 4. Wait for 1.5 second
    # to wait for 1.5 seconds time.sleep func is used to sleep the program for 1.5 sec
    time.sleep(1.5)
    # 5. Display decision image
    if decision=='out':
        # if descision is out it gived out
        frame = cv2.cvtColor(cv2.imread("out.png"), cv2.COLOR_BGR2RGB)
    else:
        # if decision not out it gives not out image
        frame = cv2.cvtColor(cv2.imread("notout.png"), cv2.COLOR_BGR2RGB)
    # after setting frame var acc to image we want i.e out ot not_out we display the image on canvas and these 4 lines are for that purpose
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    # 6. Wait for 1.5 second
    time.sleep(1.5)

def out():
    # used threading and called pending function
    # pending function is called using threading because IN BETWEEN OF VIDEO FRAMES A OUT or NOT-OUT IMAGE HAS
    # HAS TO BE DISPLAYED. IF WE DIPLAY IT WITHOUT USING THREADING IT WILL GO OUT OF LOOP AND APPLICATION WILL END
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()

def not_out():
    # used threading and called pending function
    # pending function is called using threading because IN BETWEEN OF VIDEO FRAMES A OUT or NOT-OUT IMAGE HAS
    # HAS TO BE DISPLAYED. IF WE DIPLAY IT WITHOUT USING THREADING IT WILL GO OUT OF LOOP AND APPLICATION WILL END
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()

#tkinter gui starts here
# window formed
window = tkinter.Tk()
# window title
window.title("Decision Review System")
# reading image using imread and then converting it from BGR format to RGB format using cvtcolor function 
cv_img = cv2.cvtColor(cv2.imread("drs.png"),cv2.COLOR_BGR2RGB)
# packing/displaying image read by cv2 into Tkinter GUi
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

# this is the mainloop for tkinter and we didn't want it to be blocked so we used threading
window.mainloop()
