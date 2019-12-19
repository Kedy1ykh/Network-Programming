#!usr/bin/python
import socket
import select
import sys
from thread import *

"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with 
any two hosts. The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in 
a continuoues flow."""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# checks whether sufficient arguments have been provided
if len(sys.argv) < 3:
    print "Invalid input.\n"
    print "eg: Server.py <ip> <port>"
    sys.exit()

# takes the first argument from command prompt as IP address
HOST = str(sys.argv[1])
# takes second argument from command prompt as port number
PORT = str(sys.argv[2])

""""binds the server to an entered IP address and at the 
specified port number.
The client must be aware of these parameters"""
try:
    server.bind((HOST, PORT))
except socket.error, msg:
    print "Bind failed. Error code: " + str(msg[0]) + " Message" + msg[1]
    sys.exit()
    
print "Socket bind completed"

""""listens for numbers(10) of active connections. This number can be
increased as per convenience."""

server.listen(10)

list_of_clients = []

def clientthread(conn, addr):

    # Welcome user
    conn.send("Welcome to this chat room")
    
    while True:
        try:
            message = conn.recv(2048)
            if message:
                """prints the message and address of the 
                users who just sent the message on the server
                terminal"""
                print "<" + addr[0] + "> " + message
                
                # Calls broadcast function to send message
                message_to_send = "<" + addr[0] + "> " + m
                broadcast(message_to_send, conn)
                
            else:
                """message may have no content if the conn 
                is broken, in this case we remove the conn"""
                remove(conn)
        except:
            continue

"""Using the function below, we broadcast the message to all 
clients who's object is not the same as the one sending
the message"""
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    """Accepts a connection request and stores two parameters,
    conn which is a socket object for that user, and addr
    which contains the IP address of the client that just connected"""
    conn, addr = server.accept()
    
    """Maintains a list of clients for ease of broadcasting 
    a message to all available people in the chatroom"""
    list_of_clients.append(conn)
    
    #prints the address of the user that just connected
    print addr[0] + "connected"
    
    #creates an individual thread for every user
    # that connects
    start_new_thread(clientthread, (conn,addr))

conn.close()
server.close()