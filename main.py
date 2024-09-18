from agent import *
        
if __name__ == '__main__':
    import socket
    HOST = 'localhost'  # Listen on localhost
    PORT = 12345   
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"Server listening on {HOST}:{PORT}")
        
        while True:
            # Accept a connection
            client_socket, addr = server_socket.accept()
            print(f"Connected by {addr}")

            message = client_socket.recv(1024)
            print(f"Received message: {message.decode()}")

            response = "Hello"
            client_socket.sendall(response.encode())