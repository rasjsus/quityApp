import pandas
import re
from tabulate import tabulate

chat = "chat.txt"

with open(chat) as file_chat:
    input_chat_bad = file_chat.read()

# Eliminar caracteres no imprimibles
input_chat = re.sub(r'[\u2000-\u20ff]', r'',
                    input_chat_bad, flags=re.MULTILINE)

# Segmentación del mensaje

lines_chat = input_chat.split("\n")
partes_del_chat = []

for line in lines_chat:
    # Descartar lineas vacias
    if len(line) == 0:
        continue
    # Selecciona inicio del mensaje
    if line[0] == "[":
        partes_del_chat.append(line)
        continue
    partes_del_chat[-1] += line


# Utilizar regex para encontrar la fecha, la hora, el Autor y un mensaje

patron = r"^\[(\d{2}/\d{2}/\d{2}) (\d{1,2}:\d{2}:\d{2})\] ([^:]*): (.*)"
patron_s = r"^\[(\d{2}/\d{2}/\d{2}) (\d{1,2}:\d{2}:\d{2})\] (.*) (salió.*|añadió.*|cambió.*|eliminó.*)"

# Clase para almacenar los datos de cada mensaje


class mensaje:
    def __init__(self, match):
        self.date = match.group(1)
        self.time = match.group(2)
        self.Autor = match.group(3)
        self.mensaje = match.group(4)

    def __repr__(self):
        return str(self.Autor)


lista_mensajes = []
for parte in partes_del_chat:
    match = re.search(patron, parte)
    if match is None:
        match = re.search(patron_s, parte)
    if match is None:
        continue
    lista_mensajes.append(mensaje(match))


data = {
    "Autor": [str(m.Autor) for m in lista_mensajes],
    "fecha": [str(m.date) for m in lista_mensajes],
    "hora": [str(m.time) for m in lista_mensajes],
    "mensaje": [str(m.mensaje) for m in lista_mensajes],
}

df = pandas.DataFrame(data)

print(tabulate(df, headers=["Autor", "Fecha", "Hora", "Mensaje"]))
