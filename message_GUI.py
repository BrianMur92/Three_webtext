# Author:       Brian Murphy
# Date started: 23/05/2020
# Last updated: 23/05/2020

from tkinter import *
from tkinter import scrolledtext
import three_webtext
from datetime import datetime


class message_GUI():
    def __init__(self):
        self.window = Tk()
        self.window.title("Three webtext GUI")
        self.window.geometry('450x300')

        self.lbl_num = Label(self.window, text="Send to:", font=("Arial Bold", 10))
        self.lbl_num.grid(row=0, column=0)
        self.txt_number = Entry(self.window, width=15, textvariable='Send to')
        self.txt_number.grid(row=0, column=1)
        self.txt_number.focus()  # Enable write text straight away

        self.lbl_message = Label(self.window, text="Message:", font=("Arial Bold", 10))
        self.lbl_message.grid(row=1, column=0)
        # self. txt = Entry(self.window, width=100)
        self.txt_message = scrolledtext.ScrolledText(self.window, width=40, height=10)
        self.txt_message.grid(row=1, column=1)
        self.txt_message.focus()  # Enable write text straight away

        self.send_self = BooleanVar()
        self.send_self.set(False)  # set check state
        self.chk = Checkbutton(self.window, text='Send copy to myself', var=self.send_self)
        self.chk.grid(row=3, column=1)

        self.btn = Button(self.window, text="Send text", bg="orange", fg="red", command=self.clicked)
        self.btn.grid(row=4, column=1)

        self.lbl_sent = Label(self.window, text="", font=("Arial Bold", 10))
        self.lbl_sent.grid(row=5, column=1)

        self.window.mainloop()

    def clicked(self):
        res = self.txt_message.get('1.0', 'end-1c')
        with open("message.txt", "w") as file1:
            file1.writelines(res)


        three_webtext.main(sent_to=self.txt_number.get())
        print('Message sent to : ' + self.txt_number.get())

        if self.send_self.get():
            three_webtext.main(sent_to=three_webtext.login_data()[0])
            print('Message sent to self: ' + three_webtext.login_data()[0])

        sent_time = datetime.now().strftime("%H:%M:%S")
        self.lbl_sent.configure(text='Message sent at: ' + sent_time)
        self.txt_message.delete('1.0', END)



a = message_GUI()
