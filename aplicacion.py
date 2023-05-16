from validaciones import *
from archivos import *
from normalizar import *
from funciones import *
from aplicacion import *

menu = ("---------------------------------\n1) Traer datos desde archivo",
        "2) Listar cantidad por raza",
        "3) Listar personajes por raza",
        "4) Listar personajes por habilidad",
        "5) Jugar batalla",
        "6) Guardar Json",
        "7) Leer Json",
        "8) Mejorar los Saiyan",
        "9) Salir del programa\n---------------------------------"
    )

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
                    #dragon_ball_mejorar_Saiyan(lista_personajes)
                    pass
                else:
                    print("No se trajo una lista del archivo")
            case 9:
                seguir = False

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



dragon_ball_aplicacion(menu)