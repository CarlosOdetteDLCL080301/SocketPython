import socket
import threading
import time

# Diccionario para almacenar los mensajes de los clientes
mensajes = {}

def handle_client(client_socket, client_address):
    while True:
        try:
            # Recibe datos enviados por el cliente (hasta 1024 bytes)
            data = client_socket.recv(1024)
            
            # Si no se recibe ningún dato, se sale del bucle
            if not data:
                break

            # Decodifica los datos recibidos en formato UTF-8 para obtener el mensaje
            message = data.decode('utf-8')
            
            # Obtiene la marca de tiempo actual del servidor
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            # Muestra el mensaje del cliente junto con la marca de tiempo y su dirección
            print(f"Mensaje de {client_address} ({timestamp}): {message}")

            # Almacena el mensaje en el diccionario de mensajes
            if client_address not in mensajes:
                mensajes[client_address] = []
            mensajes[client_address].append((timestamp, message))

            # Envia una respuesta al cliente confirmando la recepción del mensaje
            response = f"Mensaje recibido de {client_address}"
            client_socket.send(response.encode('utf-8'))

        except Exception as e:
            # Si ocurre un error, se muestra en la consola y se sale del bucle
            print(f"Ocurrió un error: {e}")
            break

    # Cierra la conexión con el cliente una vez que se completa la comunicación
    client_socket.close()


def main():
    # Crea un socket de tipo AF_INET (IPv4) y SOCK_STREAM (TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enlaza el socket al localhost en el puerto 8000
    server_socket.bind(('localhost', 8000))

    # Escucha hasta 5 conexiones entrantes en el socket
    server_socket.listen(5)
    print("Servidor esperando conexiones...")

    while True:
        # Acepta una conexión entrante y obtiene el socket del cliente y su dirección
        client_socket, client_address = server_socket.accept()
        print(f"Nueva conexión establecida con {client_address}")

        # Inicia un subproceso para manejar al cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()


if __name__ == "__main__":
    # Verifica si este archivo se está ejecutando como un programa independiente
    # y no está siendo importado como un módulo en otro programa.
    # Si es el programa principal, ejecuta la función 'main()'.
    main()
