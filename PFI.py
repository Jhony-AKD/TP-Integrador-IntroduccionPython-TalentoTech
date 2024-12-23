import sqlite3
import os
from colorama import init, Fore, Back, Style
init(autoreset=True)

estilo_titulo = Fore.WHITE + Back.BLUE + Style.BRIGHT
estilo_menu = Style.BRIGHT + Fore.BLUE
estilo_aviso = Back.RED + Fore.YELLOW
estilo_alerta = Back.RED + Fore.BLACK + Style.BRIGHT
estilo_exito = Back.GREEN + Fore.BLACK + Style.BRIGHT
estilo_input = Fore.MAGENTA
estilo_despedida = Fore.GREEN + Style.BRIGHT + Style.BRIGHT

conexion = sqlite3.connect("./inventario.db")
cursor = conexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                descripcion TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT NOT NULL)''')
conexion.close()

def agregar_producto(nombre, descripcion, cantidad, precio, categoria):
    '''Funcion para agregar nuevos productos al inventario'''
    datos = [nombre, descripcion, cantidad, precio, categoria]
    conexion = sqlite3.connect("./inventario.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)", datos)
    conexion.commit()
    print(f"Producto {nombre} agregado con exito.")
    conexion.close()

def mostrar_productos(productos=0, unico_producto=False):
    '''Funcion para mostrar todos los productos en el inventario en forma de tabla'''
    if productos == 0:
        conexion = sqlite3.connect("./inventario.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        resultados = cursor.fetchall()
        conexion.close()

        if len(resultados) == 0:
            print(estilo_alerta + "\nNo hay productos en el inventario.")
            return
        print("\nListado de productos:")
        print("-" * 100)
        for registro in resultados:
            print(f"ID: {registro[0]:<3} Nombre: {registro[1]:<15} Cantidad: {registro[3]:<6} Precio: ${registro[4]:<10} Categoría: {registro[5]}")
        print("-" * 100)

    else:
        if unico_producto:
            print("\nInformación del producto:")
            print("-" * 150)
            print(f"ID: {productos[0]:<3} Nombre: {productos[1]:<15} Descripción: {productos[2]:<20} Cantidad: {productos[3]:<6} Precio: ${productos[4]:<10} Categoría: {productos[5]}")
            print("-" * 150)
        else:
            print("\nListado de productos seleccionados:")
            print("-" * 100)
            for registro in productos:
                print(f"ID: {registro[0]:<3} Nombre: {registro[1]:<15} Cantidad: {registro[3]:<6} Precio: ${registro[4]:<10} Categoría: {registro[5]}")
            print("-" * 100)
     
def actualizar_producto():
    '''Funcion para actualizar productos del inventario'''
    mostrar_productos()
    codigo = 0
    while codigo <= 0:
        try:
            codigo = int(input(estilo_input + "Ingrese el codigo del producto que desea modificar: "))
            if codigo <=0:
                print("Ingrese un numero mayor que 0: ")
        except ValueError:
            print("Ingrese un numero: ")
            codigo = 0
    nombre = input(estilo_input + "Ingrese el nuevo nombre del producto: ")
    descripcion = input(estilo_input + "Ingrese la nueva descripcion del producto: ")
    cantidad = 0
    while cantidad <= 0:
        try:
            cantidad = int(input(estilo_input + "Ingrese la nueva cantidad: "))
            if cantidad <0:
                print(estilo_input + "Ingrese un numero mayor que 0: ")
        except ValueError:
            print(estilo_alerta + "Ingrese un numero. ")
            cantidad = 0
    precio = 0
    while precio <= 0:
        try:
            precio = int(input(estilo_input + "Ingrese el nuevo precio: "))
            if precio <= 0:
                print(estilo_input + "Ingrese un numero mayor que 0: ")
        except ValueError:
            print(estilo_input + "Ingrese un numero: ")
            precio = 0
    categoria = input(estilo_input + "Ingrese la nueva categoria: ")
    conexion = sqlite3.connect("./inventario.db")
    cursor = conexion.cursor()
    cursor.execute('''UPDATE productos SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, 
                   categoria = ? WHERE id = ?''', (nombre, descripcion, cantidad, precio, categoria, codigo))
    conexion.commit()
    conexion.close()
    mostrar_productos()

def eliminar_producto():
    '''Funcion para eliminar productos del inventario'''
    mostrar_productos()
    codigo = 0
    while codigo <= 0:
        try:
            codigo = int(input(estilo_input + "Ingrese el codigo del producto que desea eliminar: "))
            if codigo <=0:
                print(estilo_aviso + "Ingrese un numero mayor que 0: ")
        except ValueError:
            print(estilo_aviso + "Ingrese un numero: ")
            codigo = 0
    try: 
        with sqlite3.connect("./inventario.db") as cursor:
            cursor.execute("DELETE FROM productos WHERE id = ?", (codigo, ))
            print(estilo_alerta + "Producto eliminado.")
    except ValueError:
        print("Codigo incorrecto.")

def reporte_bajo_stock():
    '''Funcion para mostrar los productos con bajo stock en el inventario en forma de tabla'''
    valor_bajo = 0
    while valor_bajo <= 0:
        try:
            valor_bajo = int(input(estilo_menu + "Ingrese la cantidad minima de stock: "))
            if valor_bajo <=0:
                print(estilo_aviso + "Ingrese un numero mayor que 0: ")
        except ValueError:
            print(estilo_aviso + "Ingrese un numero: ")
            valor_bajo = 0
    conexion = sqlite3.connect("./inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE cantidad <= ?",(valor_bajo,))
    resultados = cursor.fetchall()
    if len(resultados) > 0:
        mostrar_productos(resultados)
    else:
        print(estilo_exito + "\nNo hay productos con bajo stock.")
    conexion.close()
        
def buscar_producto_por_nombre():
    '''Funcion para buscar productos del inventario por su nombre'''
    nombre = input(estilo_input + "Ingrese el nombre del producto a buscar: ").capitalize()
    conexion = sqlite3.connect("./inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre = ?",(nombre,))
    resultados = cursor.fetchone()
    if resultados != None:
        mostrar_productos(resultados, True)
    else:
        print(estilo_alerta + "Registro no encontrado")
    conexion.close()

def mostrar_menu():
    print("")
    print(estilo_titulo + "---------------------------------")
    print(estilo_titulo + "      Gestion de inventario      ")
    print(estilo_titulo + "---------------------------------\n")
    print(estilo_menu + "1- ➕ Agregar producto.")
    print(estilo_menu + "2- 📄 Mostrar todos los productos.")
    print(estilo_menu + "3- 🔁 Actualizar producto.")
    print(estilo_menu + "4- ➖ Eliminar producto.")
    print(estilo_menu + "5- 📑 Reporte de bajo stock.")
    print(estilo_menu + "6- 🔎 Buscar producto.")
    print(estilo_menu + "7- 👋 Salir.")

def main():
    '''Funcion del menu principal del inventario'''
    menu = True
    while menu:
        mostrar_menu()
        opcion = input(estilo_input + "\nIngrese la opcion deseada: ")
        if opcion == "1":
            nombre = input(estilo_input + "Ingrese el nombre del producto: ").capitalize()
            descripcion = input(estilo_input + "Descripcion: ").capitalize()
            cantidad = 0
            while cantidad <= 0:
                try:
                    cantidad = int(input(estilo_input + "Cantidad: "))
                    if cantidad <=0:
                        print(estilo_aviso + "Ingrese un numero mayor que 0")
                except ValueError:
                    print(estilo_aviso + "Ingrese un numero")
                    cantidad = 0
            precio = 0
            while precio <= 0:
                try:
                    precio = int(input(estilo_input + "Precio: "))
                    if precio <=0:
                        print(estilo_aviso + "Ingrese un numero mayor que 0")
                except ValueError:
                    print(estilo_aviso + "Ingrese un numero")
                    precio = 0
            categoria = input(estilo_input + "Categoria: ").capitalize()
            agregar_producto(nombre, descripcion, cantidad, precio, categoria)
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            reporte_bajo_stock()
        elif opcion == "6":
            buscar_producto_por_nombre()
        elif opcion == "7":
            print(estilo_despedida + "\nGracias por utilizar nuestro sistema.\n")
            menu = False
        else:
            print(estilo_alerta + "Opcion incorrecta\n")

main()