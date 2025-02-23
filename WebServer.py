#import socket module
from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)
# creates a server socket using internet protocols and http requests

#Prepare a server socket

serverSocket.bind(('', 8080))
serverSocket.listen(1)

while True:
# continues to serve incoming http requests
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    # the server accepts incoming connections and returns the address
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        # parses http for filename in terminal at index 1 as a string
        f = open(filename[1:])
        # opens requested file
        outputdata = f.readlines()
        # reads lines in the file

        #Send one HTTP header line into socket

        connectionSocket.send("HTTP/1.1 200 OK\r\n")
        connectionSocket.send("Content-Type: text/html\r\n\r\n")

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
            
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    
    except IOError:
        #Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n")
        connectionSocket.send("Content-Type: text/html\r\n\r\n")
        #Close client socket       
        connectionSocket.close() 

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
