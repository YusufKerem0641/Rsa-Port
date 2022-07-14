import socket
from multiprocessing.dummy import Process
from random import randint
from RSA import Rsa ,SocketPort

class baglanmaServer():
    clients = []
    n = e = 0
    rsa = Rsa()
    # server portu açar ve bağlan çihazları kullanıcının oluşturdupu sınıfa gönderir
    def __init__(self,IP,PORT,sinif,limit): # "192.168.1.99" # 8093
        server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket1.bind((IP, PORT))
        server_socket1.listen(5)
        while True:
            client_socket, client_addres = server_socket1.accept()
            socketPort = SocketPort(client_socket,limit)
            n, e = socketPort.rsa.n, socketPort.rsa.e
            print(f"socket {client_addres} baglandi")
            socketPort.senddatalen(f"Rsa : {str(n)},{str(e)}")
            socketPort.n = 1 # sifreyi çözmesi için gerekli yoksa lag oluyor
            data = socketPort.recve1()
            RsaData = data[6:]
            socketPort.n, socketPort.e = RsaData.split(",")
            print("sifre",data)
            bagliSocketProcess = Process(target=sinif, args = (client_socket,client_addres,socketPort))
            bagliSocketProcess.daemon = True
            bagliSocketProcess.start()
            self.clients.append(bagliSocketProcess)

def bagliSocket(client_socket, client_addres, socketServerClient):
    data = socketServerClient.recve1()
    print(data)
    socketServerClient.senddatalen("naber")
    print(socketServerClient.recve1())
if __name__ == '__main__':
    # bir sınıf göndererek port bağlandıktan sonra ne yapacağını belirliyoruz
    limit = 100#rsa için asal sayı limit
    server=baglanmaServer("192.168.1.99",8093,bagliSocket,limit)

