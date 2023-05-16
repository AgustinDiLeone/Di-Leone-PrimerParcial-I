from os import system
system("cls")
import re
import random
import datetime
import json

########################     PROGRAMA   #################################
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
        "8) Mejorar los Saiyan",
        "9) Salir del programa\n---------------------------------"
    )

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
                if bandera_lista == True:
                    deragon_ball_mejorar_Saiyan(lista_personajes)
                else:
                    print("No se trajo una lista del archivo")
            case 9:
                seguir = False


###############         TRAER LISTA DE UN ARCHIVO       #########################################


def parser_csv(path:str)->list:
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
        lista_personajes = []
        with open(path, "r", encoding="utf-8") as archivo:
            for line in archivo:
                registro = re.split(",|\n", line)
                personaje = {
                    "id": int(registro[0]),
                    "nombre": (registro[1]).lower(),
                    "raza": registro[2].lower(),
                    "poder_pelea": int(registro[3]),
                    "poder_ataque": int(registro[4]),
                    "habilidades": registro[5].lower()
                }
                lista_personajes.append(personaje)
        return lista_personajes

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
        lista_personajes = parser_csv(path)
        if type(lista_personajes) == list:
            for personaje in lista_personajes:
                if personaje["raza"] != "shin-jin" and personaje["raza"]  != "three-eyed people":
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


######################## IMPRIMIR DICCIONARIO #######################################

def imprimir_diccionarios(diccionario:dict):
    '''
    Breif:
        Imprime el diccionario
    Parameters:
        diccionario:dict -> El diccionario a imprimir
    Return:
        -1: Error
    '''
    if type(diccionario) == dict:
        for key in diccionario:
            print(f'{key.capitalize()}: {diccionario[key]}')
    else:
        return -1

################# MUESTRA TODOS LOS TIPOS SEGUN LA KEY ##############################

def mostrar_caracteristicas(lista:list, key:str)->set:
    '''
    Brief: Crea un set con los distintos tipos que existene de una key
    Parameters: 
        lista: list -> lista sobre la que voy a hacer la busqueda
        key: str -> La clave del diccionario de donde voy sacar los datos
    Return:
        set -> Un set con los distintos tipos de la variable ingresada
        -1 -> Hubo un error
    '''
    if type(lista) == list and len(lista)>0 and type(key) == str and len(key)>0:
        lista_caracteristicas = []
        for personaje in lista:
            for caracteristica in personaje[key]:
                lista_caracteristicas.append(caracteristica)
        set_caracteristicas = set(lista_caracteristicas)
        return set_caracteristicas
    else:
        return -1

#################   CUENTA SEGUN LA KEY     #####################################

def contar_segun_caracteristicas(lista:list, key:str)->list:
    '''
    Breif:
        crea un diccionario con la cantidad de personajes que poseen cierta caracteristica
    Parameters:
        lista:list -> Una lista de personajes 
        key:str -> La clave del diccionario segun la caracteristica deseada
    Return:
        list-> Una lista con diccionarios.
    '''
    if type(lista) == list and len(lista)>0 and type(key) == str and len(key)>0:
        set_carac = mostrar_caracteristicas(lista, key)
        diccionario = {}
        for caracteristica in set_carac:
            contador = 0
            for personaje in lista:
                for atributo in personaje[key]:
                    if caracteristica == atributo:
                        contador += 1
            diccionario[caracteristica] = contador
        return diccionario
    else:
        return -1

#################       REALIZA FUNCION DEL PUNTO 4 ####################################

def dragon_ball_cantidad_segun_caracteristica(lista:list, key:str):
    '''
    Breif:
        Imprime la cantidad de personajes que poseen cada caracteristica
    Parameters:
        lista:list -> Una lista de personajes 
        key:str -> La clave del diccionario segun la caracteristica deseada
    Return:
        None
    '''
    if type(lista) == list and len(lista)>0 and type(key) == str and len(key)>0:
        diccionario = contar_segun_caracteristicas(lista, key)
        impresion = imprimir_diccionarios(diccionario)
        if impresion == -1:
            print("Hubo un error")
    else:
        print("se ingresaron mal los datos")


###############################################################################################3
def mostrar_personaje_segun_caracteristica(lista:list, key:str)->dict:
    '''
    Breif:
        Crea un diccionario con los personajes que cumplen con cada caracteristica
    Parameters:
        lista:list -> Una lista de personajes 
        key:str -> La clave del diccionario segun la caracteristica deseada
    Return:
        list-> Una lista con diccionarios.
        -1:int -> Hubo un error
    '''
    if type(lista) == list and len(lista)>0 and type(key) == str and len(key)>0:
        lista_carac = mostrar_caracteristicas(lista, key)
        diccionario = {}
        for caracteristica in lista_carac:
            lista_personajes = []
            for personaje in lista:
                for atributo in personaje[key]:
                    if caracteristica == atributo:
                        lista_personajes.append(personaje)
            diccionario[caracteristica] = lista_personajes
        return diccionario
    else:
        return -1

def dragon_ball_mostrar_nombre_poder_segun_caracteristica(lista:list, key:str):
    '''
    Brief: 
        Muestra los nombres y poder de personajes que cumplen con la caracteristicas
    Parameters: 
        lista: list -> lista sobre la que voy a hacer la busqueda
        atributo: str -> La clave del diccionario de donde voy sacar los datos
    Return:
        None
    '''
    if type(lista) == list and len(lista)>0 and type(key) == str and len(key)>0:
        diccionario = mostrar_personaje_segun_caracteristica(lista, key)
        if type(diccionario) == dict:
            print("Los personajes con su poder segun las razas son:")
            for caracteristica in diccionario:
                print(f'\n{caracteristica}:\n')
                for personaje in diccionario[caracteristica]:
                    print(f'\t{personaje["nombre"]} : {personaje["poder_ataque"]}')
        else:
            print("Ocurrio un error en la funcion")
    else:
        print("Ocurrio un error en la funcion")


##################################################################################################

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

def ingresar(busqueda:str):
    '''
    Brief: Ingresar un dato
    Parameters: 
        busqueda:str -> que se desea buscar
    Return: 
        str -> La habilidad ingresada
    '''
    habilidad_ingresada = input(f"Ingrese {busqueda}: ")
    habilidad_ingresada = habilidad_ingresada.lower()
    return habilidad_ingresada

#################################################################################################

def validar_dato_ingresado(dato_ingresado:str, lista)->bool:
    '''
    Brief: 
        Valida que el dato ingresado por el usuario se encuentre en la lista
    Parameters: 
        lista: list/set -> lista sobre la que voy a hacer la busqueda
        dato_ingresado: str -> El dato que verifico si se encuentra
    Return:
        bool -> Si esta True o sino False
        1:int -> Error
    '''
    if type(dato_ingresado) == str and type(lista) == list or type(lista) == set:
        if dato_ingresado in lista:
            return True
        else:
            return False
    else:
        return 1

def buscar_personajes(lista:list, atributo_elegido:str, key:str)->list:
    '''
    Brief:
        Busca los personajes que cumplan con el key ingresado
    Parameters:
        lista:list -> lista de personajes
        atributo_elegido: str -> caracteristica elegida por el usuario
        key:str -> El tipo de atributo (raza, habilidad)
    return:
        lista:list -> lista de los personajes que cumplen el atributo
        2: int -> No se encontro personajes con esa caracteristica
        -1 : int -> Hubo un error en los datos ingresados
    '''
    if type(lista) == list and type(atributo_elegido) == str and type(key) == str:
        lista_personajes = mostrar_personaje_segun_caracteristica(lista, key)
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

def dragon_ball_personajes_habilidad_ingresada(lista:list, key:str):
    '''
    Brief: 
        Muestra las caracteristicas y la cantidad de personajes que la poseen
    Parameters: 
        lista: list -> lista sobre la que voy a hacer la busqueda
        atributo: str -> La clave del diccionario de donde voy sacar los datos
    Return:
        None
    '''
    if type(lista) == list and len(lista)>0 and type(key) == str and len(key)>0:
        agregar_promedio_pelea_ataque(lista)
        habilidad_ingresada = ingresar("la habilidad")
        set_caracteristicas = mostrar_caracteristicas(lista, key)
        validar = validar_dato_ingresado(habilidad_ingresada, set_caracteristicas)
        if validar == True:
            personajes_habilidad_ingresada = buscar_personajes(lista,habilidad_ingresada,"habilidades")
            print("los personajes que poseen dicha habilidad son:")
            for personaje in personajes_habilidad_ingresada:
                print("-------------------------------")
                for detalle in personaje:
                    if detalle == "nombre" or detalle == "raza" or detalle == "promedio_pelea_ataque":
                        print(f'{detalle}: {personaje[detalle]}')
        else:
            print("No se encontro dicha habilidad")
    else:
        print("Ocurrio un error en la funcion")

###############################################################################################

def mostrar_nombres(lista:list, key:str='nombre')->list:
    '''
    Brief: Crea una lista con los nombres
    Parameters: 
        lista: list -> lista sobre la que voy a hacer la busqueda
        key: str -> La clave del diccionario de donde voy sacar los datos
    Return:
        list -> Ua lista con los distintos tipos de la variable ingresada
        -1 -> Hubo un error
    '''
    if type(lista) == list and len(lista)>0 and type(key) == str and len(key)>0:
        lista_nombres = []
        for personaje in lista:
            lista_nombres.append(personaje[key])
        return lista_nombres
    else:
        return -1

def elegir_personaje_random(lista:list)->str:
    '''
    Brief: Elegir un personaje random para ser contrincante
    Parameters: 
        lista:list -> Lista donde buscar el personaje
    Return: 
        str -> El personaje random
        -1 -> Error
    '''
    if type(lista) == list and len(lista)>0:
        id_random = random.randint(0,len(lista))
        contrincante_random = lista[id_random]
        return contrincante_random
    else:
        return -1

def buscar_personaje_elegido(lista:list, nombre_elegido:str):
    '''
    Brief: Buscar el personaje elegido
    Parameters: 
        lista:list -> Lista donde buscar el personaje
    Return: 
        str -> El personaje ingresado
        -1 -> Error
    '''
    if type(lista) == list and len(lista)>0:
        for personaje in lista:
            if personaje["nombre"] == nombre_elegido:
                personaje_elegido = personaje
        return personaje_elegido
    else:
        return -1

def comparar_personajes(lista:list, nombre_elegido:str):
    '''
    Brief: Compara el poder de ataque de los personajes y da un ganador o un empate
    Parameters: 
        lista:list -> Lista donde buscar el personaje
    Return: 
        list -> Una lista con el ganador y el perdedor
        -1 -> Error
    '''
    if type(lista) == list and len(lista)>0:
        personaje_elegido = buscar_personaje_elegido(lista, nombre_elegido)
        contrincante = elegir_personaje_random(lista)
        if personaje_elegido == contrincante:
            contrincante = elegir_personaje_random(lista)
        if personaje_elegido["poder_ataque"] > contrincante["poder_ataque"]:
            ganador = personaje_elegido
            perdedor = contrincante
        elif personaje_elegido["poder_ataque"] < contrincante["poder_ataque"]:
            ganador = contrincante
            perdedor = personaje_elegido
        return [ganador,perdedor]
    else:
        return -1

def escribir_archivo_txt(path:str, lista:list):
    mi_archivo = open(path, "a", encoding="utf-8")
    for line in lista:
        mi_archivo.write(line)
    mi_archivo.close()

def guardar_batalla_archivo(ganador_perdedor):
    '''
    Brief: Guarda la batalla en un archivo de texto
    Parameters: 
        ganador_perdedor:list -> Lista que diga ganador y perdedor
    Return: 
        -1 -> Error
    '''
    if type(ganador_perdedor) == list and len(ganador_perdedor)>1:
        fecha_actual = str(datetime.date.today())
        lista = [
            f'\n{fecha_actual}\n',
            f'El ganador es: {ganador_perdedor[0]["nombre"]}\n',
            f'El perdedor es: {ganador_perdedor[1]["nombre"]}'
        ]
        escribir_archivo_txt("batallas.txt",lista)
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
    if type(lista) == list and len(lista)>0:
        nombre_elegido = ingresar("personaje")
        lista_nombres_personajes = mostrar_nombres(lista)
        validacion = validar_dato_ingresado(nombre_elegido,lista_nombres_personajes )
        if validacion == True:
            ganador_perdedor = comparar_personajes(lista, nombre_elegido)
            guardar_batalla_archivo(ganador_perdedor)
            print('Se produjo la batalla y se guardaron los datos en "batalla.txt"')
        else:
            print("No existe dicho personaje")
    else:
        print("error: lista ingresada no valida ")

#################        ARCHIVO JSON            ####################################

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
        -1 : int -> Hubo un error en los datos ingresados
    '''
    if type(lista) == list and type(raza) == str and type(habilidad) == str:
        lista_raza = buscar_personajes(lista, raza, "raza")
        lista_habilidad = buscar_personajes(lista, habilidad, "habilidades")
        lista_coincidencia = []
        for personaje in lista_raza:
            if personaje in lista_habilidad:
                lista_coincidencia.append(personaje)
        return lista_coincidencia
    else:
        return -1

def escribir_json(nomenclatura:str, lista:list):
    with open(f"{nomenclatura}", "w", encoding="utf-8") as mi_archivo:
        json.dump(lista, mi_archivo, indent=4)

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
        escribir_json(nomenclatura,lista)
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
        lista:list -> Una lista de str con el formato del personaje para guardar en .json
        -1: int -> Error en los datos ingresados
    '''
    if type(habilidad) == str and type(lista_coincidencias) == list:
        lista = []
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
        razas = mostrar_caracteristicas(lista, "raza")
        validar = validar_dato_ingresado(raza,razas)
        if validar == True:
            habilidad = ingresar("una habilidad")
            habilidades = mostrar_caracteristicas(lista, "habilidades")
            validar = validar_dato_ingresado(habilidad, habilidades)
            if validar == True:
                lista_coincidencia = buscar_coincidencias(lista, raza, habilidad)
                if lista_coincidencia != []:
                    path_json = guardar_json(raza, habilidad, lista_coincidencia)
                    if type (path_json) == str:
                        print("Se creo el archivo .json con los datos ")
                        return path_json
                else:
                    print("No hay personajes que cumplan ambas caracteristicas")
            else:
                print("Se ingreso una raza inexistente")
        else:
            print("Se ingreso una raza inexistente")
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
        for personaje in data:
            print("----------------------")
            imprimir_diccionarios(personaje)
    else:
        print("No se creo ningun archivo")

##############          NUEVO REQUERIMIENTO             #################

def calcular_suma_porcentaje(sacar_porcentaje:int, porcentaje:int):
    '''
    Brief:
        Calcula los porcentajes requeridos y los suma 
    Parameters: 
        sacar_porcentaje: int -> entero al que le queremos calcular el porcentaje
        porcentaje: int -> Cual es el porcentaje
    return:
        porcentaje_calculado: float -> el porcentaje sumado al numero ingresado
        1:int -> Hubo un error
    '''
    if type (sacar_porcentaje) == int and type (porcentaje) == int:
        porcentaje_calculado = sacar_porcentaje * porcentaje / 100
        porcentaje_calculado += sacar_porcentaje
        return porcentaje_calculado
    else:
        return 1

def agregar_lista_mejoras_personajes(personaje:dict):
    '''
    Brief:
        Agrega las mejoras al personaje
    Parameters: 
        personaje: dict -> el personaje a mejorar
    return:
        1:int -> Hubo un error
    '''
    if type (personaje) == dict:
        porcentaje_agregado = calcular_suma_porcentaje(personaje["poder_pelea"], 50)
        personaje["poder_pelea"] = porcentaje_agregado
        porcentaje_agregado = calcular_suma_porcentaje(personaje["poder_ataque"], 70)
        personaje["poder_ataque"] = porcentaje_agregado
        personaje["habilidades"].append("transformacion nivel dios")
    else:
        return 1

def escribir_csv(lista:list):
    with open("Saiyan_mejorados.csv", "a") as archivo:
        for i in range(len(lista)):
            for caracteristica in lista:
                registro = (
                    f"{caracteristica[i]}"
                    )
                archivo.write(registro)

def subir_personajes_csv(lista:list):
    '''
    Brief:
        Sube el personaje mejorado a un archivo .csv
    Parameters: 
        lista: list -> los personajes mejorados
    return:
        1:int -> Hubo un error
    '''
    if type(lista) == list:
        escribir_csv(lista)
    else:
        return 1

def deragon_ball_mejorar_Saiyan(lista:list):
    '''
    Brief:
        Mejora los Saiyan
    Parameters: 
        lista: list -> lista de personaje
    return:
        None
    '''
    if type(lista) == list:
        for personaje in lista:
            raza_saiyan = False
            for caracteristica in personaje["raza"]:
                if caracteristica == "Saiyan":
                    raza_saiyan = True
            if raza_saiyan == True:
                agregar_lista_mejoras_personajes(personaje)
        subir_personajes_csv(lista)
        print("se mejoraron los saiyan")
    else:
        print("No se ingreso una lista valida")

dragon_ball_aplicacion(menu)