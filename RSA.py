from random import randint
import socket
class Rsa():
    p = q = n = e = fi = d = 0
    def asalSayi(self,limit): # asal sayı oluşturur
        asalSayilar = []
        for i in range(2, limit):
            asal = True
            for k in asalSayilar:
                if i % k == 0:
                    asal = False
                    break
            if asal:
                asalSayilar.append(i)
        return asalSayilar
    def arasindaAsalmi(self,sayi1,sayi2):
        bolenSayi = 2
        asalSayilar = []

        # aşağıdaki döngüde sayi1'in asal çarpımlarına ayırır
        while True:

            if sayi1 < bolenSayi:
                break

            if sayi1 % bolenSayi == 0:
                asal = True
                for i in asalSayilar:
                    if bolenSayi % i == 0:
                        asal = False

                if asal:
                    asalSayilar.append(bolenSayi)

            bolenSayi += 1

        # sayi2 asal çarpanlara bölünüyormu diye bakılır
        for i in asalSayilar:
            if sayi2 % i == 0:
                return False
        return True

    def baslangic(self,limit):
        asalSayilar = Rsa.asalSayi(self,limit)
        pr = randint(6, len(asalSayilar)-1)
        qr = randint(6, len(asalSayilar)-1)
        while True:
            if pr != qr: # aralarında asal olana kadar çalışşın diye
                self.p = int(asalSayilar[pr])
                self.q = int(asalSayilar[qr])
                break

            else:
                pr = randint(0, len(asalSayilar)-1)

        self.n = self.q * self.p
        self.fi = (self.p - 1) * (self.q - 1)
        while True:
            self.e = int(asalSayilar[randint(6, len(asalSayilar)-1)])
            if Rsa.arasindaAsalmi(self,self.e,self.fi): # aralarında asal olana kadar çalışşın diye
                break
        self.d = 1
        while True:
            self.d += self.fi
            if self.d % self.e == 0:
                self.d = int(self.d/self.e)
                break
    def alNandE(self):
        return [self.n,self.e]

    def sifreleme(self,m1,e,n):
        # şifrelenecek mesaj
        cString=""
        for i in m1:
            c = ord(i) ** int(e) % int(n)
            cString += str(c) + ","
        return cString
    def sifreCozme(self,c):
        mString=""
        c = c.split(",")[:-1]
        for i in c:
            m = int(i) ** int(self.d) % int(self.n)
            mString += chr(m)
        return mString

class SocketPort():
    n = e = 0
    rsa = Rsa()
    client_socket=socket.socket()
    def __init__(self,client_socket,limit):
        self.rsa.baslangic(limit)
        self.client_socket = client_socket
        n, e = self.rsa.alNandE()
        print(n, e)
    #şifreli bir biçimde veri gönderir
    def senddatalen(self,data,bytemi=False):
        if self.n != 0 and self.e != 0:
            data = Rsa.sifreleme(Rsa,data,self.e,self.n)
        if not bytemi:
            self.client_socket.send((str(len(data.encode("utf-8"))).ljust(11)+data).encode("utf-8"))
        else:
            self.client_socket.send(str(len(data)).ljust(11).encode("utf-8") + data)

    #şifreli mesajı alır ve şifresini çözer
    def recve1(self,byteall=1024):
        datafile = b""
        header = self.client_socket.recv(11).decode("utf-8")
        if header != "":
            while True:
                if len(header) == 11:
                    break
                print("demekki oluyormus arada")
                header = header + self.client_socket.recv(11-len(header)).decode("utf-8")
            if int(header) > byteall:
                while True:
                    print("gelen data", len(datafile), "olmasi gereken", header)
                    if (int(header)-len(datafile)) // byteall != 0:
                        datafile = datafile + self.client_socket.recv(byteall)
                    if (int(header)-len(datafile)) % byteall != 0:
                        ilkbyte = (int(header)-len(datafile)) % byteall
                        datafile = datafile + self.client_socket.recv(ilkbyte)
                    if len(datafile) == int(header):
                        break
            else:
                datafile = datafile + self.client_socket.recv(int(header))
                while len(datafile) != int(header):
                    print(len(datafile))
                    datafile = datafile + self.client_socket.recv(int(header)-len(datafile))
            print("gelen data", len(datafile),"olmasi gereken",header)
            print(datafile,len(datafile))
            if (self.rsa.n != 0 and self.rsa.e != 0) and (self.n != 0):
                datafile = self.rsa.sifreCozme(datafile.decode("utf-8"))

            return datafile
