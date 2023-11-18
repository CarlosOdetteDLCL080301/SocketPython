import socket
import threading
import time

mensajes = {}
#ip_servidor = "192.168.91.130"  # Cambia la IP del servidor según tus necesidades

def escribir_diccionario_en_archivo(diccionario, nombre_archivo):
    """
    Escribe el contenido de un diccionario en un archivo de texto.

    :param diccionario: El diccionario a escribir en el archivo.
    :type diccionario: dict
    :param nombre_archivo: El nombre del archivo de texto a crear o sobrescribir.
    :type nombre_archivo: str
    """
    with open(nombre_archivo, 'w') as archivo:
        for clave, valor in diccionario.items():
            archivo.write(f"{clave}: {valor}\n")


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
            mensajes[ipCliente].append((mensaje))

            # Envia una respuesta al cliente confirmando la recepción del mensaje
            respuesta = f"Mensaje recibido de {ipCliente}"
            socketCliente.send(respuesta.encode('utf-8'))
            print(f"Mensaje {mensaje}")
            
            # Cierra la conexión con el cliente una vez que se completa la comunicación
            socketCliente.close()
            
            if ("FIN" in mensaje):
                print("Se recibio un mensaje para finalizar el servidor")
                break
        except Exception as error:
            # Si ocurre un error, se muestra en la consola y se sale del bucle
            print(f"Ocurrió un error: {error}")
            break




def iniciar_servidor():
    socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Aqui debemos cambiarlo por nuestro ip
    ip_servidor = "localhost"
    socketServer.bind((ip_servidor, 8000))
    socketServer.listen(5)
    print("Servidor esperando conexiones...")

    while True:
        socketCliente, ipCliente = socketServer.accept()
        print(f"Nueva conexión establecida con {ipCliente}")
        manejandoCliente = threading.Thread(target=procesarCliente, args=(socketCliente, ipCliente))
        manejandoCliente.start()

# Función para enviar mensajes al servidor
def enviar_mensaje(socketCliente, mensaje):
    # Obtiene la marca de tiempo actual del cliente
    tiempoProcesado = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    # Construye el mensaje concatenando la marca de tiempo con el mensaje original
    mensajeCompleto = f"[{tiempoProcesado}] {mensaje}"
    
    # Envia el mensaje al servidor como bytes codificados en UTF-8
    socketCliente.send(mensajeCompleto.encode('utf-8'))


# Función para enviar mensajes a otro servidor
def enviar_mensaje_a_servidor(ip_destino, mensaje):
    miSocket = socket.socket()
    miSocket.connect((str(ip_destino), 8000))
    try:
        enviar_mensaje(miSocket, mensaje)
        respuesta = miSocket.recv(1024)
        print(respuesta.decode('utf-8'))
    except ConnectionResetError as error:
        print("No se pudo enviar el mensaje al servidor destino:", error)
    miSocket.close()

def main():
    # Iniciar el servidor en un hilo separado
    servidor_thread = threading.Thread(target=iniciar_servidor)
    servidor_thread.start()

    while True:
        print("Opciones:")
        print("1. Enviar mensaje a otro servidor")
        print("2. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            ip_destino = input("Ingresa la dirección IP de destino: ")
            mensaje = input("Escribe el mensaje: ")
            enviar_mensaje_a_servidor(ip_destino, mensaje)
        elif opcion == "2":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")

if __name__ == "__main__":
    main()
