Name: Jason Berry
ID: 5349067
Email: berry487@umn.edu

Run the server with:
	python3 ftp_server.py <port_number>

Run the client with:
	python3 ftp_client.py <port number>

The server and client need to be run in different terminals on the same machine.

Message format:
	All messages are sent as strings. They are encoded when sent and decoded when received. The encoding used is UTF-8.

	Client messages:
		<field_1_type>: <field_1_data>
		<field_2_type>: <field_2_data>
		...and so on...

	Server messages:
		<message_code> <human_readable_message>