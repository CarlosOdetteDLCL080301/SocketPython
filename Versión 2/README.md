# Segundo y último entregable, Sistemas Distribuidos, Grupo 5, 24-1
__Diseña y codifica un sistema distribuido de inventario y logística que cumpla con las siguientes características:__
* [x] Que el nodo maestro distribuya automáticamente los artículos entre las sucursales
(nodos).
* [ ] Que se pueda consultar y actualizar la lista de clientes *DISTRIBUIDA* en cualquier sucursal.
* [ ] Que se pueda comprar un artículo de cualquier sucursal (exclusión mutua).
    * Antes de vender un artículo debe de haber exclusión mutua, para no venderlo 2
veces.
* [ ] Que se pueda comprar un artículo de cualquier sucursal (exclusión mutua).
Que “genere” y guarde la guía de envío (**IDARTICULO**+**SERIE**+**SUCURSAL**+**IDCLIENTE**) y la
descuente del inventario general *DISTRIBUIDO*.
* [ ] Que se pueda comprar un artículo de cualquier sucursal (exclusión mutua).
Que se pueda agregar artículos al inventario general *DISTRIBUIDO* desde cualquier
sucursal y los distribuya equitativamente, revisando que sucursal tiene mayor espacio.
* [ ] Que se pueda comprar un artículo de cualquier sucursal (exclusión mutua).
Cada actualización a los datos de inventario, clientes, etc. debe de haber consenso.
* [ ] Que se pueda comprar un artículo de cualquier sucursal (exclusión mutua).
Si una sucursal tiene falla de sistema debe redistribuir los artículos a las demás y actualizar
la información.
* [ ] Que se pueda comprar un artículo de cualquier sucursal (exclusión mutua).
Si el nodo maestro falla, debe de haber elección.