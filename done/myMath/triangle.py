import tkinter as tk
from PIL import Image, ImageTk
import math as m
root = tk.Tk()
root.title("Triangle Solver")
root.geometry("1200x1000")

image = Image.open("myMath/tri.png")
photo = ImageTk.PhotoImage(image)

label = tk.Label(root, image=photo)
label.place(x=300, y=100)


global hyp_inp, tLeg_inp, bLeg_inp, bAngle_inp, tAngle_inp, hyp_label, tLeg_label, bLeg_label, bAngle_label, tAngle_label
    



hyp_inp = tk.Entry(root, width=7)
tLeg_inp = tk.Entry(root, width=7)
bLeg_inp = tk.Entry(root, width=7)
bAngle_inp = tk.Entry(root, width=7)
tAngle_inp = tk.Entry(root, width=7) 

hyp_inp.place(x=600, y=240)
tLeg_inp.place(x=200, y=300)
bLeg_inp.place(x=580, y=500)
bAngle_inp.place(x=800, y=440)
tAngle_inp.place(x=320, y=170)



round_decimals = 4


hyp_label = tk.Label(root, text="")
tLeg_label = tk.Label(root, text="")
bLeg_label = tk.Label(root, text="")
bAngle_label = tk.Label(root, text="")
tAngle_label = tk.Label(root, text="") 


hyp_label = tk.Label(root, text="")
tLeg_label = tk.Label(root, text="")
bLeg_label = tk.Label(root, text="")
bAngle_label = tk.Label(root, text="")
tAngle_label = tk.Label(root, text="") 

hyp = (hyp_inp.get())
bLeg = (bLeg_inp.get())
tLeg = (tLeg_inp.get())
bAngle = (bAngle_inp.get())
tAngle = (tAngle_inp.get())






def main():
    hyp = (hyp_inp.get())
    bLeg = (bLeg_inp.get())
    tLeg = (tLeg_inp.get())
    bAngle = (bAngle_inp.get())
    tAngle = (tAngle_inp.get())

    if hyp != "":
        hyp = float(hyp)
    else:
        hyp = False

    if bLeg != "":
        bLeg = float(bLeg)
    else:
        bLeg = False
    
    if tLeg != "":
        tLeg = float(tLeg)
    else:
        tLeg = False
    
    if bAngle != "":
        bAngle = float(bAngle)
    else:
        bAngle = False
    
    if tAngle != "":
        tAngle = float(tAngle)
    else:
        tAngle = False


    go_button.destroy()

    hyp_inp.destroy()
    bLeg_inp.destroy()
    tLeg_inp.destroy()
    bAngle_inp.destroy()
    tAngle_inp.destroy()

    if bLeg and tLeg:
        bAngle = round(m.degrees(m.atan(tLeg/bLeg)), round_decimals)
        tAngle = round(90-bAngle, round_decimals)
        hyp = round(m.sqrt(bLeg**2 + tLeg**2), round_decimals)
        print (bAngle) 
        print (tAngle) 
        print(hyp)

    elif hyp and tLeg:
        bLeg = round(m.sqrt(hyp**2 - tLeg**2), round_decimals)
        bAngle = round(m.degrees(m.atan(tLeg/bLeg)), round_decimals)
        tAngle = round(90-bAngle, round_decimals)
        print (bAngle) 
        print (tAngle) 
        print(bLeg)

    elif hyp and bLeg:
        tLeg = round(m.sqrt(hyp**2 - bLeg**2), round_decimals)
        bAngle = round(m.degrees(m.atan(tLeg/bLeg)), round_decimals)
        tAngle = round(90-bAngle, round_decimals)
        print (bAngle) 
        print (tAngle) 
        print(tLeg)

    elif hyp and bAngle:
        tAngle = round(90-bAngle, round_decimals)
        bLeg = round(hyp*(m.cos(m.radians(bAngle))))
        tLeg = round(hyp*(m.cos(m.radians(tAngle))))
        print (bLeg) 
        print (tAngle) 
        print(tLeg)

    elif hyp and tAngle:
        bAngle = round(90-tAngle, round_decimals)
        bLeg = round(hyp*(m.cos(m.radians(bAngle))))
        tLeg = round(hyp*(m.cos(m.radians(tAngle))))
        print (bLeg) 
        print (bAngle) 
        print(tLeg)

    elif bLeg and bAngle:
        tAngle = round(90-bAngle, round_decimals)
        tLeg = round(bLeg*(m.tan(m.radians(bAngle))), round_decimals)
        hyp = round(m.sqrt(tLeg**2 + bLeg**2), round_decimals)
        print(tLeg)
        print(tAngle)
        print(hyp)

    elif bLeg and tAngle:
        bAngle = round(90-tAngle, round_decimals)
        tLeg = round(bLeg*(m.tan(m.radians(bAngle))), round_decimals)
        hyp = round(m.sqrt(tLeg**2 + bLeg**2), round_decimals)
        print(tLeg)
        print(bAngle)
        print(hyp)

    elif tLeg and bAngle:
        tAngle = round(90-bAngle, round_decimals)
        bLeg = round(tLeg*(m.tan(m.radians(tAngle))), round_decimals)
        hyp = round(m.sqrt(tLeg**2 + bLeg**2), round_decimals)
        print(bLeg)
        print(tAngle)
        print(hyp)

    elif tLeg and tAngle:
        bAngle = round(90-tAngle, round_decimals)
        bLeg = round(tLeg*(m.tan(m.radians(tAngle))), round_decimals)
        hyp = round(m.sqrt(tLeg**2 + bLeg**2), round_decimals)
        print(bLeg)
        print(bAngle)
        print(hyp)
    else:
        print("nah bro")


    hyp_label.config(text=hyp)
    bLeg_label.config(text=bLeg)
    tLeg_label.config(text=tLeg)
    bAngle_label.config(text=f"{bAngle}\u00B0")
    tAngle_label.config(text=f"{tAngle}\u00B0")

    hyp_label.place(x=600, y=240)
    tLeg_label.place(x=230, y=300)
    bLeg_label.place(x=580, y=500)
    bAngle_label.place(x=800, y=440)
    tAngle_label.place(x=320, y=170)



go_button = tk.Button(root, text="Go", font=("Arial", 18), command=main)

go_button.place(x=400, y=800)



root.mainloop()