"""
27/11/2023

Práctica del examen para realizar en casa
-----------------------------------------

* El programa debe estar correctamente documentado.

* Debes intentar ajustarte lo máximo que puedas a lo que se pide en los comentarios TODO.

* Tienes libertad para desarrollar los métodos o funciones que consideres, pero estás obligado a usar como mínimo todos los que se solicitan en los comentarios TODO.

* Además, tu programa deberá pasar correctamente las pruebas unitarias que se adjuntan en el fichero test_agenda.py, por lo que estás obligado a desarrollar los métodos que se importan y prueban en la misma: pedir_email(), validar_email() y validar_telefono()

"""

import os
import pathlib
from os import path

# Constantes globales
RUTA = pathlib.Path(__file__).parent.absolute() 

NOMBRE_FICHERO = 'contactos.csv'

RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)

#TODO: Crear un conjunto con las posibles opciones del menú de la agenda
OPCIONES_MENU = {1,2,3,4,5,6,7,8}
#TODO: Utiliza este conjunto en las funciones agenda() y pedir_opcion()


def borrar_consola():
    """ Limpia la consola
    """
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def cargar_contactos(contactos: list) -> list:
    """ Carga los contactos iniciales de la agenda desde un fichero
    Args:

        contactos (list[dict]): Una lista conformada por diccionarios, siendo cada diccionario
        un contacto.

    Returns:

        contactos (lista[dict]): Una lista con los contactos cargados del archivo contactos.csv.
    """
    #TODO: Controlar los posibles problemas derivados del uso de ficheros...
    vaciar_agenda(contactos)
    todo_escrito = False
    while not todo_escrito:
        with open(RUTA_FICHERO, 'r') as fichero:
            claves = ('nombre','apellido','email','telefonos')
            if not fichero == '':
                for linea in fichero:
                    datos = linea.rstrip('\n').split(';')
                    contacto = {}
                    numeros = []

                    for i,dato in enumerate(datos):
                        if i>2 and len(datos) > 3:
                            numeros.append(dato)

                        elif i < 3:
                            contacto.setdefault(claves[i],dato)
                    
                    if len(numeros) > 0:
                        contacto.setdefault(claves[3],numeros)
                    else:
                        contacto.setdefault(claves[3],numeros)
                    contactos.append(contacto)

                todo_escrito = True
                return contactos
            
            else:
                print('El fichero esta vacío')

def buscar_contacto(contactos:list[dict],email:str) -> int:
    """Busca en la lista de contactos algunoo que tenga el mismo e-mail que el introducido por el usuario.

    Args: 
        contactos (list[dict]): Lista de diccionarios con cada diccionario siendo un contacto.
        email (str): Correo electrónico introducido por el usuario que se busca en la lista.

    Returns:
        i (int): La posicion en la que se encuentra el diccionario que contiene el email dentro de la lista.
    """
    for i, contacto in enumerate(contactos):
        for dato in contacto.values():
            if email == dato:
                return i
            
def eliminar_contacto(contactos: list, email: str):
    """ Elimina un contacto de la agenda
    
    Args: 
        contactos (list[dict]): Lista de diccionarios con cada diccionario siendo un contacto.
        email (str): Correo electrónico introducido por el usuario que se busca en la lista.
    """
    try:
        #TODO: Crear función buscar_contacto para recuperar la posición de un contacto con un email determinado
        pos = buscar_contacto(contactos,email)
        if pos != None:
            del contactos[pos]
            print("Se eliminó 1 contacto")
        else:
            print("No se encontró el contacto para eliminar")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se eliminó ningún contacto")

def mostrar_menu():
    """Muestra el menu con las distintas opciones que tiene el usuario.
    """
    print('--------')
    print('Menu')
    print('1. Nuevo contacto')
    print('2. Modificar contacto')
    print('3. Eliminar contacto')
    print('4. Vaciar agenda')
    print('5. Cargar agenda inicial')
    print('6. Mostrar contactos por criterio')
    print('7. Mostrar la agenda completa')
    print('8. Salir')
    print('--------')

def pedir_opcion():
    """Pide al usuario introducir una opción de las disponibles, sino retorna -1.

    Returns: 
        -1 (int): Valor que devuelve si la opción no es válida.
        opcion_entero (int): La opción elegida por el usuario.
    """
    opcion = input('\n>> Seleccione una opción:')
    try:

            opcion_entero = int(opcion)
            
            if opcion_entero not in OPCIONES_MENU:
                if OPCIONES_MENU ^ {opcion_entero}:
                    raise ValueError(f'Opción no válida. Debe ser un número entero del 1 al 7.')
            
            return opcion_entero
        
    except ValueError as e:
            print(f"Error: {e}")
            return -1

def validar_email(email:str, contactos_iniciales:list[dict], check:bool):
    """Valida un correo electrónico.

    Args:
        email (str): El correo electrónico a validar.
        contactos_iniciales (list): Lista de contactos iniciales para verificar duplicados.
        check (bool): Si es True, verifica duplicados en la lista de contactos iniciales.

    Raises:
        ValueError: Se da en tres casos
            1.El email es una cadena vacía.
            2.El email no contiene el símbolo '@' o '.'.
            3.Si check es True, busca si el correo existe en la lista de contactos.

    """
    if email == '':
        raise ValueError("el email no puede ser una cadena vacía")
    
    if "@" not in email or "." not in email:
        raise ValueError("el email no es un correo válido")

    if check and any(contacto['email'] == email for contacto in contactos_iniciales): #con que haya una coincidencia dentro de any(), devuelve True.
        raise ValueError("el email ya existe en la agenda")

  


def pedir_email(contactos_iniciales, check):
    """Valida un correo electrónico.

    Args:
        contactos_iniciales (list[dict]): Lista de contactos iniciales para verificar duplicados.
        check (bool): Si es True, verifica duplicados en la lista de contactos iniciales.

    Returns:
        email (str): El correo electrónico introducido por el usuario.
    """
    email = input("Ingrese su correo electrónico: ")

    validar_email(email, contactos_iniciales, check)

    return email

def pedir_nombre():
    """Pide introducir un nombre

    Returns:
        nombre (str): El nombre introducido por el usuario, el cual puede ser compuesto.

    Raises:
        TypeError: Si el nombre introducido es una cadena vacía.
    """

    try:
        nombre = input('Nombre -> ')
        if nombre.strip() == '':
            raise TypeError('No ha introducido ningun nombre')
        
        elif ' ' in nombre:
            nombre = nombre.split()
            nombre = ' '.join(nombre_compuesto.capitalize() for nombre_compuesto in nombre)

        return nombre
    
    except TypeError as e:
        print(e)
        
def pedir_apellido():
    """Pide introducir un apellido
    Returns:
        apellido (str): El apellido introducido por el usuario, el cual puede ser compuesto.

    Raises:
        TypeError: Si el apellido introducido es una cadena vacía.
    """

    try:
        apellido = input('Apellido -> ')
        if apellido.strip() == '':
            raise TypeError('No ha introducido ningun nombre')
        
        elif ' ' in apellido:
            apellido = apellido.split()
            apellido = ' '.join(nombre_compuesto.capitalize() for nombre_compuesto in apellido)

        return apellido
    
    except TypeError as e:
        print(e)

def validar_telefono(numero) -> bool:
        """Valida un número de teléfono.

        Args:
            numero (str): Un número de telefono que puede tener o no un prefijo +34.

        Returns:
            True (bool): Si en sus primeras 3 posiciones tiene el prefijo +34 o si tiene 9 numeros enteros y son numericos.
            False (bool): Si no se cumplen alguna de las dos condiciones anteriores.
        """

        if ((numero[:3] == '+34') and len(numero) == 12 and numero[1:].isdigit()) or len(numero) == 9 and numero.isdigit():
            return True
        else:
            return False
        
def pedir_telefono() -> list:
    """Pide un numero de telefono que es validado por la funcion validar_telefono

    Returns:
        numeros (list): Lista de numeros de telefonos (puede estar vacia)
    """
    numeros = []
    numero = None

    while numero != '':
        numero = input('Introduce numeros (ENTER PARA SALIR) -> ').strip().replace(' ','')
        if validar_telefono(numero):
            numeros.append(numero)
        else:
            print('Formato inválido')
        

    return numeros

def agregar_contacto(contactos:list) -> list:
    """Pide diversos datos para agregar un nuevo contacto a la lista.

    Args:
        contactos (list[dict]): Lista de diccionarios con cada diccionario siendo un contacto.

    Raises:
        ValueError: Si hay algun fallo en la introduccion de los propios datos.
    """
    try:
        claves = ('nombre','apellido','email','telefonos')
        datos = []
        contacto = {}
        i = 0

        nombre = pedir_nombre()
        apellidos = pedir_apellido()
        correo = pedir_email(contactos,False)
        numeros = pedir_telefono()
        
        datos.extend([nombre,apellidos,correo,numeros])

        for clave in claves:
            contacto.setdefault(clave,datos[i])
            i += 1

        contactos.append(contacto)

    except ValueError as e:
        print(f'ERROR {e}')

def modificar_contacto(contactos:list[dict]) -> list:
    """Modifica un contacto ya existente en la lista con su email.

    Args:
        contactos (list[dict]): Lista de diccionarios con cada diccionario siendo un contacto.
    
    Raises:
        ValueError: Si hay algun problema introduciendo los datos.
    """
    try:
        email = input('Introduzca el e-mail del usuario a modificar -> ')
        dato = None
        for contacto in contactos:
            if email in contacto.values():
                dato_a_cambiar = input('Dato a cambiar (email/nombre/apellido/telefonos) -> ').lower().strip()
                match dato_a_cambiar:
                    case 'email':
                        dato = pedir_email(contactos,True)
                    case 'nombre':
                        dato = pedir_nombre()
                    case 'apellido':
                        dato = pedir_apellido()
                    case 'telefonos':
                        dato = pedir_telefono()
            
                contacto[dato_a_cambiar] = dato

                
    except ValueError as e:
        print(f'ERROR {e}')

def vaciar_agenda(contactos:list[dict]):
    """Vacia toda la lista de contactos.
    
    Args:
        contactos (list[dict]): Lista de diccionarios con cada diccionario siendo un contacto.

    Returns:
        contactos (list): Una lista vacia.
    """
    contactos.clear()

    return contactos

def format_numero(numero:str):
    """Si es un numero con prefijo, lo retorna en el formato buscado.

    Args:
        numero (str): Un numero telefonico con prefijo +34.

    Returns:
        numero (str): Numero telefonico con el prefijo y el numero separado por -.
    """
    if len(numero) == 12:
        return numero[:3] + '-' + numero[3:]
    return numero

def mostrar_usuario(nombre:str,contactos:list[dict]):
    """Muestra un usuario de la lista de contactos.

    Args:
        nombre (str): Nombre de una persona de la lista de contactos.
        contactos (list[dict]): Lista de diccionarios con cada diccionario siendo un contacto.

    """
    for contacto in contactos:
        if contacto.get('nombre') == nombre:
            correo = contacto.get('email')
            numeros = contacto.get('telefonos')
            apellido = contacto.get('apellido')

            print(f'Nombre: {nombre} {apellido} ({correo})')

            if not numeros == []:
                print('Telefonos:',end='')
                formatted_numbers = [format_numero(numero) for numero in numeros]
                print('/'.join(formatted_numbers))
            else:
                print('Telefonos: Ninguno')

def mostrar_contactos(contactos:list[dict]):
    """Muestra todos los contactos de la lista.

    Args:
        contactos (list[dict]): Lista de diccionarios con cada diccionario siendo un contacto.
    """
    nombres = []
    for contacto in contactos:
        nombres.append(contacto.get('nombre'))
    nombres.sort()

    print(f'Agenda {len(contactos)}')
    print('------')
    for nombre in nombres:
        mostrar_usuario(nombre,contactos)
        print('------')

def mostrar_usuario_criterio(contactos:list[dict],criterio:str,parametro:str):
    """Muestra los usuario que coincidan con el parametro introducido.

    Args:
        contactos (list[dict]): Lista de diccionarios con cada diccionario siendo un contacto.
        criterio (str): Que clave va a buscar en los clientes.
        parametro (str): La coincidencia que debe haber con los valores del criterio en cuestion.
    """
    print('Contactos coincidentes')
    print('------')

    for contacto in contactos:
        value = contacto.get(criterio, '')
        if any(parametro in number for number in value) or parametro in value:
            correo = contacto.get('email', '')
            numeros = contacto.get('telefonos', [])
            nombre = contacto.get('nombre', '')
            apellido = contacto.get('apellido','')
            
            print(f'Nombre: {nombre} {apellido} ({correo})')
            if numeros:
                print('Telefonos:', end='')
                formatted_numbers = [format_numero(numero) for numero in numeros]
                print('/'.join(formatted_numbers))
            else:
                print('Telefonos: Ninguno')
            print('------')
            
def mostrar_contactos_por_criterio(contactos:list[dict]):
    """Muestra todos los contactos que coincidan con un parametro en un criterio concreto.

    Args:
        contactos (list[dict]): Lista de diccionarios con cada diccionario siendo un contacto.
    """

    criterio = input('¿Que criterio usara para la busqueda? (email/nombre/apellido/telefonos) -> ').lower().strip()
    parametro = input('Parametro de busqueda ->')

    mostrar_usuario_criterio(contactos,criterio,parametro)
  

def agenda(contactos: list[dict]):
    """ Ejecuta el menú de la agenda con varias opciones
    
    Args:
        contactos (list[dict]): Lista de diccionarios con cada diccionario siendo un contacto.
    """
    #TODO: Crear un bucle para mostrar el menú y ejecutar las funciones necesarias según la opción seleccionada...
    opcion = None
    while opcion != 8:
        mostrar_menu()
        opcion = pedir_opcion()

        #TODO: Se valorará que utilices la diferencia simétrica de conjuntos para comprobar que la opción es un número entero del 1 al 7
        match opcion:
            case 1:
                agregar_contacto(contactos)
            case 2:
                borrar_consola()
                mostrar_contactos(contactos)
                modificar_contacto(contactos)
            case 3:
                try:
                    borrar_consola()
                    mostrar_contactos(contactos)
                    email = pedir_email(contactos,False)
                    eliminar_contacto(contactos,email)
                except ValueError as e:
                    print(f'ERROR {e}')
            case 4:
                vaciar_agenda(contactos)
            case 5:
                cargar_contactos(contactos)
            case 6:
                borrar_consola()
                mostrar_contactos(contactos)
                mostrar_contactos_por_criterio(contactos)
            case 7:
                mostrar_contactos(contactos)

        print('Gracias por usar la mejor agenda.')
        pulse_tecla_para_continuar()
        borrar_consola()


def pulse_tecla_para_continuar():
    """ Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("\n")
    input("Presione Enter para continuar...")


def main():
    """ Función principal del programa
    """
    borrar_consola()

    #TODO: Asignar una estructura de datos vacía para trabajar con la agenda
    contactos = []

    #TODO: Modificar la función cargar_contactos para que almacene todos los contactos del fichero en una lista con un diccionario por contacto (claves: nombre, apellido, email y telefonos)
    #TODO: Realizar una llamada a la función cargar_contacto con todo lo necesario para que funcione correctamente.
    cargar_contactos(contactos)

    #TODO: Crear función para agregar un contacto. Debes tener en cuenta lo siguiente:
    # - El nombre y apellido no pueden ser una cadena vacía o solo espacios y se guardarán con la primera letra mayúscula y el resto minúsculas (ojo a los nombre compuestos)
    # - El email debe ser único en la lista de contactos, no puede ser una cadena vacía y debe contener el carácter @.
    # - El email se guardará tal cuál el usuario lo introduzca, con las mayúsculas y minúsculas que escriba. 
    #  (CORREO@gmail.com se considera el mismo email que correo@gmail.com)
    # - Pedir teléfonos hasta que el usuario introduzca una cadena vacía, es decir, que pulse la tecla <ENTER> sin introducir nada.
    # - Un teléfono debe estar compuesto solo por 9 números, aunque debe permitirse que se introduzcan espacios entre los números.
    # - Además, un número de teléfono puede incluir de manera opcional un prefijo +34.
    # - De igual manera, aunque existan espacios entre el prefijo y los 9 números al introducirlo, debe almacenarse sin espacios.
    # - Por ejemplo, será posible introducir el número +34 600 100 100, pero guardará +34600100100 y cuando se muestren los contactos, el telófono se mostrará como +34-600100100. 
    #TODO: Realizar una llamada a la función agregar_contacto con todo lo necesario para que funcione correctamente.
    agregar_contacto(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Realizar una llamada a la función eliminar_contacto con todo lo necesario para que funcione correctamente, eliminando el contacto con el email rciruelo@gmail.com
    
    eliminar_contacto(contactos,'rciruelo@gmail.com')

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear función mostrar_contactos para que muestre todos los contactos de la agenda con el siguiente formato:
    # ** IMPORTANTE: debe mostrarlos ordenados según el nombre, pero no modificar la lista de contactos de la agenda original **
    #
    # AGENDA (6)
    # ------
    # Nombre: Antonio Amargo (aamargo@gmail.com)
    # Teléfonos: niguno
    # ......
    # Nombre: Daniela Alba (danalba@gmail.com)
    # Teléfonos: +34-600606060 / +34-670898934
    # ......
    # Nombre: Laura Iglesias (liglesias@gmail.com)
    # Teléfonos: 666777333 / 666888555 / 607889988
    # ......
    # ** resto de contactos **
    #
    #TODO: Realizar una llamada a la función mostrar_contactos con todo lo necesario para que funcione correctamente.
    mostrar_contactos(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear un menú para gestionar la agenda con las funciones previamente desarrolladas y las nuevas que necesitéis:
    # AGENDA
    # ------
    # 1. Nuevo contacto
    # 2. Modificar contacto
    # 3. Eliminar contacto
    # 4. Vaciar agenda
    # 5. Cargar agenda inicial
    # 6. Mostrar contactos por criterio
    # 7. Mostrar la agenda completa
    # 8. Salir
    #
    # >> Seleccione una opción: 
    #
    #TODO: Para la opción 3, modificar un contacto, deberás desarrollar las funciones necesarias para actualizar la información de un contacto.
    #TODO: También deberás desarrollar la opción 6 que deberá preguntar por el criterio de búsqueda (nombre, apellido, email o telefono) y el valor a buscar para mostrar los contactos que encuentre en la agenda.
    agenda(contactos)


if __name__ == "__main__":
    main()