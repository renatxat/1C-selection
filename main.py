import tkinter as tk
from client import Client
from server import Server
from window import Window


class Menu:
    __window = ["tk.Tk()"]
    __address = "localhost"
    __error_label = ["tk.Label()"]
    __number = 0

    def __init__(self):
        self.__window = Window()
        button1 = tk.Button(self.__window,
                            text="Участвовать в эксперименте",
                            font=("Trebuchet MS", 13, "bold"),
                            command=lambda: self.__submit_server_address())
        button1.pack(anchor="center", expand=True, fill="both", ipadx=10, ipady=10)

        button2 = tk.Button(self.__window,
                            text="Создать эксперимент",
                            font=("Trebuchet MS", 13, "bold"),
                            command=lambda: (self.__window.destroy(), Server()))
        button2.pack(anchor="center", expand=True, fill="both", ipadx=10, ipady=10)

        self.__window.mainloop()

    def __submit_server_address(self):
        self.__window.destroy()
        self.__window = Window()

        server_address_label = tk.Label(self.__window,
                                        text="Введите адрес сервера:",
                                        font=("Trebuchet MS", 13, "bold"))
        server_address_label.pack(ipadx=10, ipady=10)

        server_address_entry = tk.Entry(self.__window)
        server_address_entry.pack(anchor="center", fill="x", expand=True, ipadx=10, ipady=10)

        self.__error_label = tk.Label(self.__window,
                                      text="",
                                      font=("Trebuchet MS", 8),
                                      fg="red")
        self.__error_label.pack()

        submit_button = tk.Button(self.__window,
                                  text="Отправить",
                                  font=("Trebuchet MS", 13, "bold"),
                                  command=lambda: self.__check_address(server_address_entry.get()))
        submit_button.pack(anchor="center", expand=True, fill="x", ipadx=10, ipady=10)

        button_back = tk.Button(self.__window,
                                text="Назад",
                                font=("Trebuchet MS", 13, "bold"),
                                command=lambda: (self.__window.destroy(), self.__init__()))
        button_back.pack(anchor="center", expand=True, fill="both", ipadx=10, ipady=10)

    def __check_address(self, address):
        if not address:
            return
        self.__address = address
        # TODO: подключиться к серверу
        # self.__error_label["text"] = "некорректный адрес"
        self.__window.destroy()
        Client(address)


if __name__ == "__main__":
    Menu()
