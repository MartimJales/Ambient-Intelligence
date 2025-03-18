import socket
import os
import time

# Configuração do Servidor
HOST = "0.0.0.0"  # Escuta em todas as interfaces de rede
PORT = 52870  # Porta que a Nicla Vision está a usar
SAVE_FOLDER = "received_images"

# Criar a pasta para armazenar as imagens
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Criar socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"📡 Servidor a escutar em {HOST}:{PORT}...")

while True:
    conn, addr = server_socket.accept()
    print(f"📥 Conexão recebida de {addr}")

    # Criar nome único para a imagem recebida
    timestamp = int(time.time())
    filename = os.path.join(SAVE_FOLDER, f"received_{timestamp}.jpg")

    # Receber os dados da imagem e salvar no ficheiro
    with open(filename, "wb") as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)

    print(f"✅ Imagem recebida e armazenada em: {filename}")
    conn.close()
