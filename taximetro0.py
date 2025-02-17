import time
import keyboard

def taximetro():

    print("Bienvenido al taximetro")
    print("1. Iniciar recorrido")
    print("Q. Finalizar recorrido")

    # Variables
    tarifa_movimiento = 0.05
    tarifa_parado = 0.02
    tiempo_movimiento = 0
    tiempo_parado = 0
    estado = "parado" #Estado inicial del taxi

    while True:

        opciones = input("Selecciona la opcion a realizar: ")

        if opciones == "Q":
            print("Fin del Recorrido")
            break
        
        if opciones == "1":
            print("Comienza el recorrido")
            ultimo_movimiento = time.time()
            print(f"Taxi parado")
            while True:
                if keyboard.is_pressed('f'):
                    print("Fin del recorrido actual")
                    tiempo_actual = time.time()
                    tiempo_parado += tiempo_actual - ultimo_movimiento
                    precio_final = (tiempo_movimiento * tarifa_movimiento) + (tiempo_parado * tarifa_parado)
                    print(f"Tiempo parado: {tiempo_parado} segundos")
                    print(f"Tiempo en movimiento: {tiempo_movimiento} segundos")
                    print(f"Precio final: {precio_final} euros")
                    tiempo_movimiento = 0
                    tiempo_parado = 0
                    break

                if keyboard.is_pressed('w'):
                    if estado == "parado":
                        print(f"Taxi en movimiento")
                        estado = "movimiento"
                    tiempo_movimiento += 0.1  # Incrementa la distancia recorrida
                    ultimo_movimiento = time.time()
                    time.sleep(0.1)  # Sleep para mantener informado al usuario de que el taxi esta en movimiento
                    keyboard.unhook_all()
                else:
                    if estado == "movimiento":
                        print(f"Taxi parado")
                        estado = "parado"
                    tiempo_actual = time.time()
                    tiempo_parado += tiempo_actual - ultimo_movimiento
                    ultimo_movimiento = tiempo_actual
                    time.sleep(0.1)  # Sleep para mantener informado al usuario de que el taxi esta parado
                    keyboard.unhook_all()

        if opciones not in ["1", "Q"]:
            print("Opción no válida. Desea comenzar un nuevo recorrido?")
            continue
    keyboard.unhook_all()

taximetro()