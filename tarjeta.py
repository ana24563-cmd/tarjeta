import tkinter as tk
from tkinter import messagebox

# Esta clase es para guardar la info del cliente, como nombre, apellidos, fecha de nacimiento y domicilio
class Cliente:
    def __init__(self, nombre, ap_p, ap_m, fecha_nac, domicilio):
        self.nombre = nombre
        self.ap_p = ap_p
        self.ap_m = ap_m
        self.fecha_nac = fecha_nac
        self.domicilio = domicilio

# Esta clase es para cada movimiento que haces en la cuenta, puede ser un cargo (gasto) o un abono (depósito)
class Movimiento:
    def __init__(self, fecha, descripccion, cargo, abono, saldo):
        self.fecha = fecha
        self.descripccion = descripccion
        self.cargo = cargo
        self.abono = abono
        self.saldo = saldo

# Aquí se maneja la cuenta bancaria: saldo, número y los movimientos que hagas
class Cuenta:
    def __init__(self, num):
        self.numero_cuenta = num
        self.saldo = 1000  # empezamos con $1000 de saldo
        self.movimientos = []  # acá guardamos todo lo que haces (movimientos)

    # Método para hacer cargos o abonos, o sea, sacar o meter plata
    def mover(self, cantidad, descripccion, tipo):
        # tipo dice si es un Cargo (gasto) o Abono (depósito)
        if tipo == "Cargo":
            if cantidad > self.saldo:
                # Si no tienes plata suficiente, te rechaza el cargo
                self.movimientos.append(Movimiento("2025-09-12", "Cargo rechazado (sin fondos)", 0, 0, self.saldo))
            else:
                # Si sí tienes plata, la quita y guarda el movimiento
                self.saldo -= cantidad
                self.movimientos.append(Movimiento("2025-09-12", descripccion, cantidad, 0, self.saldo))
        else:  # Si es un abono, simplemente suma la plata
            self.saldo += cantidad
            self.movimientos.append(Movimiento("2025-09-12", descripccion, 0, cantidad, self.saldo))

# Esta clase es la interfaz gráfica, la ventana donde interactúas con la app
class Interfaz:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("💖 Estado de Cuenta Bancaria 💖")
        self.ventana.configure(bg="#ffe6f0")

        self.cliente = None  # Aquí guardamos al cliente
        self.cuenta = None   # Aquí guardamos la cuenta del cliente

        self.crear_formulario_cliente()  # Empezamos con el formulario para meter datos del cliente

    # Esto crea las cajas de texto y etiquetas para que ingreses tu nombre, apellidos, etc.
    def crear_formulario_cliente(self):
        tk.Label(self.ventana, text="--- INGRESO DE DATOS DEL CLIENTE ---", bg="#fafafa", fg="#b30059", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        # Estas son las etiquetas para cada dato que tienes que llenar
        self.etiquetas = ["Nombre:", "Apellido paterno:", "Apellido materno:", "Fecha de nacimiento (YYYY-MM-DD):", "Domicilio:"]
        self.entradas_cliente = []  # Lista para guardar las cajas de texto

        # Aquí creamos las etiquetas y cajas de texto para que ingreses los datos
        for i in range(5):
            tk.Label(self.ventana, text=self.etiquetas[i], bg="#f5cfde", fg="#b30059", font=("Arial", 10, "bold")).grid(row=i+1, column=0, sticky="e", padx=5, pady=2)
            entrada = tk.Entry(self.ventana, bg="#fff0f5", fg="#b30059")
            entrada.grid(row=i+1, column=1, pady=2, sticky="w")
            self.entradas_cliente.append(entrada)

        # Botón para decir “Ya, ya llené todo” y continuar
        tk.Button(self.ventana, text="Registrar Cliente", bg="#D8579A", fg="white", font=("Arial", 10, "bold"), command=self.registrar_cliente).grid(row=6, column=0, columnspan=2, pady=10)

    # Aquí se guarda lo que escribiste, y si falta algo te avisa
    def registrar_cliente(self):
        nombre = self.entradas_cliente[0].get().strip()
        ap_p = self.entradas_cliente[1].get().strip()
        ap_m = self.entradas_cliente[2].get().strip()
        fecha_nac = self.entradas_cliente[3].get().strip()
        domicilio = self.entradas_cliente[4].get().strip()

        # Si dejaste algún campo vacío, te avisa que lo llenes
        if nombre == "" or ap_p == "" or ap_m == "" or fecha_nac == "" or domicilio == "":
            messagebox.showwarning("Datos incompletos", "Por favor, completa todos los campos.")
            return

        # Si está todo bien, crea el cliente y la cuenta (con saldo inicial)
        self.cliente = Cliente(nombre, ap_p, ap_m, fecha_nac, domicilio)
        self.cuenta = Cuenta("1234567890")

        # Quita las cajas para que no las sigas viendo y te muestra la siguiente parte
        for entrada in self.entradas_cliente:
            entrada.destroy()

        # Aquí se crean los controles para que hagas movimientos y se muestre el estado
        self.crear_operaciones()
        self.mostrar_estado()

    # Esta parte crea los controles para agregar cargos o abonos y la lista con los movimientos
    def crear_operaciones(self):
        tk.Label(self.ventana, text="--- REGISTRO DE MOVIMIENTOS ---", bg="#ffe6f0", fg="#b30059", font=("Arial", 12, "bold")).grid(row=7, column=0, columnspan=3, pady=5)

        # Opción para elegir si es Cargo o Abono
        tk.Label(self.ventana, text="Tipo:", bg="#ffe6f0", fg="#b30059", font=("Arial", 10, "bold")).grid(row=8, column=0, pady=2, sticky="e")
        self.tipo_var = tk.StringVar(value="Cargo")
        tk.OptionMenu(self.ventana, self.tipo_var, "Cargo", "Abono").grid(row=8, column=1, pady=2, sticky="w")

        # Caja para poner el monto
        tk.Label(self.ventana, text="Monto:", bg="#ffe6f0", fg="#b30059", font=("Arial", 10, "bold")).grid(row=9, column=0, pady=2, sticky="e")
        self.cant = tk.Entry(self.ventana, bg="#fff0f5", fg="#b30059")
        self.cant.grid(row=9, column=1, pady=2, sticky="w")

        # Caja para poner una descripción del movimiento
        tk.Label(self.ventana, text="Descripción:", bg="#ffe6f0", fg="#b30059", font=("Arial", 10, "bold")).grid(row=10, column=0, pady=2, sticky="e")
        self.descripccion = tk.Entry(self.ventana, bg="#fff0f5", fg="#b30059")
        self.descripccion.grid(row=10, column=1, pady=2, sticky="w")

        # Botón para agregar el movimiento
        tk.Button(self.ventana, text="Agregar monto", bg="#d41f67", fg="white", font=("Arial", 10, "bold"), command=self.registrar).grid(row=10, column=2, padx=5)

        # Área de texto donde se muestra todo el resumen: datos y movimientos
        self.salida = tk.Text(self.ventana, width=80, height=20, bg="#fff0f5", fg="#b30059")
        self.salida.grid(row=11, column=0, columnspan=3, pady=10)

    # Cuando le das clic a agregar monto, acá se procesa todo
    def registrar(self, event=None):
        try:
            cantidad = float(self.cant.get())
            if cantidad <= 0:
                self.salida.insert("end", "⚠️ Error: El monto debe ser mayor a cero.\n")
                return
        except:
            self.salida.insert("end", "⚠️ Error: El monto debe ser numérico.\n")
            return

        tipo = self.tipo_var.get()
        descripcion = self.descripccion.get().strip()
        if descripcion == "":
            self.salida.insert("end", "⚠️ Error: La descripción no puede estar vacía.\n")
            return

        # Aquí se manda a la cuenta a que registre el movimiento
        self.cuenta.mover(cantidad, descripcion, tipo)

        # Limpia las cajas para que pongas otro movimiento
        self.cant.delete(0, tk.END)
        self.descripccion.delete(0, tk.END)
        # Actualiza la pantalla con los datos y movimientos nuevos
        self.mostrar_estado()

    # Esta función muestra en el área de texto todo el resumen: cliente, cuenta y movimientos
    def mostrar_estado(self):
        self.salida.delete("1.0", tk.END)  # limpia todo lo que había

        c = self.cliente
        cuenta = self.cuenta

        # Muestra info del cliente
        self.salida.insert("end", "--- DATOS DEL CLIENTE ---\n")
        self.salida.insert("end", f"Nombre: {c.nombre}\n")
        self.salida.insert("end", f"Apellido paterno: {c.ap_p}\n")
        self.salida.insert("end", f"Apellido materno: {c.ap_m}\n")
        self.salida.insert("end", f"Fecha de nacimiento: {c.fecha_nac}\n")
        self.salida.insert("end", f"Domicilio: {c.domicilio}\n\n")

        # Muestra info de la cuenta
        self.salida.insert("end", "--- DATOS DE LA CUENTA ---\n")
        self.salida.insert("end", f"Número de cuenta: {cuenta.numero_cuenta}\n")
        self.salida.insert("end", f"Saldo actual: {cuenta.saldo}\n\n")

        # Muestra todos los movimientos, o dice que no hay si está vacío
        self.salida.insert("end", "--- MOVIMIENTOS ---\n")
        if cuenta.movimientos:
            for m in cuenta.movimientos:
                self.salida.insert("end", f"Fecha: {m.fecha} | Descripción: {m.descripccion} | Cargo: {m.cargo} | Abono: {m.abono} | Saldo: {m.saldo}\n")
        else:
            self.salida.insert("end", "No hay movimientos registrados.\n")

# Aquí empieza el programa, se crea la ventana y se lanza la interfaz
if __name__ == "__main__":
    ventana = tk.Tk()
    Interfaz(ventana)
    ventana.mainloop()
