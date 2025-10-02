import tkinter as tk
from assets.words_for_hangman import *
import random
root = tk.Tk()
root.title("Hangman")
root.geometry("600x600")
root.resizable(False, False)

abc = "abcdefghijklmnopqrstuvwxyz"

images_for_hangman = ["hangman/assets/stage1.png", "hangman/assets/stage2.png", 
                      "hangman/assets/stage3.png", "hangman/assets/stage4.png", 
                      "hangman/assets/stage5.png", "hangman/assets/stage6.png", 
                      "hangman/assets/stage7.png", "hangman/assets/stage8.png", 
                      "hangman/assets/stage9.png", "hangman/assets/stage10.png", 
                      "hangman/death.png"]
master_word_list = [words_a, words_b, words_c, words_d, words_e, 
                    words_f, words_g, words_h, words_i, words_j, 
                    words_k, words_l, words_m, words_n, words_o, 
                    words_p, words_q, words_r, words_s, words_t, 
                    words_u, words_v, words_w, words_y, words_z]

random_1 = random.randint(0, 24)
random_2 = random.randint(0, (len(master_word_list[random_1]))-1)
invalid_input_label = tk.Label(text="Invalid input!", font=("Arial", 15))

word = master_word_list[random_1][random_2]

print(word)
foundLetters = tk.StringVar()
foundLetters.set(" ")
temporary_foundletters = " "
for z in range(0, len(word)):
    temporary_foundletters = temporary_foundletters + "_ "
    foundLetters.set(temporary_foundletters)

list_of_inputs = []


photo = tk.PhotoImage(file=images_for_hangman[0])
stage = 0
yn = ""

in_list = ""


def submit():
    global list_of_inputs
    global yn 
    global stage
    global hangmanImage
    global photo
    global images_for_hangman
    global in_list
    global win
    win = "y"
    in_list = "n"
    yn = "n"
    global foundLetters
    global temporary_foundletters
    global foundLettersLabel
    global word
    global incorrectText
    global INPUT
    global letterEntry
    global invalid_input_label
    INPUT = letterEntry.get()
    INPUT = INPUT.lower()
    
    letterEntry.delete(0, tk.END)
    if INPUT in abc and len(INPUT) == 1:
        invalid_input_label.config(text="")
        for g in range(0, len(list_of_inputs)):
            if INPUT == list_of_inputs[g]:
                in_list = "y"
        if in_list == "n":
            list_of_inputs.append(INPUT)
            
        print(in_list)
        print(list_of_inputs)
        if in_list == "n":
            for x in range(0, len(word)):
                if INPUT == word[x]:
                    temp = changeChar(temporary_foundletters, x*2+1, word[x])
                    temporary_foundletters = temp
                    yn = "y"
            if yn == "n":
                stage = stage+1
                hangmanImage.place_forget()
                photo = tk.PhotoImage(file=images_for_hangman[stage])
                hangmanImage.config(image=photo)
                hangmanImage.place(x=0, y=200)
                incorrectText.insert(tk.END, f"{INPUT}, ")

            if stage == 10:
                temporary_foundletters = f"You failed! The word was {word}"
                foundLetters.set(temporary_foundletters)
                return

        for c in range(1, len(temporary_foundletters)):
            if temporary_foundletters[c] == "_":
                win = "n"

        if win == "y":
            temporary_foundletters = f"You won! The word was {word}."
        foundLetters.set(temporary_foundletters)
        print(stage)

        print(temporary_foundletters)
            
        print(INPUT)
    else:
        invalid_input_label.config(text="Invalid input!")
        invalid_input_label.place(x=400, y=100)

def changeChar(string, index, newChar):
    return string[:index] + newChar + string[index + 1:]


letterEntry = tk.Entry(root, width = 5)

hangmanImage = tk.Label(root, image=photo)
submitButton = tk.Button(root, text = "Submit", height=4, width=5, command=submit)
incorrectText = tk.Text(root, wrap=tk.WORD, height = 5, width = 12, font=("Arial", 14))
incorrectText.insert(tk.END, "Incorrect guesses: \n")
foundLettersLabel = tk.Label(root, textvariable=foundLetters, font=("Arial", 18))


foundLettersLabel.place(x=100, y=100)
submitButton.place(x=500, y=475)
hangmanImage.place(x=0, y=200)
letterEntry.place(x=425, y=500)
incorrectText.place(x=425, y = 300)







root.mainloop()