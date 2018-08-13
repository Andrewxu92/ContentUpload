#import thread
#import socket

if (__name__ == "__main__"):
        import socket
        print ("server is starting")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#bind your local IP address, not public, not source
        sock.bind(('', 9001))
        sock.listen(5)
        print("server is listening port 9001")
        while (1):
                connection, address = sock.accept()
                try:
                        connection.settimeout(50)
                        while (1):
                                buf = connection.recv(1024)
                                if (buf):
                                        
                                        print(buf)
                                else:
                                        break
                except socket.timeout:
                        print ("time out")

                connection.close()
                print ("closing")

