import tkinter as tk
from tkinter import ttk

# ==================================================
# CONFIGURACIÓN PRINCIPAL
# ==================================================

ventana = tk.Tk()
ventana.title("RESTAURANTE SALUDABLE")
ventana.geometry("900x650")
ventana.config(bg="#E8F5E9")

titulo = tk.Label(
    ventana,
    text="🍽 RESTAURANTE DE HÁBITOS ALIMENTICIOS 🍽",
    font=("Arial", 24, "bold"),
    bg="#E8F5E9",
    fg="#1B5E20"
)
titulo.pack(pady=20)

subtitulo = tk.Label(
    ventana,
    text="Seleccione un menú especializado",
    font=("Arial", 14),
    bg="#E8F5E9"
)
subtitulo.pack()


# ==================================================
# MENÚ DIABÉTICOS
# ==================================================

def menu_diabeticos():

    form = tk.Toplevel()
    form.title("Menú para Diabéticos")
    form.geometry("600x500")
    form.config(bg="#BBDEFB")

    tk.Label(
        form,
        text="🩺 MENÚ PARA DIABÉTICOS",
        font=("Arial", 20, "bold"),
        bg="#BBDEFB",
        fg="#0D47A1"
    ).pack(pady=15)

    menu = """
🥗 Ensalada Verde Especial

🐟 Salmón a la Plancha

🥦 Verduras al Vapor

🍎 Manzana Fresca

🥤 Agua Natural


"""

    tk.Label(
        form,
        text=menu,
        font=("Arial", 14),
        justify="left",
        bg="#BBDEFB"
    ).pack(pady=20)


# ==================================================
# MENÚ SOBREPESO
# ==================================================

def menu_sobrepeso():

    form = tk.Toplevel()
    form.title("Menú para Sobrepeso")
    form.geometry("600x500")
    form.config(bg="#C8E6C9")

    tk.Label(
        form,
        text="⚖ MENÚ PARA CONTROL DE PESO",
        font=("Arial", 20, "bold"),
        bg="#C8E6C9",
        fg="#1B5E20"
    ).pack(pady=15)

    menu = """
🥗 Ensalada César Ligera

🍗 Pechuga Asada

🥕 Vegetales Mixtos

🍍 Piña Natural

🥤 Té sin Azúcar


"""

    tk.Label(
        form,
        text=menu,
        font=("Arial", 14),
        justify="left",
        bg="#C8E6C9"
    ).pack(pady=20)


# ==================================================
# MENÚ ADULTOS MAYORES
# ==================================================

def menu_adultos():

    form = tk.Toplevel()
    form.title("Menú Adultos Mayores")
    form.geometry("600x500")
    form.config(bg="#FFF9C4")

    tk.Label(
        form,
        text="👴 MENÚ ADULTOS MAYORES",
        font=("Arial", 20, "bold"),
        bg="#FFF9C4",
        fg="#F57F17"
    ).pack(pady=15)

    menu = """
🍲 Sopa de Verduras

🐟 Filete de Pescado

🥔 Puré de Papa

🍌 Plátano

🥛 Leche Deslactosada


"""

    tk.Label(
        form,
        text=menu,
        font=("Arial", 14),
        justify="left",
        bg="#FFF9C4"
    ).pack(pady=20)


# ==================================================
# MENÚ INFANTIL
# ==================================================

def menu_ninos():

    form = tk.Toplevel()
    form.title("Menú Infantil Saludable")
    form.geometry("600x500")
    form.config(bg="#F8BBD0")

    tk.Label(
        form,
        text="🧒 MENÚ INFANTIL SALUDABLE",
        font=("Arial", 20, "bold"),
        bg="#F8BBD0",
        fg="#AD1457"
    ).pack(pady=15)

    menu = """
🍔 Mini Hamburguesa Integral

🥕 Bastones de Zanahoria

🍓 Fresas Frescas

🧃 Jugo Natural

🍪 Galleta de Avena


"""

    tk.Label(
        form,
        text=menu,
        font=("Arial", 14),
        justify="left",
        bg="#F8BBD0"
    ).pack(pady=20)


# ==================================================
# BOTONES PRINCIPALES
# ==================================================

tk.Button(
    ventana,
    text="🩺 Menú Diabéticos",
    font=("Arial", 14, "bold"),
    bg="#42A5F5",
    fg="white",
    width=25,
    command=menu_diabeticos
).pack(pady=10)

tk.Button(
    ventana,
    text="⚖ Menú Sobrepeso",
    font=("Arial", 14, "bold"),
    bg="#4CAF50",
    fg="white",
    width=25,
    command=menu_sobrepeso
).pack(pady=10)

tk.Button(
    ventana,
    text="👴 Menú Adultos Mayores",
    font=("Arial", 14, "bold"),
    bg="#FBC02D",
    fg="black",
    width=25,
    command=menu_adultos
).pack(pady=10)

tk.Button(
    ventana,
    text="🧒 Menú Infantil",
    font=("Arial", 14, "bold"),
    bg="#EC407A",
    fg="white",
    width=25,
    command=menu_ninos
).pack(pady=10)

tk.Button(
    ventana,
    text="❌ Salir",
    font=("Arial", 14, "bold"),
    bg="#D32F2F",
    fg="white",
    width=25,
    command=ventana.destroy
).pack(pady=20)

ventana.mainloop()
