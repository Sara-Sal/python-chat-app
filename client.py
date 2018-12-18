from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

s = socket(AF_INET, SOCK_STREAM)
HOST = "127.0.0.1"  #change to IP address of machine hosting the server

PORT = 12345
SIZE = 1024

ADDRESS = (HOST, PORT)



def recceive_message():
    while True:
        try:
            message = s.recv(SIZE).decode("utf8")
            if message[0] == '>':
                usrs = message[1:].split(">")
                if usrs[-1] != "":
                    message = usrs[-1]
                    usrs = usrs[:-1]
                    message_list.insert(tkinter.END, message)
                print("active users:")
                connected_Listbox.delete(0,tkinter.END)
                for u in usrs:
                    connected_Listbox.insert(tkinter.END, u)
                    print(u)
            else:
                message_list.insert(tkinter.END, message)
        except OSError:
            break

def send_message( event = None):
    message = user_message.get()
    targetSet = False
    if message[0] == "@":
        ms = ""
        target = ""
        for ch in message:
            if not targetSet:
                if ch != ' ':
                    target = target + ch
                else:
                    print("target: "+target)
                    targetSet = True
            else:
                ms = ms + ch
        message = ms


    user_message.set("")
    if targetSet:
        s.send(bytes(target, "utf8"))
    s.send(bytes(message, "utf8"))
    if message == "{QUIT}":
        s.close()
        Title.quit()

def closing(event = None):
    user_message.set("{QUIT}")
    send_message()





Title = tkinter.Tk()
Title.title("410 Chat Program")

#create distinct frames for messages and connected users
messages_frame = tkinter.Frame(Title)
connected_frame = tkinter.Frame(Title)

user_message = tkinter.StringVar()# For the messages to be sent.
find_user = tkinter.StringVar()


user_message.set("Type your messages here.")
find_user.set("Search for User here.")

#create the structure of the frames
connected_Listbox = tkinter.Listbox(connected_frame)
scrollbar = tkinter.Scrollbar(messages_frame)
connected_scrollbar = tkinter.Scrollbar(connected_frame)
message_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
connected_label = tkinter.Label(connected_frame, text="Connected", bg="maroon", fg="white")

#pack the structure into the frames
connected_frame.pack(side=tkinter.RIGHT)
connected_scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)
connected_Listbox.pack(side = tkinter.BOTTOM, fill = tkinter.BOTH)
connected_label.pack(side = tkinter.TOP)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_list.pack(side=tkinter.TOP, fill=tkinter.BOTH)
message_list.pack()
messages_frame.pack(side = tkinter.LEFT)

#user interface portion: text box and send button
entry_field = tkinter.Entry(messages_frame, textvariable = user_message)
entry_field.bind("<Return>", send_message)
entry_field.pack(side = tkinter.BOTTOM)
send_button = tkinter.Button(messages_frame, text = "Send", command = send_message)
send_button.pack(side = tkinter.BOTTOM)

Title.protocol("WM_DELETE_WINDOW", closing)

s.connect(ADDRESS)


receive_thread = Thread(target = recceive_message)
receive_thread.start()
tkinter.mainloop()
