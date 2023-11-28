import socket, threading, time
mensaje = {}

def procesarCliente(socketCliente, ipCliente):
    while True:
        try:
            datos = socketCliente.recv(1024)
            if not datos:
                break
            mensaje = datos.decode('utf-8')
            tiempoProcesado = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            print(f"Mensaje de {ipCliente} ({tiempoProcesado}): {mensaje}")
            if ipCliente not in mensaje:
                mensaje[ipCliente] = []
            mensaje[ipCliente].append((tiempoProcesado, mensaje))
            respuesta = f"Mensaje recibido de {ipCliente}"
            socketCliente.send(respuesta.encode('utf-8'))            
        except Exception as error:
            print("Ocurrio un error: {error}")
            break
    socketCliente.close()

def main(miIP):
    socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketServer.bind((miIP, 8000))
    socketServer.listen(5)
    print("Servidor iniciado, esperando clientes...")
    while True:
        socketCliente, ipCliente = socketServer.accept()
        print(f"Nueva conexión establecida con {ipCliente}")
        manejandoCliente = threading.Thread(target=procesarCliente, arg=(socketCliente,ipCliente))
        manejandoCliente.start()

if __name__ == "__main__":
    main("192.168.100.5")