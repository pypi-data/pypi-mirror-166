import ipaddress
from threading import Thread
from typing import Callable, Tuple, Any
from sockTCPReader import sockTCPReader, socket

class tcpWebServer(object):
    def __init__(self, address: tuple | Tuple[ipaddress.IPv4Address, int], func_sensitived : None | Any = None) -> None:
        self.__address__ = address
        self.__f_sensitive__ = func_sensitived
        self.__sock__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __1_comunication__ (s: socket.socket, a : Tuple[str, int], f: Callable | None):
        if f:
            f(s, a)
            try:
                s.close()
            except:
                return None
        else:
            sockTCPReader.sent(s, 'Hello')
            s.close()
            return None

    def runserver_loop(self):
        self.__sock__.bind(self.__address__)
        self.__sock__.listen()
        while True:
            s, ra = self.__sock__.accept()
            Thread(target=tcpWebServer.__1_comunication__, args=(s, ra, self.__f_sensitive__)).start()

if __name__ == "__main__":
    def b(s:socket.socket, *args):
        print(sockTCPReader.recv(s))
        sockTCPReader.sent(s, 'Hello')
        s.close()
    a = tcpWebServer(('127.0.0.1', 1234), b)
    a.runserver_loop()
    