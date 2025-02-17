import tkinter as tk
import time
import keyboard
import os

class TaximetroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Taximetro")
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()
        self.car = self.canvas.create_rectangle(390, 290, 410, 310, fill="blue")
        self.start_button = tk.Button(root, text="Iniciar Trayecto", command=self.start_trip)
        self.start_button.pack()
        self.stop_button = tk.Button(root, text="Detener Trayecto", command=self.stop_trip, state=tk.DISABLED)
        self.stop_button.pack()
        self.hist_button = tk.Button(root, text="Historal de Trayectos", command=self.trip_hist)
        self.hist_button.pack()
        self.time_movement_label = tk.Label(root, text="Tiempo en movimiento: 0.00 segundos")
        self.time_movement_label.pack()
        self.time_stop_label = tk.Label(root, text="Tiempo en parado: 0.00 segundos")
        self.time_stop_label.pack()
        self.tarifas_label = tk.Label(root, text="Tarifas: $0.05 por segundo en movimiento, $0.02 por segundo parado")
        self.tarifas_label.pack()
        self.price_label = tk.Label(root, text="Precio total a pagar: $0.00")
        self.price_label.pack()
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.moving = False
        self.trip_started = False
        self.last_time = time.time()
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0
        self.estado_taxi = "parado"
        self.update()

    def start_trip(self):
        self.trip_started = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.tiempo_parado = 0
        self.tiempo_movimiento = 0
        self.estado_taxi = "parado"
        self.price_label.config(text="Precio total a pagar: $0.00")
        self.time_movement_label.config(text="Tiempo en movimiento: 0.00 segundos")
        self.time_stop_label.config(text="Tiempo en parado: 0.00 segundos")
        print("Trayecto iniciado")

    def stop_trip(self):
        self.trip_started = False
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.calculate_price()
        self.save_trip_history()
        print("Trayecto detenido")

    def trip_hist(self):
        self.trip_started = False
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        os.startfile("historial_trayectos.txt")

    def calculate_price(self):
        precio_movimiento = self.tiempo_movimiento * 0.05  # Precio por segundo en movimiento
        precio_parado = self.tiempo_parado * 0.02  # Precio por segundo parado
        precio_total = precio_movimiento + precio_parado
        self.price_label.config(text=f"Precio total a pagar: ${precio_total:.2f}")
        self.time_movement_label.config(text=f"Tiempo en movimiento: {self.tiempo_movimiento:.2f} segundos")
        self.time_stop_label.config(text=f"Tiempo en parado: {self.tiempo_parado:.2f} segundos")
    
    def save_trip_history(self):
        with open("historial_trayectos.txt", "a") as file:
            file.write(f"El taxi se ha movido durante {self.tiempo_movimiento:.2f} segundos\n")
            file.write(f"El taxi ha estado detenido durante {self.tiempo_parado:.2f} segundos\n")
            file.write(f"El precio total a pagar es de ${(self.tiempo_movimiento * 0.05) + (self.tiempo_parado * 0.02):.2f}\n")
            file.write("-----\n")


    def on_key_press(self, event):
        if self.trip_started and event.keysym in ['w', 'a', 's', 'd']:
            self.moving = True
            if self.estado_taxi == "parado":
                print("Taxi en movimiento")
                self.estado_taxi = "movimiento"

    def on_key_release(self, event):
        if self.trip_started and event.keysym in ['w', 'a', 's', 'd']:
            self.moving = False
            if self.estado_taxi == "movimiento":
                print("Taxi parado")
                self.estado_taxi = "parado"

    def update(self):
        current_time = time.time()
        if self.moving:
            self.tiempo_movimiento += current_time - self.last_time
            self.move_car()
        else:
            self.tiempo_parado += current_time - self.last_time
        self.last_time = current_time
        self.root.after(100, self.update)

    def move_car(self):
        if keyboard.is_pressed('w'):
            self.canvas.move(self.car, 0, -5)
        if keyboard.is_pressed('a'):
            self.canvas.move(self.car, -5, 0)
        if keyboard.is_pressed('s'):
            self.canvas.move(self.car, 0, 5)
        if keyboard.is_pressed('d'):
            self.canvas.move(self.car, 5, 0)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaximetroApp(root)
    root.mainloop()