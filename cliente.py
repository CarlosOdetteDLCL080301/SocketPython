# Importamos la biblioteca 'socket' para habilitar la comunicación de red, 
# el cual nos permite la creación y el uso de sockets para la comunicación entre
# el cliente y el servidor.
import socket

# Importamos la biblioteca 'time' para trabajar con funciones relacionadas con el tiempo,
# en este caso, se utiliza para obtener la marca de tiempo actual y formatearla.
import time


# Función para enviar mensajes al servidor
def enviar_mensaje(socketCliente, mensaje):
    # Obtiene la marca de tiempo actual del cliente
    tiempoProcesado = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    # Construye el mensaje concatenando la marca de tiempo con el mensaje original
    mensajeCompleto = f"[{tiempoProcesado}] {mensaje}"
    
    # Envia el mensaje al servidor como bytes codificados en UTF-8
    socketCliente.send(mensajeCompleto.encode('utf-8'))


def main():
    # Crea un nuevo socket del cliente
    miSocket = socket.socket()
    
    # Establece una conexión con el servidor en localhost y el puerto 8000
    miSocket.connect(('localhost', 8000))

    while True:
        # Obtiene un mensaje ingresado por el usuario
        mensaje = input("Escribe un mensaje: ")
        
        # Llama a la función 'enviar_mensaje' para enviar el mensaje al servidor
        enviar_mensaje(miSocket, mensaje)

        # Recibe una respuesta del servidor (hasta 1024 bytes) y la decodifica
        respuesta = miSocket.recv(1024)
        print(respuesta.decode('utf-8'))

    # Cierra la conexión con el servidor
    miSocket.close()


if __name__ == "__main__":
    # Verifica si este archivo se está ejecutando como un programa independiente
    # y no está siendo importado como un módulo en otro programa.
    # Si es el programa principal, ejecuta la función 'main()'.
    main()
