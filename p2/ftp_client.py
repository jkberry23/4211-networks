import socket
import sys

def send_msg(msg, server):
    server.send(msg.encode("utf-8")[:1024])

def recv_msg(server):
    return server.recv(1024).decode("utf-8")

def authenticate(server):
	server_msg = recv_msg(server)
	
	while (server_msg != "230 User logged in."):
		print(server_msg)
		msg = "username: " + input("Enter username: ") + "\npassword: " + input("Enter password: ")
		send_msg(msg, server)
		server_msg = recv_msg(server)

	print(server_msg)

def run_client():

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server_ip = "127.0.0.1"
	server_port = int(sys.argv[1])
	
	client.connect((server_ip, server_port))
		
	authenticate(client)

	while True:
		command = input("Enter command (list_server, upload, download, exit): ")
			
		if (command == "list_server"):
				send_msg("command: list_server", client)
			
		if (command == "upload"):
			filename = input("Enter filename: ")
			filecontent = input("Enter file content: ")
			send_msg("command: upload\nfilename: " + filename + "\nfile content: " + filecontent, client)
		
		if (command == "download"):
			filename = input("Enter filename: ")
			send_msg("command: download\nfilename: " + filename, client)

		if (command == "exit"):
			send_msg("exit", client)

		response = recv_msg(client)
		print(response)

		if response == "221 Service closing control connection.":
			break
			
	client.close()
	print("Connection to server closed")

run_client()