#import socket module
from socket import *
import sys  # In order to terminate the program

# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 80  # You can choose a different port if needed
serverSocket.bind(('', serverPort))  # Bind to the specified port
serverSocket.listen(1)  # Listen for incoming connections

print(f'Server is ready to serve on port {serverPort}...')

while True:
    # Establish the connection
    connectionSocket, addr = serverSocket.accept()
    print(f'Connection established with {addr}')

    try:
        # Receive the HTTP request message from the client
        message = connectionSocket.recv(1024).decode()
        
        if not message:
            connectionSocket.close()
            continue
        
        # Extract the requested filename from the HTTP request
        filename = message.split()[1]
        filepath = filename[1:]  # Remove leading '/'
        
        # Open and read the requested file
        f = open(filepath, 'r')
        outputdata = f.read()
        f.close()
        
        # Send HTTP response header
        responseHeader = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(responseHeader.encode())

        # Send the content of the requested file to the client
        connectionSocket.send(outputdata.encode())
        connectionSocket.send("\r\n".encode())

    except IOError:
        # Send response message for file not found
        errorResponse = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
        errorResponse += "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
        connectionSocket.send(errorResponse.encode())

    # Close client socket
    connectionSocket.close()

# Close the server socket (not reachable in infinite loop)
serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data