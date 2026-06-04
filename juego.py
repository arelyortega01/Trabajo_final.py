import tkinter as tk
from tkinter import messagebox

# ---------------------------
# Juego de Hábitos Alimenticios
# ---------------------------

preguntas = [
    {
        "pregunta": "¿Cuántos vasos de agua se recomienda tomar al día?",
        "opciones": ["2", "8", "20"],
        "correcta": "8"
    },
    {
        "pregunta": "¿Cuál es una opción saludable?",
        "opciones": ["Manzana", "Refresco", "Papas fritas"],
        "correcta": "Manzana"
    },
    {
        "pregunta": "¿Qué comida es importante no saltarse?",
        "opciones": ["Desayuno", "Cena", "Merienda"],
        "correcta": "Desayuno"
    },
    {
        "pregunta": "¿Cuántas veces se recomienda comer frutas y verduras?",
        "opciones": ["5 porciones al día", "1 vez por semana", "Nunca"],
        "correcta": "5 porciones al día"
    },
    {
        "pregunta": "¿Qué bebida es más saludable?",
        "opciones": ["Agua", "Refresco", "Bebida energética"],
        "correcta": "Agua"
    }
]

indice = 0
puntaje = 0

def verificar():
    global indice, puntaje

    respuesta = opcion.get()

    if respuesta == preguntas[indice]["correcta"]:
        puntaje += 1

    indice += 1

    if indice < len(preguntas):
        mostrar_pregunta()
    else:
        finalizar_juego()

def mostrar_pregunta():
    pregunta_label.config(
        text=preguntas[indice]["pregunta"]
    )

    opcion.set(None)

    for i in range(3):
        botones[i].config(
            text=preguntas[indice]["opciones"][i],
            value=preguntas[indice]["opciones"][i]
        )

def finalizar_juego():

    if puntaje == 5:
        mensaje = "¡Excelente! Tienes muy buenos conocimientos sobre hábitos alimenticios."
    elif puntaje >= 3:
        mensaje = "¡Bien hecho! Conoces varios hábitos saludables."
    else:
        mensaje = "Necesitas aprender más sobre alimentación saludable."

    messagebox.showinfo(
        "Resultado Final",
        f"Puntaje: {puntaje}/5\n\n{mensaje}"
    )

    ventana.destroy()

# Ventana principal
ventana = tk.Tk()
ventana.title("Juego de Hábitos Alimenticios")
ventana.geometry("600x400")
ventana.config(bg="#E8F5E9")

titulo = tk.Label(
    ventana,
    text="🎮 Juego de Hábitos Alimenticios",
    font=("Arial", 18, "bold"),
    bg="#E8F5E9",
    fg="green"
)
titulo.pack(pady=20)

pregunta_label = tk.Label(
    ventana,
    text="",
    font=("Arial", 14),
    wraplength=500,
    bg="#E8F5E9"
)
pregunta_label.pack(pady=20)

opcion = tk.StringVar()

botones = []

for i in range(3):
    rb = tk.Radiobutton(
        ventana,
        text="",
        variable=opcion,
        value="",
        font=("Arial", 12),
        bg="#E8F5E9"
    )
    rb.pack(anchor="w", padx=150)
    botones.append(rb)

btn = tk.Button(
    ventana,
    text="Siguiente",
    command=verificar,
    bg="green",
    fg="white",
    font=("Arial", 12, "bold")
)
btn.pack(pady=20)

mostrar_pregunta()

ventana.mainloop()