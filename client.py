#se importa las librerías de subprocesos y socket
import threading
import socket

#se obtiene un nickname en forma de entrada
nickname=input('Ingrese su nickname: ')
#se crea un objeto de cliente
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#se vincula un cliente a un host y puerto
client.connect(('127.0.0.1', 5900))

#funcion para recibir mensajes de otros clientes a traves del servidor
def client_receive():
    while True:
        try:
            message=client.recv(1024).decode('utf-8')
            if message=="nickname?":
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error')
            client.close()
            break

#funcion para enviar mensajes de otros clientes a traves del servidor
def client_send():
    while True:
        message=f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

#se crea el subproceso para que el cliente reciba
receive_thread=threading.Thread(target=client_receive)
receive_thread.start()

#se crea el subproceso para que el cliente envie
send_thread=threading.Thread(target=client_send)
send_thread.start()