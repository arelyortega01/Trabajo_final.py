import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import csv
import random
import math
import os
import logging
from datetime import datetime

# ---------------------------
# Configuración
# ---------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
CSV_REPORTE = "reporte_habitos.csv"
BD_USUARIOS = "usuarios.db"
BD_HABITOS = "habitos.db"
BD_ESTADISTICAS = "estadisticas.db"
BD_REGISTRO = "registro_diario.db"

# ---------------------------
# CREAR BASES DE DATOS
# ---------------------------

def inicializar_bases_datos():
    """Crea las bases necesarias del sistema si no existen.

    Bases principales del proyecto:
    1. usuarios.db: guarda usuarios registrados.
    2. habitos.db: guarda respuestas y resultados de hábitos.
    3. estadisticas.db: guarda un resumen estadístico general.

    También se conserva registro_diario.db porque ya existía en tu proyecto.
    """
    try:
        with sqlite3.connect(BD_USUARIOS) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            """)

        with sqlite3.connect(BD_HABITOS) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER,
                peso REAL,
                altura REAL,
                comidas INTEGER,
                frutas INTEGER,
                chatarra INTEGER,
                agua INTEGER,
                ejercicio TEXT,
                genero TEXT,
                resultado TEXT,
                imc REAL,
                timestamp TEXT
            )
            """)

        with sqlite3.connect(BD_ESTADISTICAS) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS estadisticas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_generacion TEXT,
                total_registros INTEGER,
                total_saludables INTEGER,
                total_poco_saludables INTEGER,
                promedio_imc REAL,
                promedio_agua REAL,
                promedio_frutas REAL,
                promedio_chatarra REAL
            )
            """)

        with sqlite3.connect(BD_REGISTRO) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                comida TEXT,
                calorias INTEGER
            )
            """)

        logging.info("Bases de datos inicializadas correctamente.")
    except Exception as e:
        logging.exception("Error al inicializar las bases de datos")
        messagebox.showerror("Error", f"No se pudieron crear las bases de datos: {e}")


def actualizar_estadisticas():
    """Actualiza estadisticas.db con datos calculados desde habitos.db."""
    try:
        with sqlite3.connect(BD_HABITOS) as conexion_habitos:
            cursor = conexion_habitos.cursor()
            cursor.execute("SELECT COUNT(*) FROM habitos")
            total_registros = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM habitos WHERE resultado='SALUDABLE'")
            total_saludables = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM habitos WHERE resultado='POCO SALUDABLE'")
            total_poco_saludables = cursor.fetchone()[0]

            cursor.execute("SELECT AVG(imc), AVG(agua), AVG(frutas), AVG(chatarra) FROM habitos")
            promedios = cursor.fetchone()

        promedio_imc = round(promedios[0], 2) if promedios and promedios[0] is not None else 0
        promedio_agua = round(promedios[1], 2) if promedios and promedios[1] is not None else 0
        promedio_frutas = round(promedios[2], 2) if promedios and promedios[2] is not None else 0
        promedio_chatarra = round(promedios[3], 2) if promedios and promedios[3] is not None else 0

        with sqlite3.connect(BD_ESTADISTICAS) as conexion_estadisticas:
            cursor = conexion_estadisticas.cursor()
            cursor.execute("DELETE FROM estadisticas")
            cursor.execute("""
            INSERT INTO estadisticas(
                fecha_generacion, total_registros, total_saludables,
                total_poco_saludables, promedio_imc, promedio_agua,
                promedio_frutas, promedio_chatarra
            ) VALUES(?,?,?,?,?,?,?,?)
            """, (
                datetime.now().isoformat(timespec="seconds"),
                total_registros,
                total_saludables,
                total_poco_saludables,
                promedio_imc,
                promedio_agua,
                promedio_frutas,
                promedio_chatarra
            ))

        logging.info("estadisticas.db actualizado correctamente.")
    except Exception as e:
        logging.exception("Error actualizando estadísticas")
        raise e


# Inicializa las bases al arrancar el programa.
inicializar_bases_datos()

# ---------------------------
# FUNCIONES AUXILIARES
# ---------------------------

def calcular_imc(peso, altura_cm):
    altura_metros = altura_cm / 100
    if altura_metros <= 0:
        return 0
    imc = peso / (altura_metros ** 2)
    return round(imc, 2)

def obtener_recomendacion(resultado):
    if resultado == "SALUDABLE":
        return "Excelente alimentación. Sigue así."
    else:
        return "Debes consumir más frutas y menos comida chatarra."

def calcular_calorias():
    try:
        comidas = int(entrada_comidas.get())
        calorias = comidas * 250
        messagebox.showinfo("Calorías", f"Consumo aproximado: {calorias} calorías.")
    except Exception:
        messagebox.showerror("Error", "Ingresa datos válidos.")

def recordar_agua():
    messagebox.showinfo("Agua", "Recuerda tomar mínimo 2 litros de agua diarios 💧")

def clasificar_alimentacion():
    try:
        frutas = int(entrada_frutas.get())
        chatarra = int(entrada_chatarra.get())
        if frutas >= 5 and chatarra <= 1:
            mensaje = "Excelente alimentación"
        elif frutas >= 3:
            mensaje = "Buena alimentación"
        else:
            mensaje = "Debes mejorar tu alimentación"
        messagebox.showinfo("Clasificación", mensaje)
    except Exception:
        messagebox.showerror("Error", "Ingresa datos válidos.")

def consejos_saludables():
    consejos = (
        "✅ Comer frutas diariamente\n"
        "✅ Tomar suficiente agua\n"
        "✅ Hacer ejercicio\n"
        "✅ Dormir bien\n"
        "✅ Evitar comida chatarra\n"
    )
    messagebox.showinfo("Consejos Saludables", consejos)

# ---------------------------
# FUNCIONES CSV (SIN TIMESTAMP)
# ---------------------------

def ensure_csv_header(path, headers):
    """Crea el CSV con cabecera si no existe."""
    try:
        if not os.path.exists(path):
            with open(path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
            logging.info(f"CSV creado con cabecera: {path}")
    except Exception as e:
        logging.exception("Error creando CSV")
        messagebox.showwarning("Error CSV", f"No se pudo crear el CSV: {e}")

def append_habitos_csv(nombre, edad, peso, altura, comidas, frutas, chatarra, agua, ejercicio, genero, resultado, imc):
    """Agrega una fila al CSV de reporte_habitos.csv (crea cabecera si hace falta).
       Nota: NO incluye timestamp en el CSV, tal como solicitaste."""
    headers = [
        "Nombre", "Edad", "Peso", "Altura",
        "Comidas", "Frutas", "Chatarra", "Agua", "Ejercicio",
        "Genero", "Resultado", "IMC"
    ]
    try:
        ensure_csv_header(CSV_REPORTE, headers)
        with open(CSV_REPORTE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                nombre, edad, peso, altura,
                comidas, frutas, chatarra, agua, ejercicio,
                genero, resultado, imc
            ])
        logging.info("Fila añadida a CSV reporte_habitos.csv (sin timestamp)")
    except Exception as e:
        logging.exception("Error al anexar al CSV")
        messagebox.showwarning("Advertencia", f"No se pudo guardar en CSV: {e}")

# ---------------------------
# EXPORTAR CSV (desde DB) SIN TIMESTAMP
# ---------------------------

def exportar_csv():
    """Genera el CSV y, al mismo tiempo, asegura/actualiza 3 bases de datos.

    Al hacer clic en el botón se generan/actualizan:
    - reporte_habitos.csv
    - usuarios.db
    - habitos.db
    - estadisticas.db
    """
    try:
        inicializar_bases_datos()

        with sqlite3.connect(BD_HABITOS) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
            SELECT nombre, edad, peso, altura, comidas, frutas, chatarra,
                   agua, ejercicio, genero, resultado, imc
            FROM habitos
            ORDER BY id ASC
            """)
            datos = cursor.fetchall()

        headers = [
            "Nombre", "Edad", "Peso", "Altura",
            "Comidas", "Frutas", "Chatarra", "Agua", "Ejercicio",
            "Genero", "Resultado", "IMC"
        ]

        with open(CSV_REPORTE, "w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(headers)
            writer.writerows(datos)

        actualizar_estadisticas()

        mensaje = (
            "Archivos generados correctamente:\n\n"
            f"✅ {CSV_REPORTE}\n"
            f"✅ {BD_USUARIOS}\n"
            f"✅ {BD_HABITOS}\n"
            f"✅ {BD_ESTADISTICAS}\n\n"
            "Nota: registro_diario.db también se conserva porque forma parte del proyecto original."
        )
        messagebox.showinfo("Éxito", mensaje)
    except Exception as e:
        logging.exception("Error generando CSV y bases de datos")
        messagebox.showerror("Error", f"No se pudieron generar los archivos: {e}")

# ---------------------------
# MOSTRAR HISTORIAL (Treeview)
# ---------------------------

def mostrar_historial():
    ventana_historial = tk.Toplevel()
    ventana_historial.title("Historial")
    ventana_historial.geometry("1200x400")
    ventana_historial.config(bg="#E8F5E9")

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#E8F5E9", foreground="black", rowheight=25, fieldbackground="#E8F5E9", font=("Arial", 10))
    style.configure("Treeview.Heading", background="green", foreground="white", font=("Arial", 10, "bold"))
    style.map("Treeview", background=[("selected", "#81C784")])

    tabla = ttk.Treeview(ventana_historial)
    tabla["columns"] = (
        "Nombre", "Edad", "Peso", "Altura", "Comidas", "Frutas",
        "Chatarra", "Agua", "Ejercicio", "Genero", "Resultado", "IMC", "Timestamp"
    )
    tabla.column("#0", width=0, stretch=tk.NO)
    for columna in tabla["columns"]:
        tabla.column(columna, anchor=tk.CENTER, width=90)
        tabla.heading(columna, text=columna)

    conexion = sqlite3.connect(BD_HABITOS)
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, edad, peso, altura, comidas, frutas, chatarra, agua, ejercicio, genero, resultado, imc, timestamp FROM habitos")
    registros = cursor.fetchall()
    conexion.close()
    for fila in registros:
        tabla.insert("", tk.END, values=fila)
    tabla.pack(fill="both", expand=True)

# ---------------------------
# ANIMACIÓN: MUÑECO BAILANDO + LETRAS + MENSAJE MOTIVACIONAL
# ---------------------------

def mostrar_animacion(resultado):
    ventana_anim = tk.Toplevel()
    ventana_anim.title("Animación de Hábitos")
    ventana_anim.geometry("700x450")
    ventana_anim.config(bg="black")

    canvas = tk.Canvas(ventana_anim, width=700, height=450, bg="black", highlightthickness=0)
    canvas.pack()

    texto = "SALUDABLE" if resultado == "SALUDABLE" else "POCO SALUDABLE"
    color_text = "#7CFC00" if resultado == "SALUDABLE" else "#FF4500"

    cx, cy = 350, 220  # centro del muñeco

    head = canvas.create_oval(cx-18, cy-90, cx+18, cy-54, fill="#FFDAB9", outline="")
    torso = canvas.create_line(cx, cy-54, cx, cy+30, fill="white", width=4)
    left_arm = canvas.create_line(cx, cy-30, cx-50, cy+10, fill="white", width=4)
    right_arm = canvas.create_line(cx, cy-30, cx+50, cy+10, fill="white", width=4)
    left_leg = canvas.create_line(cx, cy+30, cx-30, cy+90, fill="white", width=4)
    right_leg = canvas.create_line(cx, cy+30, cx+30, cy+90, fill="white", width=4)
    eye_l = canvas.create_oval(cx-10, cy-80, cx-6, cy-76, fill="black")
    eye_r = canvas.create_oval(cx+6, cy-80, cx+10, cy-76, fill="black")
    smile = canvas.create_arc(cx-10, cy-72, cx+10, cy-60, start=190, extent=160, style="arc", outline="black", width=2)

    particles = []
    for i in range(12):
        p = canvas.create_oval(-10, -10, -6, -6, fill="#FFD700", outline="")
        particles.append(p)

    letters = []
    start_x = 350 - (len(texto) * 22) // 2
    for i, ch in enumerate(texto):
        t = canvas.create_text(start_x + i*22, 60, text=ch, fill=color_text, font=("Helvetica", 28, "bold"), state="hidden")
        letters.append(t)

    mensajes = [
        "¡Sigue así, cada paso cuenta!",
        "Pequeños hábitos, grandes cambios.",
        "Tu salud es tu mejor inversión.",
        "Hoy elegiste bien, mañana será mejor.",
        "Un día a la vez: ¡tú puedes!",
        "Tu constancia te llevará lejos.",
        "Celebra el progreso, no la perfección.",
        "Cada porción de fruta es una victoria."
    ]
    mensaje_random = random.choice(mensajes)
    msg_text = canvas.create_text(350, 400, text=mensaje_random, fill="#FFFFFF", font=("Helvetica", 14, "bold"))

    arm_angle = 0
    arm_dir = 1
    leg_angle = 0
    leg_dir = 1
    bob = 0
    bob_dir = 1
    frame = 0

    def animar():
        nonlocal arm_angle, arm_dir, leg_angle, leg_dir, bob, bob_dir, frame
        frame += 1

        arm_angle += 6 * arm_dir
        if abs(arm_angle) > 40:
            arm_dir *= -1

        leg_angle += 5 * leg_dir
        if abs(leg_angle) > 30:
            leg_dir *= -1

        bob += 1 * bob_dir
        if bob > 6 or bob < -6:
            bob_dir *= -1

        rad_arm = math.radians(arm_angle)
        rad_leg = math.radians(leg_angle)

        ax = cx + int(math.sin(rad_arm) * 60)
        ay = cy - 30 + int(math.cos(rad_arm) * 30)
        bx = cx - int(math.sin(rad_arm) * 60)
        by = cy - 30 - int(math.cos(rad_arm) * 30)

        canvas.coords(right_arm, cx, cy-30 + bob, ax, ay + bob)
        canvas.coords(left_arm, cx, cy-30 + bob, bx, by + bob)

        lx = cx - int(math.sin(rad_leg) * 40)
        ly = cy + 30 + int(math.cos(rad_leg) * 60)
        rx = cx + int(math.sin(rad_leg) * 40)
        ry = cy + 30 - int(math.cos(rad_leg) * 60)

        canvas.coords(left_leg, cx, cy+30 + bob, lx, ly + bob)
        canvas.coords(right_leg, cx, cy+30 + bob, rx, ry + bob)

        canvas.coords(torso, cx, cy-54 + bob, cx, cy+30 + bob)
        canvas.coords(head, cx-18, cy-90 + bob, cx+18, cy-54 + bob)
        canvas.coords(eye_l, cx-10, cy-80 + bob, cx-6, cy-76 + bob)
        canvas.coords(eye_r, cx+6, cy-80 + bob, cx+10, cy-76 + bob)
        canvas.coords(smile, cx-10, cy-72 + bob, cx+10, cy-60 + bob)

        if resultado == "SALUDABLE":
            for i, p in enumerate(particles):
                angle = (frame*6 + i*30) % 360
                rad = math.radians(angle)
                px = cx + int(math.cos(rad) * 140)
                py = cy + int(math.sin(rad) * 80) - 60
                size = 4 + (i % 3)
                canvas.coords(p, px-size, py-size, px+size, py+size)
                canvas.itemconfig(p, state="normal", fill=["#FFD700", "#ADFF2F", "#7CFC00"][i % 3])
        else:
            for p in particles:
                canvas.itemconfig(p, state="hidden")

        for i, t in enumerate(letters):
            if frame > 6 + i*4:
                canvas.itemconfig(t, state="normal")
                bounce = int(8 * math.sin((frame - i*4) * 0.25))
                canvas.coords(t, start_x + i*22, 60 + bounce)
                pulse = 120 + int(80 * math.sin(frame * 0.15 + i))
                if resultado == "SALUDABLE":
                    g = min(255, pulse)
                    canvas.itemconfig(t, fill=f"#00{g:02x}00")
                else:
                    r = min(255, pulse)
                    canvas.itemconfig(t, fill=f"#{r:02x}0000")

        canvas.delete("halo")
        if resultado == "SALUDABLE":
            for r in range(1, 4):
                canvas.create_oval(cx-120*r//3, cy-140*r//3 + bob, cx+120*r//3, cy-20*r//3 + bob,
                                   outline="#7CFC00", width=1, tags="halo")

        pulse_msg = 1.0 + 0.05 * math.sin(frame * 0.12)
        canvas.itemconfig(msg_text, font=("Helvetica", int(14 * pulse_msg), "bold"))

        ventana_anim.after(60, animar)

    animar()

# ---------------------------
# GUARDAR DATOS (DB + CSV + ANIMACIÓN) SIN TIMESTAMP EN CSV
# ---------------------------

def guardar_datos():
    try:
        nombre = entrada_nombre.get().strip()
        edad = int(entrada_edad.get()) if entrada_edad.get().strip() != "" else 0
        peso = float(entrada_peso.get()) if entrada_peso.get().strip() != "" else 70.0
        altura = float(entrada_altura.get()) if entrada_altura.get().strip() != "" else 170.0
        comidas = int(entrada_comidas.get()) if entrada_comidas.get().strip() != "" else 3
        frutas = int(entrada_frutas.get()) if entrada_frutas.get().strip() != "" else 2
        chatarra = int(entrada_chatarra.get()) if entrada_chatarra.get().strip() != "" else 2
        agua = int(entrada_agua.get()) if entrada_agua.get().strip() != "" else 6
        ejercicio = combo_ejercicio.get()
        genero = genero_var.get()

        if nombre == "":
            messagebox.showerror("Error", "Ingresa un nombre.")
            return

        if peso <= 0 or altura <= 0:
            messagebox.showerror("Error", "Peso y altura deben ser mayores a 0.")
            return

        imc = calcular_imc(peso, altura)

        if comidas >= 3 and frutas >= 3 and chatarra <= 2:
            resultado = "SALUDABLE"
        else:
            resultado = "POCO SALUDABLE"

        timestamp = datetime.now().isoformat()

        conexion = sqlite3.connect(BD_HABITOS)
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO habitos(
            nombre, edad, peso, altura, comidas, frutas, chatarra, agua, ejercicio, genero, resultado, imc, timestamp
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            nombre, edad, peso, altura, comidas, frutas, chatarra, agua, ejercicio, genero, resultado, imc, timestamp
        ))
        conexion.commit()
        conexion.close()

        # Guardar también en CSV (sin timestamp)
        append_habitos_csv(nombre, edad, peso, altura, comidas, frutas, chatarra, agua, ejercicio, genero, resultado, imc)

        recomendacion = obtener_recomendacion(resultado)

        texto = (
            f"DATOS GUARDADOS CORRECTAMENTE\n\n"
            f"Nombre: {nombre}\n\n"
            f"IMC: {imc}\n\n"
            f"Resultado: {resultado}\n\n"
            f"Recomendación:\n{recomendacion}"
        )
        messagebox.showinfo("Resultado", texto)

        mostrar_animacion(resultado)

        entrada_nombre.delete(0, tk.END)
        entrada_edad.delete(0, tk.END)
        entrada_peso.delete(0, tk.END)
        entrada_altura.delete(0, tk.END)
        entrada_comidas.delete(0, tk.END)
        entrada_frutas.delete(0, tk.END)
        entrada_chatarra.delete(0, tk.END)
        entrada_agua.delete(0, tk.END)

    except Exception as e:
        logging.exception("Error en guardar_datos")
        messagebox.showerror("Error", str(e))

# ---------------------------
# REGISTRAR USUARIO
# ---------------------------

def registrar_usuario():
    usuario = entrada_usuario.get().strip()
    password = entrada_password.get().strip()
    if usuario == "" or password == "":
        messagebox.showerror("Error", "Completa todos los campos.")
        return
    try:
        conexion = sqlite3.connect(BD_USUARIOS)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios(usuario, password) VALUES(?,?)", (usuario, password))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Registro", "Usuario registrado correctamente.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "El usuario ya existe.")
    except Exception as e:
        logging.exception("Error registrando usuario")
        messagebox.showerror("Error", f"No se pudo registrar: {e}")

# ---------------------------
# LOGIN
# ---------------------------

def verificar_login():
    usuario = entrada_usuario.get().strip()
    password = entrada_password.get().strip()
    try:
        conexion = sqlite3.connect(BD_USUARIOS)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND password=?", (usuario, password))
        resultado = cursor.fetchone()
        conexion.close()
        if resultado:
            messagebox.showinfo("Bienvenida", f"Bienvenido {usuario} 😊")
            ventana_login.destroy()
            abrir_sistema(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
    except Exception as e:
        logging.exception("Error en login")
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def cerrar_sesion(ventana):
    respuesta = messagebox.askyesno("Cerrar Sesión", "¿Deseas cerrar sesión?")
    if respuesta:
        messagebox.showinfo("Sesión", "Sesión cerrada correctamente.")
        ventana.destroy()

# ---------------------------
# VENTANA PRINCIPAL (INTEGRADA)
# ---------------------------

def abrir_sistema(usuario):
    global entrada_nombre, entrada_edad, entrada_peso, entrada_altura
    global entrada_comidas, entrada_frutas, entrada_chatarra, entrada_agua
    global combo_ejercicio, genero_var

    ventana = tk.Tk()
    ventana.title("Sistema Inteligente de Hábitos Alimenticios")
    ventana.geometry("750x850")
    ventana.config(bg="#E8F5E9")

    bienvenida = tk.Label(ventana, text=f"Bienvenido {usuario} 😊", font=("Arial", 14, "bold"), bg="#E8F5E9", fg="green")
    bienvenida.pack(pady=5)

    titulo = tk.Label(ventana, text="SISTEMA INTELIGENTE DE HÁBITOS ALIMENTICIOS", font=("Arial", 18, "bold"), bg="#E8F5E9", fg="green")
    titulo.pack(pady=10)

    tk.Label(ventana, text="Nombre:", bg="#E8F5E9").pack()
    entrada_nombre = tk.Entry(ventana)
    entrada_nombre.pack()

    tk.Label(ventana, text="Edad:", bg="#E8F5E9").pack()
    entrada_edad = tk.Entry(ventana)
    entrada_edad.pack()

    tk.Label(ventana, text="Peso (kg):", bg="#E8F5E9").pack()
    entrada_peso = tk.Entry(ventana)
    entrada_peso.pack()

    tk.Label(ventana, text="Altura en cm (Ej: 170):", bg="#E8F5E9").pack()
    entrada_altura = tk.Entry(ventana)
    entrada_altura.pack()

    tk.Label(ventana, text="Comidas al día:", bg="#E8F5E9").pack()
    entrada_comidas = tk.Entry(ventana)
    entrada_comidas.pack()

    tk.Label(ventana, text="Frutas y verduras:", bg="#E8F5E9").pack()
    entrada_frutas = tk.Entry(ventana)
    entrada_frutas.pack()

    tk.Label(ventana, text="Comida chatarra por semana:", bg="#E8F5E9").pack()
    entrada_chatarra = tk.Entry(ventana)
    entrada_chatarra.pack()

    tk.Label(ventana, text="Vasos de agua al día:", bg="#E8F5E9").pack()
    entrada_agua = tk.Entry(ventana)
    entrada_agua.pack()

    tk.Label(ventana, text="Nivel de ejercicio:", bg="#E8F5E9").pack()
    combo_ejercicio = ttk.Combobox(ventana, values=["Bajo", "Moderado", "Alto"])
    combo_ejercicio.pack()
    combo_ejercicio.current(0)

    tk.Checkbutton(ventana, text="Acepto recomendaciones saludables", bg="#E8F5E9").pack(pady=5)

    genero_var = tk.StringVar()
    tk.Label(ventana, text="Género:", bg="#E8F5E9").pack()
    tk.Radiobutton(ventana, text="Masculino", variable=genero_var, value="Masculino", bg="#E8F5E9").pack()
    tk.Radiobutton(ventana, text="Femenino", variable=genero_var, value="Femenino", bg="#E8F5E9").pack()
    genero_var.set("Femenino")

    tk.Button(ventana, text="Guardar Datos", bg="green", fg="white", command=guardar_datos).pack(pady=10)
    tk.Button(ventana, text="Generar CSV y 3 BD", bg="blue", fg="white", command=exportar_csv).pack(pady=5)
    tk.Button(ventana, text="Mostrar Historial", bg="orange", fg="white", command=mostrar_historial).pack(pady=5)
    tk.Button(ventana, text="Consejos Saludables", bg="purple", fg="white", command=consejos_saludables).pack(pady=5)
    tk.Button(ventana, text="Calcular Calorías", bg="red", fg="white", command=calcular_calorias).pack(pady=5)
    tk.Button(ventana, text="Recordatorio de Agua", bg="cyan", command=recordar_agua).pack(pady=5)
    tk.Button(ventana, text="Clasificar Alimentación", bg="gold", command=clasificar_alimentacion).pack(pady=5)
    tk.Button(ventana, text="Cerrar Sesión", bg="black", fg="white", command=lambda: cerrar_sesion(ventana)).pack(pady=10)

    ventana.mainloop()

# ---------------------------
# VENTANA LOGIN (INICIAL)
# ---------------------------

ventana_login = tk.Tk()
ventana_login.title("Login")
ventana_login.geometry("400x350")
ventana_login.config(bg="#C8E6C9")

titulo_login = tk.Label(ventana_login, text="INICIAR SESIÓN", font=("Arial", 20, "bold"), bg="#C8E6C9", fg="green")
titulo_login.pack(pady=20)

tk.Label(ventana_login, text="Usuario:", bg="#C8E6C9").pack()
entrada_usuario = tk.Entry(ventana_login)
entrada_usuario.pack()

tk.Label(ventana_login, text="Contraseña:", bg="#C8E6C9").pack()
entrada_password = tk.Entry(ventana_login, show="*")
entrada_password.pack()

tk.Button(ventana_login, text="Entrar", bg="green", fg="white", command=verificar_login).pack(pady=10)
tk.Button(ventana_login, text="Registrarse", bg="blue", fg="white", command=registrar_usuario).pack(pady=5)

# Asegurar que exista el CSV con cabecera al iniciar (sin timestamp)
ensure_csv_header(CSV_REPORTE, [
    "Nombre", "Edad", "Peso", "Altura",
    "Comidas", "Frutas", "Chatarra", "Agua", "Ejercicio",
    "Genero", "Resultado", "IMC"
])

ventana_login.mainloop()

