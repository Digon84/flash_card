import random
from tkinter import *
import pandas
from gtts import gTTS
import os
from pygame import mixer

BACKGROUND_COLOR = "#B1DDC6"
MP3_FOLDER = "./data/mp3"

current_word = {}

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50,bg=BACKGROUND_COLOR)

try:
    words_list = pandas.read_csv("./data/words_to_learn.csv").to_dict(orient="records")
except FileNotFoundError:
    words_list = pandas.read_csv("./data/spanish_words.csv").to_dict(orient="records")

card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")
wrong_image = PhotoImage(file="./images/wrong.png")
right_image = PhotoImage(file="./images/right.png")


canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front_image)
language_text = canvas.create_text(400, 150, font="Arial 40 italic", text="Title")
noun_text = canvas.create_text(400, 263, font="Arial 60 bold", text="word")
canvas.grid(column=0, row=0, columnspan=2)


def play_sound(language="en", word="test"):
    if not os.path.exists(f"{MP3_FOLDER}/{word}_{language}.mp3"):
        myobj = gTTS(text=word, lang=language, slow=False)
        myobj.save(f"{MP3_FOLDER}/{word}_{language}.mp3")
    mixer.init()
    mixer.music.load(f"{MP3_FOLDER}/{word}_{language}.mp3")
    mixer.music.play()


def remove_known_get_new():
    words_list.remove(current_word)
    pandas.DataFrame(words_list).to_csv("./data/words_to_learn.csv", index=False)
    set_random_word()


def set_random_word():
    global current_word
    canvas.itemconfig(canvas_image, image=card_front_image)
    current_word = random.choice(words_list)
    play_sound(language="en", word=current_word["English"])
    canvas.itemconfigure(language_text, text="English", fill="#000000")
    canvas.itemconfigure(noun_text, text=current_word["English"], fill="#000000")
    window.after(3000, flip_card)


def flip_card():
    global current_word
    play_sound(language="es", word=current_word["Spanish"])
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfigure(language_text, text="Spanish", fill="#FFFFFF")
    canvas.itemconfigure(noun_text, text=current_word["Spanish"], fill="#FFFFFF")

set_random_word()

wrong_button = Button(image=wrong_image, highlightthickness=0, command=set_random_word)
wrong_button.grid(column=0, row=1)

right_button = Button(image=right_image, highlightthickness=0, command=remove_known_get_new)
right_button.grid(column=1, row=1)

window.mainloop()