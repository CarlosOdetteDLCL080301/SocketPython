import socket,time

def enviar_mensaje(socketCliente, mensaje):
    tiempoProcesado = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    mensajeCompleto = f"[{tiempoProcesado}] {mensaje}"
    socketCliente.send(mensajeCompleto.encode('utf-8'))

def main(IP_aContectar):
    miSocket = socket.socket()
    miSocket.connect((IP_aContectar,800))
    while True:
        mensaje = input("Escribe un mensaje: ")
        try:
            enviar_mensaje(miSocket,mensaje)
            respuesta = miSocket.recv(1024)
            print(respuesta.decode('utf-8'))
        except:
            print("Se interrumpio la conexion con el servidor")
            break
    miSocket.close()

if __name__ == "__main__":
    main("localhost")