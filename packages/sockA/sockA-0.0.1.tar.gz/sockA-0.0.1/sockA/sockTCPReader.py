import socket

class sockTCPReader(object):
    def recv(s:socket.socket, b : int = 2048, f : int = 0):
        r = b""
        while True:
            tmp = s.recv(b, f)
            r += tmp
            if len(tmp) < b:
                break
        return r.decode()
        pass

    def sent(s:socket.socket, d: bytes | str):
        if type(d) is str:
            d = d.encode()
        try:
            s.send(d)
            return 1
        except:
            return 0
