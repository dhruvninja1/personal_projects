import tkinter as tk
import random
import enchant
from assets.variables_for_wordle import *
import json




dictionary = enchant.Dict("en_Us")
root = tk.Tk()
root.title("Wordle")
root.geometry("700x700")
root.resizable(False, False)

variable = random.randint(0, len(words)-1)
word = words[variable]
print(word)
inputs = []
words_submitted = 0

yellow = "#d19900"

with open("wordle/wordle_data.json", "r") as f:
    stats = json.load(f)

stats_stringvar = tk.StringVar()
stats_stringvar.set(f"Wins: {stats["wins"]} \n Losses: {stats["losses"]} \n Wins on word 1: {stats["wins_on_1"]} \n Wins on word 2: {stats["wins_on_2"]} \n Wins on word 3: {stats["wins_on_3"]} \n Wins on word 4: {stats["wins_on_4"]} \n Wins on word 5: {stats["wins_on_5"]} \n Wins on word 6: {stats["wins_on_6"]}")

stats_label = tk.Label(font=("Arial", 15), textvariable=stats_stringvar)
stats_label.place(x=450, y=300)

while not dictionary.check(word):
    variable = random.randint(0, len(words)-1)
    word = words[variable]
    print(word)

win_label = tk.Label(text=f"You won! The word was {word}", font=("Arial", 16))
lose_label = tk.Label(text=f"You lost. The word was {word}", font=("Arial", 16))
not_a_word_label = tk.Label(text="Not a word!",  font=("Arial", 16))

word_1_letters = {}
word_2_letters = {}
word_3_letters = {}
word_4_letters = {}
word_5_letters = {}
word_6_letters = {}
all_word_letters = [word_1_letters, word_2_letters, word_3_letters, word_4_letters, word_5_letters, word_6_letters]



for x in range(0, 6):
    for y in range(1, 6):
        key = f"var_{y}"
        all_word_letters[x][key] = tk.StringVar()
        all_word_letters[x][key].set("_")

all_word_letters = [word_1_letters, word_2_letters, word_3_letters, word_4_letters, word_5_letters, word_6_letters]


word_1_letter_labels = {}
word_2_letter_labels = {}
word_3_letter_labels = {}
word_4_letter_labels = {}
word_5_letter_labels = {}
word_6_letter_labels = {}
all_words_labels = [word_1_letter_labels, word_2_letter_labels, word_3_letter_labels, word_4_letter_labels, word_5_letter_labels, word_6_letter_labels]

for x in range(0, 6):
    for y in range(1, 6):
        key=f"var_{y}"
        all_words_labels[x][key] = tk.Label(borderwidth=2, relief="solid", padx=20, pady = 10, font =("Courier New", 35), textvariable=all_word_letters[x][key])
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
    
    if dictionary.check(input):
        not_a_word_label.config(text="")
        entry.delete("0", tk.END)
        inputs.append(input)
        if len(input) == 5:
            print(inputs)
            for x in range(1, 6):
                key = f"var_{x}"
                all_word_letters[words_submitted][key].set(input[x-1])

            word_counts = {}
            for char in word:
                word_counts[char] = word_counts.get(char, 0) + 1

            for x in range(0, 5):
                key = f"var_{x+1}"
                if all_word_letters[words_submitted][key].get() == word[x]:
                    all_words_labels[words_submitted][key].config(bg="green")
                    word_counts[all_word_letters[words_submitted][key].get()] -= 1
            for x in range(0, 5):
                key = f"var_{x+1}"
                if all_words_labels[words_submitted][key]['bg'] == 'green':
                    continue
                if all_word_letters[words_submitted][key].get() in word and all_words_labels[words_submitted][key]['bg'] != 'green':
                    correct = False
                    if word_counts.get(all_word_letters[words_submitted][key].get(), 0) > 0:
                        all_words_labels[words_submitted][key].config(bg=yellow)
                        word_counts[all_word_letters[words_submitted][key].get()] -= 1
                    else:
                        all_words_labels[words_submitted][key].config(bg="black")
                else:
                    all_words_labels[words_submitted][key].config(bg="black")
                    correct = False

            words_submitted += 1
            if correct:
                win_label.grid(column=6, row=1)
                stats["wins"] += 1
                stats[f"wins_on_{words_submitted}"] += 1
                with open("wordle/wordle_data.json", "w") as f:
                    json.dump(stats, f)
            elif words_submitted >= 6:
                stats["losses"] += 1
                lose_label.grid(column=6, row=1)
                with open("wordle/wordle_data.json", "w") as f:
                    json.dump(stats, f)
        else:
            if len(input) > 5:
                not_a_word_label.config(text="Input too long!")
                not_a_word_label.grid(column=6, row=2)
            elif len(input) < 5:
                not_a_word_label.config(text="Input too short!")
                not_a_word_label.grid(column=6, row=2)
    else:
        entry.delete("0", tk.END)
        not_a_word_label.config(text="Not a word!")
        not_a_word_label.grid(column=6, row=2)
    


        



entry = tk.Entry()
entry.grid(column = 6, row = 0)
submit = tk.Button(text="Submit", command=submit)
submit.grid(column = 7, row = 0)


for x in range(0, 6):
    for y in range(1, 6):
        key = f"var_{y}"
        all_words_labels[x][key].grid(row = x, column = y)


root.mainloop()