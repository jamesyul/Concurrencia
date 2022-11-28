#se importa las librerias de subprocesos y socket
import threading
import socket

host='127.0.0.1'
port=5900

#se crea un objeto para el servidor
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#se vincula el servidor con el host y el puerto
server.bind((host, port))

#se activa el modo de escucha oara cualquier servidor
server.listen()
#se crea una lista vacía para clientes
clients=[]
#se crea una lista vacía para nicknames
nicknames=[]

#función que envia un mensaje desde el servidor a todos los clientes conectados
def broadcast(message):
    for client in clients:
        client.send(message)

#función que maneja los clientes
def handle_client(client):
    while True:
        try:
            message=client.recv(1024)#el mensaje será igual al cliente coon un máximo de 1024 bytes
            broadcast(message)
        except:#en caso de error se identifica el cliente del que debemos deshacernos
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            broadcast(f'{nickname} abandono el chat'.encode('utf-8'))
            nicknames.remove(nickname)
            break#salir del bucle al eliminar con exito el cliente

#funcion principal para recibir las conexiones del cliente
def receive():
    while True:
        print('Servidor inicializando y escuchando....')
        client, address=server.accept()#se configura el cliente en la direccion del servidor, el metodo se ejecuta constantemente
        #además que el metodo accept devuelve el metodo socket que representa la conexión 
        print(f'conexion establecida con {str(address)}')
        client.send('nickname?'.encode('utf-8'))
        nickname=client.recv(1024)#se crea un nickname con la informacion recibida
        nicknames.append(nickname)
        clients.append(client)
        print(f'El nickname del usuario es {nickname}'.encode('utf-8'))
        broadcast(f'{nickname} se conecto a al sala de chat'.encode('utf-8'))
        client.send('tu estas conectado'.encode('utf-8'))#se envia un mensaje desde el servidor al cliente
        thread=threading.Thread(target=handle_client, args=(client,))#
        thread.start()

if __name__=="__main__":
    receive()