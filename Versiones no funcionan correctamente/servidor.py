# Importa la biblioteca 'socket' para habilitar la comunicación de red, 
# lo que permite la creación y el uso de sockets para establecer conexiones
# y transmitir datos entre el cliente y el servidor.
import socket

# Importa la biblioteca 'threading' que proporciona herramientas para trabajar
# con subprocesos, lo que permite manejar múltiples conexiones de clientes de forma concurrente.
import threading

# Importa la biblioteca 'time' para trabajar con funciones relacionadas con el tiempo,
# como la obtención de la marca de tiempo actual, que se utiliza en la función de manejo
# de clientes para marcar los mensajes con la hora en que se enviaron.
import time


# Diccionario para almacenar los mensajes de los clientes
mensajes = {}

def procesarCliente(socketCliente, ipCliente):
    while True:
        try:
            # Recibe datos enviados por el cliente (hasta 1024 bytes)
            datos = socketCliente.recv(1024)
            
            # Si no se recibe ningún dato, se sale del bucle
            if not datos:
                break

            # Decodifica los datos recibidos en formato UTF-8 para obtener el mensaje
            mensaje = datos.decode('utf-8')
            
            # Obtiene la marca de tiempo actual del servidor
            tiempoProcesado = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            # Muestra el mensaje del cliente junto con la marca de tiempo y su dirección
            print(f"Mensaje de {ipCliente} ({tiempoProcesado}): {mensaje}")

            # Almacena el mensaje en el diccionario de mensajes
            if ipCliente not in mensajes:
                mensajes[ipCliente] = []
            mensajes[ipCliente].append((tiempoProcesado, mensaje))

            # Envia una respuesta al cliente confirmando la recepción del mensaje
            respuesta = f"Mensaje recibido de {ipCliente}"
            socketCliente.send(respuesta.encode('utf-8'))

        except Exception as error:
            # Si ocurre un error, se muestra en la consola y se sale del bucle
            print(f"Ocurrió un error: {error}")
            break

    # Cierra la conexión con el cliente una vez que se completa la comunicación
    socketCliente.close()


def main():
    # Crea un socket de tipo AF_INET (IPv4) y SOCK_STREAM (TCP)
    socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enlaza el socket al localhost en el puerto 8000
    # En el caso para obtener este ip, lo conseguimos usando 
    # el comando ipconfig en la terminal de windows
    socketServer.bind(('192.168.100.5', 8000))

    # Escucha hasta 5 conexiones entrantes en el socket
    socketServer.listen(5)
    print("Servidor esperando conexiones...")

    while True:
        # Acepta una conexión entrante y obtiene el socket del cliente y su dirección
        socketCliente, ipCliente = socketServer.accept()
        print(f"Nueva conexión establecida con {ipCliente}")

        # Inicia un subproceso para manejar al cliente
        manejandoCliente = threading.Thread(target=procesarCliente, args=(socketCliente, ipCliente))
        manejandoCliente.start()


if __name__ == "__main__":
    # Verifica si este archivo se está ejecutando como un programa independiente
    # y no está siendo importado como un módulo en otro programa.
    # Si es el programa principal, ejecuta la función 'main()'.
    main()
