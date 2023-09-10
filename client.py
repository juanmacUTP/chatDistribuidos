import tkinter as tk
import socket
import threading

# Configura la ventana de la aplicación
root = tk.Tk()
root.title("Chat en Tkinter")

# Configura el socket del cliente
HOST = '192.168.0.113'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Función para enviar mensajes
def enviar_mensaje(event=None):
    mensaje = mensaje_entry.get()
    if mensaje:
        mostrar_mensaje(f'Tú: {mensaje}')  # Muestra el mensaje en la ventana del chat
        client_socket.send(mensaje.encode('utf-8'))
        mensaje_entry.delete(0, tk.END)

# Función para manejar la recepción de mensajes
def recibir_mensajes():
    try:
        while True:
            mensaje = client_socket.recv(1024).decode('utf-8')
            mostrar_mensaje(mensaje)
    except:
        mostrar_mensaje("Se ha perdido la conexión al servidor.")
        client_socket.close()

# Función para mostrar mensajes en la interfaz
def mostrar_mensaje(mensaje):
    mensaje_text.config(state=tk.NORMAL)
    mensaje_text.insert(tk.END, mensaje + '\n')
    mensaje_text.config(state=tk.DISABLED)


# Configura la interfaz de usuario
mensaje_text = tk.Text(root, state=tk.DISABLED)
mensaje_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

mensaje_entry = tk.Entry(root)
mensaje_entry.pack(pady=10, fill=tk.BOTH, expand=True)

enviar_button = tk.Button(root, text="Enviar", command=enviar_mensaje)
enviar_button.pack(pady=5)

mensaje_entry.bind("<Return>", enviar_mensaje)

# Inicia un hilo para recibir mensajes
recepcion_thread = threading.Thread(target=recibir_mensajes)
recepcion_thread.start()

# Función para cerrar la aplicación
def cerrar_aplicacion():
    client_socket.close()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

# Ejecuta la aplicación
root.mainloop()
