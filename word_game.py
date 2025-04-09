import tkinter as tk
import random
from functools import partial
root = tk.Tk()
root.title("Word game")
root.geometry("700x700")
root.resizable(False, False)

words_submitted = []
score = 0

abcs = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()

letter1 = abcs[random.randint(0, 25)]
letter2 = abcs[random.randint(0, 25)]
letter3 = abcs[random.randint(0, 25)]
letter4 = abcs[random.randint(0, 25)]
letter5 = abcs[random.randint(0, 25)]
letter6 = abcs[random.randint(0, 25)]
letter7 = abcs[random.randint(0, 25)]
letter8 = abcs[random.randint(0, 25)]
letter9 = abcs[random.randint(0, 25)]

word_label_strinvar = tk.StringVar()
word_label_strinvar.set("")
word_label_var = []

def letter_click(letter, number):
    word_label_var.append("f")
    print(word_label_var)



letter1_button = tk.Button(text=letter1, font=("Arial", 16), fg="black", command=partial(letter_click, letter1, 1))
letter2_button = tk.Button(text=letter2, font=("Arial", 16), fg="black", command=partial(letter_click, letter2, 2))
letter3_button = tk.Button(text=letter3, font=("Arial", 16), fg="black", command=partial(letter_click, letter3, 3))
letter4_button = tk.Button(text=letter4, font=("Arial", 16), fg="black", command=partial(letter_click, letter4, 4))
letter5_button = tk.Button(text=letter5, font=("Arial", 16), fg="black", command=partial(letter_click, letter5, 5))
letter6_button = tk.Button(text=letter6, font=("Arial", 16), fg="black", command=partial(letter_click, letter6, 6))
letter7_button = tk.Button(text=letter7, font=("Arial", 16), fg="black", command=partial(letter_click, letter7, 7))
letter8_button = tk.Button(text=letter8, font=("Arial", 16), fg="black", command=partial(letter_click, letter8, 8))
letter9_button = tk.Button(text=letter9, font=("Arial", 16), fg="black", command=partial(letter_click, letter9, 9))

letter1_button.pack()

word_label=tk.Label(textvariable=word_label_strinvar)



root.mainloop()