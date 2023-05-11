from os import system
system("cls")
import re
import random
import datetime
import json

########################     PROGRAMA   #################################


def dragon_ball_aplicacion(menu):
    seguir = True
    bandera_lista = False
    bandera_json = False
    while seguir:
        respuesta = dragon_ball_menu_principal(menu)
        print(f'Se ingreso la opcion: {respuesta}')
        match respuesta:
            case 1:
                lista_personajes = dragon_ball_traer_datos("DBZ.csv")
                bandera_lista = True
            case 2:
                if bandera_lista == True:
                    dragon_ball_cantidad_segun_caracteristica(lista_personajes, "raza")
                else:
                    print("No se trajo una lista del archivo")
            case 3:
                if bandera_lista == True:
                    dragon_ball_mostrar_nombre_poder_segun_caracteristica(lista_personajes, "raza")
                else:
                    print("No se trajo una lista del archivo")
            case 4:
                if bandera_lista == True:
                    dragon_ball_personajes_habilidad_ingresada(lista_personajes, "habilidades")
                else:
                    print("No se trajo una lista del archivo")
            case 5:
                if bandera_lista == True:
                    dragon_ball_generar_batalla(lista_personajes)
                else:
                    print("No se trajo una lista del archivo")
            case 6:
                if bandera_lista == True:
                    nombre_archivo = dragon_ball_json(lista_personajes)
                    bandera_json = True
                else:
                    print("No se trajo una lista del archivo")
            case 7:
                if bandera_lista == True:
                    if bandera_json == True:
                        dragon_ball_leer_json(nombre_archivo)
                    else:
                        print("No se creo ningun archivo en el punto 6")
                else:
                    print("No se trajo una lista del archivo")
            case 8:
                seguir = False


########################    MENU DEL PROGRAMA   #################################

def imprimir_menu(menu:tuple):
    '''
    Brief:
        Imprime el menu ingresado
    Parameters:
        menu:tuple -> El menu del juego
    Return:
        -1 -> Hubo un error
    '''
    if type(menu) == tuple and len(menu)>0:
        for option in menu:
            print(option)
    else: 
        return -1

def dragon_ball_menu_principal(menu):
    '''
    Brief:
        Imprime el menu ingresado y pide al usuario que elija la opcion
    Parameters:
        menu:tuple -> El menu del juego
    Return:
        int -> El numero del menu electo
        -1 -> Hubo un error
    '''
    if type(menu) == tuple and len(menu)>0:
        imprimir_menu(menu)
        while True:
            respuesta = input("Elija una opcion: ")
            if not respuesta.isnumeric():
                print("Error: No se encuentra dicha opcion")
                continue
            respuesta = int(respuesta)
            if respuesta > len(menu) or respuesta < 1:
                print("Error: No se encuentra dicha opcion")
                continue
            break
        return respuesta
    else:
        return -1

menu = \
        ("---------------------------------\n1) Traer datos desde archivo",
        "2) Listar cantidad por raza",
        "3) Listar personajes por raza",
        "4) Listar personajes por habilidad",
        "5) Jugar batalla",
        "6) Guardar Json",
        "7) Leer Json",
        "8) Salir del programa\n---------------------------------"
    )

###########      TRAER DATOS DESDE EL ARCHIVO (punto 1)        #############################

def crear_lista(path:str)->list:
    '''
    Breif:
        Crea una lista con los personajes y sus caracteristicas con el archivo ingresado.
    Parameters:
        path:str -> El path del archivo.
    Return:
        list-> Una lista con diccionarios que contiene la informacion del archivo.
        -1 -> Hubo un error
    '''
    if type(path) == str and len(path)>0:
        with open(path, "r", encoding="utf-8") as archivo:
            lista_personajes = []
            for line in archivo:
                registro = re.split(",|\n", line)
                personaje = {
                    "id": int(registro[0]),
                    "nombre": registro[1],
                    "raza": registro[2],
                    "poder_pelea": int(registro[3]),
                    "poder_ataque": int(registro[4]),
                    "habilidades": registro[5]
                }
                lista_personajes.append(personaje)
            return lista_personajes
    else:
        return -1

def normalizar_lista_personajes(path:str)->list:
    '''
    Breif:
        Modifica la lista creada con el archivo ingresado, enlistando la raza y las habilidades.
    Parameters:
        path:str -> El path del archivo.
    Return:
        list-> Una lista con diccionarios.
        -1 -> Hubo un error
    '''
    if type(path) == str and len(path)>0:
        lista_personajes = crear_lista(path)
        if type(lista_personajes) == list:
            for personaje in lista_personajes:
                if personaje["raza"] != "Shin-jin" and personaje["raza"]  != "Three-Eyed People":
                    personaje["raza"] = re.split("-",personaje["raza"])
                else:
                    personaje["raza"] = [personaje["raza"]]
                personaje["habilidades"] = (re.split("[|$%]+", personaje["habilidades"]))
                habilidad_normalizada = []
                for habilidad in personaje["habilidades"]:
                    habilidad_norma = habilidad.strip()
                    habilidad_normalizada.append(habilidad_norma)
                personaje["habilidades"] = habilidad_normalizada
            return lista_personajes
        else:
            return -1
    else:
        return -1

def dragon_ball_traer_datos(path:str):
    '''
    Breif:
        Devuelve la lista e informa sobre la funcion realizada
    Parameters:
        path:str -> El path del archivo.
    Return:
        list-> Una lista con diccionarios.
    '''
    if type(path) == str and len(path)>0:
        lista = normalizar_lista_personajes(path)
        if type(lista) == list:
            print('Se trajeron los datos con exito')   
            return lista
        else:
            print("Ocurrio un error con la extraccion de datos del archivo")
    else:
        print("Ocurrio un error con la extraccion de datos del archivo")

###########      PERSONAJES SEGUN CARACTERISTICA   ########################

def mostrar_caracteristicas(lista:list, atributo:str)->list:
    '''
    Brief: Crea una lista con los distintos tipos que existene de una variable determinada
    Parameters: 
        lista: list -> lista sobre la que voy a hacer la busqueda
        atributo: str -> La clave del diccionario de donde voy sacar los datos
    Return:
        list -> Una list con los distintos tipos de la variable ingresada
        -1 -> Hubo un error
    '''
    if type(lista) == list and len(lista)>0 and type(atributo) == str and len(atributo)>0:
        diccionario_carac = {}

        for personaje in lista:
            for caracteristica in personaje[atributo]:
                diccionario_carac[caracteristica] = 0
        return diccionario_carac
    else:
        return -1

def contar_personajes_segun_tipo(lista:list, atributo:str)->list:
    '''
    Brief: Crea una lista con los distintos tipos que existene 
    Parameters: 
        lista: list -> lista sobre la que voy a hacer la busqueda
        atributo: str -> La clave del diccionario de donde voy sacar los datos
    Return:
        list -> Una list con los distintos tipos de la variable ingresada
        -1 -> Hubo un error
    '''
    if type(lista) == list and len(lista)>0 and type(atributo) == str and len(atributo)>0:
        diccionario_carac = mostrar_caracteristicas(lista, atributo)
        if type(diccionario_carac) == dict:
            for personaje in lista:
                for caracteristica in personaje[atributo]:
                    diccionario_carac[caracteristica] += 1
            return diccionario_carac
        else:
            return -1
    else:
        return -1

def dragon_ball_cantidad_segun_caracteristica(lista:list, atributo:list):
    '''
    Brief: Muestra las caracteristicas y la cantidad de personajes que la poseen
    Parameters: 
        lista: list -> lista sobre la que voy a hacer la busqueda
        atributo: str -> La clave del diccionario de donde voy sacar los datos
    Return:
        None
    '''
    if type(lista) == list and len(lista)>0 and type(atributo) == str and len(atributo)>0:
        contar_segun = contar_personajes_segun_tipo(lista,atributo)
        print("La cantidad de personajes que se ingresaron segun las razas es:")
        for x in contar_segun:
            print(f'{x}: {contar_segun[x]}')
    else:
        print("Ocurrio un error en la funcion")

def mostrar_personaje_segun_caracteristica(lista:list, atributo:str)->dict:
    '''
    Brief: Enlista los personajes que cumplen con la caracteristica
    Parameters: 
        lista: list -> lista sobre la que voy a hacer la busqueda
        atributo: str -> La clave del diccionario de donde voy sacar los datos
    Return:
        dict -> Un diccionarion con los distintos tipos de la variable ingresada y los personajes que lo cumplan
        -1 -> Hubo un error
    '''
    if type(lista) == list and len(lista)>0 and type(atributo) == str and len(atributo)>0:
        diccionario_carac = mostrar_caracteristicas(lista, atributo)
        if type(diccionario_carac) == dict:
            for personaje in lista:
                    for caracteristica in personaje[atributo]:
                        if diccionario_carac[caracteristica] == 0:
                            diccionario_carac[caracteristica] = []
                        for tipo in diccionario_carac:
                            if tipo == caracteristica:
                                diccionario_carac[caracteristica].append(personaje)
            return diccionario_carac
        else:
            return -1
    else:
        return -1

def dragon_ball_mostrar_nombre_poder_segun_caracteristica(lista:list, atributo:str):
    '''
    Brief: 
        Muestra los nombres y poder de personajes que cumplen con la caracteristicas
    Parameters: 
        lista: list -> lista sobre la que voy a hacer la busqueda
        atributo: str -> La clave del diccionario de donde voy sacar los datos
    Return:
        None
    '''
    if type(lista) == list and len(lista)>0 and type(atributo) == str and len(atributo)>0:
        lista_personajes = mostrar_personaje_segun_caracteristica(lista, atributo)
        if type(lista_personajes) == dict:
            print("Los personajes con su poder segun las razas son:")
            for caracteristica in lista_personajes:
                print(f'\n{caracteristica}:\n')
                for personaje in lista_personajes[caracteristica]:
                    print(f'\t{personaje["nombre"]} : {personaje["poder_ataque"]}')
        else:
            print("Ocurrio un error en la funcion")
    else:
        print("Ocurrio un error en la funcion")

############    AGREGAR PROMEDIO ENTRE PELEA Y ATAQUE       ########################

def agregar_promedio_pelea_ataque(lista:list):
    '''
    Brief: suma los numeros de poder de pelea y ataque de los personajes de la lista
    Parameters: 
        lista: list -> lista sobre el que voy a ejecutar
    Return: 
        error:str -> Hubo un error
    '''
    if type(lista) == list and len(lista)>0:
        for personaje in lista:
            suma_dato = personaje["poder_pelea"] + personaje["poder_ataque"]
            promedio = suma_dato / 2
            personaje["promedio_pelea_ataque"] = promedio
    else:
        return "error"

###############     INGRESAR HABILIDAD     ################################

def ingresar(busqueda:str):
    '''
    Brief: Ingresar un dato
    Parameters: 
        busqueda:str -> que se desea buscar
    Return: 
        str -> La habilidad ingresada
    '''
    habilidad_ingresada = input(f"Ingrese {busqueda}: ")
    while len(habilidad_ingresada)<3 and type(habilidad_ingresada) == str:
        habilidad_ingresada = input(f"Error: Ingrese {busqueda}: ")
    return habilidad_ingresada

###############     INGRESAR HABILIDAD Y MOSTRAR PERSONAJES     #####################

def dragon_ball_personajes_habilidad_ingresada(lista:list, atributo:str):
    '''
    Brief: Muestra las caracteristicas y la cantidad de personajes que la poseen
    Parameters: 
        lista: list -> lista sobre la que voy a hacer la busqueda
        atributo: str -> La clave del diccionario de donde voy sacar los datos
    Return:
        None
    '''
    if type(lista) == list and len(lista)>0 and type(atributo) == str and len(atributo)>0:
        agregar_promedio_pelea_ataque(lista)
        habilidad_ingresada = ingresar("la habilidad")
        lista_personajes = mostrar_personaje_segun_caracteristica(lista, atributo)
        if habilidad_ingresada in lista_personajes:
            personajes_habilidad = lista_personajes[habilidad_ingresada]
            print("los personajes que poseen dicha habilidad son:")
            for personaje in personajes_habilidad:
                print("-------------------------------")
                for detalle in personaje:
                    if detalle == "nombre" or detalle == "raza" or detalle == "promedio_pelea_ataque":
                        print(f'{detalle}: {personaje[detalle]}')
        else:
            print("No se encontro dicha habilidad")
    else:
        print("Ocurrio un error en la funcion")

################        BATALLA         ###################################

def buscar_personaje_elegido(lista:list):
    '''
    Brief: Buscar el personaje elegido
    Parameters: 
        lista:list -> Lista donde buscar el personaje
    Return: 
        str -> El personaje ingresado
        -1 -> Error
    '''
    if type(lista) == list and len(lista)>0:
        while True:
            bandera_personaje = False
            nombre_elegido = ingresar("personaje")
            for personaje in lista:
                if personaje["nombre"] == nombre_elegido:
                    personaje_elegido = personaje
                    bandera_personaje = True
            if bandera_personaje == True:
                break
        return personaje_elegido
    else:
        return -1

def elegir_personaje_random(lista:list):
    '''
    Brief: Elegir un personaje random para ser contrincante
    Parameters: 
        lista:list -> Lista donde buscar el personaje
    Return: 
        str -> El personaje random
    '''
    if type(lista) == list and len(lista)>0:
        id_random = random.randint(0,len(lista))
        contrincante_random = lista[id_random]
        return contrincante_random
    else:
        return -1

def comparar_personajes(lista:list):
    '''
    Brief: Compara el poder de ataque de los personajes y da un ganador o un empate
    Parameters: 
        lista:list -> Lista donde buscar el personaje
    Return: 
        list -> Una lista con el ganador y el perdedor
        -1 -> Error
    '''
    if type(lista) == list and len(lista)>0:
        personaje_elegido = buscar_personaje_elegido(lista)
        contrincante = elegir_personaje_random(lista)
        if personaje_elegido == contrincante:
            contrincante = elegir_personaje_random(lista)
        if personaje_elegido["poder_ataque"] > contrincante["poder_ataque"]:
            ganador = personaje_elegido
            perdedor = contrincante
        elif personaje_elegido["poder_ataque"] < contrincante["poder_ataque"]:
            ganador = contrincante
            perdedor = personaje_elegido
        else:
            ganador = "EMPATE"
            perdedor = "EMPATE"
        return [ganador,perdedor]
    else:
        return -1

def guardar_batalla_archivo(ganador_perdedor):
    '''
    Brief: Guarda la batalla en un archivo de texto
    Parameters: 
        ganador_perdedor:list -> Lista que diga ganador y perdedor
    Return: 
        -1 -> Error
    '''
    if type(ganador_perdedor) == list and len(ganador_perdedor)>1:
        fecha_actual = datetime.date.today()
        mi_archivo = open("batallas.txt", "a", encoding="utf-8")
        mi_archivo.write(f'\n{fecha_actual}\n')
        mi_archivo.write(f'El ganador es: {ganador_perdedor[0]["nombre"]}\n')
        mi_archivo.write(f'El perdedor es: {ganador_perdedor[1]["nombre"]}')
        mi_archivo.close()
    else:
        return -1

def dragon_ball_generar_batalla(lista:list):
    '''
    Brief: Genera la batalla de los personajes
    Parameters: 
        lista:list -> Lista de los personajes
    Return: 
        None
    '''
    ganador_perdedor = comparar_personajes(lista)
    guardar_batalla_archivo(ganador_perdedor)
    print('Se produjo la batalla y se guardaron los datos en "batalla.txt"')

#################        ARCHIVO JSON            ####################################

def buscar_personajes(lista:list, atributo_elegido:str, atributo:str)->list:
    '''
    Brief:
        Busca los personajes que cumplan con el atributo ingresado
    Parameters:
        lista:list -> lista de personajes
        atributo_elegido: str -> caracteristica elegida por el usuario
        atributo:str -> El tipo de atributo (raza, habilidad)
    return:
        lista:list -> lista de los personajes que cumplen el atributo
        2: int -> No se encontro personajes con esa caracteristica
        -1 : int -> Hubo un error en los datos ingresados
    '''
    if type(lista) == list and type(atributo_elegido) == str and type(atributo) == str:
        lista_personajes = mostrar_personaje_segun_caracteristica(lista, atributo)
        if atributo_elegido in lista_personajes:
            personajes_habilidad = lista_personajes[atributo_elegido]
            lista = []
            for personaje in personajes_habilidad:
                lista.append(personaje)
            return lista
        else:
            return 2
    else: 
        return -1

def buscar_coincidencias(lista:list, raza:str, habilidad:str)->list:
    '''
    Brief:
        Busca los personajes que cumplan con ambos atributos ingresado
    Parameters:
        lista:list -> lista de personajes
        raza: str -> tipo de raza elegida por el usuario
        atributo:str -> tipo de habilidad elegida por el usuario
    return:
        lista_coincidencia:list -> lista de los personajes que cumplen con ambos atributos
        2: int -> Se ingreso una raza inexistente
        2: int -> Se ingreso una habilidad inexistente
        -1 : int -> Hubo un error en los datos ingresados
    '''
    if type(lista) == list and type(raza) == str and type(habilidad) == str:
        lista_raza = buscar_personajes(lista, raza, "raza")
        if lista_raza == 2:
            return 2
        lista_habilidad = buscar_personajes(lista, habilidad, "habilidades")
        if lista_habilidad == 2:
            return 3
        lista_coincidencia = []
        for personaje in lista_raza:
            if personaje in lista_habilidad:
                lista_coincidencia.append(personaje)
        return lista_coincidencia
    else:
        return -1

def guardar_json(raza:str, habilidad:str, lista_coincidencias)->str:
    '''
    Brief:
        Guarda una lista en un archivo .json
    Parameters:
        lista:list -> lista de personajes
        raza: str -> tipo de raza elegida por el usuario
        atributo:str -> tipo de habilidad elegida por el usuario
    return:
        nomenclatura : str -> El nombre del archivo
        3 : int -> Se ingreso mal un dato
    '''
    if type(raza) == str and type(habilidad) == str and type(lista_coincidencias) == list:
        nomenclatura = f"{raza} {habilidad}.json"
        nomenclatura = nomenclatura.replace(" ", "_")
        lista = definir_que_agregar_json(lista_coincidencias, habilidad)
        if lista == 1:
            print("No hay personajes con esa raza y habilidad")
        else:
            with open(f"{nomenclatura}", "w", encoding="utf-8") as mi_archivo:
                json.dump(lista, mi_archivo, indent=4)
            print("Se creo el archivo .json con los datos ")
            return nomenclatura
    else:
        return 3

def definir_que_agregar_json(lista_coincidencias:list, habilidad:str):
    '''
    Brief:
        Define que se va a guardar en el archivo .json
    Parameters:
        lista_coincidencias:list -> lista de personajes que coinciden con ambos atributos ingresados
        habilidad: str -> La habilidad elegida por el usuario
    return:
        1 : int -> Si la lista esta vacia (no existen personajes)
        lista:list -> Una lista de str con el formato del personaje para guardar en .json
        -1: int -> Error en los datos ingresados
    '''
    if type(habilidad) == str and type(lista_coincidencias) == list:
        lista = []
        if lista_coincidencias == []:
            return 1
        else:
            for personaje in lista_coincidencias:
                habilidades = []
                for caracteristica in personaje['habilidades']:
                    if caracteristica != habilidad:
                        habilidades.append(caracteristica)
                personaje_ = {
                    "nombre" : personaje ["nombre"], 
                    "poder_pelea" : personaje ["poder_pelea"],
                    "habilidades": habilidades
                    }
                lista.append(personaje_)
            return lista
    else: 
        return -1    

def dragon_ball_json(lista:list):
    '''
    Brief:
        Hace ingresar al usuario un tipo de raza y habilida, busca personajes que tenga ambas
        y los guarda en un .json, nombrado en articular.
    Parameters:
        lista:list -> lista de personajes
    return:
        nombre_json :str ->El nombre del archivo creado
    '''
    if type(lista) == list:
        raza = ingresar("una raza")
        habilidad = ingresar("una habilidad")
        lista_coincidencia = buscar_coincidencias(lista, raza, habilidad)
        if type(lista_coincidencia) == int:
            print("Se ingreso una habilidad o raza inexistente")
        else:
            nombre_json = guardar_json(raza, habilidad, lista_coincidencia)
            return nombre_json
    else:
        print("Error en los datos ingresados")

################    LEER .JSON ######################################

def leer_json(nombre_archivo:str)->list:
    '''
    Brief:
        Lee el archivo .json
    Parameters:
        nombre_archivo:str -> nombre del archivo .json
    return:
        data:list ->El archivo en forma de lista
    '''
    with open(nombre_archivo, "r") as mi_archivo:
        data = json.load(mi_archivo)
        return data

def dragon_ball_leer_json(nombre_archivo:str):
    '''
    Brief:
        imprime la lista de personajes del archivo .json
    Parameters:
        nombre_archivo:str -> nombre del archivo .json
    return:
        None
    '''
    if type(nombre_archivo) == str:
        data = leer_json(nombre_archivo)
        print("Los personajes guardados en el punto 6 son: ")
        for x in range(len(data)):
            print(data[x])
    else:
        print("No se creo ningun archivo")

##########     HACER FUNCIONAR AL PROGRAMA      ###########

dragon_ball_aplicacion(menu)