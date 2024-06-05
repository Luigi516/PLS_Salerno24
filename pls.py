import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.ttk as ttk
from tkinter.ttk import *


class QuantumGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum game")
        self.states = []
        self.measures = []
        self.axes = []
        self.results = []
        self.chosen_state = None
        self.score = 0
        self.create_widgets()

    def create_widgets(self):
        self.Font_tuple = ("Aptos", 14, "bold") 
        self.frame = tk.Frame(self.root, bg="#2F3033")
        self.frame.pack(pady= 80)

        self.create_state_btn = tk.Button(self.frame, text="Crea Stato", command=self.create_quantum_states, background="#227050", height = 2, width = 16, font= self.Font_tuple, foreground="white")
        self.create_state_btn.grid(row=0, column=0, padx=0, pady=0)

        self.start_game_btn = tk.Button(self.frame, text="Avvia Gioco", command=self.start_game, height = 2, background="#227050", width = 16, font=self.Font_tuple, foreground="white")
        self.start_game_btn.grid(row=0, column=1, padx=80)

        self.instructions_label = tk.Label(self.frame, text="", wraplength=400, bg = "#2F3033")
        self.instructions_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.guess_btn = tk.Button(self.frame, text="Indovina lo stato", command=self.guess_state, state=tk.DISABLED, height = 2, width = 16, font = self.Font_tuple, bg = "#227050", foreground="white")
        self.guess_btn.grid(row=2, column=0, pady=9)

        self.measure_btn = tk.Button(self.frame, text="Misura", command=self.measure, state=tk.DISABLED, height = 2, width = 16, font = self.Font_tuple, bg = "#227050", foreground="white")
        self.measure_btn.grid(row=2, column=1, pady=9)

    def create_quantum_states(self):
        self.states = []
        self.instructions_label.config(text="Creazione dello stato quantistico, inserisci i dettagli richiesti", bg = "#2F3033", fg= "white", font = self.Font_tuple)

        number_of_states = simpledialog.askinteger("Input", "Quanti stati vuoi creare?")
        if not number_of_states or number_of_states <= 0:
            messagebox.showerror("Error", "Numero invalido di stati")
            return

        for i in range(number_of_states):
            state_id = simpledialog.askstring("Input", f"Inserisci ID per lo stato {i + 1}:")
            theta = simpledialog.askfloat("Input", f"Inserisci angolo theta (0-180) per lo stato {i + 1}:")
            phi = simpledialog.askfloat("Input", f"Inserisci angolo phi (0-360) per lo stato {i + 1}:")

            x = round(math.sin(math.radians(theta)) * math.cos(math.radians(phi)), 2)
            y = round(math.sin(math.radians(theta)) * math.sin(math.radians(phi)), 2)
            z = round(math.cos(math.radians(theta)), 2)

            state = {
                "ID": state_id,
                "x": x,
                "y": y,
                "z": z,
                "PX": round(0.5 * (1 + x), 2),
                "PY": round(0.5 * (1 + y), 2),
                "PZ": round(0.5 * (1 + z), 2)
            }
            self.states.append(state)

        messagebox.showinfo("Success", "Stati quantisitici creati correttamente")
        self.instructions_label.config(text="Stati quantisitici creati correttamente, puoi avviare il gioco")

    def start_game(self):
        if not self.states:
            messagebox.showerror("Error", "nessuno stato quantistico trovato; creane prima uno")
            return

        self.chosen_state = random.choice(self.states)
        self.measures = []
        self.axes = []
        self.results = []
        self.score = 0

        self.guess_btn.config(state=tk.NORMAL)
        self.measure_btn.config(state=tk.NORMAL)
        self.instructions_label.config(text="Partita avviata; Misura uno stato e prova ad indovinarlo")
    def measure(self):
        axis = simpledialog.askstring("Input", "Scegli un asse (x, y, z):")
        if axis not in ['x', 'y', 'z']:
            messagebox.showerror("Error", "Asse invalido.")
            return

        dice = random.randint(1, 20)
        probability = self.chosen_state[f'P{axis.upper()}']
        result = 1 if dice * 0.05 <= probability else -1

        self.measures.append(dice)
        self.axes.append(axis)
        self.results.append(result)

        self.instructions_label.config(text=f"Misurato sull'asse {axis}. Risultato: {result}. Continua a misurare oppure indovina lo stato")

    def guess_state(self):
        if not self.chosen_state:
            messagebox.showerror("Error", "Nessuno stato scelto. Avvia prima il gioco")
            return
        
        state_id = simpledialog.askstring("Input", "Inserisci l'ID dello stato:")
        if state_id == self.chosen_state["ID"]:
            self.score += len(self.measures)
            if self.score < 0:
                self.score = 0
            messagebox.showinfo("Correct", f"CORRETTO! Punteggio: {self.score}")
            self.instructions_label.config(text="Corretto! Puoi avviare una nuova partita o continuare a misurare.")
            self.plot_measurements()
        else:
            self.score -= 5
            messagebox.showinfo("Incorrect", "SBAGLIATO! Continua a misurare.")
            self.instructions_label.config(text="SBAGLIATO Continua a misurare o indovina di nuovo.")

    def plot_measurements(self):
        root.geometry("650x770+10+10")
        fig, ax = plt.subplots()
        ax.plot(range(1, len(self.measures) + 1), self.measures, marker='o', linestyle='-', color='#227050', label='Lancio Dado')
        ax.set_xlabel('Misura')
        ax.set_ylabel('Lancio dei dadi')
        ax.set_title('Misure quantistiche')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    root = tk.Tk()
    p1 = tk.PhotoImage(file= "dice.png")
    root.iconphoto(False, p1)
    root.geometry("650x400+10+10")
    root.configure(background="#2F3033")
    app = QuantumGameApp(root)
    root.mainloop()
