import socket
import time

def main():
    host = "127.0.0.1"
    puerto = 5555

    # Configurar el socket de la sucursal
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, puerto))

    print(f"Conectado a nodo maestro en {host}:{puerto}")

    try:
        while True:
            # Simular actividad de la sucursal
            time.sleep(5)
            mensaje = "Datos actualizados desde sucursal"
            cliente.sendall(mensaje.encode("utf-8"))
    except KeyboardInterrupt:
        print("Sucursal desconectándose.")
    finally:
        cliente.close()

if __name__ == "__main__":
    main()

