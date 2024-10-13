import socket
import threading
import pickle
import tkinter as tk
from tkinter import messagebox, simpledialog
from window import Window
from config import PORT


class Server:
    def __init__(self):
        self.participants_list = None
        self.clients = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', PORT))
        self.server_socket.listen(5)
        self.experiment_running = False

        # GUI
        self.__window = Window()

        self.start_button = tk.Button(self.__window,
                                      text="Начать эксперимент",
                                      font=("Trebuchet MS", 13, "bold"),
                                      command=self.start_experiment)
        self.start_button.pack(anchor="center", expand=True, fill="both", ipadx=10, ipady=10)
        self.__window.mainloop()

    def start_experiment(self):
        threading.Thread(target=self.accept_clients, daemon=True).start()
        self.__window.destroy()
        self.__window = Window()
        self.experiment_running = True
        messagebox.showinfo("Информация", "Эксперимент начат!")
        self.participants_list = tk.Listbox(self.__window)
        self.participants_list.pack(padx=100)
        tk.Button(text="Ответить", command=lambda: self.answer()).pack()
        self.__window.mainloop()

    def answer(self):
        selection = self.participants_list.curselection()
        if not selection:
            return
        selected_language = self.participants_list.get(selection[0])
        # TODO: отправить ответ
        self.participants_list.delete(selection[0])

    def accept_clients(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.clients[addr] = client_socket
            self.participants_list.insert(tk.END, f"{addr[0]}:{addr[1]}")
            threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()

    def handle_client(self, client_socket, addr):
        while True:
            if self.experiment_running:
                number = simpledialog.askinteger("Ввод числа", "Введите число:")
                if number is not None:
                    client_socket.send(pickle.dumps(number))
                    response = client_socket.recv(1024)
                    if response:
                        data = pickle.loads(response)
                        messagebox.showinfo("Ответ клиента", f"Клиент {addr} выбрал: {data}")
            else:
                break

    def on_closing(self):
        self.server_socket.close()
        self.__window.destroy()
