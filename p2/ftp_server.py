import socket
import os
import sys
import threading

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

def parse_user_data():
    file = open('./server_files/user_data.txt', mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
	
    users = []
	
    for line in lines:
        info = line.split()
        users.append(User(info[0][:-1], info[1]))
		
    return users

def send_msg(msg, socket):
    socket.send(msg.encode("utf-8"))

def recv_msg(socket):
    return socket.recv(1024).decode("utf-8")

def authenticate(userList, socket):

    ruser = None
    send_msg("220 Ready for new user. Please enter your username and password.", socket)

    while ruser == None:
        
        response = recv_msg(socket)

        unrsp = response.split()[1]
        pwrsp = response.split()[3]

        goodUN = 0

        for user in userList:
            if user.username == unrsp:
                
                goodUN = 1
                if(user.password == pwrsp):
                    ruser = user

        if(goodUN == 0):
            send_msg("530 Username not accepted. Please check your username and try again.", socket)
        
        if((goodUN == 1) & (ruser == None)):
            send_msg("530 Password not accepted. Please check your password and try again.", socket)

    send_msg("230 User logged in.", socket)
    return ruser

def list_directory_contents(user):
    dirpath = os.path.join("./server_files/user_files/", user.username)

    message = "["

    for file in os.listdir(dirpath):
        message += file + ", "
    
    if(len(message) > 1):
        message = message[:-2]

    message +=  "]"

    return message

def add_owned_file(user, filename, filecontent):

    dirpath = "./server_files/user_files/"
    filepath = os.path.join(dirpath, user.username, filename)
    with open(filepath, "w") as file:
        file.write(filecontent)

def get_owned_file(user, filename):
    rs = ""

    dirpath = "./server_files/user_files/"
    for subdir in os.listdir(dirpath):
        subdirpath = os.path.join(dirpath, subdir)
        for subdirfile in os.listdir(subdirpath):
            if subdirfile == filename:
                if subdir == user.username:
                    file_path = os.path.join(subdirpath, subdirfile)
                    with open(file_path, "r") as file:
                            rs = f"250 Requested file action okay, completed.\nfilename: {filename}\ncontents: " + file.read()
                else:
                    rs = "550 Requested action not taken. File not owned by user."

    if rs == "":
        rs = "550 Requested action not taken. File does not exist."

    return rs

def handle_client(client_socket, client_address, users):
    user = authenticate(users, client_socket)
    while True:
        
        request = recv_msg(client_socket)

        if request == "exit":
            send_msg("221 Service closing control connection.", client_socket)
            break

        request_lines = request.splitlines()
        request_key = request_lines[0].split()[1]

        print(f"Received: {request}")

        if request_key == "list_server":
            msg = "250 Requested file action okay, completed.\nfiles: "
            msg += list_directory_contents(user)
            send_msg(msg, client_socket)

        if request_key == "upload":
            msg = "250 Requested file action okay, completed."
            filename = request_lines[1].split()[1]
            request_lines[2] = ' '.join(request_lines[2].split()[2:])
            content = '\n'.join(request_lines[2:])
            add_owned_file(user, filename, content)
            send_msg(msg, client_socket)

        if request_key == "download":
            filename = request_lines[1].split()[1]
            msg = get_owned_file(user, filename)
            send_msg(msg, client_socket)
    
    print(f"Connection from {client_address[0]}:{client_address[1]} closed")

def run_server():
    users = parse_user_data()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    port = int(sys.argv[1])
    server.bind((server_ip, port))

    server.listen(0)
    print(f"Listening on {server_ip}:{port}")

    while True: 
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        thread = threading.Thread(target = handle_client, args = (client_socket, client_address, users))
        thread.start()

run_server()