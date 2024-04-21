import random
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import pandas
from tkinter.messagebox import showinfo

FONT_NAME = "Courier 14"
FONT = "Courier 12"
MINUTES = [3, 5, 10, 15, 20, 30, 60]
WORDS_NUMBER = [75, 150, 250, 500]

timer = None
session_timer = None
session_timer_words = None
letters = ''
new_prompt = ''
original_data = pandas.read_csv('prompts.csv')
prompts = original_data['prompt'].to_list()

window = Tk()
method = StringVar()
goal_min = StringVar()
goal_word = StringVar()
enabled = IntVar()

window.title("Text Writing")
window.config(padx=50, pady=30, background='#DABDAB')


# set session timer
def count_down_duration(sec):
    if sec > 0:
        global session_timer
        session_timer = window.after(1000, count_down_duration, sec-1)
    else:
        session_timer = None
        after_end()


# 5 sec timer
def count_down(count):
    if count > 0:
        global timer, session_timer_words, session_timer
        timer = window.after(1000, count_down, count-1)
    else:
        if session_timer:
            window.after_cancel(session_timer)
            text.delete(1.0, END)
        elif session_timer_words:
            session_timer_words = None
            text.delete(1.0, END)
        after_end()


# add combobox depending on words or minutes chosen as goal
def add_functionality():
    if method.get() == 'min':
        min_combobox.grid(column=1, row=1)
        word_combobox.grid_forget()

    elif method.get() == 'word':
        word_combobox.grid(column=1, row=2, )
        min_combobox.grid_forget()


def generate_prompt():
    global new_prompt
    text.delete(1.0, END)
    new_prompt = random.choice(prompts)
    text.insert(1.0, new_prompt)


def start():
    global session_timer, session_timer_words
    label.config(text='')
    if new_prompt == '':
        text.delete(1.0, END)
    count_minutes = goal_min.get()
    count_word = goal_word.get()
    try:
        if goal_min.get():
            duration_sec = int(count_minutes) * 60
            count_down_duration(duration_sec)
        elif count_words:
            session_timer_words = int(count_word)
    except ValueError:
        showinfo('Set your goal', message="Choose how many minutes you'll typing or how many words you aim to type")


def after_end():
    global enabled, letters, new_prompt
    goal_min.set('')
    goal_word.set('')
    text.config(fg='black')
    enabled = 0
    letters = ''
    new_prompt = ''


# listen user's input
def check_input(event):
    global session_timer, letters, session_timer_words
    if session_timer or session_timer_words:
        symbol_input = event.keysym
        if symbol_input:
            if timer:
                window.after_cancel(timer)
            count_down(5)
        if symbol_input == 'space':
            if letters:
                if letters[-1] != " ":
                    letters += ' '
                    count_words()
        else:
            letters += symbol_input


def count_words():
    global session_timer_words
    words = letters[:-2].split(" ")
    label.config(text=f'{len(words)} words')
    if session_timer_words:
        if session_timer_words - len(words) == 0:
            session_timer_words = None
            after_end()


# hardcore mode
def hide_input():
    if enabled.get() == 1:
        text.config(foreground='#fffaf0')


start = Button(text='Start', command=start, width=15, bg='#BDECB6', relief='ridge', font=FONT)
start.grid(column=8, row=0)

prompt_btn = Button(text='Generate a prompt', command=generate_prompt,  bg='#FFDB8B', relief='ridge', font=FONT)
prompt_btn.grid(column=0, row=0)

minutes_btn = Radiobutton(text='Minutes', value='min', variable=method, background='#DABDAB', command=add_functionality, font=FONT)
minutes_btn.grid(column=0, row=1, )

words_btn = Radiobutton(text='Words  ', value='word', variable=method, background='#DABDAB', command=add_functionality, font=FONT)
words_btn.grid(column=0, row=2)

min_combobox = ttk.Combobox(textvariable=goal_min, values=MINUTES, width=7)
word_combobox = ttk.Combobox(textvariable=goal_word, values=WORDS_NUMBER, width=7)
mode_checkbutton = Checkbutton(text="Hardcore mode", variable=enabled, command=hide_input, background='#DABDAB')

mode_checkbutton.grid(column=8, row=2)

text = ScrolledText(wrap='word', relief='groove', height=18, spacing2=18, spacing1=7, width=80, font=FONT_NAME)
text.grid(column=0, row=4, columnspan=10)
text.bind('<Key>', check_input)

label = Label(text='', background='#DABDAB', font=FONT)
label.grid(column=0, row=5, columnspan=10)

window.mainloop()