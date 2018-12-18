from socket import AF_INET, socket, SOCK_STREAM
import threading

"""
CS410 Final Project
Sara, Jordan, and Ethan
Server code written by Ethan
"""


#define globals
clients = {}
addresses = {}
HOST = ''
PORT = 12345
SIZE = 1024

def listen():
    #wait for incoming connections, start client dialog in a new thread
    print("listening for connection...")
    s.listen(5)
    while True:
        c, addr = s.accept()
        addresses[c] = addr
        print("Client @%s:%s Connected" % addr)
        c.send(bytes("SERVER: Please enter your username in the textbox.","utf8"))
        threading.Thread(target = listenToClient, args = (c, addr)).start()

def listenToClient(c, addr):
    #get username and send welcome messages
    name = c.recv(SIZE).decode("utf8")
    clients[c] = name
    cltString = activeClients()
    shareMessage(bytes(cltString,"utf8"))
    print(cltString)
    shareMessage(bytes("Welcome to the chat %s! Type {QUIT} to close program. Use @username to send private messages." % name, "utf8"),"SERVER",name)
    targetSet=False
    while True:
        data = c.recv(SIZE)
        if data:
            #check to see if msg is a private message directed @target user
            msg = data.decode("utf8")
            if msg[0] == "@":
                target = msg[1:]
                print("target: ", target)
                targetSet = True
            elif msg == "{QUIT}":
                #remove disconnecting client
                print("client "+name+" disconnected")
                del clients[c]
                cltString = activeClients()
                print(cltString)
                shareMessage(bytes(cltString,"utf8"))
                shareMessage(bytes("%s has left the chat." % name, "utf8"),"SERVER")
                c.close()
                break
            else:
				#broadcast msg
                shareMessage(data, name)
            while targetSet:
				#send next msg to target
                data = c.recv(SIZE)
                if data:
                    shareMessage(data, name, target)
                    targetSet = False

def shareMessage(message, name="",target=""):
	#send message to recipients
    #listClients()
    header = ""
    if name != "":
        header = name+": "
    if target != "":
        #send only to target user and sender.
        if validTarget(target): #make sure target user exists
            for c in clients:
                if clients[c] == target or clients[c] == name:
                    c.send(bytes(header,"utf8")+message)
        else:
			#send invalid target message back to sender
            message = bytes("Invalid target user.","utf8")
            header = "SERVER: "
            for c in clients:
                if clients[c] == name:
                    c.send(bytes(header,"utf8")+message)

    else:
        #broadcast message
        for c in clients:
            c.send(bytes(header,"utf8")+message)

def activeClients():
	#send string with all client names for Tkinter window
    str = ">"
    for c in clients:
        str = str + clients[c]+">"
    return str

def validTarget(target):
	#make sure target user exists
    valid = False
    for c in clients:
        if clients[c]==target:
            valid = True
    return valid



if __name__ == "__main__":
    #bind socket, start listening
    s = socket(AF_INET, SOCK_STREAM)
    ADDRESS = (HOST, PORT)
    s.bind(ADDRESS)
    listen()
