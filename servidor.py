import socket
import threading
import time

# Diccionario para almacenar los mensajes de los clientes
mensajes = {}

def handle_client(client_socket, client_address):
    while True:
        try:
            # Recibe datos del cliente
            data = client_socket.recv(1024)
            if not data:
                break

            # Decodifica los datos recibidos
            message = data.decode('utf-8')
            
            # Obtiene la marca de tiempo actual del servidor
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            # Muestra el mensaje junto con la marca de tiempo y la dirección del cliente
            print(f"Mensaje de {client_address} ({timestamp}): {message}")

            # Almacena el mensaje en el diccionario de mensajes
            if client_address not in mensajes:
                mensajes[client_address] = []
            mensajes[client_address].append((timestamp, message))

            # Envia una respuesta al cliente
            response = f"Mensaje recibido de {client_address}"
            client_socket.send(response.encode('utf-8'))

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            break

    # Cierra la conexión con el cliente
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8000))
    server_socket.listen(5)
    print("Servidor esperando conexiones...")

    while True:
        # Acepta una conexión entrante
        client_socket, client_address = server_socket.accept()
        print(f"Nueva conexión establecida con {client_address}")

        # Inicia un subproceso para manejar al cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    main()
