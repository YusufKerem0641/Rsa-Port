import socket , datetime
from RSA import Rsa ,SocketPort

class baglanmaClient():
    n = e = 0
    rsa = Rsa()
    socketPort = 0
    def __init__(self,IP,PORT,limit):

        self.IP = IP #"192.168.1.99"
        self.PORT = PORT #8093
        now = datetime.datetime.now()
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect((IP, PORT))
        self.socketPort = SocketPort(socket1,limit)
        data = self.socketPort.recve1().decode("utf-8")
        RsaData = data[6:]
        self.socketPort.n,self.socketPort.e = RsaData.split(",")
        self.socketPort.senddatalen(f"Rsa : {str(self.socketPort.rsa.n)},{str(self.socketPort.rsa.e)}")
        metin = f"Giris Yapildi : {now.day}.{now.month}.{now.year} {now.hour}:{now.minute} \n"
        self.socketPort.senddatalen(metin)

    def recv(self):
        return self.socketPort.recve1()
    def send(self,data):
        self.socketPort.senddatalen(data)

if __name__ == '__main__':
    limit = 100 # limit rsa asal sayıları için kullanılır
    client = baglanmaClient("192.168.1.99",8093,limit)
    print(client.recv())
    client.send("iyi")