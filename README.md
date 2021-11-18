# Screenshare-Streaming-Python
This is a Client-Server-System which can share the screen from the server to client and in the other direction.

You have to change the IP-Adress. You can do this in line 134 and in the server and in line 135 in the client.
For the first test, I recommend using the localhost and run the server and client at the same system.
If you use IPv6 it is "::1", otherwise it is "127.0.0.1".
You can change the ports in the same lines aswell.

This is made for a IPv6-Network, you can change it to IPv4 at the server in line 39 (self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)) and at the client in line 40 (self.client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)).
