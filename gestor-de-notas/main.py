import mysql.connector
import os
import time

# conexion a la base de datos
database = mysql.connector.connect(
 	host= "localhost",
 	user = "alex",
 	passwd = "mortadela",
    database = "data_notes_db" 
)

cursor = database.cursor(buffered = True)
# crea la tabla usuarios si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id int(10) auto_increment not null,
    name varchar(20) not null UNIQUE,
    password varchar(10) not null UNIQUE,
    email varchar(30) not null,
    CONSTRAINT pk_users PRIMARY KEY(id)
)
""")
# crea la tabla para guardar las notas en caso de que no exista
cursor.execute("""
CREATE TABLE IF NOT EXISTS notes(
    owner varchar(20) not null UNIQUE,
    name varchar(30) not null UNIQUE,
    content text not null,
    CONSTRAINT pk_notes PRIMARY KEY(owner)
)
"""
)
# limpiar todo el texto que hay en la consola en ese momento
def limpiar_consola():
    if os.name == "nt":
        os.system('cls') # en caso de que se ejecute en windows
    else:
        os.system('clear') # en caso de que se ejecute en linux

def crear_usuario():
    limpiar_consola()
    print("---------- Crear usuario ----------\n\n")
    nuevo_nombre = str(input("* Ingrese un nombre: \n")).strip()
    nueva_contraseña = str(input("* Ingrese una contraseña: \n")).strip()
    nuevo_correo = str(input("* Ingrese un correo electronico: \n")).strip()
    try:
        cursor.execute("INSERT INTO users(name, password, email) VALUES (null, %s, %s, %s)", (nuevo_nombre, nueva_contraseña, nuevo_correo))
        database.commit()
        print("\n* Correcto\n")
        print(f"* Se creo el usuario {nuevo_nombre}")
        time.sleep(2)
        limpiar_consola()
    except mysql.connector.errors.IntegrityError:
        print("* Error: el nombre o la contraseña ya existen, porfavor ingrese uno/s nuevo/s *\n")
        time.sleep(3)
def iniciar_sesion():
    limpiar_consola()
    print("---------- Iniciar sesion ----------\n\n")
    global nombre
    nombre = str(input("*Ingrese el nombre: \n")).strip()
    contraseña = str(input("*Ingrese la contraseña: \n")).strip()
    cursor.execute("SELECT name, password FROM users WHERE name = %s AND password = %s", (nombre, contraseña))
    result = cursor.fetchall()
    if len(result) > 0 and result[0][0] == nombre and result[0][1] == contraseña:
        print("\n* Sesion iniciada correctamente *\n")
        time.sleep(3)
        limpiar_consola()
        print(f"-- Bienvenido {nombre}, aca estan las acciones disponibles --\n\n")

    else:
        print("\n* Usuario no encontrado *\n")
        time.sleep(3)
        limpiar_consola()

def crear_nota():
    limpiar_consola()
    titulo = str(input("* Introduce el titulo de la nota: "))
    contenido = str(input("\n* Introduce el contenido de la nota (maximo 200 caracteres): \n"))
    try:
        cursor.execute("INSERT INTO notes (owner, name, content) VALUES (%s, %s, %s)", (nombre, titulo, contenido))
        database.commit()
        print("\n\n* Se ha creado la nota exitosamente *")
        time.sleep(3)
    except mysql.connector.errors.IntegrityError:
        print("* Error: la nota ya existe *\n")
        time.sleep(3)
def abrir_nota():
    limpiar_consola()
    cursor.execute(f"SELECT name FROM notes WHERE owner = '{nombre}'")
    notes_list = cursor.fetchall()
    if notes_list:
        print(f"---------- Notas de {nombre} ----------\n")
        for note in notes_list:
            print(f"- {note}\n")
        search = str(input("* Ingrese el titulo de la nota que desea abrir: \n")).lower().strip()
        try:
            cursor.execute(f"SELECT name, content FROM notes WHERE owner LIKE '{nombre}' AND name LIKE '{search}'")
            content = cursor.fetchall()
            while True:
                limpiar_consola()
                print(f"-- {content[0][0]} --\n\n")
                print(f"* {content[0][1]}\n\n")
                salida = str(input("* Ingrese salir para cerrar la nota\n")).lower().strip()
                if salida == "salir":
                    break
                else:
                    print("* no es valido\n")
                    continue
        except IndexError:
            print(f"* Error: no existe una nota con el nombre {search}")
            time.sleep(3)
    else:
        print("* No tienes ninguna nota creada *\n")
        time.sleep(3)

def eliminar_nota():
    limpiar_consola()
    cursor.execute(f"SELECT name FROM notes WHERE owner LIKE '{nombre}'")
    notes_list = cursor.fetchall()
    if notes_list:
        print(f"---------- Notas de {nombre} ----------\n")
        for note in notes_list:
            print(f"- {note}\n")
        search = str(input("* Ingrese el titulo de la nota que desea eliminar: \n")).lower().strip()
        cursor.execute(f"DELETE FROM notes WHERE name = %s", [search])
        if cursor.rowcount > 0:
            database.commit()
            print(f"* La nota {search} ha sido eliminada exitosamente *")
            time.sleep(3)
        else:
            print(f"* Error: no existe una nota con el nombre {search} *\n")
            time.sleep(3)
    else:
        print("* No tienes ninguna nota creada *\n")
        time.sleep(3)
            
# bucle de inicio del programa
while True:
    limpiar_consola()
    print("---------- NotePad ----------\n")
    print("-- Bienvenido al gestor de notas--\n\n")
    print("* Iniciar sesion *\n")
    print("* Crear usuario *\n")
    print("* Cerrar\n")
    inicio = str(input("¿Que desea hacer?\n")).lower().strip()

    if inicio == "crear":
        crear_usuario()
        continue
    elif inicio == "iniciar":
        iniciar_sesion()
        
        # bucle de acciones disponibles
        while True:
            limpiar_consola()
            print("* crear una nueva nota\n")
            print("* abrir una nota\n")
            print("* eliminar una nota\n")
            print("* salir\n")
            accion = str(input("¿que desea hacer?\n")).lower().strip()
            if accion == "crear":
                crear_nota()
                continue
            elif accion == "abrir":
                abrir_nota()
                continue
            elif accion == "eliminar":
                eliminar_nota()
                continue
            elif accion == "salir":
                break
            else:
                print("* no valido, ingrese una de las opciones disponibles")
                time.sleep(2)
                continue
    elif inicio == "cerrar":
        break
    else:
        print("* no valido, ingrese una de las opciones disponibles")
        time.sleep(2)
        continue