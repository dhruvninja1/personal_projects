import tkinter as tk
import random
import enchant
dictionary = enchant.Dict("en_Us")
root = tk.Tk()
root.title("Wordle")
root.geometry("700x700")
root.resizable(False, False)

word = "tests"
inputs = []
words_submitted = 0

yellow = "#d19900"
win_label = tk.Label(text=f"You won! The word was {word}", font=("Arial", 16))
lose_label = tk.Label(text=f"You lost. The word was {word}", font=("Arial", 16))
not_a_word_label = tk.Label(text="Not a word!",  font=("Arial", 16))

word_1_letter_1 = tk.StringVar()
word_1_letter_2 = tk.StringVar()
word_1_letter_3 = tk.StringVar()
word_1_letter_4 = tk.StringVar()
word_1_letter_5 = tk.StringVar()

word_2_letter_1 = tk.StringVar()
word_2_letter_2 = tk.StringVar()
word_2_letter_3 = tk.StringVar()
word_2_letter_4 = tk.StringVar()
word_2_letter_5 = tk.StringVar()

word_3_letter_1 = tk.StringVar()
word_3_letter_2 = tk.StringVar()
word_3_letter_3 = tk.StringVar()
word_3_letter_4 = tk.StringVar()
word_3_letter_5 = tk.StringVar()

word_4_letter_1 = tk.StringVar()
word_4_letter_2 = tk.StringVar()
word_4_letter_3 = tk.StringVar()
word_4_letter_4 = tk.StringVar()
word_4_letter_5 = tk.StringVar()

word_5_letter_1 = tk.StringVar()
word_5_letter_2 = tk.StringVar()
word_5_letter_3 = tk.StringVar()
word_5_letter_4 = tk.StringVar()
word_5_letter_5 = tk.StringVar()

word_6_letter_1 = tk.StringVar()
word_6_letter_2 = tk.StringVar()
word_6_letter_3 = tk.StringVar()
word_6_letter_4 = tk.StringVar()
word_6_letter_5 = tk.StringVar()

word_1_letter_1.set("_")
word_1_letter_2.set("_")
word_1_letter_3.set("_")
word_1_letter_4.set("_")
word_1_letter_5.set("_")

word_2_letter_1.set("_")
word_2_letter_2.set("_")
word_2_letter_3.set("_")
word_2_letter_4.set("_")
word_2_letter_5.set("_")

word_3_letter_1.set("_")
word_3_letter_2.set("_")
word_3_letter_3.set("_")
word_3_letter_4.set("_")
word_3_letter_5.set("_")

word_4_letter_1.set("_")
word_4_letter_2.set("_")
word_4_letter_3.set("_")
word_4_letter_4.set("_")
word_4_letter_5.set("_")

word_5_letter_1.set("_")
word_5_letter_2.set("_")
word_5_letter_3.set("_")
word_5_letter_4.set("_")
word_5_letter_5.set("_")

word_6_letter_1.set("_")
word_6_letter_2.set("_")
word_6_letter_3.set("_")
word_6_letter_4.set("_")
word_6_letter_5.set("_")



word_1_letters = [word_1_letter_1, word_1_letter_2, word_1_letter_3, word_1_letter_4, word_1_letter_5]
word_2_letters = [word_2_letter_1, word_2_letter_2, word_2_letter_3, word_2_letter_4, word_2_letter_5]
word_3_letters = [word_3_letter_1, word_3_letter_2, word_3_letter_3, word_3_letter_4, word_3_letter_5]
word_4_letters = [word_4_letter_1, word_4_letter_2, word_4_letter_3, word_4_letter_4, word_4_letter_5]
word_5_letters = [word_5_letter_1, word_5_letter_2, word_5_letter_3, word_5_letter_4, word_5_letter_5]
word_6_letters = [word_6_letter_1, word_6_letter_2, word_6_letter_3, word_6_letter_4, word_6_letter_5]

all_word_letters = [word_1_letters, word_2_letters, word_3_letters, word_4_letters, word_5_letters, word_6_letters]


word_1_letter_1_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_1_letter_1)
word_1_letter_2_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_1_letter_2)
word_1_letter_3_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_1_letter_3)
word_1_letter_4_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_1_letter_4)
word_1_letter_5_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_1_letter_5)


word_2_letter_1_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_2_letter_1)
word_2_letter_2_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_2_letter_2)
word_2_letter_3_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_2_letter_3)
word_2_letter_4_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_2_letter_4)
word_2_letter_5_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_2_letter_5)


word_3_letter_1_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_3_letter_1)
word_3_letter_2_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_3_letter_2)
word_3_letter_3_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_3_letter_3)
word_3_letter_4_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_3_letter_4)
word_3_letter_5_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_3_letter_5)


word_4_letter_1_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_4_letter_1)
word_4_letter_2_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_4_letter_2)
word_4_letter_3_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_4_letter_3)
word_4_letter_4_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_4_letter_4)
word_4_letter_5_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_4_letter_5)


word_5_letter_1_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_5_letter_1)
word_5_letter_2_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_5_letter_2)
word_5_letter_3_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_5_letter_3)
word_5_letter_4_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_5_letter_4)
word_5_letter_5_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_5_letter_5)


word_6_letter_1_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_6_letter_1)
word_6_letter_2_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_6_letter_2)
word_6_letter_3_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_6_letter_3)
word_6_letter_4_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_6_letter_4)
word_6_letter_5_label = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=word_6_letter_5)


word_1_letter_labels = [word_1_letter_1_label, word_1_letter_2_label, word_1_letter_3_label, word_1_letter_4_label, word_1_letter_5_label]
word_2_letter_labels = [word_2_letter_1_label, word_2_letter_2_label, word_2_letter_3_label, word_2_letter_4_label, word_2_letter_5_label]
word_3_letter_labels = [word_3_letter_1_label, word_3_letter_2_label, word_3_letter_3_label, word_3_letter_4_label, word_3_letter_5_label]
word_4_letter_labels = [word_4_letter_1_label, word_4_letter_2_label, word_4_letter_3_label, word_4_letter_4_label, word_4_letter_5_label]
word_5_letter_labels = [word_5_letter_1_label, word_5_letter_2_label, word_5_letter_3_label, word_5_letter_4_label, word_5_letter_5_label]
word_6_letter_labels = [word_6_letter_1_label, word_6_letter_2_label, word_6_letter_3_label, word_6_letter_4_label, word_6_letter_5_label]

all_words_labels = [word_1_letter_labels, word_2_letter_labels, word_3_letter_labels, word_4_letter_labels, word_5_letter_labels, word_6_letter_labels]

def submit():
    global inputs
    global words_submitted
    global all_word_letters
    global all_words_labels
    global word
    global win_label
    global lose_label
    global not_a_word_label
    correct = True
    input = entry.get()
    if len(input) == 5:
        if dictionary.check(input):
            not_a_word_label.config(text="")
            entry.delete("0", tk.END)
            inputs.append(input)

            print(inputs)
            for x in range(0, 5):
                all_word_letters[words_submitted][x].set(input[x])

            word_counts = {}
            for char in word:
                word_counts[char] = word_counts.get(char, 0) + 1

            for x in range(0, 5):
                if all_word_letters[words_submitted][x].get() == word[x]:
                    all_words_labels[words_submitted][x].config(bg="green")
                    word_counts[all_word_letters[words_submitted][x].get()] -= 1
                elif all_word_letters[words_submitted][x].get() in word:
                    correct = False
                    if word_counts.get(all_word_letters[words_submitted][x].get(), 0) > 0:
                        [words_submitted][x].config(bg=yellow)
                        word_counts[all_word_letters[words_submitted][x].get()] -= 1
                    else:
                        all_words_labels[words_submitted][x].config(bg="black")
                else:
                    all_words_labels[words_submitted][x].config(bg="black")
                    correct = False

            words_submitted += 1
            if correct:
                win_label.grid(column=6, row=1)
            elif words_submitted >= 6:
                lose_label.grid(column=6, row=1)
        else:
            entry.delete("0", tk.END)
            not_a_word_label.config(text="Not a word!")
            not_a_word_label.grid(column=6, row=2)
    else:
        not_a_word_label.config(text="Word too short!")
        not_a_word_label.grid(column=6, row=2)

    
entry = tk.Entry()
entry.grid(column = 6, row = 0)
submit = tk.Button(text="Submit", command=submit)
submit.grid(column = 7, row = 0)


for x in range(0, 6):
    for y in range(0, 5):
        all_words_labels[x][y].grid(row = x, column = y)


root.mainloop()