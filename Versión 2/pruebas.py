import socket
import threading

def manejar_conexion_sucursal(cliente, direccion, sucursales):
    print(f"Conexión establecida con sucursal en {direccion}")

    with cliente:
        while True:
            data = cliente.recv(1024)
            if not data:
                print(f"Sucursal en {direccion} se desconectó.")
                sucursales.remove((cliente, direccion))
                break

            mensaje = data.decode("utf-8")
            print(f"Mensaje recibido de sucursal en {direccion}: {mensaje}")

def escuchar_sucursales(servidor, sucursales):
    while True:
        cliente, direccion = servidor.accept()
        sucursales.append((cliente, direccion))

        # Iniciar un hilo para manejar la conexión con la sucursal
        threading.Thread(target=manejar_conexion_sucursal, args=(cliente, direccion, sucursales)).start()

def main():
    host = "127.0.0.1"
    puerto = 5555

    sucursales = []

    # Configurar el socket del nodo maestro
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen()

    print(f"Nodo maestro escuchando en {host}:{puerto}")

    # Iniciar un hilo para escuchar sucursales
    threading.Thread(target=escuchar_sucursales, args=(servidor, sucursales)).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Apagando el nodo maestro.")
        servidor.close()

if __name__ == "__main__":
    main()
