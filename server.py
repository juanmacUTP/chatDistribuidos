import socket
import threading

# Configura el servidor
HOST = '192.168.0.113'
PORT = 12345

# Diccionario para almacenar las conexiones de los clientes
clientes = {}

# Función para manejar la comunicación con un cliente
def manejar_cliente(cliente, username):
    try:
        while True:
            mensaje = cliente.recv(1024).decode('utf-8')
            if not mensaje:
                break

            # Si el mensaje comienza con "/private", procesarlo
            if mensaje.startswith("/private "):
                partes = mensaje.split(" ")
                if len(partes) >= 3:
                    destinatario = partes[1]
                    mensaje = " ".join(partes[2:])
                    if destinatario in clientes and destinatario != username:
                        destinatario_socket = clientes[destinatario]
                        destinatario_socket.send(f'{username} (privado): {mensaje}'.encode('utf-8'))
                    else:
                        cliente.send("Usuario no encontrado o no disponible.".encode('utf-8'))
                else:
                    cliente.send("Formato incorrecto. Uso: /private nombre_destinatario mensaje".encode('utf-8'))
            else:
                mensaje = f'{username}: {mensaje}'
                broadcast(mensaje)
    except:
        # Si ocurre un error o el cliente se desconecta, quitarlo de la lista de clientes
        del clientes[username]
        broadcast(f'{username} se ha desconectado.')


# Función para enviar un mensaje a todos los clientes
def broadcast(mensaje):
    for cliente_socket in clientes.values():
        cliente_socket.send(mensaje.encode('utf-8'))

# Configura el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Servidor de chat en {HOST}:{PORT}")

# Escucha a los clientes y maneja sus conexiones en hilos separados
while True:
    cliente, addr = server_socket.accept()
    print(f'Conexión entrante desde {addr}')

    # Pide al cliente su nombre de usuario
    cliente.send("Por favor, ingresa tu nombre de usuario: ".encode('utf-8'))
    username = cliente.recv(1024).decode('utf-8')

    # Agrega al cliente a la lista de clientes
    clientes[username] = cliente

    # Notifica a todos los clientes que un nuevo usuario se ha conectado
    broadcast(f'{username} se ha unido al chat.')

    # Inicia un hilo para manejar la comunicación con el cliente
    cliente_thread = threading.Thread(target=manejar_cliente, args=(cliente, username))
    cliente_thread.start()
