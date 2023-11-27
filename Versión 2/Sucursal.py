import socket
import json

class NodoSucursal:
    def __init__(self, host, port, sucursal):
        # Inicializa la sucursal con la dirección, puerto y nombre de sucursal especificados.
        self.host = host
        self.port = port
        self.sucursal = sucursal

    def conectar_a_maestro(self, mensaje):
        # Establece una conexión con el nodo maestro y envía un mensaje.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect(("localhost", 5000))
            cliente.sendall(json.dumps(mensaje).encode())

    def agregar_articulo(self, articulo, cantidad):
        # Envía un mensaje al nodo maestro para agregar un artículo al inventario de la sucursal.
        mensaje = {
            "comando": "agregar_articulo",
            "articulo": articulo,
            "cantidad": cantidad,
            "sucursal": self.sucursal
        }
        self.conectar_a_maestro(mensaje)

    def comprar_articulo(self, id_cliente, articulo):
        # Envía un mensaje al nodo maestro para realizar una compra de un artículo.
        mensaje = {
            "comando": "comprar_articulo",
            "id_cliente": id_cliente,
            "articulo": articulo,
            "sucursal": self.sucursal
        }
        self.conectar_a_maestro(mensaje)

if __name__ == "__main__":
    sucursal_a = NodoSucursal("localhost", 5001, "sucursal_ecatepec")
    sucursal_b = NodoSucursal("localhost", 5002, "sucursal_guadalajara")

    sucursal_b.agregar_articulo("Fritos", 20)
    #sucursal_a.comprar_articulo("Cliente1", "Producto1")
