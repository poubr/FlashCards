from tkinter import *
from tkinter import messagebox
import pandas
from random import choice
import os
from create_wordlist import get_list

# CONSTANTS
FONT_LANG = ("Arial", 30, "italic")
FONT_WORD = ("Arial", 40, "bold")
FONT_BUTTON = ("Arial", 20)
LIGHT_BLUE = "#c4e9fd"
DARK_BLUE = "#3858ca"


class FlashCards:
    def __init__(self, window):

        self.window = window
        self.window.title("Suomenkielinen sanasto")
        self.window.config(padx=20, pady=20, background=LIGHT_BLUE)

        self.current_word = ""
        self.seconds = 5
        self.timer = None
        self.timerIsOn = False
        self.cardIsTurned = False
        self.timeToggle = False

        # GETTING THE LEXICON
        try:
            self.wordlist_df = pandas.read_csv("words_to_learn.csv")
        except FileNotFoundError:
            self.wordlist_df = get_list()
            self.wordlist_df = pandas.read_csv("wordlist.csv")
        self.wordlist = self.wordlist_df.to_dict(orient="records")

        self.learned = 0
        self.learned_out_of = len(self.wordlist)

        self.current_card = {}

        # SETTING UP UI
        self.canvas = Canvas(width=604, height=400, bd=0, highlightthickness=0)
        self.canvas.config(bg=LIGHT_BLUE)
        self.front_card = PhotoImage(file="card_front.png")
        self.back_card = PhotoImage(file="card_back.png")
        self.card = self.canvas.create_image(302, 200, image=self.front_card)
        self.language = self.canvas.create_text(300, 150, text="Suomi", fill="black", font=FONT_LANG)
        self.word_to_guess = self.canvas.create_text(300, 230, text="sana", fill="black", font=FONT_WORD)
        self.canvas.grid(row=1, column=0, columnspan=4, rowspan=3)

        # BUTTONS AND WIDGETS
        self.word_counter = Label(text=f"{self.learned} / {self.learned_out_of}",
                                  bg=LIGHT_BLUE, fg=DARK_BLUE, highlightthickness=0, font=FONT_BUTTON)
        self.word_counter.grid(row=0, column=3)

        self.timer_countdown = Label(text="Timer Off", bg=LIGHT_BLUE, fg="white",  font=FONT_LANG)
        self.timer_countdown.grid(row=0, column=0)

        self.turn_img = PhotoImage(file="button_turn.png")
        self.turn_button = Button(image=self.turn_img, bd=0, bg=LIGHT_BLUE, highlightthickness=0,
                                  command=self.turn_card)
        self.turn_button.grid(row=1, column=4, rowspan=2, pady=20, padx=20)

        self.next_img = PhotoImage(file="button_next.png")
        self.next_button = Button(image=self.next_img, bd=0, bg=LIGHT_BLUE, highlightthickness=0,
                                  command=self.next_card)
        self.next_button.grid(row=2, column=4, rowspan=2, pady=20, padx=20)

        self.correct_img = PhotoImage(file="button_correct.png")
        self.correct_button = Button(image=self.correct_img, bd=0, highlightthickness=0, command=self.correct_guess)
        self.correct_button.grid(row=4, column=0, columnspan=2, pady=20)

        self.wrong_img = PhotoImage(file="button_wrong.png")
        self.wrong_button = Button(image=self.wrong_img, bd=0, bg=LIGHT_BLUE, highlightthickness=0,
                                   command=self.wrong_guess)
        self.wrong_button.grid(row=4, column=2, columnspan=2,  pady=20)

        self.timer_button = Button(text="Timer on / off", background=LIGHT_BLUE, fg=DARK_BLUE,
                                   highlightbackground=DARK_BLUE, font=FONT_BUTTON, command=self.toggle_timer)
        self.timer_button.grid(row=5, column=0, columnspan=2, pady=20)

        self.reset_button = Button(text="Reset progress", background=LIGHT_BLUE, fg=DARK_BLUE,
                                   highlightbackground=DARK_BLUE, font=FONT_BUTTON,
                                   command=self.reset_progress)
        self.reset_button.grid(row=5, column=2, columnspan=2, pady=20)

    # Turns the timer on / off
    def toggle_timer(self):
        if self.timeToggle:
            self.timeToggle = False
            self.timer_countdown.config(text="Timer Off", fg="white",  font=FONT_LANG)
            if self.timerIsOn:
                self.timerIsOn = False
                self.window.after_cancel(self.timer)
        else:
            self.timeToggle = True
            self.start_timer(self.seconds)

    # Starts the timer
    def start_timer(self, count):
        if self.timeToggle:
            self.timerIsOn = True
            if count >= 0 and not self.cardIsTurned:
                self.timer_countdown.config(text=count, fg="black", font=FONT_WORD)
                self.timer = self.window.after(1000, self.start_timer, count - 1)
            else:
                self.turn_card()

    # Gets the next card
    def next_card(self):
        if self.timerIsOn:
            self.window.after_cancel(self.timer)
            self.timerIsOn = False
        self.cardIsTurned = False
        self.current_word = choice(self.wordlist)
        self.canvas.itemconfig(self.card, image=self.front_card)
        self.canvas.itemconfig(self.language, text="Suomi")
        self.canvas.itemconfig(self.word_to_guess, text=self.current_word["Suomi"])
        if self.timeToggle:
            self.start_timer(self.seconds)

    # Turns the card to reveal the translation
    def turn_card(self):
        self.cardIsTurned = True
        if self.timerIsOn:
            self.timerIsOn = False
            self.window.after_cancel(self.timer)
        self.timer_countdown.config(text="")
        self.canvas.itemconfig(self.card, image=self.back_card)
        self.canvas.itemconfig(self.language, text="English")
        self.canvas.itemconfig(self.word_to_guess, text=self.current_word["English"])

    # Removes the word which user has learned
    def correct_guess(self):
        self.wordlist.remove(self.current_word)
        self.learned += 1
        self.word_counter.config(text=f"{self.learned} / {self.learned_out_of}")
        df = pandas.DataFrame(self.wordlist)
        df.to_csv("words_to_learn.csv", index=False)
        self.next_card()

    # Goes to the next card - basically only there for the visual symmetry
    def wrong_guess(self):
        if self.cardIsTurned:
            self.next_card()
        else:
            self.turn_card()

    # Deletes the learned words
    def reset_progress(self):
        should_reset = messagebox.askokcancel(title="Reset learned words?",
                                              message="Are you sure you want to reset your learned words?")
        if should_reset:
            try:
                os.remove("words_to_learn.csv")
            except FileNotFoundError:
                pass

    def main(self):
        self.next_card()
        self.window.mainloop()


if __name__ == '__main__':
    flash_cards = FlashCards(Tk())
    flash_cards.main()
