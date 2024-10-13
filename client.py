import socket
import pickle
import tkinter as tk
from tkinter import messagebox
from window import Window
from config import PORT


class Client:
    def __init__(self, host):
        self.__error_label = None
        self.__is_closing = False
        self.__number_of_attempts = 0
        self.client_socket = socket.socket()
        self.client_socket.connect((host, PORT))
        self.__window = Window()
        self.__input_number()
        self.__start_loops()

    def __input_number(self):
        # Запрос числа от пользователя
        hidden_number_label = tk.Label(self.__window,
                                       text="Загадайте целое число:",
                                       font=("Trebuchet MS", 13, "bold"))
        hidden_number_label.pack(ipadx=10, ipady=10)

        hidden_number_entry = tk.Entry(self.__window)
        hidden_number_entry.pack(anchor="center", fill="x", expand=True, ipadx=10, ipady=10)

        self.__error_label = tk.Label(self.__window,
                                      text="",
                                      font=("Trebuchet MS", 8),
                                      fg="red")
        self.__error_label.pack()

        submit_button = tk.Button(self.__window,
                                  text="Отправить",
                                  font=("Trebuchet MS", 13, "bold"),
                                  command=lambda: self.__check_number(hidden_number_entry.get()))
        submit_button.pack(anchor="center", expand=True, fill="x", ipadx=10, ipady=10)

    def __check_number(self, number):
        if not number.isdigit():
            self.__error_label["text"] = "не подходит"
            return
        self.__number_of_attempts += 1
        self.__send_number(number)

    def __send_number(self, user_number):
        # Отправка числа на сервер
        data_to_send = (self.__number_of_attempts, user_number)
        self.client_socket.send(pickle.dumps(data_to_send))
        response = self.client_socket.recv(1024)
        if response:
            result = pickle.loads(response)
            messagebox.showinfo("Ответ сервера", f"Результат: {result}")

    def __start_loops(self):
        if self.__is_closing:
            self.client_socket.close()
            return
        self.__window.after_idle(self.__loop, 0)  # start endless __loop
        self.__window.mainloop()

    def __loop(self, n):
        if self.__is_closing or type(self.__window) == str or self.__window.is_destroyed():
            self.client_socket.close()
            return
        if n == 0:
            self.__window.after(1, self.__loop, n + 1)
        self.__check_game_over(n)

    def __check_game_over(self, n):
        if not self.__is_closing:
            self.client_socket.close()
            self.__window.after(1, self.__loop, n + 1)  # endless cycle!
        else:
            if messagebox.showinfo(title="Чел, хорош!",
                                   message=f"Вы угадали за {self.__number_of_attempts} попыток",
                                   parent=self.__window):
                self.__window.destroy()
