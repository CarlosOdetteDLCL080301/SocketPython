# Importamos la biblioteca 'socket' para habilitar la comunicación de red, 
# el cual nos permite la creación y el uso de sockets para la comunicación entre
# el cliente y el servidor.
import socket

# Importamos la biblioteca 'time' para trabajar con funciones relacionadas con el tiempo,
# en este caso, se utiliza para obtener la marca de tiempo actual y formatearla.
import time


# Función para enviar mensajes al servidor
def send_message(client_socket, message):
    # Obtiene la marca de tiempo actual del cliente
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    # Construye el mensaje concatenando la marca de tiempo con el mensaje original
    full_message = f"[{timestamp}] {message}"
    
    # Envia el mensaje al servidor como bytes codificados en UTF-8
    client_socket.send(full_message.encode('utf-8'))


def main():
    # Crea un nuevo socket del cliente
    mi_socket = socket.socket()
    
    # Establece una conexión con el servidor en localhost y el puerto 8000
    mi_socket.connect(('localhost', 8000))

    while True:
        # Obtiene un mensaje ingresado por el usuario
        message = input("Escribe un mensaje: ")
        
        # Llama a la función 'send_message' para enviar el mensaje al servidor
        send_message(mi_socket, message)

        # Recibe una respuesta del servidor (hasta 1024 bytes) y la decodifica
        response = mi_socket.recv(1024)
        print(response.decode('utf-8'))

    # Cierra la conexión con el servidor
    mi_socket.close()


if __name__ == "__main__":
    # Verifica si este archivo se está ejecutando como un programa independiente
    # y no está siendo importado como un módulo en otro programa.
    # Si es el programa principal, ejecuta la función 'main()'.
    main()
