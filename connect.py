import socket

def connect_to_server(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"Connected to {host}:{port}")
            
            message = "Hello, Server!"
            s.sendall(message.encode())
            print("Message sent to the server.")
            
            response = s.recv(1024)
            print("Received from server:", response.decode())
    
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    server_host = '127.0.0.1'
    server_port = 65432
    connect_to_server(server_host, server_port)