import socket
import json
import threading
import random
plantilla = {}
class NodoMaestro:
    def __init__(self, host, port):
        # Inicializa el nodo maestro con la dirección y puerto especificados,
        # y crea estructuras de datos para el inventario, clientes y un mutex para la exclusión mutua.
        self.host = host
        self.port = port
        self.limitarInventarioMax = 1000
        self.inventarioMaestro = {            
            "Fritos":               random.randint(0, self.limitarInventarioMax),
            "Cheetos":              random.randint(0, self.limitarInventarioMax),
            "Doritos":              random.randint(0, self.limitarInventarioMax),
            "Ruffles":              random.randint(0, self.limitarInventarioMax),
            "Tostitos":             random.randint(0, self.limitarInventarioMax),
            "Sabritas Adobadas":    random.randint(0, self.limitarInventarioMax),
            "Rancheritos":          random.randint(0, self.limitarInventarioMax),
            "Chocoretas":           random.randint(0, self.limitarInventarioMax),
            "Sabritas":             random.randint(0, self.limitarInventarioMax),
        }
        self.inventario = {}
        self.clientes = {}
        self.mutex = threading.Lock()

    def iniciar_servidor(self):
        # Inicia el servidor para aceptar conexiones de las sucursales.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.bind((self.host, self.port))
            servidor.listen()
            print(f"Nodo Maestro escuchando en {self.host}:{self.port}")
            print(self.inventarioMaestro)
            while True:
                conexion, direccion = servidor.accept()
                threading.Thread(target=self.atender_cliente, args=(conexion, direccion)).start()

    def distribuirAutomaticamente(self):
        
        for producto, cantidad in self.inventarioMaestro.items():
            if len(self.inventario) != 0:
                for sucursal in self.inventario:
                    self.inventario[sucursal][producto] = 0

        print("DISTRIBUIR")
        for producto, cantidad in self.inventarioMaestro.items():
            #print(f"producto {producto}, cantidad {cantidad}")
            if len(self.inventario) != 0:
                cantidad_por_sucursal = cantidad // len(self.inventario)
                #print(f"cantidad_por_sucursal {cantidad_por_sucursal} = cantidad {cantidad}// len(self.inventario) {len(self.inventario)}")
                for sucursal in self.inventario:
                    print(f"self.inventario[sucursal {sucursal}][producto {producto}]{self.inventario[sucursal][producto]} += cantidad_por_sucursal {cantidad_por_sucursal}")
                    self.inventario[sucursal][producto] += cantidad_por_sucursal
                self.inventario[sucursal][producto] += cantidad%len(self.inventario)
        print(self.inventario)               
        
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
        elif comando == "agregar_sucursal":
            self.agregar_sucursal(mensaje["sucursal"])
        # Agregar más comandos según sea necesario
    
    #Creamos una función, unicamente para considerarlo para el inventario 
    def agregar_sucursal(self, sucursal):
        self.inventario[sucursal] = {
            "Fritos": 0,
                "Cheetos": 0,
                "Doritos": 0,
                "Ruffles": 0,
                "Tostitos": 0,
                "Sabritas Adobadas": 0,
                "Rancheritos": 0,
                "Chocoretas": 0,
                "Sabritas": 0,
        }
        self.distribuirAutomaticamente()

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
