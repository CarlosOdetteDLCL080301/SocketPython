import socket
import time

# Función para enviar mensajes al servidor
def send_message(client_socket, message):
    # Obtiene la marca de tiempo actual del cliente
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    # Construye el mensaje con la marca de tiempo
    full_message = f"[{timestamp}] {message}"
    
    # Envia el mensaje al servidor como bytes
    client_socket.send(full_message.encode('utf-8'))

def main():
    mi_socket = socket.socket()
    mi_socket.connect(('localhost', 8000))

    while True:
        # Obtiene un mensaje del usuario
        message = input("Escribe un mensaje: ")
        
        # Llama a la función para enviar el mensaje al servidor
        send_message(mi_socket, message)

        # Recibe y muestra la respuesta del servidor
        response = mi_socket.recv(1024)
        print(response.decode('utf-8'))

    # Cierra la conexión con el servidor
    mi_socket.close()

if __name__ == "__main__":
    main()
