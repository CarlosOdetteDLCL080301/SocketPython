# Importamos la biblioteca 'socket' para habilitar la comunicación de red, 
# el cual nos permite la creación y el uso de sockets para la comunicación entre
# el cliente y el servidor.
import socket

# Importamos la biblioteca 'time' para trabajar con funciones relacionadas con el tiempo,
# en este caso, se utiliza para obtener la marca de tiempo actual y formatearla.
import time

def guardar_ip_y_mensaje(ip, mensaje):
    # Abre el archivo en modo de escritura con la opción de agregar ('a' para append)
    with open('registro_ip.txt', 'a') as archivo:
        # Concatena la dirección IP y el mensaje en una sola cadena
        entrada = f"IP: {ip}, Mensaje: {mensaje}\n"
        
        # Escribe la entrada en el archivo
        archivo.write(entrada)

# Función para enviar mensajes al servidor
def enviar_mensaje(socketCliente, mensaje):
    # Obtiene la marca de tiempo actual del cliente
    tiempoProcesado = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    # Construye el mensaje concatenando la marca de tiempo con el mensaje original
    mensajeCompleto = f"[{tiempoProcesado}] {mensaje}"
    
    # Envia el mensaje al servidor como bytes codificados en UTF-8
    socketCliente.send(mensajeCompleto.encode('utf-8'))


def main(ip):
    # Crea un nuevo socket del cliente
    miSocket = socket.socket()
    
    # Establece una conexión con el servidor en localhost y el puerto 8000
    miSocket.connect((str(ip), 8000))

    while True:
        # Obtiene un mensaje ingresado por el usuario
        mensaje = input("Escribe un mensaje: ")
        #Se agrego un try - except, ya que se considera el caso en el que el servidor se desconecta a mitad
        #del proceso, así que es mejor tambien finalizar la actividad del cliente con el servidor. 
        try:
            # Llama a la función 'enviar_mensaje' para enviar el mensaje al servidor
            enviar_mensaje(miSocket, mensaje)

            # Recibe una respuesta del servidor (hasta 1024 bytes) y la decodifica
            respuesta = miSocket.recv(1024)
            print(respuesta.decode('utf-8'))
            guardar_ip_y_mensaje(str(ip),mensaje)
            #agregar todos los mensajes,que se envian desde este I, y los almacena en un diccionario, donde unicamente aparrezca el IP y el mensaje referen
        #Cuando se interrumpe la comunicación con el servidor, se finaliza la petición de más mensajes
        #y esto provoca que el programa al igual finalice de este lado. 
        except ConnectionResetError as error:
            print("Se interrumpio la conexión con el servidor")
            break

    # Cierra la conexión con el servidor
    miSocket.close()


if __name__ == "__main__":
    # Verifica si este archivo se está ejecutando como un programa independiente
    # y no está siendo importado como un módulo en otro programa.
    # Si es el programa principal, ejecuta la función 'main()'.
    main("192.168.91.130")
