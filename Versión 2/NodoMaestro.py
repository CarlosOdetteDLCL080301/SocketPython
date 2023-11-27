import socket
import json
import threading
import random
class NodoMaestro:
    def __init__(self, host, port):
        # Inicializa el nodo maestro con la dirección y puerto especificados,
        # y crea estructuras de datos para el inventario, clientes y un mutex para la exclusión mutua.
        self.host = host
        self.port = port
        self.inventario = {
            # Sucursal de Ecatepec
            "sucursal_ecatepec" : {
                "Fritos": random.randint(0, 100),
                "Cheetos": random.randint(0, 100),
                "Doritos": random.randint(0, 100),
                "Ruffles": random.randint(0, 100),
                "Tostitos": random.randint(0, 100),
                "Sabritas Adobadas": random.randint(0, 100),
                "Rancheritos": random.randint(0, 100),
                "Chocoretas": random.randint(0, 100),
                "Sabritas": random.randint(0, 100),
            },

            # Sucursal de Guadalajara
            "sucursal_guadalajara" : {
                "Fritos": random.randint(0, 100),
                "Cheetos": random.randint(0, 100),
                "Doritos": random.randint(0, 100),
                "Ruffles": random.randint(0, 100),
                "Tostitos": random.randint(0, 100),
                "Sabritas Adobadas": random.randint(0, 100),
                "Rancheritos": random.randint(0, 100),
                "Chocoretas": random.randint(0, 100),
                "Sabritas": random.randint(0, 100),
            },

            # Sucursal de Monterrey
            "sucursal_monterrey" : {
                "Fritos": random.randint(0, 100),
                "Cheetos": random.randint(0, 100),
                "Doritos": random.randint(0, 100),
                "Ruffles": random.randint(0, 100),
                "Tostitos": random.randint(0, 100),
                "Sabritas Adobadas": random.randint(0, 100),
                "Rancheritos": random.randint(0, 100),
                "Chocoretas": random.randint(0, 100),
                "Sabritas": random.randint(0, 100),
            }
        }
        self.clientes = {}
        self.mutex = threading.Lock()

    def iniciar_servidor(self):
        # Inicia el servidor para aceptar conexiones de las sucursales.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.bind((self.host, self.port))
            servidor.listen()
            print(f"Nodo Maestro escuchando en {self.host}:{self.port}")

            while True:
                conexion, direccion = servidor.accept()
                threading.Thread(target=self.atender_cliente, args=(conexion, direccion)).start()

    def atender_cliente(self, conexion, direccion):
        # Atiende a un cliente (sucursal) específico.
        with conexion:
            print(f"Conexión aceptada desde {direccion}")
            while True:
                data = conexion.recv(1024)
                if not data:
                    break
                mensaje = json.loads(data.decode())
                self.procesar_mensaje(mensaje)

    def procesar_mensaje(self, mensaje):
        # Procesa los mensajes recibidos de las sucursales.
        comando = mensaje.get("comando")

        if comando == "agregar_articulo":
            self.agregar_articulo(mensaje["articulo"], mensaje["cantidad"], mensaje["sucursal"])
        elif comando == "comprar_articulo":
            self.comprar_articulo(mensaje["id_cliente"], mensaje["articulo"], mensaje["sucursal"])
        # Agregar más comandos según sea necesario

    def agregar_articulo(self, articulo, cantidad, sucursal):
        # Agrega un artículo al inventario de una sucursal.
        with self.mutex:
            print("--------->>",self.inventario,"\n")
            if sucursal not in self.inventario:
                self.inventario[sucursal] = {}
            if articulo not in self.inventario[sucursal]:
                self.inventario[sucursal][articulo] = 0
            self.inventario[sucursal][articulo] += cantidad
            print(f"Artículo {articulo}{self.inventario[sucursal][articulo]} agregado a la sucursal {sucursal}. Inventario actualizado: {self.inventario}")

    def comprar_articulo(self, id_cliente, articulo, sucursal):
        # Procesa la compra de un artículo, genera la guía de envío y actualiza el inventario.
        with self.mutex:
            if sucursal in self.inventario and articulo in self.inventario[sucursal] and self.inventario[sucursal][articulo] > 0:
                # Realizar la venta y generar la guía de envío
                self.inventario[sucursal][articulo] -= 1
                id_articulo = hash(articulo)
                serie = hash(id_cliente)
                id_envio = f"{id_articulo}_{serie}_{sucursal}_{id_cliente}"
                print(f"Venta realizada. Guía de envío generada: {id_envio}. Inventario actualizado: {self.inventario}")
            else:
                print(f"No hay stock disponible del artículo {articulo} en la sucursal {sucursal}")

if __name__ == "__main__":
    nodo_maestro = NodoMaestro("localhost", 5000)
    nodo_maestro.iniciar_servidor()
